# csc.fbx / csc.external.fbx

FBX のインポート・エクスポートと設定。実践的な使い方は [FBX 入出力 ガイド](../guides/fbx-io.md) を参照。

### 目次
[FbxSceneLoader](#fbxsceneloader) ・ [FbxLoader](#fbxloader) ・ [FbxSettings](#fbxsettings) ・ [FbxSettingsMode / FbxSettingsAxis](#fbxsettingsmode--fbxsettingsaxis) ・ [csc.external.fbx](#cscexternalfbx)

取得経路: `tools_manager.get_tool("FbxSceneLoader")` → `.get_fbx_loader(view_scene)` → `FbxLoader`。

---

## FbxSceneLoader

FBX シーン全体を扱うツール。`tools_manager.get_tool("FbxSceneLoader")` で取得。

| メソッド | 説明 |
|---|---|
| `get_fbx_loader(view_scene)` → `FbxLoader` | シーン用ローダー取得 |
| `import_fbx_scene(view_scene, path)` | シーンをインポート |
| `import_fbx_animation(view_scene, path)` | アニメをインポート |
| `export_fbx_scene(view_scene, path)` | シーンをエクスポート |

---

## FbxLoader

実際の入出力を担う。

### インポート

| メソッド | 説明 |
|---|---|
| `import_scene(path)` | シーンとして取り込む |
| `import_model(path)` | モデルを取り込む |
| `import_animation(path)` | アニメを取り込む |
| `import_animation_to_selected_objects(path)` | 選択オブジェクトへアニメ |
| `import_animation_to_selected_frames(path)` | 選択フレームへアニメ |
| `add_model(path)` | モデルを追加 |
| `add_model_to_selected(path)` | 選択へモデル追加 |

### エクスポート

| メソッド | 説明 |
|---|---|
| `export_all_objects(path)` | 全対象を書き出し |
| `export_model(path)` | モデル |
| `export_joints(path)` | ジョイントのみ |
| `export_scene_selected(path)` | 選択分 |

### 設定

| メソッド | 説明 |
|---|---|
| `set_settings(settings)` | `FbxSettings` を適用 |

```python
def run(scene):
    app = csc.app.get_application()
    def do_export(path):
        loader = app.get_tools_manager().get_tool("FbxSceneLoader") \
                    .get_fbx_loader(app.get_scene_manager().current_scene())
        loader.export_all_objects(path)
    app.get_file_dialog_manager().show_save_file_dialog("fbx", "", ["*.fbx"], do_export)
```

---

## FbxSettings

エクスポート設定。

| プロパティ | 型 | 説明 |
|---|---|---|
| `mode` | `FbxSettingsMode` | Binary / Ascii |
| `up_axis` | `FbxSettingsAxis` | X / Y / Z |
| `apply_euler_filter` | `bool` | オイラーフィルタ |
| `bake_animation` | `bool` | アニメをベイク |
| `export_selected_interval` | — | 選択区間のエクスポート |

```python
from csc import fbx
s = fbx.FbxSettings()
s.mode = fbx.FbxSettingsMode.Ascii
s.up_axis = fbx.FbxSettingsAxis.Y
s.apply_euler_filter = False
loader.set_settings(s)
```

---

## FbxSettingsMode / FbxSettingsAxis

### FbxSettingsMode
`Binary`(0) / `Ascii`(1)。プロパティ `name` / `value`。

### FbxSettingsAxis
`X`(0) / `Y`(1) / `Z`(2)。プロパティ `name` / `value`。

---

## csc.external.fbx

FBX ノードの付加情報を扱う型。

### ExtraDatas
FBX ノードの追加情報。

| プロパティ | 説明 |
|---|---|
| `node_index` | ノードインデックス |
| `pre_rotation` / `post_rotation` | 前/後回転 |
| `size` | サイズ情報 |
| `look` | look |

### FbxDatas
FBX データ設定。

| プロパティ | 説明 |
|---|---|
| `translation` / `rotation` / `scale` | 変換データ |
| `order` | 処理順 |
| `ignore_namespace` | 名前空間を無視するか |

---

[← API 目次](README.md)
