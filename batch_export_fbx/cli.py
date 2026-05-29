"""
batch_export_fbx.cli
====================

Python コンソール / 起動スクリプト用のエントリポイント。

このモジュールは Cascadeur のプロセス内で実行されることを前提とする
（素のターミナル python では `import csc` できない）。

使い方は 3 通り:

1) Python コンソール（最も確実）
   ----------------------------------------------------------------
   from commands.batch_export_fbx import cli
   cli.run_folder(r"D:\\path\\to\\projects")            # 既定: 再帰・all・上書き
   cli.run_folder(r"D:\\proj", recursive=False, ascii=True, up_axis="Y")

2) 起動時スクリプト + 環境変数（ランチャ Export-CascToFbx.ps1 が使用）
   ----------------------------------------------------------------
   環境変数 CASC_BATCH_EXPORT_DIR にフォルダを入れて Cascadeur を起動し、
   起動スクリプトから cli.main_from_env() を呼ぶ。

3) argv（Cascadeur が起動スクリプトへ引数を渡せる場合のみ）
   ----------------------------------------------------------------
   cli.main(["D:/proj", "--no-recursive", "--ascii", "--up-axis", "Y"])
"""

import os
import sys

from . import core


def run_folder(folder, *, recursive=True, export_mode="all",
               skip_existing=False, enter_rig_mode=False,
               ascii=False, up_axis=None, log=print, quit_after=False):
    """フォルダ以下の .casc を一括 FBX 書き出し（コンソール向けの薄いラッパ）。"""
    fbx_settings = None
    if ascii or up_axis is not None:
        fbx_settings = core.make_fbx_settings(ascii=ascii, up_axis=up_axis)

    summary = core.export_folder_to_fbx(
        folder,
        recursive=recursive,
        export_mode=export_mode,
        skip_existing=skip_existing,
        enter_rig_mode=enter_rig_mode,
        fbx_settings=fbx_settings,
        log=log,
    )

    if quit_after:
        _quit_app(log)
    return summary


def default_config_path():
    """ランチャと共有する設定ファイルの既定パス。

    PowerShell 側と一致させるため、~/.casc_batch_export_fbx.json を使う
    （PS: Join-Path $env:USERPROFILE ".casc_batch_export_fbx.json"）。
    """
    return os.path.join(os.path.expanduser("~"), ".casc_batch_export_fbx.json")


def main_from_config(config_path=None, log=print, delete_after=True):
    """設定ファイル(JSON)を読み取って実行する（ランチャ用・最も確実）。

    `--run-script` が「起動済みインスタンス」に転送されると、ランチャ側プロセスの
    環境変数はそのインスタンスに届かない。そのため設定はファイル経由で受け渡す。

    JSON キー: folder(必須), recursive, export_mode, skip_existing,
               enter_rig_mode, ascii, up_axis, quit_after
    """
    import json
    path = config_path or default_config_path()
    # BOM 付き/無し どちらでも読めるよう utf-8-sig
    with open(path, encoding="utf-8-sig") as f:
        cfg = json.load(f)

    folder = cfg.get("folder") or cfg.get("dir")
    if not folder:
        raise RuntimeError(f"設定ファイルに folder がありません: {path}")

    summary = run_folder(
        folder,
        recursive=bool(cfg.get("recursive", True)),
        export_mode=cfg.get("export_mode", "all"),
        skip_existing=bool(cfg.get("skip_existing", False)),
        enter_rig_mode=bool(cfg.get("enter_rig_mode", False)),
        ascii=bool(cfg.get("ascii", False)),
        up_axis=cfg.get("up_axis") or None,
        log=log,
        quit_after=bool(cfg.get("quit_after", False)),
    )

    if delete_after:
        try:
            os.remove(path)  # 使い捨て: 残しておくと次回誤実行の原因になる
        except OSError:
            pass
    return summary


def run_auto(log=print):
    """設定ファイル → 環境変数 の順に探して実行する（_startup.py から呼ぶ）。"""
    cfg = default_config_path()
    if os.path.exists(cfg):
        log(f"[batch_export_fbx] using config: {cfg}")
        return main_from_config(cfg, log=log)
    if os.environ.get("CASC_BATCH_EXPORT_DIR"):
        log("[batch_export_fbx] using environment variables")
        return main_from_env(log=log)
    raise RuntimeError(
        "設定が見つかりません。設定ファイル "
        f"({cfg}) も 環境変数 CASC_BATCH_EXPORT_DIR も未設定です。")


def _env_bool(name, default=False):
    val = os.environ.get(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


def main_from_env(log=print):
    """環境変数から設定を読み取って実行する（ランチャ用）。

    CASC_BATCH_EXPORT_DIR          : 対象フォルダ（必須）
    CASC_BATCH_EXPORT_RECURSIVE    : 0/1（既定 1）
    CASC_BATCH_EXPORT_MODE         : all/model/joints/scene（既定 all）
    CASC_BATCH_EXPORT_SKIP_EXISTING: 0/1（既定 0）
    CASC_BATCH_EXPORT_RIG_MODE     : 0/1（既定 0）
    CASC_BATCH_EXPORT_ASCII        : 0/1（既定 0）
    CASC_BATCH_EXPORT_UP_AXIS      : X/Y/Z（既定 空=未設定）
    CASC_BATCH_EXPORT_QUIT         : 0/1（既定 0。1 なら処理後に Cascadeur を終了）
    """
    folder = os.environ.get("CASC_BATCH_EXPORT_DIR")
    if not folder:
        raise RuntimeError("CASC_BATCH_EXPORT_DIR が設定されていません")

    up_axis = os.environ.get("CASC_BATCH_EXPORT_UP_AXIS") or None
    return run_folder(
        folder,
        recursive=_env_bool("CASC_BATCH_EXPORT_RECURSIVE", True),
        export_mode=os.environ.get("CASC_BATCH_EXPORT_MODE", "all"),
        skip_existing=_env_bool("CASC_BATCH_EXPORT_SKIP_EXISTING", False),
        enter_rig_mode=_env_bool("CASC_BATCH_EXPORT_RIG_MODE", False),
        ascii=_env_bool("CASC_BATCH_EXPORT_ASCII", False),
        up_axis=up_axis,
        log=log,
        quit_after=_env_bool("CASC_BATCH_EXPORT_QUIT", False),
    )


def main(argv=None, log=print):
    """argv を解析して実行する。

    Cascadeur が起動スクリプトへ引数を渡せる場合のみ有効。
    argv=None のときは sys.argv ではなく環境変数経由（main_from_env）にフォールバックする。
    """
    if argv is None:
        # Cascadeur 本体の argv を誤解析しないよう、設定ファイル/環境変数経由にフォールバック
        return run_auto(log=log)

    import argparse
    parser = argparse.ArgumentParser(
        prog="batch_export_fbx",
        description="指定フォルダ以下の全 .casc を同じ場所・同じ名前で FBX 書き出し")
    parser.add_argument("folder", help="対象フォルダ")
    parser.add_argument("--no-recursive", action="store_true", help="サブフォルダを辿らない")
    parser.add_argument("--mode", choices=list(core.EXPORT_MODES), default="all",
                        help="エクスポート種別（既定 all）")
    parser.add_argument("--skip-existing", action="store_true", help="既存 .fbx をスキップ")
    parser.add_argument("--rig-mode", action="store_true", help="読み込み後に rig mode on->off")
    parser.add_argument("--ascii", action="store_true", help="FBX を Ascii で出力")
    parser.add_argument("--up-axis", choices=["X", "Y", "Z"], default=None, help="上方向軸")
    parser.add_argument("--quit", action="store_true", help="処理後に Cascadeur を終了")
    args = parser.parse_args(argv)

    return run_folder(
        args.folder,
        recursive=not args.no_recursive,
        export_mode=args.mode,
        skip_existing=args.skip_existing,
        enter_rig_mode=args.rig_mode,
        ascii=args.ascii,
        up_axis=args.up_axis,
        log=log,
        quit_after=args.quit,
    )


def _quit_app(log=print):
    """処理後に Cascadeur を終了する（ヘッドレス用途）。"""
    try:
        import csc
        csc.app.get_application().get_action_manager().call_action("Application.Exit")
    except Exception as ex:  # noqa: BLE001
        log(f"[batch_export_fbx] quit failed: {ex}")


if __name__ == "__main__":
    # 起動スクリプトとして argv 付きで直接実行された場合
    main(sys.argv[1:])
