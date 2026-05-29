# csc.layers.index.FramesIndices

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.index.FramesIndices.html

`class csc.layers.index.FramesIndices`

FramesIndices class

It helps to work with animation intervals

## Properties

- **add** – overridden method by int || FramesIndices

## Methods

- `add(*args, **kwargs)`
  - Overloaded function.
  - add(self: csc.layers.index.FramesIndices, index: int) -> None
  - add(self: csc.layers.index.FramesIndices, other: csc.layers.index.FramesIndices) -> None
  - add(self: csc.layers.index.FramesIndices, indices: set[int]) -> None
  - add(self: csc.layers.index.FramesIndices, indices: list[int]) -> None
- `clamp(self: csc.layers.index.FramesIndices, min: int, max: int) -> csc.layers.index.FramesIndices`
- `empty(self: csc.layers.index.FramesIndices) -> bool`
- `first(self: csc.layers.index.FramesIndices) -> int`
- `static from_range(min: int, max: int) -> csc.layers.index.FramesIndices`
  - -> FramesIndices
- `static intersect_indices(l: csc.layers.index.FramesIndices, r: csc.layers.index.FramesIndices) -> csc.layers.index.FramesIndices`
- `last(self: csc.layers.index.FramesIndices) -> int`
- `size(self: csc.layers.index.FramesIndices) -> int`
- `static to_intervals(indices: csc.layers.index.FramesIndices) -> list[csc.layers.index.FramesInterval]`
  - -> FramesInterval[]
- `static union_indices(l: csc.layers.index.FramesIndices, r: csc.layers.index.FramesIndices) -> csc.layers.index.FramesIndices`
