# csc.layers.Layer

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Layer.html

`class csc.layers.Layer`

Layer class

The Layer is the basic element that implements intervals and sections to set interpolation properties of scene objects

## Properties

- **header** – Get Header
- **is_locked** – Get bool
- **is_visible** – Get bool
- **obj_ids** – Get csc.Guid{}
- **sections** – Get std::map<Pos, Section>

## Methods

- `actual_key(self: csc.layers.Layer, pos: int) -> domain::scene::layers::layer::Key`
  - -> Key
- `actual_key_pos(self: csc.layers.Layer, pos: int) -> int`
  - -> int
- `actual_section(self: csc.layers.Layer, pos: int) -> domain::scene::layers::layer::Section`
  - -> Section
- `actual_section_pos(self: csc.layers.Layer, pos: int) -> int`
  - -> int
- `find_section(self: csc.layers.Layer, pos: int) -> object`
  - pos : int | -> Section
- `interval(self: csc.layers.Layer, pos: int) -> domain::scene::layers::layer::Interval`
  - -> Interval
- `is_key(self: csc.layers.Layer, pos: int) -> bool`
- `is_key_or_fixed(self: csc.layers.Layer, pos: int) -> bool`
- `key(self: csc.layers.Layer, pos: int) -> domain::scene::layers::layer::Key`
  - -> Key
- `key_frame_indices(self: csc.layers.Layer) -> domain::scene::layers::index::FramesIndices`
  - -> FramesIndices
- `last_key_pos(self: csc.layers.Layer) -> int`
  - -> int
- `section(self: csc.layers.Layer, pos: int) -> domain::scene::layers::layer::Section`
  - -> Section
