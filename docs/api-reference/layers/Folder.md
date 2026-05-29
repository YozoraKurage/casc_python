# csc.layers.Folder

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Folder.html

`class csc.layers.Folder`

Folder class

Implements the parent folder properties of children layers and sub folders items

## Properties

- `property header`
  - -> Header

## Methods

- `child_by_id(self: csc.layers.Folder, id: csc.Guid) -> csc.Guid`
  - -> ItemId
- `child_by_pos(self: csc.layers.Folder, pos: int) -> csc.Guid`
  - pos : int -> ItemId
- `child_pos(self: csc.layers.Folder, id: csc.Guid) -> int`
  - id : ItemId | -> int
- `children_cnt(self: csc.layers.Folder) -> int`
  - -> int
- `children_ids(self: csc.layers.Folder) -> list[csc.Guid]`
  - -> ItemId[]
- `children_ordered(self: csc.layers.Folder) -> list[csc.Guid]`
  - -> ItemId[]
- `has_child(self: csc.layers.Folder, id: csc.Guid) -> bool`
- `is_empty(self: csc.layers.Folder) -> bool`
