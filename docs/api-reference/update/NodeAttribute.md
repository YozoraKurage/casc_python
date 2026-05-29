# csc.update.NodeAttribute

> 公式: https://cascadeur.com/python-api/_generate/csc.update.NodeAttribute.html

NodeAttribute represents a generic node attribute and the standard operations you can do with such an attribute.

`class csc.update.NodeAttribute`

## Methods

- `connect(self: csc.update.NodeAttribute, attribute: csc.update.NodeAttribute) → None`
  - attribute: NodeAttribute
- `connected_attributes(self: csc.update.NodeAttribute) → list[csc.update.NodeAttribute]`
  - -> NodeAttribute[]
- `connected_leaves(self: csc.update.NodeAttribute, get_only_first: bool = False) → list[csc.update.NodeAttribute]`
  - -> NodeAttribute[]
- `connected_leaves_in_undirected_graph(self: csc.update.NodeAttribute) → list[csc.update.NodeAttribute]`
- `direction(self: csc.update.NodeAttribute) → csc.Direction`
  - -> csc.DirectionValue
- `disconnect`
  - Overloaded function.
  - `disconnect(self: csc.update.NodeAttribute) -> None`
  - `disconnect(self: csc.update.NodeAttribute, attribute: csc.update.NodeAttribute) -> None`
- `id(self: csc.update.NodeAttribute) → csc.update.RegularFunctionAttributeId | csc.model.HyperedgeId | csc.update.RegularDataAttributeId | csc.update.ActualityAttributeId | csc.update.SettingFunctionAttributeId | csc.model.SettingId | csc.update.GroupAttributeId | csc.update.ExternalPropertyAttributeId | csc.update.ConstantDataAttributeId | csc.update.ConstantSettingAttributeId`
  - -> AttributeId
- `is_active(self: csc.update.NodeAttribute) → bool`
- `name(self: csc.update.NodeAttribute) → str`
- `node(self: csc.update.NodeAttribute) → domain::update_editor::Node`
  - -> Node
