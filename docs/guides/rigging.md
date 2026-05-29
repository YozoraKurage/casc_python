# リギング

リギングは Cascadeur Python API の中でも最も奥が深い領域です。自動リグ生成、リグ要素の追加、IK/FK、コンストレイント、T ポーズ管理などが含まれます。ここでは全体マップと、実装の入口・実例を示します。

---

## 関連パッケージ・コマンドの地図

| 場所 | 役割 |
|---|---|
| `csc.rig`（API） | リグ用データ構造（`AutoRigData`, `AddElementData`, `NamesInfo`, `RigValues`） |
| `rig_gen/`, `rig_gen2/` | リグ生成エンジン（ボックスコントローラ、IK、重心、ポイント、リジッド等） |
| `rigging/` | リグビルダー（units / fulcrum groups / center of mass などの builder 群） |
| `rig_mode/` | リギングモード関連 |
| `commands/rig_info/` | リグ情報の作成・ジョイント追加・JSON 保存（`create.py`, `add_joints.py`, `save_json.py`） |
| `commands/rig_additional/` | 追加ジョイント、バインド、リネーム、質量変更、各種リグ補正 |
| `commands/ik/` | IK・ポール・比例角度・方向追加など |
| `commands/center_of_mass/`, `commands/constrain/` | 重心・コンストレイント |
| `commands/go_to_default_pose.py` | T ポーズへのリセット（実例として後述） |
| `csc.tools.RiggingModeTool` | リギングモードのジョイントデータ・保持データ操作 |

> リグ生成エンジン（`rig_gen2` 等）は内部実装が大きく、フルスクラッチで再実装するより、**既存コマンドを起点に改造**するのが現実的です。

---

## リグ用データ構造（csc.rig）

自動リグ生成に渡す設定データです（[csc.rig リファレンス](../api/rig.md)）。

### `AutoRigData`
自動リグ全体の設定。ボディパーツ（`arms`, `foots`, `hands`, `neck`, `pelvis`, `spine_names`, `thighs`, `toes` ...）、`finger_names`、`hinge_names`、`directions`、`fulcrum_groups`、`additionals`、`values` などをリストで保持します。

### `AddElementData`
リグ要素（コントローラ）を追加する際の設定。`box_multiplier`、`joint_size_without_child`、`only_box_controller`、`orthogonal_with_parent`、`use_global_axis`、`point_color`、`axis_point_controller` など。

### `NamesInfo`
ジョイント名と影響範囲（`begin_joint` / `end_joint` / `is_left` / `is_inverse` / `is_affect_parent`）。

### `RigValues`
寸法・質量系の値（`box_global_offset`, `box_scale_width`, `box_scale_depth`, `mass`, `width`, `additional_point_global_offset`）と `get_names()`。

---

## リグ情報（RigInfo ビヘイビア）を読む

リグは `RigInfo` ビヘイビアで表現され、`rig_objects`（コントローラ群）と `related_joints`（対象ジョイント）を範囲スロットに持ちます。

```python
def run(scene):
    bv = scene.model_viewer().behaviour_viewer()
    for rig_info in bv.get_behaviours("RigInfo"):
        owner = bv.get_behaviour_owner(rig_info)
        rig_objs = bv.get_behaviour_objects_range(rig_info, "rig_objects")
        joints   = bv.get_behaviour_objects_range(rig_info, "related_joints")
        scene.info(f"Rig: {len(rig_objs)} controllers, {len(joints)} joints")
```

選択オブジェクトから所属リグを逆引きするヘルパーが [`common/selection_operations.py`](../cookbook.md) の `get_rig_info(scene)` にあります（`RigInfo` / `MeshObject` / `ObjectsContainer` を辿って対応付け）。

---

## 実例: T ポーズへのリセット（go_to_default_pose.py）

[`commands/go_to_default_pose.py`](../cookbook.md) は、選択中のボックスコントローラを、保存された T ポーズ（`T Pose Position` / `T Pose Rotation`）にリセットします。リギング処理の典型 — 「親子の相対変換」「特殊ビヘイビア（Untwist）の考慮」を含む good example です。

### 全体構造（pycsc 利用）

```python
import csc, pycsc

def run(scene):
    @pycsc.run_update_session
    def go(py_scene: pycsc.DomainScene):
        selected = py_scene.get_scene_objects(selected=True, with_behaviour="BoxView")
        if not selected:
            raise Exception("ボックスコントローラを1つ以上選択してください")
        frame = py_scene.get_current_frame()
        actuals = set()
        for sel in selected:
            node = pycsc.TransformUpdate(sel, py_scene)
            ...   # T ポーズ変換を計算してローカルに書き込む
        py_scene.su.handle.run_update(actuals, frame)
    go()
```

### T ポーズデータの取得

オブジェクトに `TPose` ビヘイビアがあれば `get_tpose()`、無ければルートグループ内の `T Pose Rotation` / `T Pose Position` ノードから組み立てます。

```python
def get_tpose(node: pycsc.TransformUpdate) -> csc.math.OrthogonalTransform:
    if node.has_behaviour("TPose"):
        return node.get_tpose()
    rg = node.root_group()
    t_rot = rg.node_deep("T Pose Rotation") or rg.node_deep("TPoseRotation")
    t_pos = rg.node_deep("T Pose Position") or rg.node_deep("TPosePosition")
    pos = t_pos.value() if t_pos else [0.0, 0.0, 0.0]
    return csc.math.OrthogonalTransform(pos, t_rot.value().to_quaternion())
```

### 親との相対変換に直す

ルートはそのまま T ポーズへ、子は「親 T ポーズ」と「自分 T ポーズ」の差分（`transforms_difference`）をローカルに書き込みます。

```python
t_diff = csc.math.transforms_difference(parent_tpose, node_tpose)
node.local_rot_data.set_value(csc.math.Rotation.from_quaternion(t_diff.rotation), frame)
node.local_pos_data.set_value(t_diff.position, frame)
actuals.add(node.local_rot_data.raw_id)
actuals.add(node.local_pos_data.raw_id)
```

### Untwist など特殊ビヘイビアの扱い

`Untwist` を持つ親の下では、`untwist` 関数（`csc.math.untwist`）で補正してから差分を取るなど、ビヘイビアごとの計算が必要になります。詳細はソースを参照。

> このコマンドは「リグ操作の定石」を凝縮しています:
> 1. 対象を `with_behaviour` で絞る
> 2. 親子をたどって相対変換で計算する
> 3. ローカルデータに書き、変更 `DataId` を集めて一括 `run_update`
> 4. 特殊ビヘイビアは個別処理

---

## リギングモードツール（RiggingModeTool）

`csc.tools.RiggingModeTool` は、リギングモード時のジョイントデータ・レイヤーID・保持データを操作します。

```python
def run(scene):
    app = csc.app.get_application()
    view_scene = app.get_scene_manager().current_scene()
    rmt = app.get_tools_manager().get_tool("RiggingModeTool").editor(view_scene)
    joints_data = rmt.get_joints_data()        # Dict[ObjectId, List[JointData]]
```

`JointData` は `local_position` / `local_rotation` / `local_scale` / `visibility` を持ちます（[csc.tools リファレンス](../api/tools.md)）。

---

## どこから手を付けるか（実務指針）

1. **既存コマンドを読む**: `commands/rig_info/create.py`、`commands/ik/add_ik.py`、`commands/rig_additional/*` が現実的な雛形。
2. **対象の特定**: `RigInfo` / `BoxView` / `Joint` ビヘイビアで対象を絞る。
3. **変換計算**: `csc.math` の `OrthogonalTransform` / `transforms_difference` / `combine_transforms` / `untwist` を活用。
4. **書き込み**: ローカル位置・回転データに書き、`run_update`。
5. **生成系**: `parts/final_rig/` などのプリセット挿入や `rig_gen2` のファクトリを利用。

---

関連: [csc.rig](../api/rig.md) / [csc.math](../api/math.md) / [csc.tools](../api/tools.md) / [発展的なアドオン](advanced-addons.md) / [pycsc](pycsc.md) / [クックブック](../cookbook.md)
