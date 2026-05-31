# batch_export_fbx — .casc 一括 FBX 書き出し（GUIコマンド）

指定したフォルダ以下の **すべての `.casc` プロジェクト** を、
**同じディレクトリ・同じファイル名** で FBX に書き出す Cascadeur アドオンです。

```
D:\proj\char\walk.casc   ->  D:\proj\char\walk.fbx
D:\proj\char\run.casc    ->  D:\proj\char\run.fbx
D:\proj\enemy\idle.casc  ->  D:\proj\enemy\idle.fbx   （サブフォルダも再帰）
```

運用は **GUI コマンド** が主役です。検証・切り分け用に Python コンソールからも呼べます。

---

## ⚠️ ソースは ASCII のみ（重要）

Cascadeur のスクリプトリローダ／`--run-script` ローダは、**ソース中の日本語などマルチバイト
文字をうまくデコードできず**、`UnicodeDecodeError: unexpected end of data` で読み込みに失敗
することがあります（同梱の動くスクリプトもコメント・docstring は基本 ASCII）。

そのため本ツールの `.py` は **すべて ASCII（英語コメント）** で書いています。
**日本語の説明はこの README に集約**しており、README は import されないので影響しません。
`.py` を編集する際は **ASCII を維持**してください（日本語コメントを足すと再び読み込みに失敗します）。

---

## ファイル構成

| ファイル | 役割 |
|---|---|
| `core.py` | 中核ロジック（`export_folder_to_fbx` ほか）。GUI/コンソール非依存 |
| `command.py` | GUIコマンド本体（`Commands` メニュー → フォルダ選択 → 一括書き出し） |
| `cli.py` | コンソール用ヘルパー（`run_folder` / `run_file`）。検証・切り分け用 |
| `README.md` | このドキュメント（日本語可・import されない） |

---

## インストール

このフォルダ `batch_export_fbx/` を、Cascadeur のユーザーコマンドフォルダ配下に置きます。

```
<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands\yozolab\batch_export_fbx\
```

Cascadeur を起動（または `Commands > Reload scripts`）すると、`Commands` メニューに
**`Export > Batch casc to FBX`** が現れます。

> このリポジトリでは `commands/yozolab/batch_export_fbx/`（インストール先と同じ構成）に置いています
> （`scripts/` は git 管理対象外のため）。利用時は `commands/yozolab/` ごと上記のユーザー
> コマンドフォルダ配下へコピー／配置してください（`yozolab/__init__.py` も必要）。

---

## 使い方

### 1) GUIコマンド（主運用）

`Commands > Export > Batch casc to FBX` を実行 → フォルダ選択ダイアログで対象フォルダを選ぶ
→ 配下の全 `.casc` が同じ場所・同じ名前で FBX 出力され、結果がダイアログ表示されます。

挙動（再帰の有無・上書き・モード等）を変えたいときは [`command.py`](command.py) 先頭の定数を編集します。

```python
RECURSIVE = True          # サブフォルダも辿る
EXPORT_MODE = "all"       # "all" / "model" / "joints" / "scene"
SKIP_EXISTING = False     # True = 既存 .fbx をスキップ（False = 上書き）
ENTER_RIG_MODE = False    # True = 読み込み後に rig mode on->off
FBX_SETTINGS = None       # 例: core.make_fbx_settings(ascii=False, up_axis="Y")
```

### 2) Python コンソール（検証・切り分け）

`Window > Python console` を開いて:

```python
from commands.yozolab.batch_export_fbx import cli
cli.run_folder(r"D:\path\to\projects")                       # 既定: 再帰 / all / 上書き
cli.run_folder(r"D:\proj", export_mode="model", skip_existing=True)

# 1 ファイルだけ試す（不具合切り分け）
cli.run_file(r"D:\proj\walk.casc")
cli.run_file(r"D:\proj\walk.casc", export_mode="scene")
```

---

## オプション

| 引数（`run_folder` / `command.py` 定数） | 既定 | 内容 |
|---|---|---|
| `recursive` / `RECURSIVE` | True | サブフォルダも辿る |
| `export_mode` / `EXPORT_MODE` | `"all"` | `all`=全オブジェクト / `model`=モデル / `joints`=ジョイント / `scene`=シーン |
| `skip_existing` / `SKIP_EXISTING` | False | 既存 `.fbx` があればスキップ（False=上書き） |
| `enter_rig_mode` / `ENTER_RIG_MODE` | False | 読み込み後に rig mode on→off（`casc_import_export.py` 相当の前処理） |
| `ascii`（`run_folder` のみ） | False | FBX を Ascii で出力（既定 Binary） |
| `up_axis`（`run_folder` のみ） | None | 上方向軸 `X`/`Y`/`Z`（未指定なら Cascadeur 既定） |

---

## 進捗の通知

Cascadeur には専用のプログレスバー API が無いため、進捗は**テキスト**で通知します。
各ファイル開始時に `[i/total] 進捗% (remaining N) ファイル名`、各 .casc の load/OK/skip/error、
最後にサマリが出ます。

| 実行方法 | 進捗の出る場所 |
|---|---|
| GUIコマンド | **イベントログ**（`Window > Event log`）＋完了時にダイアログ |
| コンソール `run_folder()` | **コンソール**＋**イベントログ**の両方（`log=None` の既定） |

GUI 等から進捗をフックしたい場合は `progress` コールバックを渡せます（粒度はファイル単位）:

```python
from commands.yozolab.batch_export_fbx import cli
def on_progress(done, total, status, casc_path):
    print(f"{int(done*100/total)}%  {status}  {casc_path}")
cli.run_folder(r"D:\proj", progress=on_progress)
```

---

## 仕組み（使用 API）

公式の確立パターン（`resources/scripts/python/samples/casc_import_export.py`）に準拠:

1. `scene_manager.create_application_scene()` で作業用シーンタブを作成
2. `csc.app.ProjectLoader.load_from(casc_path, scene.domain_scene())` で `.casc` を読み込み
3. `tools_manager.get_tool("FbxSceneLoader")` →
   `get_fbx_loader(scene).export_all_objects(out_path)`（モードに応じて `export_model` 等）
4. 書き出し後に**実ファイルの存在・サイズ・更新時刻を検証**（`export_*` は失敗しても例外を出さない
   ことがあるため。作られていなければ `failed` 扱い）
5. `scene_manager.remove_application_scene(scene)` で作業タブを閉じる（メモリ肥大防止）

パスは `.casc` 読み込み・`.fbx` 出力ともに**フォワードスラッシュに正規化**します
（バックスラッシュだとエクスポータがサイレント失敗し得るため）。
1ファイルが失敗しても残りは継続し、最後に `exported / skipped / failed` を集計します。

---

## トラブルシュート

| 症状 | 原因・対処 |
|---|---|
| `UnicodeDecodeError: unexpected end of data`（読み込み時） | `.py` に非ASCII文字が混入。コメント等を ASCII に戻す（上記「ソースは ASCII のみ」） |
| `OK` と出るのに FBX が無い | 旧版の不具合。現行版はパス正規化＋実ファイル検証済み。まだ出る場合は `cli.run_file(...)` でモードを変えて切り分け |
| `export reported success but file was not created` | シーンに書き出し対象が無い／モード不一致。`export_mode` を `scene`/`model`/`all` で試す |
| `Commands` メニューに出ない | 配置先が違う／`Commands > Reload scripts` 未実行／`command_name`・`run` の有無を確認 |

---

## 注意

- `csc` は Cascadeur 内蔵モジュールのため、**Cascadeur のプロセス内**でのみ動作します（素のターミナル python では `import csc` 不可）。
- 既定は**上書き**です。残したい場合は `skip_existing=True` / `SKIP_EXISTING=True`。
- `enter_rig_mode` はリグの重い変換を伴うため、通常のエクスポートでは不要です（既定 OFF）。
- 対象バージョン: Cascadeur v2026.1.2（API 名はバージョンで変わる可能性あり）。

関連ドキュメント: [FBX 入出力](../../../docs/guides/fbx-io.md) / [csc.fbx](../../../docs/api/fbx.md) / [コマンドアドオン](../../../docs/guides/commands.md)
