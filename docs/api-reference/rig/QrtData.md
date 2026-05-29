# csc.rig.QrtData

> 公式: https://cascadeur.com/python-api/_generate/csc.rig.QrtData.html

Data structure for quadruped rigging configuration in Cascadeur.

## Methods

- `__init__(self: csc.rig.QrtData) → None`
  - Constructor for QrtData class

## Properties

- `body`
  - Body component of the quadruped rig

- `left_hand`
  - Left hand/front limb configuration

- `right_hand`
  - Right hand/front limb configuration

- `quadruped`
  - Quadruped-specific rigging data

- `hinge_arm_direction`
  - Direction vector for arm hinge joints

- `hinge_leg_direction`
  - Direction vector for leg hinge joints

- `twists`
  - Twist bone properties for the rig

- `untwists`
  - Untwist bone properties for the rig

- `is_align_pelvis`
  - Boolean flag to align pelvis during rigging

- `is_spline_ik`
  - Boolean flag to use spline IK setup

- `is_create_layers`
  - Boolean flag to create animation layers

- `is_replace_existing`
  - Boolean flag to replace existing rig data
