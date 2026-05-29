# csc.layers.index.IndicesContainer

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.index.IndicesContainer.html

`class csc.layers.index.IndicesContainer`

IndicesContainer class

Contains of indices items in the structure std::map<ItemId, FramesIndices>

## Properties

- **all_frame_indices** – overridden method by int (sizeLimit)
- **frames_interval** – overridden method by int (sizeLimit)

## Methods

- `add(self: csc.layers.index.IndicesContainer, other_container: csc.layers.index.IndicesContainer) -> None`
  - otherContainer : IndicesContainer
- `add_frame_indices(self: csc.layers.index.IndicesContainer, frame_indices: csc.layers.index.FramesIndices) -> None`
  - frame_indices: int{}
- `add_item(self: csc.layers.index.IndicesContainer, item_indices: domain::scene::layers::index::ItemIndices) -> None`
  - itemIndices : ItemIndices
- `all_frame_indices(*args, **kwargs)`
  - Overloaded function.
  - all_frame_indices(self: csc.layers.index.IndicesContainer) -> csc.layers.index.FramesIndices
  - all_frame_indices(self: csc.layers.index.IndicesContainer, size_limit: int) -> csc.layers.index.FramesIndices
- `cell_indices(self: csc.layers.index.IndicesContainer) -> list[csc.layers.index.CellIndex]`
  - -> CellIndex[]
- `delete_empty_items(self: csc.layers.index.IndicesContainer) -> None`
- `direct_indices(*args, **kwargs)`
  - Overloaded function.
  - direct_indices(self: csc.layers.index.IndicesContainer) -> dict[csc.Guid, csc.layers.index.FramesIndices]
  - direct_indices(self: csc.layers.index.IndicesContainer) -> dict[csc.Guid, csc.layers.index.FramesIndices]
- `frames_interval(*args, **kwargs)`
  - Overloaded function.
  - frames_interval(self: csc.layers.index.IndicesContainer) -> csc.layers.index.FramesInterval
  - frames_interval(self: csc.layers.index.IndicesContainer, size_limit: int) -> csc.layers.index.FramesInterval
- `is_empty(self: csc.layers.index.IndicesContainer) -> bool`
- `item_ids(self: csc.layers.index.IndicesContainer) -> list[csc.Guid]`
  - -> Guid[]
- `item_indices(self: csc.layers.index.IndicesContainer, id: csc.Guid) -> csc.layers.index.FramesIndices`
  - -> FramesIndices
- `items_indices(self: csc.layers.index.IndicesContainer) -> list[domain::scene::layers::index::ItemIndices]`
  - -> ItemIndices[]
- `rect(self: csc.layers.index.IndicesContainer) -> csc.layers.index.RectIndicesContainer`
  - -> RectIndicesContainer
- `set_frame_indices(self: csc.layers.index.IndicesContainer, start: int, end: int) -> None`
  - start, end : int
