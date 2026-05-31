"""
batch_export_fbx.command
=========================

Cascadeur command addon (GUI).

Running it from the `Commands` menu opens a folder picker; every .casc under the
chosen folder is exported to FBX in the same directory with the same base name.

Edit the constants at the top of this file to change the behavior.

NOTE: ASCII-only on purpose. Cascadeur's script loader can fail to decode
multibyte (e.g. Japanese) source bytes, so comments/strings here are English.
"""

import csc

from . import core


# ---- Defaults (edit as needed) --------------------------------------------
RECURSIVE = True          # also walk subfolders
EXPORT_MODE = "all"       # "all" / "model" / "joints" / "scene"
SKIP_EXISTING = False     # True = skip existing .fbx (False = overwrite)
ENTER_RIG_MODE = False    # True = run rig mode on->off after load
# FBX settings (None = Cascadeur default). Example:
#   FBX_SETTINGS = core.make_fbx_settings(ascii=False, up_axis="Y")
FBX_SETTINGS = None
# ---------------------------------------------------------------------------


def command_name():
    return "Export.Batch casc to FBX"


def command_description():
    return ("Export every .casc under a chosen folder to FBX, into the same "
            "directory with the same base name (foo/bar.casc -> foo/bar.fbx)")


def run(scene):
    fdm = csc.app.get_application().get_file_dialog_manager()

    def on_folder(folder_path):
        if not folder_path:
            scene.warning("No folder was selected. Aborting.")
            return

        folder_path = folder_path.replace("\\", "/")
        scene.info(f"[batch_export_fbx] start: {folder_path}")
        try:
            summary = core.export_folder_to_fbx(
                folder_path,
                recursive=RECURSIVE,
                export_mode=EXPORT_MODE,
                skip_existing=SKIP_EXISTING,
                enter_rig_mode=ENTER_RIG_MODE,
                fbx_settings=FBX_SETTINGS,
                log=scene.info,
            )
        except Exception as ex:  # noqa: BLE001
            scene.error(f"[batch_export_fbx] failed: {ex}")
            raise

        msg = (f"Done: {summary['exported']} exported / "
               f"{summary['skipped']} skipped / "
               f"{summary['failed']} failed (of {summary['total']})")
        if summary["failed"]:
            scene.warning(msg)
        else:
            scene.info(msg)

        # Also notify via a dialog
        try:
            csc.view.DialogManager.instance().show_info("Batch casc -> FBX", msg)
        except Exception:  # noqa: BLE001
            pass

    fdm.show_folder_dialog("Select a folder to search for .casc", on_folder)
