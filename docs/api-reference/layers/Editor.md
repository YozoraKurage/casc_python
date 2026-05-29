# csc.layers.Editor

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Editor.html

`class csc.layers.Editor`

Editor class

This class contains all methods and properties that need to edit the structure of scene objects’ interpolation properties. The structure is represented in the hierarchy of layers divided by folders.

## Properties

- **create_folder** – name : string, parent : FolderId, withDefaultLayer : bool (true), pos : int or None, -> FolderId
- **create_layer** – name : string, parent : FolderId, pos : int or None, -> FolderId
- **set_fixed_interpolation_if_need** – overridden method by ItemId, int, int || LayerId, int (frame)
- **set_fixed_interpolation_or_key_if_need** – overridden method by LayerId, int, bool

## Methods

- `change_section(self: csc.layers.Editor, arg0: int, arg1: csc.Guid, arg2: Callable) -> None`
- `clear(self: csc.layers.Editor) -> None`
- `create_folder(self: csc.layers.Editor, name: str, parent: csc.Guid, with_default_layer: bool = True, pos: int | None = None) -> csc.Guid`
  - name : string | parent : FolderId | withDefaultLayer : bool (true) | pos : int or None | -> FolderId
- `create_layer(self: csc.layers.Editor, name: str, parent: csc.Guid, pos: int | None = None) -> csc.Guid`
  - name : string | parent : FolderId | pos : int or None | -> FolderId
- `delete_empty_folders(self: csc.layers.Editor) -> None`
- `delete_empty_layers(self: csc.layers.Editor) -> None`
- `delete_folder(self: csc.layers.Editor, id: csc.Guid) -> None`
- `delete_layer(self: csc.layers.Editor, id: csc.Guid) -> None`
- `find_header(self: csc.layers.Editor, arg0: csc.Guid) -> object`
  - -> Header
- `insert_layer(self: csc.layers.Editor, layer: csc.layers.Layer, pos: int | None) -> None`
  - layer : Layer | pos : int or None
- `move_item(self: csc.layers.Editor, item_id: csc.Guid, folder_id: csc.Guid, pos: int | None = None) -> None`
  - pos : int or None
- `normalize_sections(self: csc.layers.Editor, scene: domain::scene::Scene) -> None`
- `set_default(self: csc.layers.Editor) -> None`
- `set_fixed_interpolation_if_need(*args, **kwargs)`
  - Overloaded function.
  - set_fixed_interpolation_if_need(self: csc.layers.Editor, id: csc.Guid, start: int, end: int) -> bool
  - set_fixed_interpolation_if_need(self: csc.layers.Editor, id: csc.Guid, frame: int) -> bool
- `set_fixed_interpolation_or_key_if_need(self: csc.layers.Editor, id: csc.Guid, frame: int, set_key: bool) -> bool`
- `set_locked_for_item(self: csc.layers.Editor, is_l: bool, id: csc.Guid) -> None`
  - isL : bool | id : ItemId
- `set_locked_for_layer(self: csc.layers.Editor, is_l: bool, id: csc.Guid) -> None`
  - isL : bool | id : LayerId
- `set_name(self: csc.layers.Editor, name: str, id: csc.Guid) -> None`
- `set_section(self: csc.layers.Editor, section: domain::scene::layers::layer::Section, pos: int, id: csc.Guid) -> None`
  - section : Section | pos : int | id : ItemId
- `set_sections(self: csc.layers.Editor, arg0: dict[int, domain::scene::layers::layer::Section], arg1: csc.Guid) -> None`
  - section : <Pos, Section>{} | id : LayerId
- `set_visible_for_item(self: csc.layers.Editor, is_v: bool, id: csc.Guid) -> None`
  - isV : bool | id : ItemId
- `set_visible_for_layer(self: csc.layers.Editor, is_v: bool, id: csc.Guid) -> None`
  - isV : bool | id : LayerId
- `unset_section(self: csc.layers.Editor, pos: int, id: csc.Guid) -> None`
  - pos : int | id : ItemId
