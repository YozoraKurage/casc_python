# はじめに — スクリプトの実行と最初の一歩

このページでは、Cascadeur 内で Python を動かし、最初のスクリプトを書いて実行するところまでを扱います。

---

> 公式ヘルプ: [Python scripting in Cascadeur](https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur)

## 1. `csc` モジュールは「Cascadeur の中」でだけ動く

最重要の前提です。`csc` は Cascadeur 本体に組み込まれたコンパイル済みモジュールなので、**通常のターミナルの `python` では `import csc` できません**。スクリプトは Cascadeur のプロセス内（Python 3.8 系。バージョンにより異なる場合あり）で実行されます。

つまり開発フローは次のようになります。

1. お好みのエディタ（VSCode など）でスクリプトを書く
2. Cascadeur 内の Python 実行機能、またはコマンドとして登録して実行
3. ログ（info/warning/error）や挙動で結果を確認

> エディタ上の補完を効かせたい場合は、`samples/api_document.py` を型ヒントの参考にするか、`csc` の各オブジェクトに対して `print(dir(obj))` / `help(obj)` を実行して定義を確認します。

---

## 2. スクリプトの実行方法

Cascadeur には Python を走らせる経路が3つあります。

### (A) Python コンソールで実行する（検証・使い捨て向き）

メニュー **`Window > Python console`** でコンソールを開きます。ウィンドウには次のボタンがあります。

| ボタン | 機能 |
|---|---|
| **Load** | `.py` ファイルを読み込む |
| **Save** | コンソールの内容を `.py` に保存 |
| **Execute** | 読み込んだスクリプトを実行 |
| **Close** | ウィンドウを閉じる |

その場でコードを書いて `Execute` で走らせる、最も手軽な方法です。

### (B) コマンドとして登録して実行する（推奨・再利用向き）

ユーザー用コマンドフォルダに `run(scene)` を持つモジュールを置きます。Cascadeur は起動時にこのフォルダを初期化し、**`Commands` メニュー**に項目を追加します。

```
<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands
```

→ [コマンドアドオン](guides/commands.md)

### (C) イベントで自動実行する

`events/<イベント名>/` 配下にモジュールを置くと、シーンのオープン・保存などの契機で自動的に呼ばれます。→ [イベントハンドラ](guides/events.md)

> **スクリプトの再読込**: 起動後にコマンドスクリプトを編集したら、**`Commands > Reload scripts`** でアプリを再起動せずに反映できます。
>
> **配置場所の使い分け**: 実運用の自作コマンドは上記の `users\<ユーザー名>\...` 側に置きます。`<Cascadeurフォルダ>\resources\scripts\python\samples` などインストール配下は参照（読み取り）用です。本作業フォルダの `scripts/` はその解析用コピーです。

---

## 3. すべての入口は `run(scene)`

コマンドもイベントも、エントリポイントの形は共通です。

```python
import csc

def run(scene):
    scene.info("Hello, Cascadeur!")  # 画面のログに表示される
```

引数 `scene` は **`csc.domain.Scene`** のインスタンスです（シーンの中身を読み書きする中心オブジェクト）。
ログ出力には次の3メソッドが使えます。

```python
def run(scene):
    scene.info("情報メッセージ")
    scene.warning("警告メッセージ")
    scene.error("エラーメッセージ")
```

---

## 4. 最初のスクリプト: シーンを読む

シーンのオブジェクト数と、各ジョイントの名前を表示してみます。**読み取りだけ**なので Viewer を使います（トランザクション不要）。

```python
import csc

def run(scene):
    mv = scene.model_viewer()        # モデルを読むための Viewer
    bv = mv.behaviour_viewer()       # ビヘイビアを読む Viewer

    objects = mv.get_objects()
    scene.info(f"シーン内オブジェクト数: {len(objects)}")

    # 'Joint' ビヘイビアを持つものを列挙
    joints = bv.get_behaviours("Joint")
    for jid in joints:
        owner = bv.get_behaviour_owner(jid)
        scene.info(f"ジョイント: {mv.get_object_name(owner)}")
```

ポイント:
- `scene.model_viewer()` → `ModelViewer`（オブジェクト一覧・名前）
- `.behaviour_viewer()` → `BehaviourViewer`（ビヘイビアの検索）
- `get_behaviours("Joint")` は **ビヘイビア ID** のリストを返す。所有オブジェクトは `get_behaviour_owner` で取得。

---

## 5. 最初の「変更」: 値を書き換える

書き換えは `scene.modify_update(名前, 関数)` のトランザクション内で、**Editor** を使って行います。次は全ジョイントを少し移動する例です（[`samples/move_joints.py`](cookbook.md) を簡略化）。

```python
import csc

def run(scene):
    mv = scene.model_viewer()
    dv = mv.data_viewer()
    bv = mv.behaviour_viewer()

    joints = bv.get_behaviours("Joint")

    def mod(model_editor, update_editor, scene_updater):
        de = model_editor.data_editor()    # 書き込み用 Editor
        changed = set()

        for jid in joints:
            owner = bv.get_behaviour_owner(jid)
            tr = bv.get_behaviour_by_name(owner, "Transform")
            pos_id = bv.get_behaviour_data(tr, "global_position")
            pos = dv.get_data_value(pos_id, 0)             # フレーム0の値を取得
            de.set_data_value(pos_id, 0, pos + [1.0, 1.0, 1.0])  # 書き込み
            changed.add(pos_id)

        scene_updater.run_update(changed, 0)   # 変更したデータの再計算を促す

    scene.modify_update("Move joints", mod)     # ← これ全体が1回のUndo単位
```

ここで登場した重要要素:
- `scene.modify_update(name, mod)`: 変更トランザクション。`mod` には `(model_editor, update_editor, scene_updater)` が渡される。
- `model_editor.data_editor()`: データ値を書き込む Editor。
- `scene_updater.run_update(data_ids, frame)`: 変更したデータ ID 集合を渡し、依存グラフを再計算。

> なぜトランザクションが必要か、`modify` と `modify_update` の違いは何か等は [シーン変更モデル](guides/scene-modification.md) で詳しく説明します。

---

## 6. デバッグの基本

- **ログ出力**: `scene.info/warning/error(...)` を使う。`print(...)` はアプリのコンソール／標準出力に出ます。
- **例外**: `run` 内で例外を投げると処理が中断します。コマンドでは `raise Exception("メッセージ")` で前提条件エラーを知らせるのが定石（標準コマンドでも多用）。
- **オブジェクトの中身を調べる**: `print(dir(obj))`、`help(type(obj))` で利用可能なメソッドを確認。
- **存在確認**: `Guid` / `ObjectId` / `DataId` などの ID は `is_null()` で有効性を確認できる。
- **リロード**: コマンドスクリプトを編集したら **`Commands > Reload scripts`** で再読込（再起動不要）。Python コンソールのコードは `Execute` で都度実行。

---

## 7. よく使う「お決まり」入口集

```python
import csc

def run(scene):
    # アプリと各種マネージャ
    app = csc.app.get_application()
    scene_manager = app.get_scene_manager()
    tools_manager = app.get_tools_manager()

    # 現在の UI シーンタブ（csc.view.Scene）
    view_scene = scene_manager.current_scene()

    # 現在フレーム
    frame = scene.get_current_frame()

    # 選択中オブジェクト（csc.model.ObjectId のみ抽出）
    selected = [sid for sid in scene.selector().selected().ids
                if isinstance(sid, csc.model.ObjectId)]

    scene.info(f"frame={frame}, selected={len(selected)}")
```

> `scene`（= `csc.domain.Scene`）と `csc.view.Scene` は別物です。`run(scene)` に渡るのは前者（中身）で、後者は UI のタブを表します。両者の関係は [アーキテクチャ](architecture.md) を参照。

---

次へ: [アーキテクチャ](architecture.md) / [アドオンの基本](guides/addon-basics.md)
