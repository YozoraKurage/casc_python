# csc.update.ObjectGroup

> 公式: https://cascadeur.com/python-api/_generate/csc.update.ObjectGroup.html

ObjectGroup class represents object group node

`class csc.update.ObjectGroup`

## Methods

- `create_object`
  - Overloaded function.
  - `create_object(self: csc.update.ObjectGroup, name: str) -> csc.update.Object`
  - `create_object(self: csc.update.ObjectGroup, name: str, id: csc.model.ObjectId) -> csc.update.Object`
- `create_sub_object_group(self: csc.update.ObjectGroup, name: str) → csc.update.ObjectGroup`
  - -> ObjectGroup
- `object_groups(self: csc.update.ObjectGroup) → set[csc.update.ObjectGroup]`
  - -> ObjectGroup{}
- `objects(self: csc.update.ObjectGroup) → set[csc.update.Object]`
  - -> Object{}
