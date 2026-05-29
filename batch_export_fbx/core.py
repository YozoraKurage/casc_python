"""
batch_export_fbx.core
=====================

指定フォルダ以下の .casc プロジェクトを再帰的に探し、
各 .casc と同じディレクトリ・同じ basename で FBX を書き出す中核ロジック。

- foo/bar/baz.casc  ->  foo/bar/baz.fbx

Cascadeur のプロセス内（Python コンソール / アドオン / 起動スクリプト）で実行することを想定。
通常のターミナルの素の python では `import csc` できない点に注意。

公式の確立パターン（resources/scripts/python/samples/casc_import_export.py）に準拠:
  create_application_scene -> set_current_scene -> ProjectLoader.load_from
  -> FbxSceneLoader/FbxLoader で export -> remove_application_scene
"""

import os
import csc


# エクスポートモード -> FbxLoader / FbxSceneLoader のどのメソッドを使うか
EXPORT_MODES = ("all", "model", "joints", "scene")


def find_casc_files(folder, recursive=True):
    """folder 以下の .casc ファイルの絶対パス一覧を返す（昇順）。"""
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


def fbx_path_for(casc_path):
    """casc と同じディレクトリ・同じ basename の .fbx パスを返す。"""
    base, _ext = os.path.splitext(casc_path)
    return base + ".fbx"


def make_fbx_settings(*, ascii=False, up_axis=None,
                      apply_euler_filter=None, bake_animation=None):
    """csc.fbx.FbxSettings を組み立てて返す（指定された項目だけ設定）。

    up_axis: "X" / "Y" / "Z"（大文字小文字不問）。None なら未設定（既定）。
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
    """ロード済みの view_scene を out_path へ FBX 書き出し。"""
    tool = tools_manager.get_tool("FbxSceneLoader")

    if export_mode == "scene":
        # シーン全体（FbxSceneLoader 経由）
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
    """rig_mode の on->off ラウンドトリップ（任意）。

    casc_import_export.py が行う「処理」を再現したい場合に使う。
    依存が重く環境により失敗しうるため遅延 import + 例外は呼び出し側に伝播。
    """
    import rig_mode.on as rm_on
    import rig_mode.off as rm_off
    rm_on.run_raw(domain_scene, [0.0, 0.5, 0.0])
    rm_off.run(domain_scene, True)


def export_one(scene_manager, tools_manager, casc_path, *,
               export_mode="all", fbx_settings=None,
               skip_existing=False, enter_rig_mode=False, log=print):
    """1 つの .casc を読み込んで FBX を書き出す。

    戻り値: ("exported" | "skipped" | "failed", message)
    """
    out_path = fbx_path_for(casc_path)

    if skip_existing and os.path.exists(out_path):
        log(f"  skip (already exists): {out_path}")
        return ("skipped", out_path)

    application_scene = scene_manager.create_application_scene()
    scene_manager.set_current_scene(application_scene)
    try:
        # .casc をこのシーンへ読み込む
        csc.app.ProjectLoader.load_from(casc_path, application_scene.domain_scene())

        if enter_rig_mode:
            _maybe_rig_round_trip(application_scene.domain_scene())

        # 出力先ディレクトリは casc と同じなので既に存在するが念のため
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        _export_loaded_scene(tools_manager, application_scene, out_path, export_mode, fbx_settings)

        log(f"  OK -> {out_path}")
        return ("exported", out_path)

    except Exception as ex:  # noqa: BLE001 - 1 ファイルの失敗で全体を止めない
        log(f"  ERROR: {casc_path}: {ex}")
        return ("failed", f"{casc_path}: {ex}")

    finally:
        # 作業用シーンタブは必ず閉じる（メモリ肥大を防ぐ）
        scene_manager.remove_application_scene(application_scene)


def export_folder_to_fbx(folder, *, recursive=True, export_mode="all",
                         skip_existing=False, enter_rig_mode=False,
                         fbx_settings=None, restore_current_scene=True,
                         log=print):
    """folder 以下の全 .casc を、同じ場所・同じ名前の .fbx に書き出す。

    引数:
      folder              探索の起点フォルダ
      recursive           サブフォルダも辿るか（既定 True）
      export_mode         "all"/"model"/"joints"/"scene"（既定 "all"）
      skip_existing       既に .fbx があればスキップ（既定 False = 上書き）
      enter_rig_mode      読み込み後に rig mode on->off を実行（既定 False）
      fbx_settings        csc.fbx.FbxSettings（既定 None = Cascadeur 既定）
      restore_current_scene  処理後に元のシーンタブへ戻すか（既定 True）
      log                 ログ出力関数（既定 print。アドオンでは scene.info を渡す）

    戻り値: 集計 dict {total, exported, skipped, failed, failures, outputs}
    """
    if export_mode not in EXPORT_MODES:
        raise ValueError(f"export_mode must be one of {EXPORT_MODES}, got {export_mode!r}")

    folder = os.path.abspath(folder)
    if not os.path.isdir(folder):
        raise NotADirectoryError(f"folder not found: {folder}")

    app = csc.app.get_application()
    scene_manager = app.get_scene_manager()
    tools_manager = app.get_tools_manager()

    original_view = None
    if restore_current_scene:
        try:
            original_view = scene_manager.current_scene()
        except Exception:  # noqa: BLE001
            original_view = None

    files = find_casc_files(folder, recursive=recursive)
    log(f"[batch_export_fbx] {len(files)} .casc files under: {folder} "
        f"(recursive={recursive}, mode={export_mode})")

    summary = {"total": len(files), "exported": 0, "skipped": 0,
               "failed": 0, "failures": [], "outputs": []}

    for i, casc_path in enumerate(files, 1):
        log(f"[{i}/{len(files)}] {casc_path}")
        status, info = export_one(
            scene_manager, tools_manager, casc_path,
            export_mode=export_mode, fbx_settings=fbx_settings,
            skip_existing=skip_existing, enter_rig_mode=enter_rig_mode, log=log)
        if status == "exported":
            summary["exported"] += 1
            summary["outputs"].append(info)
        elif status == "skipped":
            summary["skipped"] += 1
        else:
            summary["failed"] += 1
            summary["failures"].append(info)

    # 元のシーンタブへ戻す
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
