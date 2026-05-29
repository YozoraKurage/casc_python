# csc.update.InterfaceAttribute

> 公式: https://cascadeur.com/python-api/_generate/csc.update.InterfaceAttribute.html

InterfaceAttribute represents a group attribute. Can be potentially connected to any attribute.

Interface attribute can be: 1. An attribute of input/output node inside the group 2. An attribute of the group node itself, in the parent group layout (outside the group) We will call this attributes “paired”. For each attribute there is a paired one. They have the same attribute ids and names. Sometimes it’s easier to think of them as of one attribute that has 2 sides. But in terms of this class this are two separate objects.

`class csc.update.InterfaceAttribute`

## Methods

- `group_attribute_id(self: csc.update.InterfaceAttribute) → csc.update.GroupAttributeId`
  - get the group attribute id
- `other_side(self: csc.update.InterfaceAttribute) → csc.update.InterfaceAttribute`
  - Get the paired attribute (e.g. the other side of the attribute)
- `set_name(self: csc.update.InterfaceAttribute, name: str) → None`
  - Rename the attribute
