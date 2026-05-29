# 発展的なアドオン

ここでは、単なる値の読み書きを超えた処理 — **オブジェクトの新規生成**、**アップデートグラフの構築**、**パーツ挿入**、**クラスタ**、**選択操作** — を扱います。前提として [アーキテクチャ](../architecture.md) と [シーン変更モデル](scene-modification.md) を理解していることを想定します。

---

## 1. パーツ（プリセット）を挿入する（最も手軽な生成）

ゼロからノードを組むのは大変です。多くの場合、`csc.parts` で**既製の部品**を挿入する方が現実的です。`parts/` フォルダの `.partscasc` をパスで指定して挿入できます。

```python
import csc

def run(scene):
    def mod(model, update, scene_updater):
        new_id = csc.parts.Buffer.get().insert_object_by_path(
            'objects/locator.partscasc',          # parts/ 配下の相対パス
            update.root().group_id(),             # 挿入先グループ
            model,
            scene_updater.scene().assets_manager())
        scene_updater.generate_update()
        scene.info(f"Locator を追加: {new_id}")
    scene.modify_update("Insert locator", mod)
```

`csc.parts.Buffer` には用途別のメソッドがあります（[csc.parts リファレンス](../api/parts.md)）。

| メソッド | 挿入単位 |
|---|---|
| `insert_object_by_path(path, group_id, model, assets)` | 1オブジェクト |
| `insert_objects_by_path(...)` | 複数オブジェクト |
| `insert_elementary_by_path(...)` | エレメンタリ（最小単位） |
| `insert_update_group_by_path(...)` | アップデートグループ |

`parts/` には `objects/`, `points/`, `boxes/`, `constraints/`, `3d node/`, `spline helpers/`, `final_rig/` などのプリセットがあります。一時的にデフォルト値を取り出す「捨て部品」としても使えます（[`commands/restore_values.py`](../cookbook.md)）。

---

## 2. オブジェクトをゼロから生成する

新規オブジェクトは `update.root().create_object(name)` で作り、ビヘイビアとデータを組み立てます。最小の流れ:

```python
def mod(model, update, scene_updater):
    be = model.behaviour_editor()
    de = model.data_editor()

    obj = update.root().create_object("MyObject")  # csc.update.Object
    obj_id = obj.object_id()

    # データを作る（アニメ用 Vector3f）
    pos = de.add_data(obj_id, "GlobalPosition", csc.model.DataMode.Animation, [0.0, 0.0, 0.0])

    # ビヘイビアを付ける
    tr = be.add_behaviour(obj_id, "Transform")
    be.set_behaviour_data(tr, "global_position", pos.id)

    scene_updater.generate_update()
    scene_updater.run_update({pos.id}, 0)
```

完全なジョイント／ボックス相当を作るには、`Basic` / `Transform` / `Joint` / `BoxView` / `Point` / `MeshObject` などのビヘイビアと、それらが参照するデータ、そして**アップデートグラフの結線**まで必要です。実装の全体像は [`samples/model_cube.py`](../cookbook.md) が決定版の例です（次節）。

---

## 3. アップデートグラフの構築（model_cube.py の解剖）

[`samples/model_cube.py`](../cookbook.md) は、グローバル/ローカル変換が相互計算されるオブジェクトを一から構築します。発展アドオンの「教科書」です。要点を抜き出します。

### 3-1. オブジェクトとサブグループ

```python
obj = update.root().create_object(name)
object_group = obj.root_group()                                   # オブジェクトのルートグループ
settings_group = object_group.create_sub_update_group("Setting graph")  # 設定用サブグループ
```

### 3-2. 入出力インターフェース（親との接続）

グループは名前付きの入出力端子を持ち、`connect` で結線します。

```python
parent_position_input = object_group.add_input("Parent Position")
parent_object.output("Position").connect(parent_position_input)   # 親の出力 → 自分の入力
```

親がいない場合は、定数（`constant_datas`）に接続します。

```python
model.init_default_constants()
constant_datas = obj.parent_group().constant_datas()
parent_rotation_input.connect(constant_datas.output("rotation identity"))
parent_position_input.connect(constant_datas.output("vector3f zero"))
```

### 3-3. レギュラーデータ（グラフ上のデータノード）

```python
global_position_data = object_group.create_regular_data(
    "GlobalPosition", global_position, csc.model.DataMode.Animation)
global_position_data.output().connect(object_group.add_output("Position").other_side())
```

### 3-4. レギュラーファンクション（計算ノード）

`create_regular_function(name, function_type)` で計算ノードを作り、引数・結果端子を結線します。

```python
edge = object_group.create_regular_function("GlobalByLocal", "CombineTransforms")
attributes = {
    "first.position": parent_position_attribute, "first.rotation": parent_rotation_attribute,
    "second.position": in_pos.output(),          "second.rotation": in_rot.output(),
    "result.position": out_pos.input(),          "result.rotation": out_rot.input(),
}
import common.update_operations as uo
uo.connect_regular_function(edge, attributes)   # 端子名→接続先 をまとめて結線
```

代表的な関数型: `CombineTransforms`（変換合成）、`TransformsDifference`（差分）、`Or` / `Not`、`BinarySwitcher`、`DataRuleOverride` など。

### 3-5. 設定グラフ（IK/global-local 切替などのロジック）

`settings_group` 側に `SettingFunction`（`Or`, `Not`, `BinarySwitcher`, `DataRuleOverride`）を置き、入力（actuality）と出力（activity）を結線して、「グローバル基準かローカル基準か」を切り替えるロジックを作ります。

```python
settings_group.add_input("global_position").connect(global_position_data.actuality())
settings_group.add_output("global_by_local").connect(global_by_local.activity())
```

### 3-6. ビヘイビアの装着

グラフを組んだら、`Transform` / `Joint` / `BoxView` / `Point` / `EdgeView` / `MeshObject` などのビヘイビアを付け、各スロットに対応データを差し込みます。

```python
transform_id = be.add_behaviour(obj_id, "Transform")
be.set_behaviour_data(transform_id, "global_position", global_position_data.data_id())
...
mesh = csc.domain.assets.AssetsManager.get_cube_mesh(box_view_size / 2.0)
bm = be.add_behaviour(obj_id, "MeshObject")
be.set_behaviour_asset(bm, "mesh", am.add(mesh))
```

### 3-7. 仕上げ

```python
scene_updater.generate_update()                # 構造を確定
scene_updater.run_update({pos.data_id(), rot.data_id()}, 0)  # 初期計算
```

> ここまで来ると `csc.update` のクラス群（`Group`/`Node`/`NodeAttribute`/`Connection`/`RegularData`/`RegularFunction`/`Interface*`）が総動員されます。各 API は [csc.update リファレンス](../api/update.md) を参照。`add_function/` 配下にもより短い生成例（`create3d_node.py`, `create_plane.py`, `add_dynamic.py`, `topology_add.py`）があります。

---

## 4. クラスタ（データのグルーピング）

`ClusterEditor`（`model.data_editor().clusters_editor()`）で、複数の `DataId` をクラスタにまとめ、束ねて扱えます。

```python
def mod(model, update, scene_updater):
    ce = model.data_editor().clusters_editor()
    cid = ce.add_cluster([data_id_a, data_id_b], "MyCluster")
    ce.add_data_to_cluster(cid, [data_id_c])
    # ce.bind_clusters(cid1, cid2) / ce.remove_cluster(cid)
```

詳細は [csc.model リファレンス](../api/model.md#clustereditor)。

---

## 5. 選択を駆使する

選択は `*_with_session` の中で `session.take_selector()` 経由で操作します。`csc.domain` の `SelectorFilter` / `SelectorMode` で挙動を制御できます。

```python
def mod(model, update, scene, session):
    sel = session.take_selector()
    sel.select(set(obj_ids), pivot_id)     # シンプルな選択（集合 + ピボット）
    # 詳細制御:
    # sel.select(ids, id, filter, mode, types_filter, auto_pivot)
scene.modify_with_session("Select", mod)
```

- `SelectorMode`: `NewSelection`（置換）/ `AdditionSelection`（追加）/ `SubtractionSelection`（除外）/ `MultiSelection` / `SingleSelection`。
- `SelectorFilter`: `Free` / `Selectable` / `ObjectType` / `Layer` / `Standart` / `Full`。

ヘルパー [`common/selection_operations.py`](../cookbook.md) に `select_all` / `clear_selection` / 型別取得などがあります。

---

## 6. 別ツールのコア機能を呼ぶ

ミラー・アトラクタ等の組み込みツールは `tools_manager.get_tool("...").editor(view_scene)` でエディタを取得して使います。

```python
def run(scene):
    app = csc.app.get_application()
    view_scene = app.get_scene_manager().current_scene()
    mirror = app.get_tools_manager().get_tool("MirrorTool").editor(view_scene)
    core = mirror.core()
    core.set_plane(csc.math.Plane([1.0, 0.0, 0.0], [0.0, 0.0, 0.0]))   # YZ平面でミラー
```

利用可能ツール例: `MirrorTool` / `AttractorTool` / `AutoPhysicTool` / `RiggingModeTool` / `SelectionGroups` / `FbxSceneLoader`。詳細は [csc.tools リファレンス](../api/tools.md)。

---

## 7. アクションを呼ぶ

メニュー項目などの内部アクションは `ActionManager` から名前で起動できます。

```python
csc.app.get_application().get_action_manager().call_action("Scene.Undo")
```

呼び出せる ID の一覧は [アクション ID 一覧](../api/actions.md) を参照。ただし公式は「`call_action` は将来的に段階的廃止予定。よく使う機能は API 側に移行」と明言しているため、専用 API（[csc.tools](../api/tools.md) / [csc.fbx](../api/fbx.md) など）があればそちらを優先してください。

---

## パフォーマンスの注意

- 1つの `modify*` の中でまとめて変更し、変更 `DataId` を `set` に貯めて**最後に一括 `run_update`**。
- ループ内で Viewer を何度も取り直さない（最初に1回取得）。
- 大量生成は `parts` 挿入の方が、手組みより安全で速いことが多い。

---

関連: [シーン変更モデル](scene-modification.md) / [csc.update](../api/update.md) / [csc.parts](../api/parts.md) / [リギング](rigging.md) / [クックブック](../cookbook.md)
