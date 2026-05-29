# csc.layers.Viewer

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Viewer.html

`class csc.layers.Viewer`

Viewer class

This class contains all methods and properties that describe the structure of scene objects’ interpolation properties. The structure is represented in the hierarchy of layers divided by folders.

## Properties

- **top_layer_id** – overridden method by ItemId || ItemId[]
- **merged_layer** – overridden method like static and member LayerId[]
- **last_key_pos** – overridden method by LayerId[], -> Layer
- **frames_count** – overridden method by LayerId[], -> int
- **significant_frames** – overridden method by LayerId{}, -> int{}

## Methods

- `actual_key_pos(self: csc.layers.Viewer, pos: int) -> int`
- `all_child_ids(self: csc.layers.Viewer, id: csc.Guid) -> list[csc.Guid]`
  - -> ItemId[]
- `all_included_layer_ids(self: csc.layers.Viewer, items: list[csc.Guid], ignore_locked: bool = False) -> list[csc.Guid]`
  - items : ItemId[] | ignoreLocked : bool (false) | -> LayerId[]
- `all_layer_ids(self: csc.layers.Viewer) -> list[csc.Guid]`
  - -> LayerId[]
- `all_parent_ids(self: csc.layers.Viewer, id: csc.Guid) -> list[csc.Guid]`
  - -> FolderId[]
- `default_layer_id(self: csc.layers.Viewer) -> csc.Guid`
  - -> LayerId
- `find_folder(self: csc.layers.Viewer, id: csc.Guid) -> object`
  - id : FolderId | -> Folder
- `find_layer(self: csc.layers.Viewer, id: csc.Guid) -> object`
  - id : LayerId | -> Layer
- `folder(self: csc.layers.Viewer, id: csc.Guid) -> object`
  - id : FolderId | -> Folder
- `folders_map(self: csc.layers.Viewer) -> dict[csc.Guid, csc.layers.Folder]`
  - -> <FolderId, Folder>{}
- `for_all_ordered_items(self: csc.layers.Viewer, arg0: Callable[[csc.Guid], bool]) -> None`
- `frames_count(*args, **kwargs)`
  - Overloaded function.
  - frames_count(self: csc.layers.Viewer) -> int
  - frames_count(self: csc.layers.Viewer, id_arr: list[csc.Guid]) -> int
- `has_item(self: csc.layers.Viewer, id: csc.Guid) -> bool`
  - -> bool
- `header(self: csc.layers.Viewer, id: csc.Guid) -> object`
  - id : ItemId | -> Header
- `is_deep_child(self: csc.layers.Viewer, item_id: csc.Guid, folder_id: csc.Guid) -> bool`
  - -> bool
- `item(self: csc.layers.Viewer, id: csc.Guid) -> csc.layers.ItemVariant`
  - id : ItemId | -> ItemVariant
- `last_key_pos(*args, **kwargs)`
  - Overloaded function.
  - last_key_pos(self: csc.layers.Viewer) -> int
  - last_key_pos(self: csc.layers.Viewer, id_arr: list[csc.Guid]) -> int
- `layer(self: csc.layers.Viewer, id: csc.Guid) -> object`
  - id : LayerId | -> Layer
- `layer_id_by_obj_id(self: csc.layers.Viewer, id: common::GenericId<domain::scene::model::ModelObject>) -> csc.Guid`
  - id : csc.model.ObjectId | -> LayerId
- `layer_id_by_obj_id_or_null(self: csc.layers.Viewer, id: common::GenericId<domain::scene::model::ModelObject>) -> csc.Guid`
  - id : csc.model.ObjectId | -> LayerId
- `layer_ids_by_obj_ids(self: csc.layers.Viewer, ids: list[common::GenericId<domain::scene::model::ModelObject>]) -> set[csc.Guid]`
  - ids : csc.model.ObjectId[] | -> LayerId{}
- `layers_indices(self: csc.layers.Viewer, id_arr: domain::scene::layers::index::IndicesContainer, ignore_locked: bool = False) -> domain::scene::layers::index::IndicesContainer`
  - -> IndicesContainer
- `layers_map(self: csc.layers.Viewer) -> dict[csc.Guid, csc.layers.Layer]`
  - -> <LayerId, Layer>{}
- `merged_layer(self: csc.layers.Viewer, scene: domain::scene::Scene, ids: list[csc.Guid], normalize: bool = True) -> csc.layers.Layer`
- `obj_ids_by_layer_ids(self: csc.layers.Viewer, id_arr: list[csc.Guid]) -> list[common::GenericId<domain::scene::model::ModelObject>]`
  - -> LayerId[]
- `pos_in_parent(self: csc.layers.Viewer, id: csc.Guid) -> int`
  - -> int
- `root_id(self: csc.layers.Viewer) -> csc.Guid`
  - -> FolderId
- `significant_frames(*args, **kwargs)`
  - Overloaded function.
  - significant_frames(self: csc.layers.Viewer) -> domain::scene::layers::index::FramesIndices
  - significant_frames(self: csc.layers.Viewer, id_arr: set[csc.Guid]) -> domain::scene::layers::index::FramesIndices
- `top_layer_id(*args, **kwargs)`
  - Overloaded function.
  - top_layer_id(self: csc.layers.Viewer, id: csc.Guid) -> csc.Guid
  - top_layer_id(self: csc.layers.Viewer, id_arr: list[csc.Guid]) -> csc.Guid
- `unlocked_layer_ids(self: csc.layers.Viewer, id_arr: list[csc.Guid]) -> list[csc.Guid]`
  - -> LayerId[]
