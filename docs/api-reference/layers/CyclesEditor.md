# csc.layers.CyclesEditor

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.CyclesEditor.html

`class csc.layers.CyclesEditor`

Cycle editor class. Represents an editor for managing cycles within layers

## Methods

- `change_inactive_parts(self: csc.layers.CyclesEditor, arg0: int, arg1: int, arg2: int) -> None`
- `create_cycle(self: csc.layers.CyclesEditor, arg0: int, arg1: int, arg2: bool) -> csc.layers.Cycle`
  - Creates a cycle within the layer structure.
  - Parameters: left_inactive_frame_index (int) – The index of the left inactive frame.
  - Parameters: right_inactive_frame_index (int) – The index of the right inactive frame.
  - Parameters: first_active_frame_index (int) – The index of the first active frame.
  - Parameters: last_active_frame_index (int) – The index of the last active frame.
  - Parameters: following_interval (int) – The following interval.
  - Returns: The created cycle.
  - Return type: csc.layers.Cycle
- `delete_cycle(self: csc.layers.CyclesEditor, arg0: int) -> None`
  - Deletes a cycle from the layer structure.
  - Parameters: cycle (csc.layers.Cycle) – The cycle to delete.
- `find_cycle(self: csc.layers.CyclesEditor, arg0: int) -> object`
  - Finds a cycle by the specified position.
  - Parameters: pos (int) – The position to search for.
  - Returns: The found cycle.
  - Return type: csc.layers.Cycle
- `normalize(self: csc.layers.CyclesEditor) -> None`
