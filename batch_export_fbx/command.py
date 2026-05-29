"""
batch_export_fbx.command
=========================

Cascadeur のコマンドアドオン。

`Commands` メニューから実行するとフォルダ選択ダイアログが開き、
選んだフォルダ以下の全 .casc を、同じ場所・同じ名前の .fbx に一括書き出しする。

設定を変えたい場合はこのファイル先頭の定数を編集する。
"""

import csc

from . import core


# ---- 既定の設定（必要に応じて編集）----------------------------------------
RECURSIVE = True          # サブフォルダも辿る
EXPORT_MODE = "all"       # "all" / "model" / "joints" / "scene"
SKIP_EXISTING = False     # True なら既存 .fbx をスキップ（False = 上書き）
ENTER_RIG_MODE = False    # True なら読み込み後に rig mode on->off を実行
# FBX 設定（None なら Cascadeur 既定）。例:
#   FBX_SETTINGS = core.make_fbx_settings(ascii=False, up_axis="Y")
FBX_SETTINGS = None
# ---------------------------------------------------------------------------


def command_name():
    return "Export.Batch casc to FBX"


def command_description():
    return ("選択したフォルダ以下の全 .casc を、同じディレクトリ・同じ名前で FBX に一括書き出しします "
            "(foo/bar.casc -> foo/bar.fbx)")


def run(scene):
    fdm = csc.app.get_application().get_file_dialog_manager()

    def on_folder(folder_path):
        if not folder_path:
            scene.warning("フォルダが選択されませんでした。中止します。")
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
            scene.error(f"[batch_export_fbx] 失敗: {ex}")
            raise

        msg = (f"完了: {summary['exported']} 件書き出し / "
               f"{summary['skipped']} 件スキップ / "
               f"{summary['failed']} 件失敗 (対象 {summary['total']} 件)")
        if summary["failed"]:
            scene.warning(msg)
        else:
            scene.info(msg)

        # 結果をダイアログでも通知
        try:
            csc.view.DialogManager.instance().show_info("Batch casc -> FBX", msg)
        except Exception:  # noqa: BLE001
            pass

    fdm.show_folder_dialog(".casc を探すフォルダを選択", on_folder)
