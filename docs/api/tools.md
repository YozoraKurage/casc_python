# csc.tools

組み込みツール群。`csc.app.get_application().get_tools_manager().get_tool(名前)` で取得し、多くは `.editor(view_scene)` でシーン用エディタを得て使います。

### 目次
[MirrorTool](#mirrortool) ・ [AttractorTool](#attractortool) ・ [AutoPhysicTool](#autophysictool) ・ [RiggingModeTool](#riggingmodetool) ・ [SelectionGroups](#selectiongroups) ・ [JointData / DataKey / ObjectKey](#補助データ型) ・ [mirror / selection / attractor 名前空間](#名前空間)

---

## MirrorTool

ミラー（左右対称）操作。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `core()` | `mirror.Core` | コア取得 |

```python
view_scene = csc.app.get_application().get_scene_manager().current_scene()
mirror = csc.app.get_application().get_tools_manager().get_tool('MirrorTool').editor(view_scene)
core = mirror.core()
core.set_plane(csc.math.Plane([1.0, 0.0, 0.0], [0.0, 0.0, 0.0]))   # YZ 平面で対称
```

### mirror.Core

| メソッド | 説明 |
|---|---|
| `plane()` → `csc.math.Plane` | ミラー平面取得 |
| `set_plane(plane)` | ミラー平面設定 |
| `mirror_frame(ids)` | フレームをミラー（`Set[ObjectId/Tool_object_id]`） |
| `mirror_interval(ids)` | 区間をミラー |

---

## AttractorTool

アトラクタ（物理的に「引き寄せる」補間）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_general_settings()` | `attractor.AttractorGeneralSettings` | 一般設定 |
| `is_only_key_frames()` | `bool` | キーフレームのみか |

```python
view_scene = csc.app.get_application().get_scene_manager().current_scene()
attractor = csc.app.get_application().get_tools_manager().get_tool('AttractorTool').editor(view_scene)
settings = attractor.get_general_settings()
args = csc.tools.attractor.Args(view_scene.domain_scene(), view_scene.gravity_per_frame(),
                                settings, attractor.is_only_key_frames(),
                                csc.tools.attractor.ArgsMode.Next)
```

---

## AutoPhysicTool

自動物理。

| メソッド | 説明 |
|---|---|
| `turn_off()` | オフにする |
| `turn_off_all_fulcrum_points()` | 全支点ポイントをオフ |

---

## RiggingModeTool

リギングモード時のジョイントデータ・保持データの操作（[リギング](../guides/rigging.md)）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_joints_data()` | `Dict[ObjectId, List[JointData]]` | ジョイントデータ |
| `set_joints_data(session, dict)` | `None` | 設定 |
| `erase_joints_data(session)` | `None` | 消去 |
| `get_layers_ids()` | `Set[LayerId]` | レイヤー ID |
| `set_layers_ids(session, set)` / `erase_layers_ids(session)` | `None` | 設定/消去 |
| `get_preserved_data()` | `Dict[DataKey, List[...]]` | 保持データ |
| `set_preserved_data(session, dict)` / `erase_preserved_data(session)` | `None` | 設定/消去 |
| `get_preserved_setting()` | `Dict[DataKey, List[bool/int]]` | 保持設定 |
| `set_preserved_setting(session, dict)` / `erase_preserved_setting` | `None` | 設定/消去 |
| `set_undo_redo_context(session, func, obj, obj)` | `None` | Undo/Redo コンテキスト |

---

## SelectionGroups

選択グループの管理。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `core()` | `selection.Core` | コア取得 |
| `import_file(path)` | `None` | ファイルから読み込み |

---

## 補助データ型

### JointData
ジョイントのローカル変換。

| プロパティ | 型 |
|---|---|
| `local_position` | Vector3（ndarray） |
| `local_rotation` | `csc.math.Rotation` |
| `local_scale` | Vector3（ndarray） |
| `visibility` | `int` |

### DataKey
データ点の識別キー。`data_name`（`str`）、`object_key`（`object`）。

### ObjectKey
オブジェクトキー。`behaviour_name`（`str`）、`path_name`（`str`）。

---

## 名前空間

### csc.tools.selection

| 型 | 説明 |
|---|---|
| `Core` | `get_group(idx)` / `get_groups()` / `set_group(i, g)` / `set_groups(map)` / `process(index, mode)` |
| `Group` | `objects`（`Set[ModelObjectId]`）, `pivot`（`ModelObjectId`） |
| `Mode`（enum） | `SetGroup`(0) / `SingleSelect`(1) / `MultiSelect`(2) |

### csc.tools.mirror
- `Core`: 上記 [mirror.Core](#mirrorcore)。

### csc.tools.attractor

| 型 | 説明 |
|---|---|
| `Args` | `for_interval`, `general_settings`, `mode`(`ArgsMode`), `only_key_frames`。コンストラクタ `Args(scene, gravity, settings, only_key_frames, mode)` |
| `AttractorGeneralSettings` | `factor`, `mode`(`ArgsMode`), `mode_relative_to_pivot`, `physic_type`, `position_axis`, `rotation_axis`, `scale_axis` |
| `ArgsMode`（enum） | `Previous`(0) / `Next`(1) / `Inertial`(2) / `InverseInertial`(3) / `Average`(4) / `Interpolation`(5) |
| `SpaceMode`（enum） | `Global`(0) / `Local`(1) |
| `GSPhysicsType`（enum） | `FrameRelax`(0) / `InterpolationRelax`(1) |
| `GSRotationAxis`（enum） | `X`(0) / `Y`(1) / `Z`(2) / `Whole`(3) / `None`(4) |
| `GSAxisFlag`（enum） | `X`(1) / `Y`(2) / `Z`(4) / `XYZ`(7) / `None`(0) |
| `GSAxisIndex`（enum） | `X`(0) / `Y`(1) / `Z`(2) |

---

[← API 目次](README.md)
