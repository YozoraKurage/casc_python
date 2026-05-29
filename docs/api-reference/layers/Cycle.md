# csc.layers.Cycle

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.Cycle.html

`class csc.layers.Cycle`

Cycle class. Represents a cycle within the layer structure, containing information about active and inactive frames.

## Properties

- `property first_active_frame_index`
- `property following_interval`
- `property last_active_frame_index`
- `property left_inactive_frame_index`
- `property right_inactive_frame_index`

## Methods

- `static get_no_pos() -> int`
- `is_the_same_frames_as(self: csc.layers.Cycle, other_cycle: csc.layers.Cycle) -> bool`
  - Checks if the current cycle has the same frames as another cycle.
  - Parameters: other_cycle (csc.layers.Cycle) – The other cycle to compare with.
  - Returns: True if the cycles have the same frames, False otherwise.
  - Return type: bool
- `left_frame_index(self: csc.layers.Cycle) -> int`
  - Retrieves the index of the left frame in the cycle.
  - Returns: The index of the left frame.
  - Return type: int
- `right_frame_index(self: csc.layers.Cycle) -> int`
  - Retrieves the index of the right frame in the cycle.
  - Returns: The index of the right frame.
  - Return type: int
