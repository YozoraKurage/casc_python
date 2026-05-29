# アドオンの基本

> 公式ヘルプ: [Python scripting in Cascadeur](https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur)

Cascadeur のアドオンは「特別なクラスを継承する」のではなく、**決められた名前の関数を持つ Python モジュール**を、決められたフォルダに置くだけで成立します。Cascadeur がフォルダを走査し、その関数を見つけて登録・実行します。

> ⚠️ **アドオンの `.py` は ASCII で書く**: Cascadeur のスクリプトリローダ／`--run-script` ローダは、
> ソース中の日本語などマルチバイト文字をうまくデコードできず `UnicodeDecodeError: unexpected end of
> data` で読み込みに失敗することがあります（同梱の動くスクリプトもコメント・docstring は基本 ASCII）。
> コメント・docstring・ログ文字列は英語（ASCII）にし、日本語の説明は別の README 等（import されない
> ファイル）に置くのが安全です。

---

## アドオンの3形態（再掲）

| 形態 | 必要な関数 | 置き場所 | 起動契機 |
|---|---|---|---|
| コマンド | `run(scene)`（+任意で `command_name()` / `command_description()`） | `commands/` 配下のどこか | ユーザーが手動実行 |
| イベントハンドラ | `run(scene)` | `events/<イベント名>/` 配下 | シーンイベントで自動 |
| スクリプト | 任意の関数 | `samples/` など任意 | アプリ内 Python 実行から |

---

## 自動検出の仕組み

仕組みは `commands_rule.py` / `events_rule.py` に実装されています。要点だけ理解すれば十分です。

### コマンドの検出（`commands_rule.py`）

`commands` パッケージ配下を再帰的に走査し、各モジュールについて関数を調べます。

- `run` 関数があれば「コマンド」とみなす。
- `command_name()` があればその戻り値をコマンド名に、`command_description()` があれば説明文に使う。
- 検出結果は `csc.app.topology_controller.CommandInfo(モジュールパス, 説明)` として登録され、**`Commands` メニュー**に並びます。

```python
# commands_rule.py の中核（抜粋・要約）
functions = getmembers(pkg, isfunction)
for f_name, func in functions:
    if f_name == 'command_name':        name = func()
    if f_name == 'command_description': description = func()
    elif f_name == 'run':               is_command = True
```

### イベントの検出（`events_rule.py`）

`events` パッケージ配下の**サブパッケージ名がイベント名**になり、その中の `run` を持つモジュールがハンドラとして登録されます。

```
events/
├── scene_opened/      ← イベント名
│   └── example.py     ← run(scene) を持てばハンドラ
├── scene_saved/
└── ...
```

---

## いちばん小さいコマンド

`commands/` 配下に次のファイルを作るだけです（例: `commands/hello.py`）。

```python
import csc

def command_name():
    return "Hello"          # コマンド一覧に表示される名前

def command_description():
    return "ログにメッセージを出すだけのサンプル"

def run(scene):
    scene.info("Hello, Cascadeur!")
```

- `command_name()` / `command_description()` は省略可能ですが、付けるとコマンド一覧で見つけやすくなります。
- 命名は `"Add.Locator"` のように**ドット区切り**にすると、メニューの階層として扱われます（標準コマンドの慣習。[`commands/add/add_locator.py`](../cookbook.md) 参照）。

---

## いちばん小さいイベントハンドラ

`events/scene_opened/my_handler.py`:

```python
import csc

def run(scene: csc.domain.Scene):
    scene.info("シーンが開かれました")
```

標準では各イベントフォルダに、何もしない雛形 `example.py`（`def run(scene): pass`）が入っています。

利用できるイベント（同梱フォルダ名）:

| イベント名 | 発火タイミング |
|---|---|
| `scene_created` | 新規シーン作成時 |
| `scene_opened` | シーンを開いた時 |
| `scene_activated` | シーンタブがアクティブになった時 |
| `scene_saved` | シーン保存時 |
| `scene_before_removed` | シーンタブが閉じられる直前 |
| `scene_removed` | シーンタブが閉じられた後 |

詳細は [イベントハンドラ](events.md)。

---

## `run(scene)` の中で使えるもの

`scene` は `csc.domain.Scene`。ここから読み取り Viewer・選択・現在フレームなどに到達します。書き込みは `scene.modify*` トランザクション内で。

```python
import csc

def run(scene):
    # --- 読み取り ---
    mv = scene.model_viewer()
    bv = mv.behaviour_viewer()
    dv = mv.data_viewer()
    lv = scene.layers_viewer()
    frame = scene.get_current_frame()
    selected = [s for s in scene.selector().selected().ids
                if isinstance(s, csc.model.ObjectId)]

    # --- ログ ---
    scene.info("情報"); scene.warning("警告"); scene.error("エラー")

    # --- 書き込み（トランザクション）---
    def mod(model, update, scene_updater):
        de = model.data_editor()
        be = model.behaviour_editor()
        # ... 変更 ...
    scene.modify_update("My command", mod)
```

---

## 前提条件のチェックとエラー通知

標準コマンドは、対象が選択されていない等の前提エラーを `raise Exception(...)` で知らせます。これは Cascadeur 側で捕捉され、ユーザーに表示されます。

```python
def run(scene):
    selected = [s for s in scene.selector().selected().ids
                if isinstance(s, csc.model.ObjectId)]
    if not selected:
        raise Exception("オブジェクトを1つ以上選択してください")
    ...
```

---

## どこに自作アドオンを置くか

実運用の自作コマンドは、ユーザー用のコマンドフォルダに置きます。

```
<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands
```

- Cascadeur は起動時にこのフォルダを初期化し、**`Commands` メニュー**に項目を追加します。
- 起動後に編集したら **`Commands > Reload scripts`** で再読込（再起動不要）。
- `C:\Program Files\Cascadeur\resources\scripts\...`（= 本作業フォルダの `scripts/` の元）は**参照用**。学習・構造の真似には便利ですが、実運用アドオンはユーザーフォルダ側へ。

---

## 次のステップ

- コマンドの詳細（命名・登録・実例） → [コマンドアドオン](commands.md)
- イベントの詳細 → [イベントハンドラ](events.md)
- 変更トランザクションの仕組み → [シーン変更モデル](scene-modification.md)
- 値の読み書き → [ビヘイビアとデータ](behaviours-and-data.md)
