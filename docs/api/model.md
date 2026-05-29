# csc.model

モデル層。シーンのオブジェクト・ビヘイビア・データ・設定を読み書きする中核モジュールです。**読み取りは Viewer、書き込みは Editor**（`modify*` 内で取得）という分離が基本です。

実践的な使い方は [ビヘイビアとデータ ガイド](../guides/behaviours-and-data.md) を参照。

### 目次
- 読み取り: [ModelViewer](#modelviewer) / [BehaviourViewer](#behaviourviewer) / [DataViewer](#dataviewer)
- 書き込み: [ModelEditor](#modeleditor) / [BehaviourEditor](#behavioureditor) / [DataEditor](#dataeditor) / [ClusterEditor](#clustereditor)
- 値: [Data](#data) / [Setting](#setting)
- ID: [ObjectId](#objectid) / [DataId](#dataid) / [SettingId](#settingid) / [SettingFunctionId](#settingfunctionid) / [HyperedgeId](#hyperedgeid)
- 列挙/その他: [DataMode](#datamode) / [SettingMode](#settingmode) / [DataModifyToView](#datamodifytoview) / [LerpMode](#lerpmode) / [CustomSelectionPolicy](#customselectionpolicy) / [PathName](#pathname) / [DescriptionTerm / IKFKTag](#descriptionterm--ikfktag)

---

## ModelViewer

シーンモデルを読み取る入口。`scene.model_viewer()` で取得。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `behaviour_viewer()` | `BehaviourViewer` | ビヘイビア Viewer |
| `data_viewer()` | `DataViewer` | データ Viewer |
| `get_objects()` | `List[ObjectId]` | 全オブジェクト |
| `get_objects(name)` | `List[ObjectId]` | 名前一致のオブジェクト |
| `get_object_name(id)` | `str` | オブジェクト名 |
| `get_object_type_name(id)` | `str` | 型名 |

```python
mv = scene.model_viewer()
for obj in mv.get_objects():
    print(mv.get_object_name(obj), mv.get_object_type_name(obj))
```

---

## BehaviourViewer

ビヘイビアとそのスロットを読む。`mv.behaviour_viewer()` で取得。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_behaviours(type_name)` | `List[Guid]` | 型名で全ビヘイビア列挙 |
| `get_behaviours(object_id)` | `List[Guid]` | オブジェクトの全ビヘイビア |
| `get_behaviour_by_name(obj_id, name)` | `Guid` | オブジェクトの指定型ビヘイビア |
| `behaviour_id(obj_id, name)` | `Guid` | 同上 |
| `get_behaviour_owner(bh)` | `ObjectId` | 所有オブジェクト |
| `get_behaviour_name(bh)` | `str` | ビヘイビア型名 |
| `get_children(obj_id)` | `List[Guid]` | 子ビヘイビア |
| `is_hidden(bh)` | `bool` | 非表示か |

スロット取得（単一 / 範囲）:

| 種別 | 単一 | 範囲 |
|---|---|---|
| データ | `get_behaviour_data(bh, name)` → `DataId` | `get_behaviour_data_range(bh, name)` → `List[DataId]` |
| オブジェクト | `get_behaviour_object(bh, name)` → `ObjectId` | `get_behaviour_objects_range(bh, name)` → `List[ObjectId]` |
| 設定 | `get_behaviour_setting(bh, name)` → `SettingId` | `get_behaviour_settings_range(bh, name)` |
| 参照 | `get_behaviour_reference(bh, name)` → `Guid` | `get_behaviour_reference_range(bh, name)` |
| 文字列 | `get_behaviour_string(bh, name)` → `str` | — |
| アセット | `get_behaviour_asset(bh, name)` → `Guid`(※利用例あり) | — |

```python
obj = mv.get_objects()[0]
tr = bv.get_behaviour_by_name(obj, "Transform")
pos_id = bv.get_behaviour_data(tr, "global_position")   # DataId
```

> `get_behaviour_property` / `get_behaviour_default_data_value` は `DataViewer` 側に定義（下記）。

---

## DataViewer

データ・設定の値を読む。`mv.data_viewer()` で取得。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_data(id)` | `Data` | データオブジェクト（`mode`, `name` 等） |
| `get_data_value(id)` | 値 | 既定フレームの値 |
| `get_data_value(id, frame)` | 値 | 指定フレームの値 |
| `union_get_data_value(id, frame=0)` | 値 | union 取得 |
| `get_data_id(obj_id, name)` | `DataId` | 名前から DataId |
| `get_all_data_id(obj_id)` | `List[DataId]` | 全 DataId |
| `get_setting(id)` | `Setting` | 設定オブジェクト |
| `get_setting_value(id)` / `(id, frame)` | `bool`/`int` | 設定値 |
| `get_setting_id(obj_id, name)` | `SettingId` | 名前から SettingId |
| `get_all_settings_id(obj_id)` | `List[SettingId]` | 全 SettingId |
| `get_animation_size()` | `int` | 総フレーム数 |
| `get_behaviour_property(id, name[, frame])` | 値/`bool`/`int` | ビヘイビアのプロパティ |
| `get_behaviour_default_data_value(id, name)` | 値/`None` | ビヘイビアの既定値 |

値の型は bool / int / float / Vector3 / `Rotation` / `Quaternion` / 3x3・4x4行列 / str / bool3（[値の型](../guides/behaviours-and-data.md#データの値の型)）。

```python
dv = mv.data_viewer()
print(dv.get_data_value(pos_id, 0))       # フレーム0
print(dv.get_animation_size())            # フレーム数
```

---

## ModelEditor

モデル編集の入口。`modify*` のコールバック第1引数（`model`）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `behaviour_editor()` | `BehaviourEditor` | ビヘイビア Editor |
| `data_editor()` | `DataEditor` | データ Editor |
| `get_viewer()` | `DataViewer` | Viewer |
| `add_object()` / `add_object(id)` | `ObjectId` | オブジェクト追加 |
| `delete_objects(ids, close_connections=True)` | `None` | オブジェクト削除 |
| `set_object_name(id, name)` | `None` | 名前設定 |
| `set_object_type_name(id, name)` | `None` | 型名設定 |
| `init_default_constants()` | `None` | 既定定数を初期化（親なしオブジェクト生成時に使用） |
| `increase_animation_size_by_setting_key(size)` | `None` | アニメ長を増やす |
| `set_fixed_interpolation_if_need(actuals, frame, ignore_locked=False)` | `None` | 必要なら固定補間を設定 |
| `layers()` | `csc.layers.Layers` | レイヤー集合 |
| `layers_editor()` | `csc.layers.Editor` | レイヤー Editor |
| `layers_selector()` | `csc.layers.Selector` | レイヤー選択 |
| `move_objects_to_layer(ids, target_layer_id)` | `None` | レイヤー移動 |
| `move_obj_ids_in_layers(objIds, layer_id)` | `None` | レイヤー内移動 |

```python
def mod(model, update, scene_updater):
    model.set_object_name(obj_id, "NewName")
    model.delete_objects({other_id})
    scene_updater.generate_update()
    scene_updater.run_update(set(), scene.get_current_frame())
scene.modify_update("Edit", mod)
```

---

## BehaviourEditor

ビヘイビアの追加・削除とスロット設定。`model.behaviour_editor()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_behaviour(obj_id, type)` | `Guid` | ビヘイビア追加 |
| `add_behaviour(obj_id, type, behaviour_id)` | `Guid` | ID 指定で追加 |
| `delete_behaviour(bh)` | `None` | 削除 |
| `delete_behaviours(obj_ids)` | `None` | 複数オブジェクトのビヘイビア削除 |
| `hide_behaviour(bh, hidden=True)` | `bool` | 表示切替 |

スロット設定:

| 種別 | 単一 | 範囲設定 / 追加 / 削除 |
|---|---|---|
| データ | `set_behaviour_data(bh, name, data_id)` | `set_behaviour_data_to_range(bh, name, [ids])` / `add_behaviour_data_to_range` / `erase_behaviour_data_from_range` |
| オブジェクト | `set_behaviour_model_object(bh, name, obj_id)` | `set_behaviour_model_objects_to_range(...)` / `add_behaviour_model_object_to_range` / `erase_behaviour_model_object_from_range` |
| 設定 | `set_behaviour_setting(bh, name, setting_id)` | `set_behaviour_settings_to_range(...)` / `add_behaviour_setting_to_range` / `erase_behaviour_setting_from_range` |
| 参照 | `set_behaviour_reference(bh, name, beh_id)` | `set_behaviour_references_to_range(...)` / `add_behaviour_reference_to_range` / `erase_behaviour_reference_from_range` |
| アセット | `set_behaviour_asset(bh, name, asset_id)` | — |
| 文字列 | `set_behaviour_string(bh, name, str)` | — |
| フィールド | `set_behaviour_field_value(bh, name, name_value)` | — |
| Viewer | `get_viewer()` | — |

```python
def mod(model, update, scene):
    be = model.behaviour_editor()
    de = model.data_editor()
    new = de.add_data(obj_id, 'New Scale', csc.model.DataMode.Animation, [5.0, 5.0, 5.0])
    tr = scene.model_viewer().behaviour_viewer().get_behaviour_by_name(obj_id, 'Transform')
    be.set_behaviour_data(tr, 'local_scale', new.id)
scene.modify("Set behaviour data", mod)
```

---

## DataEditor

データ・設定の追加と値の書き込み。`model.data_editor()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_data(obj_id, name, mode, value[, id])` | `Data` | データ追加 |
| `add_constant_data(name, value[, id])` | `Data` | 定数データ追加 |
| `add_setting(obj_id, name, value[, mode][, id])` | `Setting` | 設定追加 |
| `add_constant_setting(name, value[, id])` | `Setting` | 定数設定追加 |
| `set_data_value(id, value)` | `None` | Static データ書き込み |
| `set_data_value(id, frame, value)` | `None` | 単一フレーム書き込み |
| `set_data_value(id, frames, value)` | `None` | 複数フレーム書き込み（`frames` は `Set[int]`） |
| `set_setting_value(id, value[, frame])` | `None` | 設定値書き込み |
| `copy_data(from_to)` | `None` | DataId 間コピー（`List[(src, dst)]`） |
| `delete_data(id)` / `delete_setting(id)` | `None` | 削除 |
| `set_animation_size(size)` | `None` | アニメ長設定 |
| `set_data_enum_name(id, enum_name)` | `None` | enum 名設定 |
| `set_data_only_key(id, only_key)` | `None` | キーのみ扱いに |
| `set_data_view_state(id, view_state)` | `None` | 表示状態（`DataModifyToView`） |
| `clusters_editor()` | `ClusterEditor` | クラスタ Editor |

`value` の Union（add_data / set_data_value）: bool / int / float / Vector3(`ndarray[float32,(3,)]`) / `Rotation` / 3x3行列 / 4x4行列 / `Quaternion` / str / bool3。

```python
def mod(model, update, scene):
    de = model.data_editor()
    new = de.add_data(obj_id, 'NewNode', csc.model.DataMode.Animation, [5.0, 5.0, 5.0])
scene.modify('Add data', mod)
```

---

## ClusterEditor

複数 `DataId` をクラスタとしてまとめる。`data_editor().clusters_editor()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_cluster(ids, name="")` | `int` | クラスタ作成（ID を返す） |
| `add_data_to_cluster(cluster_index, ids)` | `None` | データ追加 |
| `remove_data_from_cluster(data_id)` | `None` | データ削除 |
| `cluster_by_data(data_id)` | `int` | データ所属クラスタ |
| `bind_clusters(a, b)` / `unbind_clusters(a, b)` | `None` | クラスタの結合/解除 |
| `unbind_cluster(id)` | `None` | クラスタ解除 |
| `remove_cluster(id)` | `None` | クラスタ削除 |
| `set_cluster_name(id, name)` | `None` | 名前設定 |

---

## Data

更新計算やビヘイビアのプロパティとして使われる値。

| プロパティ | 型 | 説明 |
|---|---|---|
| `id` | `DataId` | 識別子 |
| `object_id` | `ObjectId` | 所属オブジェクト |
| `name` | `str` | 名前 |
| `mode` | `DataMode` | Static / Animation |
| `enum_name` | `str` | enum 型の場合の名前 |

---

## Setting

bool/int の設定値。

| プロパティ | 型 | 説明 |
|---|---|---|
| `id` | `DataId` | 関連 DataId |
| `name` | `str` | 名前 |
| `object_id` | `ObjectId` | 所属オブジェクト |
| `type` | `int` | 型 |
| `mode` | `SettingMode` | Static / Animation |

---

## ObjectId

オブジェクトの識別子。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_null()` | `bool` | null 判定 |
| `static null()` | `ObjectId` | null を返す |
| `to_string()` | `str` | 文字列表現 |

```python
null_obj = csc.model.ObjectId.null()
```

---

## DataId

データの識別子。`is_null()` / `static null()` / `to_string()`。

---

## SettingId

設定の識別子。`is_null()` / `static null()` / `to_string()`。

---

## SettingFunctionId

設定関数の識別子。`is_null()` / `static null()` / `to_string()`。

---

## HyperedgeId

ハイパーエッジの識別子。`is_null()` / `static null()` / `to_string()`。

---

## DataMode

| メンバー | 値 | 説明 |
|---|---|---|
| `Static` | 0 | 時間で変化しない |
| `Animation` | 1 | フレーム単位で変化 |

---

## SettingMode

| メンバー | 値 |
|---|---|
| `Static` | 0 |
| `Animation` | 1 |

---

## DataModifyToView

データ表示の変換。

| メンバー | 値 | 説明 |
|---|---|---|
| `None` | 0 | 変換なし |
| `Degrees` | 1 | 度数表示 |

---

## LerpMode

補間モード。

| メンバー | 値 | 説明 |
|---|---|---|
| `none` | 0 | 補間なし |
| `linear` | 1 | 線形 |
| `spherical` | 2 | 球面 |

---

## CustomSelectionPolicy

選択ポリシー。

| メンバー | 値 | 説明 |
|---|---|---|
| `Default` | 0 | 他と一緒に選択される |
| `Single` | 1 | 単独選択時のみ |
| `SingleType` | 2 | 同型のみの選択時 |

---

## PathName

階層的な名前構造。

| メソッド / 静的 | 戻り値 | 説明 |
|---|---|---|
| `empty()` | `bool` | 空か |
| `full_path()` | `List[str]` | フルパス |
| `get_namespace()` / `set_namespace(ns)` | `str` / `None` | 名前空間 |
| `to_string()` | `str` | 文字列化 |
| `static get_path_name(obj_id, mv, beh_name='Joint')` | `PathName` | 取得 |
| `static get_path_names(dict)` | `Dict[str, PathName]` | 取得 |
| `static get_path_names_by_behavior(beh, mv)` | `Dict[PathName, ObjectId]` | ビヘイビア別 |

プロパティ: `name`、`path`（`List[str]`）。

---

## DescriptionTerm / IKFKTag

- `DescriptionTerm`: 記述目的の用語を表す（詳細メンバーなし）。
- `IKFKTag`: IK/FK ポイントの識別タグ。

---

[← API 目次](README.md)
