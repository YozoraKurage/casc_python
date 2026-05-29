# csc.view

ビュー（UI）層。シーンタブ、ビューポート、カメラ、各種ダイアログを扱います。

- [Scene](#scene)
- [ViewPort / ViewPortDomain](#viewport--viewportdomain)
- [Camera / CameraType / SphericalCameraStruct](#camera--cameratype--sphericalcamerastruct)
- [DialogManager](#dialogmanager)
- [DialogButton / StandardButton](#dialogbutton--standardbutton)
- [FileDialogManager](#filedialogmanager)

> UI の使い方の解説は [UI・ダイアログ ガイド](../guides/ui-dialogs.md) を参照。

---

## Scene

UI 上のシーンタブ（ビュー）。ドメインの中身へは `domain_scene()` で到達します。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `domain_scene()` | `csc.domain.Scene` | 紐づくドメインシーン（= `run(scene)` の引数と同じ中身） |
| `name()` | `str` | シーン名 |
| `get_path_name()` | `str` | ディスク上のパス |
| `save(path_name)` | `bool` | 指定パスへ保存 |
| `event_log()` | `object` | イベントログ |
| `gravity_per_frame()` | `float` | フレームあたりの重力値 |
| `set_left_bar_visible(enable)` | `None` | 左バーの表示切替 |
| `view_ports()` | `List[object]` | ビューポート一覧 |

```python
import csc
def run(scene):
    sm = csc.app.get_application().get_scene_manager()
    app_scene = sm.current_scene()                  # csc.view.Scene
    print(app_scene.get_path_name(), app_scene.name())
```

> `active_viewport()` は UI 側で提供され、`.domain_viewport()` で `ViewPortDomain` を得られます（FBX 例・ビューポート例で使用）。

---

## ViewPort / ViewPortDomain

### ViewPort

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `domain_viewport()` | `ViewPortDomain` | ドメイン側のビューポート |

### ViewPortDomain

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `camera()` | `object` | カメラ |
| `camera_struct()` | `SphericalCameraStruct` | カメラ構造体 |
| `set_camera_struct(s)` | `None` | カメラ構造体を設定 |
| `id()` | `csc.Guid` | ビューポート ID |
| `mode_visualizers()` | `int` | 可視化モード取得 |
| `set_mode_visualizers(mode)` | `None` | 可視化モード設定 |

```python
def run(scene):
    cs = csc.app.get_application().current_scene()
    vp = cs.active_viewport().domain_viewport()
    print(vp.id())
```

---

## Camera / CameraType / SphericalCameraStruct

### Camera（球面カメラ）

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `set_target(point)` | `None` | 注視点を設定（`ndarray[float32,(3,)]`） |
| `zoom_to_points(points)` | `None` | 指定点群が収まるようズーム |

### CameraType（enum）

| メンバー | 値 |
|---|---|
| `ISOMETRIC` | 0 |
| `PERSPECTIVE` | 1 |

### SphericalCameraStruct

| メンバー | 型 | 説明 |
|---|---|---|
| `target` | Vector3f | 注視点 |
| `position` | Vector3f | 位置 |
| `type` | `CameraType` | カメラ種別 |

---

## DialogManager

ダイアログ表示のシングルトン。`csc.view.DialogManager.instance()` で取得。

| メソッド | 説明 |
|---|---|
| `static instance()` | シングルトンインスタンス |
| `show_info(title, text)` | 情報ダイアログ |
| `show_buttons_dialog(title, text, buttons)` | ボタン群ダイアログ（`buttons` は `List[DialogButton]`） |
| `show_input_dialog(title, label, default, handler)` | 単一入力ダイアログ |
| `show_inputs_dialog(title, field_names, field_fills, field_count, handler)` | 複数入力ダイアログ |

```python
dm = csc.view.DialogManager.instance()
dm.show_info("完了", "処理が終わりました")
```

入力・ボタンの詳しい例は [UI・ダイアログ](../guides/ui-dialogs.md)。

---

## DialogButton / StandardButton

### DialogButton

ダイアログ内のボタン。

- `DialogButton(text, callback)`: 任意ラベル + コールバック
- `DialogButton(standard_button[, callback])`: 標準ボタン

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `text()` | `str` | ボタンの文言 |
| `force_active_focus()` | `bool` | フォーカスを強制するか |

### StandardButton（enum）

| メンバー | 値 |
|---|---|
| `Ok` | 0 |
| `Cancel` | 1 |
| `Yes` | 2 |
| `No` | 3 |

```python
buttons = [
    csc.view.DialogButton("実行", callback),
    csc.view.DialogButton(csc.view.StandardButton.Cancel),
]
csc.view.DialogManager.instance().show_buttons_dialog("確認", "実行?", buttons)
```

---

## FileDialogManager

ファイル・フォルダ選択。`csc.app.get_application().get_file_dialog_manager()` で取得。

| メソッド | 引数 | 説明 |
|---|---|---|
| `show_open_file_dialog` | `(title, path, filters, handler)` | 開くダイアログ |
| `show_save_file_dialog` | `(title, path, filters, handler)` | 保存ダイアログ |
| `show_folder_dialog` | `(title, handler)` | フォルダ選択 |

`filters` はワイルドカードのリスト（例 `["*.fbx"]`）。`handler` には選択パスが渡る。

```python
fdm = csc.app.get_application().get_file_dialog_manager()
fdm.show_save_file_dialog("保存", "", ["*.fbx"], lambda p: scene.info(p))
```

---

[← API 目次](README.md)
