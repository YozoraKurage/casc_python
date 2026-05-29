# API リファレンス目次

`csc` モジュール（および `csc.external`）の全サブモジュール・全クラスを網羅したリファレンスです。同梱の [`samples/api_document.py`](../cookbook.md) を基に、説明を日本語化し、使い方を補足しています。

> 表記について
> - メソッドのシグネチャは `api_document.py` 由来です。`arg0` などの匿名引数はソースのままです。
> - `csc` はコンパイル済みモジュールのため、実環境のバージョンによりメンバーが増減します。最終的には `print(dir(...))` / `help(...)` で確認してください。
> - 型 `numpy.ndarray[numpy.float32[3,1]]` は「3要素の float ベクトル」を意味します（`[x, y, z]` のリストでも受け付ける場面が多い）。

---

## モジュール一覧

| モジュール | 主な内容 | リファレンス |
|---|---|---|
| `csc` | 共通型: `Direction` / `DirectionValue` / `Guid` / `SystemVariables` / `Version` | [csc.md](csc.md) |
| `csc.app` | アプリと各種マネージャ。エントリポイント `get_application()` | [app.md](app.md) |
| `csc.view` | ビュー層: `Scene`（UIタブ）、カメラ、各種ダイアログ | [view.md](view.md) |
| `csc.domain` | ドメインの `Scene`、選択、ピボット、`SceneUpdater`、`Session` | [domain.md](domain.md) |
| `csc.model` | モデル層: Viewer/Editor、ビヘイビア、データ、設定、クラスタ | [model.md](model.md) |
| `csc.layers` | タイムライン: レイヤー、キー、補間、接線、サイクル、選択 | [layers.md](layers.md) |
| `csc.math` | 数学型（行列・回転・クォータニオン・幾何）と関数 | [math.md](math.md) |
| `csc.parts` | パーツ挿入（`Buffer`）、クリップボード、型 | [parts.md](parts.md) |
| `csc.fbx` / `csc.external.fbx` | FBX ローダー・設定 / 付加データ | [fbx.md](fbx.md) |
| `csc.rig` | リギング用データ構造 | [rig.md](rig.md) |
| `csc.tools` | ツール: ミラー・アトラクタ・選択グループ・リギングモード | [tools.md](tools.md) |
| `csc.physics` | 物理: `PosMass` | [physics.md](physics.md) |
| `csc.update` | アップデートグラフ: ノード・グループ・データ・関数・接続 | [update.md](update.md) |
| （アクション） | `call_action` 用アクション ID 一覧（メニュー操作の名前実行） | [actions.md](actions.md) |

---

## よく使う到達経路（早見）

```python
import csc

# アプリ → マネージャ
app = csc.app.get_application()                 # csc.app.Application
app.get_scene_manager()                         # csc.app.SceneManager
app.get_tools_manager()                         # csc.app.ToolsManager
app.get_action_manager()                        # csc.app.ActionManager
app.get_file_dialog_manager()                   # csc.view.FileDialogManager
app.get_setting_manager()                       # csc.app.SettingsManager

# UIシーン → ドメインシーン
view_scene = app.get_scene_manager().current_scene()   # csc.view.Scene
domain     = view_scene.domain_scene()                 # csc.domain.Scene（= run(scene)）

# 読み取り Viewer
mv = domain.model_viewer()                      # csc.model.ModelViewer
bv = mv.behaviour_viewer()                      # csc.model.BehaviourViewer
dv = mv.data_viewer()                           # csc.model.DataViewer
lv = domain.layers_viewer()                     # csc.layers.Viewer

# 書き込み（modify の中）
def mod(model, update, scene_updater):
    be = model.behaviour_editor()               # csc.model.BehaviourEditor
    de = model.data_editor()                    # csc.model.DataEditor
    le = model.layers_editor()                  # csc.layers.Editor
```

---

[← ドキュメントトップへ戻る](../README.md)
