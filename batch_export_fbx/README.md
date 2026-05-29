# batch_export_fbx — .casc 一括 FBX 書き出し

指定したフォルダ以下の **すべての `.casc` プロジェクト** を、
**同じディレクトリ・同じファイル名** で FBX に書き出します。

```
D:\proj\char\walk.casc   ->  D:\proj\char\walk.fbx
D:\proj\char\run.casc    ->  D:\proj\char\run.fbx
D:\proj\enemy\idle.casc  ->  D:\proj\enemy\idle.fbx   （サブフォルダも再帰）
```

アドオン（GUI）／Python コンソール／コマンドライン（`--run-script`）の3通りで使えます。

> 公式: [Python scripting in Cascadeur](https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur) / [FAQ](https://cascadeur.com/help/faq)

---

## ファイル構成

| ファイル | 役割 |
|---|---|
| `core.py` | 中核ロジック（`export_folder_to_fbx` など）。GUI/CLI 非依存 |
| `command.py` | アドオン（`Commands` メニュー → フォルダ選択 → 一括書き出し） |
| `cli.py` | コンソール / 起動スクリプト用エントリ（`run_folder` / `main_from_env`） |
| `_startup.py` | 起動スクリプト用ブートストラップ（環境変数を読んで実行） |
| `Export-CascToFbx.ps1` | Windows ランチャ（env 設定 + Cascadeur 起動） |

---

## インストール

このフォルダ `batch_export_fbx/` を、Cascadeur のユーザーコマンドフォルダ配下に置きます。

```
<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands\batch_export_fbx\
```

Cascadeur を起動（または `Commands > Reload scripts`）すると、`Commands` メニューに
**`Export > Batch casc to FBX`** が現れます。

> このリポジトリではツール本体をリポジトリ最上階の `batch_export_fbx/` に置いています
> （`scripts/` は git 管理対象外のため）。利用時はこのフォルダをそのまま上記のユーザー
> コマンドフォルダ配下へコピー／配置してください。

---

## 使い方

### 1) アドオン（GUI・最も簡単）

`Commands > Export > Batch casc to FBX` を実行 → フォルダ選択ダイアログで対象フォルダを選ぶ
→ 配下の全 `.casc` が同じ場所・同じ名前で FBX 出力され、結果がダイアログ表示されます。

挙動（再帰の有無・上書き・モード等）を変えたいときは `command.py` 先頭の定数を編集します。

### 2) Python コンソール（確実・推奨）

`Window > Python console` を開き、次を実行:

```python
from commands.batch_export_fbx import cli
cli.run_folder(r"D:\path\to\projects")                       # 既定: 再帰 / all / 上書き
cli.run_folder(r"D:\proj", recursive=False, ascii=True, up_axis="Y")
cli.run_folder(r"D:\proj", export_mode="model", skip_existing=True)

cli.run_auto()        # 設定ファイル(~/.casc_batch_export_fbx.json) → 環境変数 から
```

### 3) コマンドライン（`--run-script` + ランチャ）

Cascadeur はコマンドラインの **`--run-script <モジュール名>`** で、起動中のインスタンスに
スクリプト（モジュール）を実行させられます。本ツールのモジュール名は
`commands.batch_export_fbx._startup` です。

**素の使い方**（Cascadeur を起動済みであることが前提）:

```powershell
& "C:\Program Files\Cascadeur\cascadeur.exe" --run-script commands.batch_export_fbx._startup
```

ただし `--run-script` はフォルダ等の設定を直接渡せない（起動済みインスタンスへ転送されると
環境変数も届かない）ため、**設定ファイル** `~/.casc_batch_export_fbx.json` 経由で渡します。
これを自動化するのがランチャ `Export-CascToFbx.ps1` です。

```powershell
# 既に Cascadeur を起動している状態で:
.\Export-CascToFbx.ps1 -Folder "D:\projects"

# Cascadeur を自動起動 → 書き出し → 終了（ヘッドレス的な一括処理）:
.\Export-CascToFbx.ps1 -Folder "D:\projects" -StartIfNotRunning -Quit -Ascii -UpAxis Y
```

ランチャは次を行います: ①設定を `~/.casc_batch_export_fbx.json` に書き出し → ②（必要なら）
Cascadeur を起動して待機 → ③`--run-script commands.batch_export_fbx._startup` を送信。
書き出しは Cascadeur プロセス内で走り、`_startup` が設定ファイルを読んで実行・使用後に削除します。

> ⚠️ 仕様上の注意:
> - `--run-script` は**モジュール名**を渡す（絶対パスではない）。モジュールは Cascadeur の
>   Python パス上に必要（`commands/` 配下に置けば自動的にパス上）。必要なら設定で Python パスを追加。
> - **Cascadeur が起動している**状態で実行する。未起動だと引数がシーン名として誤解釈され得る
>   （だから未起動時は `-StartIfNotRunning` で起動＋待機する）。
> - 起動済みの自分の作業セッションに対して `-Quit` を使うとそのセッションごと閉じる点に注意。

---

## オプション

| 引数（`run_folder` / CLI） | 既定 | 内容 |
|---|---|---|
| `recursive` / `--no-recursive` | True | サブフォルダも辿る |
| `export_mode` / `--mode` | `"all"` | `all`=全オブジェクト / `model`=モデル / `joints`=ジョイント / `scene`=シーン |
| `skip_existing` / `--skip-existing` | False | 既存 `.fbx` があればスキップ（False=上書き） |
| `enter_rig_mode` / `--rig-mode` | False | 読み込み後に rig mode on→off（`casc_import_export.py` 相当の前処理） |
| `ascii` / `--ascii` | False | FBX を Ascii で出力（既定 Binary） |
| `up_axis` / `--up-axis` | None | 上方向軸 `X`/`Y`/`Z`（未指定なら Cascadeur 既定） |
| `quit_after` / `--quit` | False | 処理後に Cascadeur を終了（ヘッドレス用途） |

設定の渡し方は2系統:
- **設定ファイル**（ランチャが使用・推奨）: `~/.casc_batch_export_fbx.json`。`_startup` が読む。
- **環境変数**（フォールバック）: `CASC_BATCH_EXPORT_DIR`（必須）, `..._RECURSIVE`, `..._MODE`,
  `..._SKIP_EXISTING`, `..._RIG_MODE`, `..._ASCII`, `..._UP_AXIS`, `..._QUIT`。
  ※`--run-script` が起動済みインスタンスへ転送される場合、起動側の環境変数は届かないため
  設定ファイル方式が確実。`cli.run_auto()` は「設定ファイル → 環境変数」の順に探す。

---

## 仕組み（使用 API）

公式の確立パターン（`resources/scripts/python/samples/casc_import_export.py`）に準拠:

1. `scene_manager.create_application_scene()` で作業用シーンタブを作成
2. `csc.app.ProjectLoader.load_from(casc_path, scene.domain_scene())` で `.casc` を読み込み
3. `tools_manager.get_tool("FbxSceneLoader")` →
   `get_fbx_loader(scene).export_all_objects(out_path)`（モードに応じて `export_model` 等）
4. `scene_manager.remove_application_scene(scene)` で作業タブを閉じる（メモリ肥大防止）

1ファイルが失敗しても残りは継続し、最後に `exported / skipped / failed` を集計します。

---

## 注意

- `csc` は Cascadeur 内蔵モジュールのため、**Cascadeur のプロセス内**でのみ動作します（素のターミナル python では `import csc` 不可）。
- 既定は**上書き**です。残したい場合は `skip_existing=True` / `--skip-existing`。
- `enter_rig_mode` はリグの重い変換を伴うため、通常のエクスポートでは不要です（既定 OFF）。
- 対象バージョン: Cascadeur v2026.1.2（API 名はバージョンで変わる可能性あり）。

関連ドキュメント: [FBX 入出力](../docs/guides/fbx-io.md) / [csc.fbx](../docs/api/fbx.md) / [コマンドアドオン](../docs/guides/commands.md)
