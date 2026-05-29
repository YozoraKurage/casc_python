# csc.tools.mirror.Core

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.mirror.Core.html

Mirror tool core class

## Methods

- `__init__(self, *args, **kwargs)` → None
  - Constructor for the Core class

- `mirror_frame(self, arg0: set[csc.model.ObjectId | csc.domain.Tool_object_id]) → None`
  - Mirror the frame of the mirror tool based on the specified set of object IDs.

- `mirror_interval(self, arg0: set[csc.model.ObjectId | csc.domain.Tool_object_id]) → None`
  - Mirror the interval of the mirror tool based on the specified set of object IDs.

- `plane(self) → csc.math.Plane`
  - Get the plane of the mirror tool.
  - Returns: Plane of the mirror tool

- `set_plane(self, plane: csc.math.Plane) → None`
  - Set the plane of the mirror tool.
  - Parameters: `plane` - Plane to set as mirror tool plane.
