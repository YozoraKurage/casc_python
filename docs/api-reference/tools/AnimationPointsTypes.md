# csc.tools.AnimationPointsTypes

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.AnimationPointsTypes.html

Class of basic types of points which physics tools and change through animation for target center of mass it contains

## Methods

- **`__init__(self: csc.tools.AnimationPointsTypes, arg0: int, arg1: int, arg2: csc.domain.Scene, arg3: csc.tools.StaticPointsTypes) → None`**

- **`get_collision_points(self: csc.tools.AnimationPointsTypes) → dict[int, set[csc.model.ObjectId]]`**
  - Dict[frame number, set of points]

- **`get_frame_collision_info_points(self: csc.tools.AnimationPointsTypes) → dict[int, dict[csc.model.ObjectId, domain::scene::collision::CollisionInfoForObject]]`**
  - Dict[frame number, Dict[csc.model.ObjectId, CollisionInfoForObject]]

- **`get_fulcrum_points(self: csc.tools.AnimationPointsTypes) → dict[int, set[csc.model.ObjectId]]`**
  - Dict[frame number, set of points]

- **`get_fulcrum_points_with_group(self: csc.tools.AnimationPointsTypes) → dict[int, set[csc.model.ObjectId]]`**
  - Dict[frame number, set of points]

- **`get_touch_points(self: csc.tools.AnimationPointsTypes) → dict[int, set[csc.model.ObjectId]]`**
  - Dict[frame number, set of points]
