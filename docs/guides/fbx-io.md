# FBX 入出力

FBX のインポート／エクスポートは `FbxSceneLoader` ツールと、そこから得られる `FbxLoader` を通じて行います。設定は `csc.fbx.FbxSettings` で調整します。

---

## ローダーの取得

`FbxSceneLoader` ツールを `tools_manager` から取得し、対象の UI シーン（`csc.view.Scene`）に対する `FbxLoader` を得ます。

```python
import csc

def get_fbx_loader():
    app = csc.app.get_application()
    current_scene = app.get_scene_manager().current_scene()        # csc.view.Scene
    tool = app.get_tools_manager().get_tool("FbxSceneLoader")
    return tool.get_fbx_loader(current_scene)                      # csc.fbx.FbxLoader
```

---

## インポート

```python
def run(scene):
    app = csc.app.get_application()

    def do_import(path):
        path = path.replace('\\', '/')                 # Windowsパス正規化
        loader = get_fbx_loader()
        loader.import_scene(path)                      # シーンとしてインポート
        # loader.import_model(path)                    # モデルのみ
        # loader.import_animation(path)                # アニメのみ
        # loader.import_animation_to_selected_objects(path)
        # loader.import_animation_to_selected_frames(path)

    app.get_file_dialog_manager().show_open_file_dialog(
        "Select .fbx file", "", ["*.fbx"], do_import)
```

| メソッド | 内容 |
|---|---|
| `import_scene(path)` | シーン全体としてインポート |
| `import_model(path)` | モデル（メッシュ・ジョイント）をインポート |
| `import_animation(path)` | アニメーションを取り込む |
| `import_animation_to_selected_objects(path)` | 選択オブジェクトにアニメを適用 |
| `import_animation_to_selected_frames(path)` | 選択フレーム範囲にアニメを適用 |
| `add_model(path)` / `add_model_to_selected(path)` | モデルを追加 |

---

## エクスポート

```python
def run(scene):
    app = csc.app.get_application()

    def do_export(path):
        loader = get_fbx_loader()
        loader.export_all_objects(path)                # 全エクスポート対象を書き出し
        # loader.export_model(path)                    # モデルのみ
        # loader.export_joints(path)                   # ジョイントのみ
        # loader.export_scene_selected(path)           # 選択分のみ

    app.get_file_dialog_manager().show_save_file_dialog(
        "Choose filename fbx", "", ["*.fbx"], do_export)
```

| メソッド | 内容 |
|---|---|
| `export_all_objects(path)` | エクスポート可能な全オブジェクト |
| `export_model(path)` | モデル |
| `export_joints(path)` | ジョイントのみ |
| `export_scene_selected(path)` | 選択中の要素 |

`FbxSceneLoader` 直接呼び出し版もあります: `export_fbx_scene(view_scene, path)` / `import_fbx_scene(view_scene, path)` / `import_fbx_animation(view_scene, path)`。

---

## 設定（FbxSettings）

`set_settings(settings)` でエクスポートの挙動を変えられます。

```python
from csc import fbx

def run(scene):
    app = csc.app.get_application()

    def do_export(path):
        settings = fbx.FbxSettings()
        settings.mode = fbx.FbxSettingsMode.Ascii        # Binary / Ascii
        settings.up_axis = fbx.FbxSettingsAxis.Y         # X / Y / Z
        settings.apply_euler_filter = False              # オイラーフィルタ
        settings.bake_animation = True                   # アニメをベイク

        loader = get_fbx_loader()
        loader.set_settings(settings)
        loader.export_all_objects(path)

    app.get_file_dialog_manager().show_save_file_dialog(
        "Choose filename fbx", "", ["*.fbx"], do_export)
```

| プロパティ | 型 | 意味 |
|---|---|---|
| `mode` | `FbxSettingsMode`（`Binary` / `Ascii`） | 出力形式 |
| `up_axis` | `FbxSettingsAxis`（`X` / `Y` / `Z`） | 上方向軸 |
| `apply_euler_filter` | bool | オイラーフィルタの適用 |
| `bake_animation` | bool | アニメーションのベイク |
| `export_selected_interval` | — | 選択区間のエクスポート設定 |

`csc.external.fbx` には、ノードごとの付加情報（`ExtraDatas`: pre/post-rotation など）や `FbxDatas`（順序・回転・スケール・名前空間無視）を扱う型もあります（[csc.fbx リファレンス](../api/fbx.md)）。

---

## 独自エクスポータの実例

同梱コマンドに、特定プラットフォーム向けのエクスポータ実装があります（クックブック参照）。

- [`commands/export_to_roblox.py`](../cookbook.md)
- [`commands/expotr_to_daz.py`](../cookbook.md)（ファイル名は原文ママ）
- [`commands/quick_export/`](../cookbook.md), [`commands/custom_export/`](../cookbook.md)

これらは「選択／対象の収集 → FBX 設定 → エクスポート → 後処理」という流れで、独自要件に合わせて FBX 出力をカスタマイズする雛形になります。

---

関連: [csc.fbx リファレンス](../api/fbx.md) / [UI・ダイアログ](ui-dialogs.md) / [クックブック](../cookbook.md)
