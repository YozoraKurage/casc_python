# csc.update

アップデートグラフ（オブジェクト内部の依存計算グラフ）を構築・編集するモジュールです。`modify*` のコールバック第2引数 `update`（`Update`）が起点。最も低レベルで、主に**新規オブジェクト生成**や**カスタム計算ノードの差し込み**で使います。

> 概念・実装の流れは [アーキテクチャ #アップデートグラフ](../architecture.md#5-アップデートグラフcscupdate) と [発展的なアドオン #アップデートグラフの構築](../guides/advanced-addons.md#3-アップデートグラフの構築model_cubepy-の解剖) を先に読むことを推奨します。

### 全体像

```
Update（更新エディタ全体）
└─ root() → ObjectGroup
     ├─ create_object(name) → Object
     │     └─ root_group() → UpdateGroup        ← オブジェクト本体のグラフ
     │           ├─ create_regular_data(...)     → RegularData（データノード）
     │           ├─ create_regular_function(...)  → RegularFunction（計算ノード）
     │           ├─ create_setting_data(...)       → SettingData
     │           ├─ create_setting_function(...)   → SettingFunction
     │           ├─ create_sub_update_group(name)  → UpdateGroup（入れ子）
     │           ├─ add_input(name)/add_output(name)→ InterfaceAttribute（端子）
     │           ├─ constant_datas()/constant_settings()/external_properties()
     │           └─ input/output_interface_node()  → InterfaceNode
     └─ create_sub_object_group(name) → ObjectGroup
```
ノード同士は `NodeAttribute.connect(other)` で結線します。

### 目次
- 入口: [Update](#update) ・ [ObjectGroup](#objectgroup) ・ [Object](#object) ・ [UpdateGroup](#updategroup) ・ [Group](#group)
- ノード基底: [Node](#node) ・ [NodeAttribute](#nodeattribute) ・ [InterfaceNode](#interfacenode) ・ [InterfaceAttribute](#interfaceattribute)
- データ/関数: [RegularData](#regulardata) ・ [RegularFunction](#regularfunction) ・ [SettingData](#settingdata) ・ [SettingFunction](#settingfunction)
- 定数/外部: [ConstantDatas](#constantdatas) ・ [ConstantSettings](#constantsettings) ・ [ExternalProperties](#externalproperties)
- 接続: [Connection](#connection) ・ [HierarchyUpdate](#hierarchyupdate)
- [属性クラス・ID・列挙](#属性クラスid列挙)

---

## Update

更新エディタ全体。`modify*` の `update` 引数。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `root()` | `ObjectGroup` | ルートオブジェクトグループ |
| `get_object_by_id(obj_id)` | `Object` | ID からオブジェクトノード |
| `get_node_by_id(id)` | `Node` | ID からノード |
| `delete_node(id)` | `None` | ノード削除 |
| `ungroup(group)` | `None` | グループ解除 |

```python
def mod(model, update, scene):
    obj = update.get_object_by_id(object_id)
    root_group = obj.root_group()
    pos = root_group.node_deep('Position')
    print(pos)
scene.modify_update('Get object', mod)
```

---

## ObjectGroup

オブジェクトの入れ物。`update.root()` がこれ。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `create_object(name[, id])` | `Object` | オブジェクト作成 |
| `create_sub_object_group(name)` | `ObjectGroup` | サブオブジェクトグループ作成 |
| `objects()` | `Set[Object]` | 配下オブジェクト |
| `object_groups()` | `Set[ObjectGroup]` | 配下グループ |

---

## Object

オブジェクトノード（機能は限定的。本体グラフは `root_group()` の `UpdateGroup` を使う）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `object_id()` | `ObjectId` | オブジェクト ID |
| `root_group()` | `UpdateGroup` | ルートグループ |
| `add_input(name)` / `add_output(name)` | `InterfaceAttribute` | 端子追加 |

---

## UpdateGroup

オブジェクト本体のグラフを構築する主役。`Group` を継承（下記 Group のメソッドも使える）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `create_regular_data(name, value, mode=Static)` | `RegularData` | データノード作成 |
| `create_regular_function(name, function)` | `RegularFunction` | 計算ノード作成（`function` は型名文字列 `"CombineTransforms"` 等） |
| `create_setting_data(name, value, mode=Static)` | `SettingData` | 設定データ作成 |
| `create_setting_function(name, function_name)` | `SettingFunction` | 設定関数作成（`"Or"`, `"Not"`, `"BinarySwitcher"`, `"DataRuleOverride"` 等） |
| `create_sub_update_group(name)` | `UpdateGroup` | サブグループ作成 |
| `create_sub_update_group2(name, group_id)` | `UpdateGroup` | ID 指定でサブグループ |
| `external_properties()` | `ExternalProperties` | 外部プロパティ |
| `regular_datas()` | `Set[RegularData]` | データノード集合 |
| `regular_functions()` | `Set[RegularFunction]` | 関数ノード集合 |
| `setting_datas()` / `settings_datas()` | `Set[SettingData]` | 設定データ集合 |
| `setting_functions()` | `Set[SettingFunction]` | 設定関数集合 |
| `groups()` | `Set[UpdateGroup]` | サブグループ集合 |

```python
group = obj.root_group()
gpos = group.create_regular_data("GlobalPosition", [0,0,0], csc.model.DataMode.Animation)
edge = group.create_regular_function("GlobalByLocal", "CombineTransforms")
```

---

## Group

`UpdateGroup` / `ObjectGroup` の基底。端子・サブグループ・ノード探索。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_input(name)` / `add_output(name)` | `InterfaceAttribute` | 入出力端子追加 |
| `input_interface_node()` / `output_interface_node()` | `InterfaceNode` | 入出力インターフェースノード |
| `interface_node(direction)` | `InterfaceNode` | 方向指定 |
| `interface_input(name)` / `interface_output(name)` | `InterfaceAttribute` | 端子取得 |
| `interface_inputs()` / `interface_outputs()` | `List[InterfaceAttribute]` | 端子一覧 |
| `constant_datas()` | `ConstantDatas` | 定数データノード |
| `constant_settings()` | `ConstantSettings` | 定数設定ノード |
| `create_group(name)` | `Group` | サブグループ作成 |
| `group(nodes, name)` | `Group` | ノード群をグループ化 |
| `group_id()` | `GroupId` | グループ ID |
| `is_root()` | `GroupId` | ルートか |
| `node(name)` / `node(id)` | `Node` | ノード取得（名前/ID） |
| `node_deep(name)` | `Node` | 再帰的にノード取得 |
| `node_with_type(type, name)` / `node_with_type_deep(...)` | `Node` | 型指定で取得 |
| `has_node(name)` | `bool` | 存在確認 |
| `nodes()` | `Set[Node]` | 直下ノード |
| `leaf_children()` | `Set[Node]` | 葉ノード（データ・設定・関数） |
| `delete_node(node)` | `None` | ノード削除 |

```python
pos_node = obj.root_group().node_deep('Position')   # 再帰検索でよく使う
```

---

## Node

すべてのノードの共通基底。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `name()` / `full_name()` / `set_name(name)` | `str`/`None` | 名前 |
| `id()` | 各種 ID | 一意 ID |
| `inputs()` / `outputs()` | `List[NodeAttribute]` | 入出力端子 |
| `input(name)` / `output(name)` | `NodeAttribute` | 単一端子のショートカット |
| `attributes(direction)` | `List[NodeAttribute]` | 方向で端子取得 |
| `has_input(name)` / `has_output(name)` | `bool` | 端子の有無 |
| `parent_group()` | `Group` | 親グループ |
| `parent_object()` | `Object` | 親オブジェクト（グループでなければ null） |
| `is_active()` | `bool` | 現在のアクチュアリティで有効か |
| `is_fictive()` | `bool` | 擬似ノード（定数・入出力・外部プロパティ）か |

---

## NodeAttribute

ノードの入出力端子。**結線の主役**。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `connect(attribute)` | `None` | 他端子へ接続 |
| `disconnect([attribute])` | `None` | 切断 |
| `connected_attributes()` | `List[NodeAttribute]` | 接続先 |
| `connected_leaves(get_only_first=False)` | `List[NodeAttribute]` | 接続先の葉 |
| `connected_leaves_in_undirected_graph()` | `List[NodeAttribute]` | 無向グラフでの葉 |
| `direction()` | `csc.Direction` | 入出力方向 |
| `name()` | `str` | 名前 |
| `node()` | `Node` | 所属ノード |
| `id()` | 各種 AttributeId | 端子 ID |
| `is_active()` | `bool` | 有効か |

```python
parent_object.output("Position").connect(parent_position_input)
data.output().connect(group.add_output("Position").other_side())
```

---

## InterfaceNode

グループの入出力をまとめるノード。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `add_attribute(name)` | `InterfaceAttribute` | 端子追加 |
| `remove_attribute(attr)` | `None` | 端子削除 |
| `move_attribute(attr, position)` | `None` | 位置変更 |
| `interface_attributes()` | `List[InterfaceAttribute]` | 端子一覧 |
| `direction()` | `csc.Direction` | 方向 |

---

## InterfaceAttribute

グループの境界端子。任意の端子へ接続可能。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `other_side()` | `InterfaceAttribute` | 反対側（内/外）の端子 |
| `set_name(name)` | `None` | 名前設定 |
| `group_attribute_id()` | `GroupAttributeId` | グループ属性 ID |

> グループの `add_input("X")` で得た端子に対し、外側からは返り値へ `connect`、内側へは `.other_side()` で結線する、という二面性が `InterfaceAttribute` の肝です。

---

## RegularData

データノード（位置・回転などの値を保持）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `data_id()` | `DataId` | データ ID |
| `value([frame])` | 値 | 値取得 |
| `set_value(v, frame)` | `None` | 値設定 |
| `input()` / `output()` | `RegularDataAttribute` | 入出力端子 |
| `attribute(direction)` | `RegularDataAttribute` | 方向で端子 |
| `actuality()` | `ActualityAttribute` | アクチュアリティ出力 |
| `is_actual()` / `set_actual(act)` | `bool`/`None` | アクチュアリティ |
| `mode()` | `DataMode` | Static / Animation |
| `set_lerp_mode(mode)` | `None` | LERP モード（`csc.model.LerpMode`） |
| `set_period(period)` / `remove_period()` | `None` | 補間の周期 |
| `get_apply_euler_filter()` / `set_apply_euler_filter(b)` | `bool`/`None` | オイラーフィルタ |
| `set_view_state(view_state)` | `None` | 表示状態 |

```python
node = obj.root_group().node_deep('Position')
print(node.value(0))         # Animation はフレーム指定
tpose = obj.root_group().node_deep('T Pose Position')
print(tpose.value())         # Static
```

---

## RegularFunction

計算ノード（同じ演算をデータに対して行う）。型名は `create_regular_function(name, type)` の第2引数で指定。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `arguments()` | `List[RegularFunctionAttribute]` | 入力端子 |
| `results()` | `List[RegularFunctionAttribute]` | 出力端子 |
| `activity()` | `ActivityAttribute` | 活性端子（有効/無効） |
| `func_id()` | `HyperedgeId` | 関数 ID |
| `increase_vector(path, direction)` / `decrease_vector(path, direction)` | — | ベクトル端子の増減 |
| `resize_vector_inputs(count, path)` / `resize_vector_outputs(count, path)` | `None` | 端子数変更 |
| `remove_attribute(attr)` | `None` | 端子削除 |
| `is_convertible()` / `set_convertible(b)` | `bool`/`None` | 最終グラフに含めるか |

代表的な型名: `CombineTransforms` / `TransformsDifference`（変換合成・差分）。
端子名（`first.position` 等）への一括結線は `common.update_operations.connect_regular_function(func, attrs)` が便利。

---

## SettingData

設定データノード（bool または int8: -128〜127）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `data_id()` | `SettingId` | 設定 ID |
| `value([frame])` | `bool`/`int` | 値取得 |
| `set_value(value[, frame])` | `None` | 値設定 |
| `output()` | `SettingDataAttribute` | 出力端子 |

---

## SettingFunction

設定関数ノード（設定に対する演算）。型名例: `Or` / `Not` / `BinarySwitcher` / `DataRuleOverride`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `arguments()` | `List[SettingFunctionAttribute]` | 入力端子 |
| `results()` | `List[SettingFunctionAttribute]` | 出力端子 |
| `func_id()` | `SettingFunctionId` | 関数 ID |
| `increase_input_vector(index)` / `decrease_input_vector(index)` | — | 入力端子の増減 |
| `resize_vector_inputs(index, count)` | `None` | 端子数変更 |
| `remove_attribute(attr)` | `None` | 端子削除 |
| `is_convertible()` / `set_convertible(b)` | `bool`/`None` | 最終グラフに含めるか |

```python
check = settings_group.create_setting_function("Check global", "Or")
inputs.output("global_position").connect(check.input("a"))
inputs.output("global_rotation").connect(check.input("b"))
```

---

## ConstantDatas

定数データノード（どのグループからも参照可能）。

| メソッド | 説明 |
|---|---|
| `add_data(name, value)` | 定数データを追加 |

既定の定数（`"vector3f zero"`, `"rotation identity"` 等）は `model.init_default_constants()` で初期化され、`group.constant_datas().output("...")` で参照します。

---

## ConstantSettings

定数設定ノード。

| メソッド | 説明 |
|---|---|
| `add_setting(name, value)` | 定数設定を追加 |

---

## ExternalProperties

外部プロパティのノード（更新が補間中か、など）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `property_outputs()` | `List[ExternalPropertyAttribute]` | 外部プロパティ端子 |

`ExternalProperty`（enum）: `Fixation`(0) / `IkFk`(1) / `InterpolationType`(2) / `IsInterpolation`(3) / `fixation`(4) / `IsKey`(5)。

---

## Connection

2つの属性間の接続を表す構造体。`HierarchyUpdate` と併用。

| メンバー | 型 | 説明 |
|---|---|---|
| `source` | AttributeId | 出力側 |
| `destination` | AttributeId | 入力側 |

---

## HierarchyUpdate

階層更新と接続の具体操作。

| メソッド | 説明 |
|---|---|
| `add_connection(connection)` | 接続を追加 |
| `remove_connection(connection)` | 接続を削除 |

---

## 属性クラス・ID・列挙

グラフの各要素には対応する属性クラスと ID があります（多くは内部用。直接生成より、ノード経由の取得・接続が中心）。

### 属性クラス
- `RegularDataAttribute` / `RegularFunctionAttribute`: データ・データ関数の端子。
- `SettingDataAttribute` / `SettingFunctionAttribute`: 設定・設定関数の端子（`SettingFunctionAttribute.is_out_true()` / `output_id()`）。
- `ActivityAttribute`: データ関数の活性（入力専用 bool。未設定なら常に活性）。
- `ActualityAttribute`: データが更新開始時に actual かを示す出力。
- `ConstantDataAttribute` / `ConstantSettingAttribute`: 定数の出力端子。
- `ExternalPropertyAttribute`: 外部プロパティの出力端子。
- `InterfaceAttribute`: 上記参照。

### ID クラス
- `GroupId`: グループ ID（`is_null()` / `static null()` / `to_string()`）。
- `GroupAttributeId`: `group_id` + `attribute_id`(Guid)。
- `InterfaceId`: `group_id` + `direction`。
- `ConstantDatasId` / `ConstantSettingsId`: グループ ID と等価な GUID。
- `ConstantDataAttributeId`: `group_id`(ConstantDatasId) + `attribute_id`(DataId)。
- `ConstantSettingAttributeId`: `group_id`(ConstantSettingsId) + `attribute_id`(SettingId)。
- `ExternalPropertiesId`: グループ ID と等価。
- `ExternalPropertyAttributeId`: `node_id` + `property`(ExternalProperty)。
- `ActualityAttributeId`: データ ID で定義（出力専用）。
- `RegularDataAttributeId`: データ ID で定義。
- `RegularFunctionAttributeId`: 関数 ID + 端子名。
- `SettingFunctionAttributeId`: `function_id` + `attribute_index` + `attribute_sub_index`。

### 列挙
- `InterfaceAttributeSide`: `InterfaceSide`(0) / `GroupSide`(1)。
- `ExternalProperty`: 上記参照。

---

[← API 目次](README.md)
