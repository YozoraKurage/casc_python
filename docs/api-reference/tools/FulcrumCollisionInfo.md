# csc.tools.FulcrumCollisionInfo

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.FulcrumCollisionInfo.html

Class of basic types of points change through animation for target center of mass it contains get_fulcrum_points – all fulcrum point with collision get_collision_points – all collision points get_fulcrum_floor_points – all fulcrum points that are on the floor get_frame_collision_info_points – all collision points with collision info

## Methods

- `__init__(self: csc.tools.FulcrumCollisionInfo, arg0: int, arg1: int, arg2: csc.domain.Scene, arg3: csc.tools.StaticPointsTypes) → None`

- `get_collision_points(self: csc.tools.FulcrumCollisionInfo) → dict[int, set[csc.model.ObjectId]]`
  - Dict[frame number, set of points]

- `get_frame_collision_info_points(self: csc.tools.FulcrumCollisionInfo) → dict[int, dict[csc.model.ObjectId, csc.tools.CollisionInfoForObject]]`
  - Dict[frame number, Dict[csc.model.ObjectId, CollisionInfoForObject]]

- `get_fulcrum_points(self: csc.tools.FulcrumCollisionInfo) → dict[int, set[csc.model.ObjectId]]`
  - Dict[frame number, set of points]

- `get_touch_points(self: csc.tools.FulcrumCollisionInfo) → dict[int, set[csc.model.ObjectId]]`
  - Dict[frame number, set of points]
