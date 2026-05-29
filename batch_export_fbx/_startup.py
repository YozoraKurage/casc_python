"""
batch_export_fbx._startup
=========================

Cascadeur の `--run-script` で実行されるためのブートストラップ。

    cascadeur.exe --run-script commands.batch_export_fbx._startup

`--run-script` は「モジュール名」を取り、Cascadeur の Python パス上にある必要がある
（本パッケージは commands 配下にあるので自動的にパス上にある）。また Cascadeur が
既に起動している状態で実行すること（未起動だと引数がシーン名として誤解釈され得る）。

設定の受け渡し:
- `--run-script` が「起動済みインスタンス」へ転送されると、起動側プロセスの環境変数は
  そのインスタンスに届かない。そのため設定は ~/.casc_batch_export_fbx.json（設定ファイル）
  経由で渡す。ランチャ Export-CascToFbx.ps1 がこのファイルを書き出す。
- 設定ファイルが無ければ環境変数 CASC_BATCH_EXPORT_* にフォールバック。

手動（Python コンソール）でも同等のことができる:
    from commands.batch_export_fbx import cli
    cli.run_auto()                 # 設定ファイル/環境変数から
    cli.run_folder(r"D:\\proj")    # 直接フォルダ指定
"""

try:
    from commands.batch_export_fbx import cli
    cli.run_auto()
except Exception:  # noqa: BLE001
    import traceback
    traceback.print_exc()
