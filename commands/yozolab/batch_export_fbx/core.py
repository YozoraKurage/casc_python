"""
batch_export_fbx.core
=====================

Recursively find .casc projects under a folder and export each one to FBX
in the SAME directory with the SAME base name.

- foo/bar/baz.casc  ->  foo/bar/baz.fbx

Must run inside the Cascadeur process (Python console / addon). A plain terminal
python cannot `import csc`.

NOTE: ASCII-only on purpose. Cascadeur's script loader can fail to decode
multibyte (e.g. Japanese) source bytes, so all comments/strings here are English.
Japanese docs live in README.md (not imported).

Progress is reported as text to the console AND the Cascadeur event log
(Window > Event log). Do NOT use csc.app.StatusManager for progress: calling
StatusManager.set_status from here causes a C++ access violation that crashes
Cascadeur (confirmed in the crash log). Text logging is the safe surface.

Follows the established pattern from the bundled working sample
resources/scripts/python/samples/change_visibility_data_type.py:
  create_application_scene -> set_current_scene -> DataSourceManager.load_scene
  -> FbxSceneLoader export -> DataSourceManager.close_scene
"""

import os
import csc


# Export mode -> which FbxLoader/FbxSceneLoader method to call.
EXPORT_MODES = ("all", "model", "joints", "scene")


def make_default_logger(to_console=True, to_event_log=True):
    """Return a logger that writes progress to the console AND the event log.

      - console: print(..., flush=True) for immediate output (avoid buffering)
      - event log: current scene domain_scene().info(...) (Window > Event log)

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
    """Optional rig_mode on->off round trip (pre-process). Heavy; lazy-imported."""
    import rig_mode.on as rm_on
    import rig_mode.off as rm_off
    rm_on.run_raw(domain_scene, [0.0, 0.5, 0.0])
    rm_off.run(domain_scene, True)


def _same_scene(a, b):
    """Best-effort identity check for two view.Scene handles. Defaults to False
    (treat as different) if comparison is not supported, so we err on closing."""
    if a is None or b is None:
        return False
    try:
        return a == b
    except Exception:  # noqa: BLE001
        return a is b


def _safe_close(data_source_manager, scene_manager, scene, keep_scenes, log):
    """Close `scene` unless it is one of keep_scenes. Never raises.

    IMPORTANT: only call this on a scene tab that is NOT currently active.
    Closing the ACTIVE tab crashes Cascadeur (it triggers an immediate UI switch
    + auto-create of a new empty scene). The batch closes each tab only AFTER the
    next file's load has made a different tab active.
    """
    if scene is None:
        return
    for k in keep_scenes:
        if _same_scene(scene, k):
            return
    try:
        data_source_manager.close_scene(scene)
    except Exception:  # noqa: BLE001
        try:
            scene_manager.remove_application_scene(scene)
        except Exception:  # noqa: BLE001
            pass


def export_one(scene_manager, tools_manager, casc_path, *,
               export_mode="all", fbx_settings=None,
               skip_existing=False, enter_rig_mode=False, log=print,
               data_source_manager=None):
    """Load one .casc and export it to FBX.

    DataSourceManager.load_scene behaves like File > Open: it opens the .casc in a
    NEW scene tab that becomes current. This function loads + exports only; it does
    NOT create or close any tab (creating/closing the ACTIVE tab crashes Cascadeur
    mid-batch). The caller is responsible for closing the returned tab later, once
    it is no longer the active tab (see export_folder_to_fbx).

    Returns: (status, message, loaded_scene)
      status: "exported" | "skipped" | "failed"
      loaded_scene: the view.Scene tab that load_scene opened (or None)
    """
    casc_fwd = to_fwd(casc_path)
    out_path = fbx_path_for(casc_path)

    if skip_existing and os.path.exists(out_path):
        log(f"  skip (already exists): {out_path}")
        return ("skipped", out_path, None)

    if data_source_manager is None:
        data_source_manager = csc.app.get_application().get_data_source_manager()

    before_exists = os.path.exists(out_path)
    before_mtime = os.path.getmtime(out_path) if before_exists else -1.0

    loaded_scene = None
    try:
        data_source_manager.load_scene(casc_fwd)

        # load_scene opened the file as a new current tab; that is what we export.
        loaded_scene = scene_manager.current_scene()
        export_scene = loaded_scene

        if enter_rig_mode:
            _maybe_rig_round_trip(export_scene.domain_scene())

        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        _export_loaded_scene(tools_manager, export_scene, out_path, export_mode, fbx_settings)

        # Verify: export_* may not raise on failure, so check the real file.
        if not os.path.exists(out_path):
            msg = (f"export reported success but file was not created: {out_path} "
                   f"(mode={export_mode}). Scene may have nothing to export, or mode mismatch.")
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}", loaded_scene)

        size = os.path.getsize(out_path)
        mtime = os.path.getmtime(out_path)
        if before_exists and mtime <= before_mtime:
            msg = f"file not updated (stale): {out_path}. Existing file may not have been overwritten."
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}", loaded_scene)
        if size == 0:
            msg = f"output file is empty (0 bytes): {out_path}"
            log(f"  WARN: {msg}")
            return ("failed", f"{casc_path}: {msg}", loaded_scene)

        log(f"  OK -> {out_path}  ({size:,} bytes)")
        return ("exported", out_path, loaded_scene)

    except Exception as ex:  # noqa: BLE001 - one failure must not stop the batch
        log(f"  ERROR: {casc_path}: {ex}")
        return ("failed", f"{casc_path}: {ex}", loaded_scene)


def export_folder_to_fbx(folder, *, recursive=True, export_mode="all",
                         skip_existing=False, enter_rig_mode=False,
                         fbx_settings=None, log=None, progress=None,
                         close_after=True):
    """Export every .casc under folder to a same-place same-name .fbx.

    Tab handling (important - this is what avoids the crashes):
      - We never create tabs with create_application_scene (that crashed Cascadeur).
      - DataSourceManager.load_scene opens each .casc as a NEW tab that becomes
        the ACTIVE tab.
      - We close each loaded tab ONLY AFTER the next file has been loaded, i.e.
        once it is no longer the active tab. Closing the ACTIVE tab crashes
        Cascadeur (it forces a UI switch + auto-create of an empty scene), which
        is what crashed earlier. Deferring the close by one step avoids that.
      - The tab that was active BEFORE the batch (keep_scene) is never closed.
      - The very last loaded tab stays open (closing it would mean closing the
        active tab). That is at most one leftover tab.

    Args:
      folder              start folder
      recursive           also walk subfolders (default True)
      export_mode         "all"/"model"/"joints"/"scene" (default "all")
      skip_existing       skip if .fbx already exists (default False = overwrite)
      enter_rig_mode      run rig mode on->off after load (default False)
      fbx_settings        csc.fbx.FbxSettings (default None = Cascadeur default)
      log                 log function (default None = console + event log both)
      progress            progress(done, total, status, casc_path) called per file
      close_after         close processed tabs (deferred). False = keep all open.

    Progress is text-only (console + event log). StatusManager is intentionally
    NOT used (it crashes Cascadeur).

    Returns: summary dict {total, exported, skipped, failed, failures, outputs}
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

    # Remember the user's tab so we never close it.
    try:
        keep_scene = scene_manager.current_scene()
    except Exception:  # noqa: BLE001
        keep_scene = None
    keep_scenes = [keep_scene]

    files = find_casc_files(folder, recursive=recursive)
    total = len(files)
    log(f"[batch_export_fbx] {total} .casc files under: {folder} "
        f"(recursive={recursive}, mode={export_mode}, close_after={close_after})")

    summary = {"total": total, "exported": 0, "skipped": 0,
               "failed": 0, "failures": [], "outputs": []}

    pending_close = None  # tab from the previous iteration (now inactive once we load the next)
    for i, casc_path in enumerate(files, 1):
        pct = int(i * 100 / total) if total else 100
        name = os.path.basename(casc_path)
        log(f"[{i}/{total}] {pct:3d}%  (remaining {total - i + 1})  {name}")

        st, info, loaded_scene = export_one(
            scene_manager, tools_manager, casc_path,
            export_mode=export_mode, fbx_settings=fbx_settings,
            skip_existing=skip_existing, enter_rig_mode=enter_rig_mode, log=log,
            data_source_manager=data_source_manager)

        # Now the just-loaded tab is active, so the PREVIOUS tab is inactive and
        # safe to close. (Closing the active tab is what crashes Cascadeur.)
        if close_after and pending_close is not None \
                and not _same_scene(pending_close, loaded_scene):
            _safe_close(data_source_manager, scene_manager, pending_close, keep_scenes, log)
        # Defer this tab's close to the next iteration (only if it really opened a
        # new tab, i.e. not the user's kept tab).
        if loaded_scene is not None and not _same_scene(loaded_scene, keep_scene):
            pending_close = loaded_scene
        else:
            pending_close = None

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

    # The last loaded tab (pending_close) is left open on purpose: it is the
    # active tab, and closing the active tab crashes Cascadeur. At most one extra
    # tab remains; the user can close it manually.
    log(f"[batch_export_fbx] done: exported={summary['exported']} "
        f"skipped={summary['skipped']} failed={summary['failed']} / total={summary['total']}")
    if summary["failures"]:
        log("[batch_export_fbx] failures:")
        for f in summary["failures"]:
            log(f"  - {f}")

    return summary
