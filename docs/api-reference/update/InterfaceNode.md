# csc.update.InterfaceNode

> 公式: https://cascadeur.com/python-api/_generate/csc.update.InterfaceNode.html

InterfaceNode is a node inside the group that represents its connections with the ouside nodes. Its attributes are csc.update.InterfaceAttributes

`class csc.update.InterfaceNode`

## Methods

- `add_attribute(self: csc.update.InterfaceNode, name: str) → csc.update.InterfaceAttribute`
- `direction(self: csc.update.InterfaceNode) → csc.Direction`
  - -> csc.DirectionValue
- `interface_attributes(self: csc.update.InterfaceNode) → list[csc.update.InterfaceAttribute]`
  - -> InterfaceAttribute[]
- `move_attribute(self: csc.update.InterfaceNode, attribute: csc.update.InterfaceAttribute, position: int) → None`
  - attribute: InterfaceAttribute | position: int
- `remove_attribute(self: csc.update.InterfaceNode, attribute: csc.update.InterfaceAttribute) → None`
  - attribute: InterfaceAttribute
