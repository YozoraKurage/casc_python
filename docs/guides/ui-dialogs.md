# UI・ダイアログ

アドオンからユーザーに情報を見せたり、入力を受け取ったりするための UI 機能をまとめます。中心は `csc.view.DialogManager`（情報・入力・ボタン）と `csc.view.FileDialogManager`（ファイル・フォルダ選択）です。

---

## ログ出力（最も手軽）

ダイアログを出すまでもない通知は、`scene`（`csc.domain.Scene`）のログメソッドで。

```python
def run(scene):
    scene.info("処理を開始します")
    scene.warning("対象が見つかりませんでした")
    scene.error("失敗しました")
```

---

## 情報ダイアログ

```python
import csc

def run(scene):
    csc.view.DialogManager.instance().show_info("タイトル", "本文メッセージ")
```

`DialogManager` は**シングルトン**で、`csc.view.DialogManager.instance()` で取得します。

---

## ボタンダイアログ

複数の選択肢を提示し、押されたボタンに応じてコールバックを実行します。

```python
import csc

def run(scene):
    dm = csc.view.DialogManager.instance()
    buttons = [
        csc.view.DialogButton("実行", lambda: scene.info("実行を押した")),
        csc.view.DialogButton(csc.view.StandardButton.Cancel),     # 標準ボタン（キャンセル）
    ]
    dm.show_buttons_dialog("確認", "処理を実行しますか？", buttons)
```

- `csc.view.DialogButton(text, callback)`: 任意ラベル + コールバック。
- `csc.view.DialogButton(csc.view.StandardButton.Ok / Cancel / Yes / No[, callback])`: 標準ボタン。
- 標準ボタンの種類は `Ok` / `Cancel` / `Yes` / `No`（`csc.view.StandardButton`）。

```python
buttons = [
    csc.view.DialogButton(csc.view.StandardButton.Yes, lambda: scene.success('Yes')),
    csc.view.DialogButton(csc.view.StandardButton.No,  lambda: scene.success('No')),
    csc.view.DialogButton(csc.view.StandardButton.Cancel, lambda: scene.success('Cancel')),
]
```

---

## 入力ダイアログ

複数のテキスト入力欄を出し、入力値をコールバックで受け取ります。

```python
import csc

def run(scene):
    def input_callback(new_values):       # new_values: List[str]
        if not new_values:
            return                        # キャンセル時は空
        for v in new_values:
            scene.warning(v)

    csc.view.DialogManager.instance().show_inputs_dialog(
        "Test1",                  # タイトル
        ["f1", "f2", "f3"],       # 各入力欄のラベル
        ["v1", "v2", "v3", "v4"], # 既定値（プレフィル）
        5,                        # 入力欄の数
        input_callback)           # 入力確定時のハンドラ
```

（[`samples/show_inputs_dialog.py`](../cookbook.md) と同じ。）

引数の並びは `show_inputs_dialog(title, field_names, field_fills, field_count, handler)`。
単一入力欄なら `show_input_dialog(title, label, default, handler)` も使えます。

### 入れ子の例（ボタン→入力→情報）

```python
def run(scene):
    dm = csc.view.DialogManager.instance()

    def on_open():
        def on_input(values):
            dm.show_info("入力値", "".join(values))
        dm.show_inputs_dialog("入力", ["a", "b"], [], 2, on_input)

    dm.show_buttons_dialog("メニュー", "開く？",
                           [csc.view.DialogButton("開く", on_open),
                            csc.view.DialogButton(csc.view.StandardButton.Cancel)])
```

---

## ファイル／フォルダ選択ダイアログ

`csc.view.FileDialogManager` は `csc.app.get_application().get_file_dialog_manager()` から取得します。コールバックに選択パスが渡る非同期スタイルです。

```python
import csc

def run(scene):
    fdm = csc.app.get_application().get_file_dialog_manager()

    # 開く
    def on_open(path):
        scene.info(f"開く: {path}")
    fdm.show_open_file_dialog("ファイルを選択", "", ["*.fbx"], on_open)

    # 保存
    def on_save(path):
        scene.info(f"保存先: {path}")
    fdm.show_save_file_dialog("保存先を選択", "", ["*.fbx"], on_save)

    # フォルダ
    def on_folder(path):
        scene.info(f"フォルダ: {path}")
    fdm.show_folder_dialog("フォルダを選択", on_folder)
```

| メソッド | 引数 |
|---|---|
| `show_open_file_dialog` | `(title, path, filters, handler)` |
| `show_save_file_dialog` | `(title, path, filters, handler)` |
| `show_folder_dialog` | `(title, handler)` |

`filters` はワイルドカードのリスト（例 `["*.fbx"]`、`["*.png", "*.jpg"]`）。
Windows パスはコールバック内で `path.replace('\\', '/')` と正規化しておくと安全です（FBX 例で頻出）。

---

## カメラ・ビューポート操作

UI 寄りの操作として、カメラのターゲット設定やズームも可能です（`csc.view.Camera` / `csc.view.ViewPortDomain`）。

```python
def run(scene):
    app = csc.app.get_application()
    vp = app.current_scene().active_viewport().domain_viewport()
    cam = vp.camera()
    # cam.zoom_to_points([...]) などはカメラの型に依存
```

詳細は [csc.view リファレンス](../api/view.md) を参照。

---

関連: [csc.view リファレンス](../api/view.md) / [FBX 入出力](fbx-io.md)
