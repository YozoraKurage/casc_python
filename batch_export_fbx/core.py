"""
batch_export_fbx.core
=====================

Recursively find .casc projects under a folder and export each one to FBX
in the SAME directory with the SAME base name.

- foo/bar/baz.casc  ->  foo/bar/baz.fbx

Must run inside the Cascadeur process (Python console / addon / startup script).
A plain terminal python cannot `import csc`.

NOTE: This file is intentionally ASCII-only. Cascadeur's script reloader /
--run-script loader can fail to decode multibyte (e.g. Japanese) source bytes
("UnicodeDecodeError: unexpected end of data"), so all comments/strings here are
English. The README (not imported) keeps the Japanese explanations.

Follows the established pattern from
resources/scripts/python/samples/casc_import_export.py:
  create_application_scene -> set_current_scene -> ProjectLoader.load_from
  -> FbxSceneLoader/FbxLoader export -> remove_application_scene
"""

import os
import csc


# Export mode -> which FbxLoader/FbxSceneLoader method to call.
EXPORT_MODES = ("all", "model", "joints", "scene")


class StatusReporter:
    """On-screen status line backed by Cascadeur's StatusManager.

    Cascadeur exposes a status surface (the same one tools use) via
    csc.app.StatusManager + csc.app.SimpleStatusInformer. This shows a live,
    updatable text status in the Cascadeur window while the batch runs, and
    optionally lets the user cancel.

    Usage:
        with StatusReporter("Batch export", cancelable=True) as st:
            for i, item in enumerate(items, 1):
                if st.is_canceled():
                    break
                st.set_text(f"[{i}/{n}] {name}")
                ...

    Degrades gracefully: if the API is missing on this build, all calls are
    no-ops and is_canceled() returns False.
    """

    def __init__(self, text="", cancelable=False, blocking=False):
        self._informer = None
        self._manager = None
        try:
            app = csc.app.get_application()
            self._manager = app.get_status_manager()
            self._informer = csc.app.SimpleStatusInformer(str(text))
            try:
                self._informer.set_cancelable(bool(cancelable))
            except Exception:  # noqa: BLE001
                pass
            try:
                self._informer.set_blocking(bool(blocking))
            except Exception:  # noqa: BLE001
                pass
            self._manager.set_status(self._informer)
        except Exception:  # noqa: BLE001 - API not available -> no-op reporter
            self._informer = None
            self._manager = None

    @property
    def active(self):
        return self._informer is not None and self._manager is not None

    def set_text(self, text):
        if self._informer is not None:
            try:
                self._informer.set_text(str(text))
            except Exception:  # noqa: BLE001
                pass

    def is_canceled(self):
        if self._informer is not None:
            try:
                return bool(self._informer.is_canceled())
            except Exception:  # noqa: BLE001
                return False
        return False

    def close(self):
        if self._manager is not None and self._informer is not None:
            try:
                self._manager.remove_status(self._informer)
            except Exception:  # noqa: BLE001
                pass
        self._informer = None
        self._manager = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


def make_default_logger(to_console=True, to_event_log=True):
    """Return a logger that writes progress to the console AND the event log.

    Progress is reported as text in two places:
      - console: print(..., flush=True) for immediate output (avoid buffering)
      - event log: current scene domain_scene().info(...) (Window > Event log)
    For a live on-screen status line, see StatusReporter (csc.app.StatusManager).

    Stays silent (never raises) if either sink is unavailable.
    """
    event_info = None
    if to_event_log:
        try:
            view_scene = csc.app.get_application().get_scene_manager().current_scene()
            event_info = view_scene.domain_scene().info
        except Exception:  # noqa: BLE001
            event_info = None

    def _log(msg):
        if to_console:
            try:
                print(msg, flush=True)
            except Exception:  # noqa: BLE001
                pass
        if event_info is not None:
            try:
                event_info(str(msg))
            except Exception:  # noqa: BLE001
                pass

    return _log


def find_casc_files(folder, recursive=True):
    """Return sorted absolute paths of .casc files under folder."""
    folder = os.path.abspath(folder)
    results = []
    if recursive:
        for root, _dirs, files in os.walk(folder):
            for f in files:
                if f.lower().endswith(".casc"):
                    results.append(os.path.join(root, f))
    else:
        for f in os.listdir(folder):
            full = os.path.join(folder, f)
            if os.path.isfile(full) and f.lower().endswith(".casc"):
                results.append(full)
    return sorted(results)


def to_fwd(path):
    """Normalize path separators to forward slashes.

    Cascadeur's FBX exporter expects forward-slash paths; the bundled samples and
    commands all do `.replace('\\\\','/')` / `.as_posix()`. Passing backslashes can
    cause a silent failure (no exception, but no file written).
    """
    return str(path).replace("\\", "/")


def fbx_path_for(casc_path):
    """Return the .fbx path next to the .casc (same dir, same base, forward slashes)."""
    base, _ext = os.path.splitext(casc_path)
    return to_fwd(base + ".fbx")


def make_fbx_settings(*, ascii=False, up_axis=None,
                      apply_euler_filter=None, bake_animation=None):
    """Build a csc.fbx.FbxSettings (only set fields that are specified).

    up_axis: "X"/"Y"/"Z" (case-insensitive). None = leave default.
    """
    settings = csc.fbx.FbxSettings()
    settings.mode = csc.fbx.FbxSettingsMode.Ascii if ascii else csc.fbx.FbxSettingsMode.Binary
    if up_axis is not None:
        axis_map = {
            "X": csc.fbx.FbxSettingsAxis.X,
            "Y": csc.fbx.FbxSettingsAxis.Y,
            "Z": csc.fbx.FbxSettingsAxis.Z,
        }
        settings.up_axis = axis_map[str(up_axis).upper()]
    if apply_euler_filter is not None:
        settings.apply_euler_filter = bool(apply_euler_filter)
    if bake_animation is not None:
        settings.bake_animation = bool(bake_animation)
    return settings


def _export_loaded_scene(tools_manager, view_scene, out_path, export_mode, fbx_settings):
    """Export the already-loaded view_scene to out_path as FBX."""
    tool = tools_manager.get_tool("FbxSceneLoader")

    if export_mode == "scene":
        # Whole scene (via FbxSceneLoader)
        tool.export_fbx_scene(view_scene, out_path)
        return

    loader = tool.get_fbx_loader(view_scene)
    if fbx_settings is not None:
        loader.set_settings(fbx_settings)

    if export_mode == "all":
        loader.export_all_objects(out_path)
    elif export_mode == "model":
        loader.export_model(out_path)
    elif export_mode == "joints":
        loader.export_joints(out_path)
    else:
        raise ValueError(f"unknown export_mode: {export_mode!r} (expected one of {EXPORT_MODES})")


def _maybe_rig_round_trip(domain_scene):
    """Optional rig_mode on->off round trip.

    Mirrors what casc_import_export.py does as a pre-process. Heavy and may fail
    on some scenes; lazy-imported and exceptions propagate to the caller.
    """
    import rig_mode.on as rm_on
    import rig_mode.off as rm_off
    rm_on.run_raw(domain_scene, [0.0, 0.5, 0.0])
    rm_off.run(domain_scene, True)


def export_one(scene_manager, tools_manager, casc_path, *,
               export_mode="all", fbx_settings=None,
               skip_existing=False, enter_rig_mode=False, log=print,
               data_source_manager=None):
    """Load one .casc and export it to FBX.

    Loading uses DataSourceManager.load_scene (File > Open equivalent): it opens
    the file into the CURRENT scene tab. This matches the working bundled sample
    change_visibility_data_type.py. (The lower-level ProjectLoader.load_from left
    the scene in a state the FBX exporter would not write, producing empty results.)

    Returns: ("exported" | "skipped" | "failed", message)
    """
    casc_fwd = to_fwd(casc_path)          # pass forward-slash path to the loader too
    out_path = fbx_path_for(casc_path)    # already forward-slash normalized

    if skip_existing and os.path.exists(out_path):
        log(f"  skip (already exists): {out_path}")
        return ("skipped", out_path)

    if data_source_manager is None:
        data_source_manager = csc.app.get_application().get_data_source_manager()

    # Record pre-export state to verify a file was actually written afterwards.
    before_exists = os.path.exists(out_path)
    before_mtime = os.path.getmtime(out_path) if before_exists else -1.0

    application_scene = scene_manager.create_application_scene()
    scene_manager.set_current_scene(application_scene)
    try:
        # Open the .casc into the current tab (File > Open equivalent).
        loaded = data_source_manager.load_scene(casc_fwd)
        if loaded is False:  # load_scene returns bool; None means "no return" -> treat as ok
            msg = f"load_scene returned False (could not open): {casc_fwd}"
            log(f"  ERROR: {msg}")
            return ("failed", f"{casc_path}: {msg}")

        # Re-fetch the current scene to feed the exporter (proven pattern).
        try:
            export_scene = scene_manager.current_scene()
        except Exception:  # noqa: BLE001
            export_scene = application_scene

        if enter_rig_mode:
            _maybe_rig_round_trip(export_scene.domain_scene())

        # Output dir is the same as the .casc, but ensure it exists anyway.
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        _export_loaded_scene(tools_manager, export_scene, out_path, export_mode, fbx_settings)

        # Verify: export_* may not raise on failure, so check the real file.
        if not os.path.exists(out_path):
            msg = (f"export reported success but file was not created: {out_path} "
                   f"(mode={export_mode}). Scene may have nothing to export, or mode mismatch.")
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}")

        size = os.path.getsize(out_path)
        mtime = os.path.getmtime(out_path)
        if before_exists and mtime <= before_mtime:
            msg = f"file not updated (stale): {out_path}. Existing file may not have been overwritten."
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}")
        if size == 0:
            msg = f"output file is empty (0 bytes): {out_path}"
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}")

        log(f"  OK -> {out_path}  ({size:,} bytes)")
        return ("exported", out_path)

    except Exception as ex:  # noqa: BLE001 - one failure must not stop the batch
        log(f"  ERROR: {casc_path}: {ex}")
        return ("failed", f"{casc_path}: {ex}")

    finally:
        # Always close the working scene tab (avoid memory growth).
        # close_scene pairs with load_scene (proven sample pattern); fall back to
        # remove_application_scene if needed.
        try:
            data_source_manager.close_scene(application_scene)
        except Exception:  # noqa: BLE001
            try:
                scene_manager.remove_application_scene(application_scene)
            except Exception:  # noqa: BLE001
                pass


def export_folder_to_fbx(folder, *, recursive=True, export_mode="all",
                         skip_existing=False, enter_rig_mode=False,
                         fbx_settings=None, restore_current_scene=True,
                         log=None, progress=None, show_status=True):
    """Export every .casc under folder to a same-place same-name .fbx.

    Args:
      folder              start folder
      recursive           also walk subfolders (default True)
      export_mode         "all"/"model"/"joints"/"scene" (default "all")
      skip_existing       skip if .fbx already exists (default False = overwrite)
      enter_rig_mode      run rig mode on->off after load (default False)
      fbx_settings        csc.fbx.FbxSettings (default None = Cascadeur default)
      restore_current_scene  restore the original scene tab afterwards (default True)
      log                 log function (default None = console + event log both)
      progress            progress(done, total, status, casc_path) called per file
      show_status         show a live on-screen status line via StatusManager
                          (default True; user can cancel). No-op if API missing.

    Returns: summary dict {total, exported, skipped, failed, failures, outputs, canceled}
    """
    if export_mode not in EXPORT_MODES:
        raise ValueError(f"export_mode must be one of {EXPORT_MODES}, got {export_mode!r}")

    if log is None:
        log = make_default_logger()

    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"folder not found: {folder}")

    app = csc.app.get_application()
    scene_manager = app.get_scene_manager()
    tools_manager = app.get_tools_manager()
    data_source_manager = app.get_data_source_manager()

    original_view = None
    if restore_current_scene:
        try:
            original_view = scene_manager.current_scene()
        except Exception:  # noqa: BLE001
            original_view = None

    files = find_casc_files(folder, recursive=recursive)
    total = len(files)
    log(f"[batch_export_fbx] {total} .casc files under: {folder} "
        f"(recursive={recursive}, mode={export_mode})")

    summary = {"total": total, "exported": 0, "skipped": 0,
               "failed": 0, "failures": [], "outputs": [], "canceled": False}

    status = StatusReporter("Batch export to FBX", cancelable=True) if show_status else None
    try:
        for i, casc_path in enumerate(files, 1):
            # On-screen cancel (StatusManager) - stop cleanly between files.
            if status is not None and status.is_canceled():
                summary["canceled"] = True
                log("[batch_export_fbx] canceled by user")
                break

            pct = int(i * 100 / total) if total else 100
            name = os.path.basename(casc_path)
            # Start line: percent / count / remaining
            log(f"[{i}/{total}] {pct:3d}%  (remaining {total - i + 1})  {name}")
            if status is not None:
                status.set_text(f"Exporting {pct}%  [{i}/{total}]  {name}")

            st, info = export_one(
                scene_manager, tools_manager, casc_path,
                export_mode=export_mode, fbx_settings=fbx_settings,
                skip_existing=skip_existing, enter_rig_mode=enter_rig_mode, log=log,
                data_source_manager=data_source_manager)
            if st == "exported":
                summary["exported"] += 1
                summary["outputs"].append(info)
            elif st == "skipped":
                summary["skipped"] += 1
            else:
                summary["failed"] += 1
                summary["failures"].append(info)

            if progress is not None:
                try:
                    progress(i, total, st, casc_path)
                except Exception:  # noqa: BLE001
                    pass
    finally:
        if status is not None:
            status.close()

    # Restore original scene tab
    if original_view is not None:
        try:
            scene_manager.set_current_scene(original_view)
        except Exception:  # noqa: BLE001
            pass

    log(f"[batch_export_fbx] done: exported={summary['exported']} "
        f"skipped={summary['skipped']} failed={summary['failed']} / total={summary['total']}")
    if summary["failures"]:
        log("[batch_export_fbx] failures:")
        for f in summary["failures"]:
            log(f"  - {f}")

    return summary
