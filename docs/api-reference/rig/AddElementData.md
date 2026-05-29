# csc.rig.AddElementData

> 公式: https://cascadeur.com/python-api/_generate/csc.rig.AddElementData.html

AddElementData class for managing element additions in the rigging process.

## Properties

- **axis_point_controller** - Axis point controller
- **box_multiplier** - Box multiplier
- **is_multiple** - Is multiple
- **joint_size_without_child** - Joint size without child
- **offset_point_controller** - Offset point controller
- **only_box_controller** - Only box controller
- **orthogonal_with_parent** - Orthogonal with parent
- **point_color** - Point color (numpy.ndarray)
- **use_global_axis** - Use global axis

## Methods

- **`__init__(self: csc.rig.AddElementData) -> None`**
  - Overloaded constructor with no arguments

- **`__init__(self: csc.rig.AddElementData, arg0: bool, arg1: bool, arg2: int, arg3: int, arg4: bool, arg5: bool, arg6: int, arg7: float, arg8: numpy.ndarray[numpy.float32[3, 1]]) -> None`**
  - Overloaded constructor accepting: only_box_controller (bool), is_multiple (bool), box_multiplier (int), axis_point_controller (int), use_global_axis (bool), orthogonal_with_parent (bool), offset_point_controller (int), joint_size_without_child (float), and point_color (numpy array)
