# ビヘイビアとデータ

オブジェクトの中身を読み書きする実践ガイドです。[アーキテクチャ](../architecture.md) の「オブジェクト・ビヘイビア・データの3層」を具体化します。

---

## 3層モデルのおさらい

```
Object（ObjectId）
  └─ Behaviour（Guid・型名つき: 'Transform','Joint','MeshObject',...）
       └─ 名前付きスロット
            ├─ data        → DataId（値: ベクトル/回転/行列…、フレーム単位）
            ├─ setting     → SettingId（bool/int）
            ├─ object      → ObjectId（別オブジェクトへの参照、例: parent）
            ├─ reference   → Guid（別ビヘイビアへの参照）
            └─ asset       → Guid（メッシュ等のアセット）
```

各スロットは「単一値」と「範囲（range / リスト）」の2系統があります。

---

## 読み取り: BehaviourViewer / DataViewer

```python
def run(scene):
    mv = scene.model_viewer()
    bv = mv.behaviour_viewer()
    dv = mv.data_viewer()

    obj = mv.get_objects()[0]

    # ① オブジェクト→ビヘイビア（型名で取得）
    tr = bv.get_behaviour_by_name(obj, "Transform")   # → Guid

    # ② ビヘイビア→データスロット
    pos_id = bv.get_behaviour_data(tr, "global_position")  # → DataId

    # ③ データ→値（フレーム指定）
    pos = dv.get_data_value(pos_id, 0)                 # フレーム0の値
    scene.info(str(pos))
```

### BehaviourViewer のスロット取得メソッド早見

| スロット種別 | 単一取得 | 範囲取得 |
|---|---|---|
| データ | `get_behaviour_data(bh, name)` | `get_behaviour_data_range(bh, name)` |
| オブジェクト | `get_behaviour_object(bh, name)` | `get_behaviour_objects_range(bh, name)` |
| 設定 | `get_behaviour_setting(bh, name)` | `get_behaviour_settings_range(bh, name)` |
| 参照(ビヘイビア) | `get_behaviour_reference(bh, name)` | `get_behaviour_reference_range(bh, name)` |
| 文字列 | `get_behaviour_string(bh, name)` | — |

その他: `get_behaviours(type_name)`（型名で全列挙）、`get_behaviours(object_id)`（オブジェクトの全ビヘイビア）、`get_behaviour_owner(bh)`（所有オブジェクト）、`get_behaviour_name(bh)`（型名）。

### 型名で横断的に集める

```python
# シーン内のすべての Joint を列挙
for jid in bv.get_behaviours("Joint"):
    owner = bv.get_behaviour_owner(jid)
    gmat_id = bv.get_behaviour_data(jid, "global_matrix")
    gmat = dv.get_data_value(gmat_id, 0)
    scene.info(f"{mv.get_object_name(owner)} の global_matrix: {gmat}")
```

（[`samples/iterate_joints.py`](../cookbook.md) と同じ形。）

---

## 親子関係を読む

親は `Basic` ビヘイビアの `parent` スロットにあります。

```python
basic = bv.get_behaviour_by_name(obj, "Basic")
parent = bv.get_behaviour_object(basic, "parent")     # → ObjectId
if parent.is_null():
    scene.info("親なし")
else:
    scene.info(f"親: {mv.get_object_name(parent)}")
```

---

## 書き込み: BehaviourEditor / DataEditor

書き込みは `modify*` 内で。

### 既存スロットの値を変える

```python
def run(scene):
    mv = scene.model_viewer(); bv = mv.behaviour_viewer()
    obj = mv.get_objects()[0]
    tr = bv.get_behaviour_by_name(obj, "Transform")
    pos_id = bv.get_behaviour_data(tr, "global_position")

    def mod(model, update, scene_updater):
        de = model.data_editor()
        de.set_data_value(pos_id, 0, [1.0, 2.0, 3.0])
        scene_updater.run_update({pos_id}, 0)
    scene.modify_update("Move", mod)
```

### 新しいデータを作ってスロットに差し込む

```python
def mod(model, update, scene):
    de = model.data_editor()
    be = model.behaviour_editor()
    new = de.add_data(obj, "New Scale", csc.model.DataMode.Animation, [5.0, 5.0, 5.0])
    tr = scene.model_viewer().behaviour_viewer().get_behaviour_by_name(obj, "Transform")
    be.set_behaviour_data(tr, "local_scale", new.id)
scene.modify("Add scale", mod)
```

### ビヘイビアを追加・削除する

```python
def mod(model, update, scene):
    be = model.behaviour_editor()
    bid = be.add_behaviour(obj, "Locator")        # 追加（→ Guid）
    # be.delete_behaviour(bid)                    # 削除
    # be.set_behaviour_model_object(bid, "parent", parent_obj_id)  # オブジェクト参照を設定
scene.modify("Add behaviour", mod)
```

### BehaviourEditor のスロット設定メソッド早見

| 操作 | 単一 | 範囲 |
|---|---|---|
| データ | `set_behaviour_data(bh, name, data_id)` | `set_behaviour_data_to_range(bh, name, [ids])` |
| オブジェクト | `set_behaviour_model_object(bh, name, obj_id)` | `set_behaviour_model_objects_to_range(bh, name, [ids])` |
| 設定 | `set_behaviour_setting(bh, name, setting_id)` | `set_behaviour_settings_to_range(...)` |
| 参照 | `set_behaviour_reference(bh, name, beh_id)` | `set_behaviour_references_to_range(...)` |
| アセット | `set_behaviour_asset(bh, name, asset_id)` | — |
| 文字列 | `set_behaviour_string(bh, name, str)` | — |
| 範囲へ追加/削除 | `add_behaviour_*_to_range` / `erase_behaviour_*_from_range` | — |

---

## データの値の型

`get_data_value` / `set_data_value` が扱う値は次の Union です（NumPy 配列が中心）。

| 種類 | Python での表現 |
|---|---|
| bool | `bool` |
| int | `int` |
| float | `float` |
| ベクトル3 | `numpy.ndarray[float32, (3,)]`（`[x, y, z]` も可） |
| 回転 | `csc.math.Rotation` |
| クォータニオン | `csc.math.Quaternion` |
| 3x3 行列 | `numpy.ndarray[float32, (3,3)]` |
| 4x4 行列 | `numpy.ndarray[float32, (4,4)]` |
| 文字列 | `str` |
| bool3 | `numpy.ndarray[bool, (3,)]` |

リストを渡すと内部で NumPy 配列に変換されます（`[1.0, 2.0, 3.0]` など）。

---

## Static と Animation（再掲・重要）

```python
data = dv.get_data(data_id)              # csc.model.Data（mode, name など）
if data.mode == csc.model.DataMode.Static:
    de.set_data_value(data_id, value)                 # フレームなし
else:
    de.set_data_value(data_id, frame, value)          # 単一フレーム
    # まとめて: de.set_data_value(data_id, {*range(dv.get_animation_size())}, value)
```

- `dv.get_animation_size()` で総フレーム数を取得。
- 値が空（`get_animation_size() == 0`）のシーンでは生成系処理が失敗することがある（[`samples/model_cube.py`](../cookbook.md) は冒頭でチェック）。

---

## メッシュとアセット

メッシュは `MeshObject` ビヘイビアの `mesh` アセットスロットにあります。

```python
am = scene.assets_manager()
for bh in bv.get_behaviours("MeshObject"):
    mesh = bv.get_behaviour_asset(bh, "mesh")     # → アセット Guid
    m = am.at(mesh)                               # → メッシュ本体
    scene.info(f"頂点数: {len(m.positions())}, ポリゴン頂点数: {m.vertices_in_polygon()}")
```

（[`commands/print_mesh_info.py`](../cookbook.md) 参照。）

---

## 設定（Setting）

`Setting` は bool/int の設定値で、`SettingId` で識別します。

```python
sid = bv.get_behaviour_setting(bh, "some_flag")     # → SettingId
val = dv.get_setting_value(sid)                     # bool/int
# 書き込み: de.set_setting_value(sid, True)  /  de.set_setting_value(sid, val, frame)
```

---

関連: [シーン変更モデル](scene-modification.md) / [csc.model リファレンス](../api/model.md) / [発展的なアドオン](advanced-addons.md) / [pycsc](pycsc.md)
