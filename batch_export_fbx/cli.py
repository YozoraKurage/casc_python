"""
batch_export_fbx.cli
====================

Convenience entry points for the Cascadeur Python console.

The addon (command.py, run via the Commands menu) is the primary way to use this
tool. These helpers are for ad-hoc runs and for diagnosing problems from the
console. Must run inside the Cascadeur process (a plain terminal python cannot
`import csc`).

Usage (Window > Python console):
    from commands.batch_export_fbx import cli
    cli.run_folder(r"D:\\path\\to\\projects")                 # recursive / all / overwrite
    cli.run_folder(r"D:\\proj", recursive=False, ascii=True, up_axis="Y")
    cli.run_file(r"D:\\proj\\walk.casc")                      # single file (diagnostics)

NOTE: ASCII-only on purpose (Cascadeur's loader can mis-decode multibyte source).
"""

from . import core


def run_folder(folder, *, recursive=True, export_mode="all",
               skip_existing=False, enter_rig_mode=False,
               ascii=False, up_axis=None, log=None, progress=None):
    """Export every .casc under folder to FBX (thin console wrapper).

    log=None -> progress goes to BOTH the console and the Cascadeur event log.
    progress(done, total, status, casc_path) is called per file (optional).
    """
    fbx_settings = None
    if ascii or up_axis is not None:
        fbx_settings = core.make_fbx_settings(ascii=ascii, up_axis=up_axis)

    return core.export_folder_to_fbx(
        folder,
        recursive=recursive,
        export_mode=export_mode,
        skip_existing=skip_existing,
        enter_rig_mode=enter_rig_mode,
        fbx_settings=fbx_settings,
        log=log,
        progress=progress,
    )


def run_file(casc_path, *, export_mode="all", ascii=False, up_axis=None,
             skip_existing=False, enter_rig_mode=False, log=None):
    """Export a single .casc (for troubleshooting).

    Example:
        cli.run_file(r"D:\\proj\\walk.casc")
        cli.run_file(r"D:\\proj\\walk.casc", export_mode="scene")
    """
    import csc
    if log is None:
        log = core.make_default_logger()
    fbx_settings = None
    if ascii or up_axis is not None:
        fbx_settings = core.make_fbx_settings(ascii=ascii, up_axis=up_axis)

    app = csc.app.get_application()
    sm = app.get_scene_manager()
    tm = app.get_tools_manager()
    original = None
    try:
        original = sm.current_scene()
    except Exception:  # noqa: BLE001
        original = None

    log(f"[batch_export_fbx] single file: {core.to_fwd(casc_path)} (mode={export_mode})")
    status, info = core.export_one(
        sm, tm, casc_path,
        export_mode=export_mode, fbx_settings=fbx_settings,
        skip_existing=skip_existing, enter_rig_mode=enter_rig_mode, log=log)

    if original is not None:
        try:
            sm.set_current_scene(original)
        except Exception:  # noqa: BLE001
            pass

    log(f"[batch_export_fbx] result: {status}  {info}")
    return status, info
