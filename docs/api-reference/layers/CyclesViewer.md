# csc.layers.CyclesViewer

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.CyclesViewer.html

`class csc.layers.CyclesViewer`

Cycle viewer class. Provides methods for viewing and interacting with cycles within a layer.

## Methods

- `any_cycles_exist_in_frames(self: csc.layers.CyclesViewer, arg0: int, arg1: int) -> bool`
  - Checks if any cycles exist within the specified frames.
  - Parameters: first_frame_index (int) – The index of the first frame.
  - Parameters: last_frame_index (int) – The index of the last frame.
  - Returns: True if any cycles exist within the frames, False otherwise.
  - Return type: bool
- `cycle_contains_frame_index(self: csc.layers.CyclesViewer, arg0: csc.layers.Cycle, arg1: int) -> bool`
  - Checks if the cycle contains the specified frame index.
  - Parameters: frame_index (int) – The frame index to check.
  - Returns: True if the cycle contains the frame index, False otherwise.
  - Return type: bool
- `find_cycle(self: csc.layers.CyclesViewer, arg0: int) -> object`
  - Finds a cycle by the specified position.
  - Parameters: pos (int) – The position to search for.
  - Returns: The found cycle.
  - Return type: csc.layers.Cycle
- `get_active_pos(self: csc.layers.CyclesViewer, arg0: int) -> int`
  - Retrieves the active position of the cycle.
  - Returns: The active position of the cycle.
  - Return type: int
- `get_active_section_pos(self: csc.layers.CyclesViewer, arg0: int) -> int`
  - Retrieves the active section position of the cycle.
  - Returns: The active section position of the cycle.
  - Return type: int
- `get_cycles_in_frames(self: csc.layers.CyclesViewer, arg0: int, arg1: int) -> list[csc.layers.Cycle]`
  - Retrieves the cycles within the specified frames.
  - Parameters: first_frame_index (int) – The index of the first frame.
  - Parameters: last_frame_index (int) – The index of the last frame.
  - Returns: The cycles within the frames.
  - Return type: List[csc.layers.Cycle]
- `get_most_left_and_right_frame_indices_of_cycle(self: csc.layers.CyclesViewer, arg0: csc.layers.Cycle) -> tuple[int, int]`
  - Retrieves the most left and right frame indices of the cycle.
  - Returns: The most left and right frame indices of the cycle.
  - Return type: Tuple[int, int]
- `is_pos_in_active_cycle_zone(self: csc.layers.CyclesViewer, arg0: int) -> bool`
  - Checks if the specified position is within the active cycle zone.
  - Parameters: pos (int) – The position to check.
  - Returns: True if the position is within the active cycle zone, False otherwise.
  - Return type: bool
- `is_pos_in_inactive_cycle_zone(self: csc.layers.CyclesViewer, arg0: int) -> bool`
  - Checks if the specified position is within the inactive cycle zone.
  - Parameters: pos (int) – The position to check.
  - Returns: True if the position is within the inactive cycle zone, False otherwise.
  - Return type: bool
- `last_pos(self: csc.layers.CyclesViewer) -> int`
