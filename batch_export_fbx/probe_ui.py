"""
batch_export_fbx.probe_ui
=========================

Diagnostic: enumerate the UI-related API that THIS Cascadeur build actually
exposes, so we can pick the best available way to show export progress.

Cascadeur's UI is Qt6 + QML (Qt6Quick*). PySide/shiboken are NOT bundled, so we
cannot drive Qt widgets directly from Python. The only supported UI surface is
whatever `csc` exposes (csc.view.* etc.). The bundled api_document.py may be
incomplete, so this script asks the live module what it has.

Run in the Cascadeur Python console:
    from commands.batch_export_fbx import probe_ui
    probe_ui.run()

It prints, for csc / csc.view / csc.app / DialogManager, every public member
whose name hints at progress/status/dialog/notify/etc. Paste the output back.

ASCII-only (Cascadeur's loader can mis-decode multibyte source).
"""

import csc

# Name fragments that would indicate a progress / status / notification surface.
HINTS = (
    "progress", "status", "busy", "wait", "spinner", "percent",
    "notify", "notification", "toast", "message", "dialog", "popup",
    "info", "warning", "error", "log", "title", "show", "set_", "update",
)


def _members(obj):
    try:
        return sorted(n for n in dir(obj) if not n.startswith("__"))
    except Exception as ex:  # noqa: BLE001
        return [f"<dir failed: {ex}>"]


def _hinted(names):
    low = {n: n.lower() for n in names}
    return [n for n in names if any(h in low[n] for h in HINTS)]


def _dump(title, obj, log):
    log("=" * 70)
    log(title)
    log("-" * 70)
    names = _members(obj)
    log(f"  ALL ({len(names)}): {names}")
    hinted = _hinted(names)
    log(f"  HINTED: {hinted}")


def run(log=print):
    log("### batch_export_fbx.probe_ui ###")
    try:
        import sys
        log(f"python: {sys.version}")
    except Exception:  # noqa: BLE001
        pass

    # Top-level csc
    _dump("csc", csc, log)

    # Sub-namespaces of interest
    for path in ("csc.view", "csc.app"):
        obj = csc
        ok = True
        for part in path.split(".")[1:]:
            obj = getattr(obj, part, None)
            if obj is None:
                ok = False
                break
        if ok:
            _dump(path, obj, log)
        else:
            log(f"(missing: {path})")

    # DialogManager class + its singleton instance
    dm_cls = getattr(getattr(csc, "view", None), "DialogManager", None)
    if dm_cls is not None:
        _dump("csc.view.DialogManager (class)", dm_cls, log)
        try:
            inst = dm_cls.instance()
            _dump("csc.view.DialogManager.instance()", inst, log)
        except Exception as ex:  # noqa: BLE001
            log(f"(DialogManager.instance() failed: {ex})")

    # Application instance + its managers
    try:
        app = csc.app.get_application()
        _dump("csc.app.get_application()", app, log)
    except Exception as ex:  # noqa: BLE001
        log(f"(get_application failed: {ex})")

    # Is any Qt binding importable at all?
    log("=" * 70)
    log("Qt bindings import test")
    log("-" * 70)
    for mod in ("PySide6", "PySide2", "shiboken6", "shiboken2", "PyQt6", "PyQt5"):
        try:
            __import__(mod)
            log(f"  {mod}: IMPORTABLE")
        except Exception as ex:  # noqa: BLE001
            log(f"  {mod}: no ({type(ex).__name__})")

    log("### done. paste the output above. ###")
