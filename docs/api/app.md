# csc.app

アプリケーション全体と各種マネージャ。すべての入口は `csc.app.get_application()` です。

- [get_application()](#get_application)
- [Application](#application)
- [SceneManager](#scenemanager)
- [ToolsManager](#toolsmanager)
- [ActionManager](#actionmanager)
- [DataSourceManager](#datasourcemanager)
- [SettingsManager](#settingsmanager)
- [CascadeurTool / SceneTool](#cascadeurtool--scenetool)
- [ProjectLoader](#projectloader)
- [Analitics](#analitics)
- [EventLog](#eventlog)

---

## get_application

```
csc.app.get_application() → csc.app.Application
```

現在のアプリケーションインスタンスを返す。ほぼすべてのスクリプトの起点。

```python
import csc
app = csc.app.get_application()
```

---

## Application

各種マネージャとシーンへのアクセスを集約する中心クラス。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `current_scene()` | `csc.view.Scene` | 現在アクティブな UI シーン |
| `get_scene_manager()` | `SceneManager` | シーン管理 |
| `get_tools_manager()` | `ToolsManager` | ツール取得 |
| `get_action_manager()` | `ActionManager` | アクション呼び出し |
| `get_data_source_manager()` | `DataSourceManager` | シーンのロード・保存 |
| `get_file_dialog_manager()` | `csc.view.FileDialogManager` | ファイルダイアログ |
| `get_scene_clipboard()` | `csc.parts.SceneClipboard` | クリップボード |
| `get_setting_manager()` | `SettingsManager` | 設定値の取得 |

```python
app = csc.app.get_application()
scene_manager = app.get_scene_manager()
tools_manager = app.get_tools_manager()
setting_manager = app.get_setting_manager()
```

---

## SceneManager

シーンタブ（`csc.view.Scene`）の管理。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `current_scene()` | `csc.view.Scene` | 現在のタブ |
| `create_application_scene()` | `csc.view.Scene` | 新規タブを作成 |
| `set_current_scene(scene)` | `None` | 指定タブをアクティブ化 |
| `scenes()` | `List[csc.view.Scene]` | 全タブ |
| `remove_application_scene(scene)` | `None` | タブを閉じる |

```python
sm = csc.app.get_application().get_scene_manager()
current = sm.current_scene()
new_scene = sm.create_application_scene()
sm.set_current_scene(new_scene)
print(len(sm.scenes()))
sm.remove_application_scene(current)
```

---

## ToolsManager

名前でツールを取得する。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_tool(name)` | `object`（ツール） | 指定名のツール |

主なツール名: `FbxSceneLoader`、`MirrorTool`、`AttractorTool`、`AutoPhysicTool`、`RiggingModeTool`、`SelectionGroups`。
多くのツールは `.editor(view_scene)` でシーン用エディタを得て使います（[csc.tools](tools.md)）。

```python
tm = csc.app.get_application().get_tools_manager()
fbx_tool = tm.get_tool("FbxSceneLoader")
```

---

## ActionManager

メニュー項目などの内部アクションを名前で実行する。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `call_action(name)` | `None` | アクションを実行 |

```python
csc.app.get_application().get_action_manager().call_action("Scene.Undo")
```

呼び出せるアクション ID の一覧は [アクション ID 一覧](actions.md) を参照（将来非推奨予定のため、専用 API があればそちらを優先）。

---

## DataSourceManager

シーンファイルのロード・保存。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `load_scene(file_name)` | `bool` | ファイルから読み込み |
| `close_scene(scene)` | `None` | シーンを閉じる |
| `save_current_scene()` | `None` | 現在シーンを保存 |
| `save_scene(scene_view)` | `None` | 指定シーンを保存 |
| `save_scene_as(scene_view, full_file_name)` | `None` | 名前を付けて保存 |

---

## SettingsManager

アプリ設定値の取得。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_color_value(key)` | `ndarray[float32, (3,)]` | 色 |
| `get_float_value(key)` | `float` | 浮動小数 |
| `get_bool_value(key)` | `bool` | 真偽値（※利用例あり） |

```python
sm = csc.app.get_application().get_setting_manager()
create_layer = sm.get_bool_value("SCENE/CreateNewLayerWhenCreatingAnObject")
```

> 設定キーは `"SCENE/..."` のようなパス文字列。`add_locator.py` で `get_bool_value` の使用例があります。

---

## CascadeurTool / SceneTool

`CascadeurTool` は `ToolsManager.get_tool(...)` で得られるツールの基底。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `editor(view_scene)` | `SceneTool` | シーンに紐づくエディタを取得 |
| `name()` | `str` | ツール名 |

`SceneTool` はシーンに紐づくツールユーティリティ（具体機能は各ツール側）。

---

## ProjectLoader

| 静的メソッド | 戻り値 | 説明 |
|---|---|---|
| `load_from(path, domain_scene)` | `None` | 指定ソースからシーンをロード |

---

## Analitics

| 静的メソッド | 説明 |
|---|---|
| `send_action(type, key='', label='')` | 解析用アクションを送信 |

---

## EventLog

アプリイベントのログを表すクラス（`csc.view.Scene.event_log()` 等から得る）。

---

> 補足: コマンド登録に使われる `csc.app.topology_controller`（`CommandInfo`）は `api_document.py` には記載がありませんが、`commands_rule.py` が内部利用します（[アドオンの基本](../guides/addon-basics.md) 参照）。

[← API 目次](README.md)
