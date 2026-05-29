# イベントハンドラ

イベントハンドラは、シーンの作成・オープン・保存などの契機で **自動的に** 実行されるアドオンです。`events/<イベント名>/` 配下に `run(scene)` を持つモジュールを置くだけで登録されます。

---

## 仕組み

`events_rule.py` が `events` パッケージを走査し、

1. `events` の**サブパッケージ名**をイベント名として扱う
2. そのサブパッケージ内で `run` 関数を持つモジュールをハンドラとして集める

という形でイベント→ハンドラの対応表を作ります。

```
events/
├── scene_created/      ← イベント名
│   ├── example.py      ← run(scene) があればハンドラ
│   └── my_handler.py   ← 複数置ける
├── scene_opened/
├── scene_activated/
├── scene_saved/
├── scene_before_removed/
└── scene_removed/
```

1つのイベントフォルダに複数のハンドラを置けます。

---

## 利用できるイベント

| フォルダ名（イベント名） | 発火タイミング | 主な用途 |
|---|---|---|
| `scene_created` | 新規シーンを作成した時 | 初期セットアップ、既定オブジェクト配置 |
| `scene_opened` | 既存シーンを開いた時 | 互換性チェック、自動修正、統計表示 |
| `scene_activated` | シーンタブがアクティブ化された時 | タブ切替時の状態更新 |
| `scene_saved` | シーンを保存した時 | 保存ログ、付随ファイル出力、バックアップ |
| `scene_before_removed` | シーンタブが閉じられる**直前** | 後始末・確認、未保存検出 |
| `scene_removed` | シーンタブが閉じられた**後** | リソース解放、ログ |

> イベント名はフォルダ名で決まります。標準では各フォルダに、何もしない雛形 `example.py`（`def run(scene): pass`）が入っています。

---

## いちばん小さいハンドラ

`events/scene_opened/log_open.py`:

```python
import csc

def run(scene: csc.domain.Scene):
    scene.info(f"シーンを開きました（オブジェクト数: {len(scene.model_viewer().get_objects())}）")
```

`run` の引数は、コマンドと同じく `csc.domain.Scene` です。

---

## 実例: 開いたシーンを検査して警告する

`scene_opened` で、メッシュが1つも無ければ警告する例。

```python
import csc

def run(scene: csc.domain.Scene):
    mv = scene.model_viewer()
    bv = mv.behaviour_viewer()
    if len(bv.get_behaviours("MeshObject")) == 0:
        scene.warning("このシーンにはメッシュがありません")
```

---

## イベント内で変更を行う場合の注意

イベントハンドラ内でもシーンを変更できますが、自動発火の文脈では副作用に注意が必要です。

- 変更は通常どおり `scene.modify*` トランザクションで行う（Undo 単位になる）。
- `scene_opened` で勝手に変更すると、ユーザーから見て「開いただけで変更扱い」になり戸惑わせることがあります。**自動修正は控えめに**、必要なら確認ダイアログ（[UI・ダイアログ](ui-dialogs.md)）を挟むのが親切です。
- `scene_saved` 中にさらに保存処理を呼ぶなど、**再帰的な発火**を招く操作は避ける。

```python
import csc

def run(scene: csc.domain.Scene):
    # 例: 開いた時に古い命名のオブジェクトを自動リネーム（必要な場合のみ）
    targets = [...]
    if not targets:
        return

    def mod(model, update, scene_updater):
        ...
    scene.modify_update("Auto fix on open", mod)
```

---

## デバッグのヒント

- イベントは UI 操作の裏で走るため、`scene.info/warning` でログを残すと挙動を追いやすい。
- 例外を投げると、そのイベントのその回の処理が中断します。重要イベントでは `try/except` で握りつぶさず、原因をログに出す。
- 「思ったタイミングで動かない」ときは、フォルダ名（=イベント名）の綴りと、`run` 関数の有無をまず確認。

---

関連: [アドオンの基本](addon-basics.md) / [コマンドアドオン](commands.md) / [シーン変更モデル](scene-modification.md)
