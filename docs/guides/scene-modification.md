# シーン変更モデル（modify / modify_update）

シーンへのあらゆる書き込みは、`scene.modify*` で始まる**トランザクション**の中で行います。これは Cascadeur API の最重要パターンです。

---

## なぜトランザクションが必要か

1. **Undo/Redo の単位**: 1回の `modify*` 呼び出し全体が、ユーザーの「元に戻す」1ステップになります。
2. **整合性**: シーンは内部に依存計算グラフ（アップデートグラフ）を持つため、生の書き換えではなく管理された経路で変更する必要があります。
3. **Editor の入手経路**: 書き込み用の Editor（`DataEditor` など）は、トランザクションのコールバック内でしか取得できません。

---

## 4つのバリエーション

| メソッド | コールバック引数 | いつ使うか |
|---|---|---|
| `modify(name, fn)` | `(model, update, scene)` | 値・ビヘイビアの変更のみ。再計算を自分で管理 or 不要 |
| `modify_update(name, fn)` | `(model, update, scene_updater)` | 変更 + アップデートグラフの再計算（**最頻出**） |
| `modify_with_session(name, fn)` | `(model, update, scene, session)` | 選択変更を伴う |
| `modify_update_with_session(name, fn)` | `(model, update, scene_updater, session)` | 選択変更 + 再計算 |

いずれも戻り値は `bool`（成功可否）。`name` は Undo 履歴に表示される文字列です。

```python
ok = scene.modify_update("My change", mod)
if not ok:
    raise Exception("変更に失敗しました")
```

---

## コールバックに渡るオブジェクト

### `model` — `csc.model.ModelEditor`
書き込み用 Editor の入口。

```python
def mod(model, update, scene_updater):
    be = model.behaviour_editor()   # ビヘイビアの追加・スロット設定
    de = model.data_editor()        # データ値の書き込み・追加
    le = model.layers_editor()      # キー・補間など
    model.delete_objects({obj_id})  # オブジェクト削除
```

### `update` — `csc.update.Update`
アップデートグラフ（オブジェクト内部構造）を編集する。

```python
def mod(model, update, scene_updater):
    root = update.root()                       # 最上位グループ
    obj  = update.get_object_by_id(obj_id)     # 既存オブジェクトのノード
    new  = root.create_object("name")          # 新規オブジェクト
```

### `scene_updater` — `csc.domain.SceneUpdater`
変更を反映させる司令塔。

```python
def mod(model, update, scene_updater):
    # 1) グラフ構造を変えた場合は先に再生成
    scene_updater.generate_update()
    # 2) 変更したデータ ID を渡して再計算
    scene_updater.run_update({data_id}, frame)
    # scene_updater.scene() で domain.Scene にも到達可能
```

### `session` — `csc.domain.Session`（with_session のみ）
選択など、セッション付きの操作。

```python
def mod(model, update, scene, session):
    session.take_selector().select({obj_id}, obj_id)   # obj_id を選択（第2引数はピボット）
```

---

## 典型パターン

### パターンA: 既存の値を変える（最も多い）

```python
def run(scene):
    mv = scene.model_viewer(); bv = mv.behaviour_viewer()
    obj = mv.get_objects()[0]
    tr = bv.get_behaviour_by_name(obj, "Transform")
    pos_id = bv.get_behaviour_data(tr, "global_position")

    def mod(model, update, scene_updater):
        de = model.data_editor()
        de.set_data_value(pos_id, 0, [10.0, 0.0, 0.0])   # フレーム0に書く
        scene_updater.run_update({pos_id}, 0)            # 依存先を再計算
    scene.modify_update("Set position", mod)
```

### パターンB: ビヘイビアやデータを追加する

```python
def run(scene):
    mv = scene.model_viewer()
    obj = mv.get_objects()[0]

    def mod(model, update, scene):                       # ← modify（再計算なし）
        de = model.data_editor()
        be = model.behaviour_editor()
        # アニメ用 Vector3f データを追加
        new = de.add_data(obj, "New Scale", csc.model.DataMode.Animation, [5.0, 5.0, 5.0])
        # Transform ビヘイビアの local_scale スロットに差し込む
        tr = mv.behaviour_viewer().get_behaviour_by_name(obj, "Transform")
        be.set_behaviour_data(tr, "local_scale", new.id)
    scene.modify("Add scale data", mod)
```

### パターンC: 選択を変える

```python
def run(scene):
    objs = scene.model_viewer().get_objects()
    def mod(model, update, scene, session):
        session.take_selector().select(set(objs), objs[0])
    scene.modify_with_session("Select all", mod)
```

（[`common/selection_operations.py`](../cookbook.md) の `select_all` / `clear_selection` がこの形です。）

---

## Static データ と Animation データ

データには2つのモードがあり（`csc.model.DataMode`）、書き込み方が異なります。

| モード | 意味 | 値の書き方 |
|---|---|---|
| `Static` | 時間で変化しない | `de.set_data_value(id, value)`（フレーム指定なし） |
| `Animation` | フレーム単位で変化 | `de.set_data_value(id, frame, value)` または `de.set_data_value(id, {frames}, value)` |

```python
data = dv.get_data(data_id)
if data.mode == csc.model.DataMode.Static:
    de.set_data_value(data_id, value)
else:
    de.set_data_value(data_id, {*range(dv.get_animation_size())}, value)  # 全フレーム
```

（[`commands/restore_values.py`](../cookbook.md) がこの分岐を行っています。）

---

## generate_update と run_update の使い分け

```
■ 既存データの値だけ変えた
    → scene_updater.run_update({変えたDataId...}, frame)   のみ

■ ノード／オブジェクト／接続を追加・変更した（グラフ構造が変わった）
    → scene_updater.generate_update()        ← まず構造を再構築
      scene_updater.run_update({...}, frame)  ← その後で値を再計算
```

`run_update` のフレーム引数は単一 `int` のほか、`csc.layers.index.FramesIndices`（範囲）も取れます。

```python
scene_updater.run_update({pos_id}, csc.layers.index.FramesIndices.from_range(3, 5))
```

---

## よくある落とし穴

- **Viewer を modify の外で取り、Editor を中で取る**。Editor を外で取ろうとすると失敗します。
- **値を変えたのに反映されない** → `run_update(...)` を呼んでいない、または対象 DataId を渡し忘れ。
- **構造を変えたのに壊れる** → `generate_update()` を呼んでいない。
- **選択が変わらない** → `modify` ではなく `*_with_session` を使い、`session.take_selector()` 経由で。
- **巨大ループで毎回 modify** → 1つの `modify*` の中でまとめて処理し、変更 DataId を `set` に貯めて最後に一括 `run_update`。

---

関連: [アーキテクチャ](../architecture.md) / [ビヘイビアとデータ](behaviours-and-data.md) / [csc.domain](../api/domain.md) / [csc.model](../api/model.md) / [csc.update](../api/update.md)
