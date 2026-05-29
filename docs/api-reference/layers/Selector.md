# csc.layers.Selector

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Selector.html

`class csc.layers.Selector`

Selector class

This class contains methods to observe and to set selected layers and folders

## Properties

- **set_full_selection_by_parts** – overridden method by ItemId[] (itms), int (first), int (last) || IndicesContainer (inds)

## Methods

- `all_included_layer_ids(self: csc.layers.Selector, ignore_locked: bool = False) -> list[csc.Guid]`
  - ignoreLocked : bool (false) | -> LayerId[]
- `all_included_layer_indices(self: csc.layers.Selector, ignore_locked: bool = False) -> domain::scene::layers::index::IndicesContainer`
  - ignoreLocked : bool (false) | -> IndicesContainer
- `is_selected(self: csc.layers.Selector, id: csc.Guid) -> bool`
- `select_default(self: csc.layers.Selector) -> None`
- `selection(self: csc.layers.Selector) -> domain::scene::layers::index::IndicesContainer`
  - -> IndicesContainer
- `set_full_selection_by_parts(*args, **kwargs)`
  - Overloaded function.
  - set_full_selection_by_parts(self: csc.layers.Selector, inds: domain::scene::layers::index::IndicesContainer) -> None inds : IndicesContainer
  - set_full_selection_by_parts(self: csc.layers.Selector, itms: list[csc.Guid], first: int, last: int) -> None
- `set_uncheckable_folder_id(self: csc.layers.Selector, id: csc.Guid, uncheckable: bool) -> None`
  - id : ItemId | uncheckable : bool
- `top_layer_id(self: csc.layers.Selector) -> csc.Guid`
