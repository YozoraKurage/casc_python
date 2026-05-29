# csc.tools.CollisionInfoForObject

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.CollisionInfoForObject.html

Structure with collision information for an object. The normal vector is directed from the other object toward the collision point.

## Properties

- **normal** → Vector3d
  - The collision normal vector

- **other** → csc.model.ObjectId
  - The object ID of the colliding entity

- **penetration_depth** → double
  - The depth of penetration between colliding objects

- **pos** → Vector3d
  - The position where collision occurs

## Methods

- **__init__**(*args, **kwargs)
  - Constructor for CollisionInfoForObject
