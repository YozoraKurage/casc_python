# csc.update.Group

> 公式: https://cascadeur.com/python-api/_generate/csc.update.Group.html

Group class

`class csc.update.Group`

## Methods

- `add_input(self: csc.update.Group, name: str) → csc.update.InterfaceAttribute`
- `add_output(self: csc.update.Group, name: str) → csc.update.InterfaceAttribute`
- `constant_datas(self: csc.update.Group) → csc.update.ConstantDatas`
  - get virtual node to access constant datas
- `constant_settings(self: csc.update.Group) → csc.update.ConstantSettings`
  - get virtual node to access constant settings
- `create_group(self: csc.update.Group, name: str) → csc.update.Group`
- `delete_node(self: csc.update.Group, node: csc.update.Node) → None`
- `group(self: csc.update.Group, nodes: set[csc.update.Node], name: str) → csc.update.Group`
- `group_id(self: csc.update.Group) → csc.update.GroupId`
  - create sub group
- `has_node(self: csc.update.Group, name: str) → bool`
  - check whether there is a child node with a given name
- `input_interface_node(self: csc.update.Group) → csc.update.InterfaceNode`
- `interface_input(self: csc.update.Group, name: str) → csc.update.InterfaceAttribute`
- `interface_inputs(self: csc.update.Group) → list[csc.update.InterfaceAttribute]`
  - get group attributes as interface attributes
- `interface_node(self: csc.update.Group, direction: csc.Direction) → csc.update.InterfaceNode`
  - access the interface node
- `interface_output(self: csc.update.Group, name: str) → csc.update.InterfaceAttribute`
- `interface_outputs(self: csc.update.Group) → list[csc.update.InterfaceAttribute]`
- `is_root(self: csc.update.Group) → csc.update.GroupId`
- `leaf_children(self: csc.update.Group) → set[csc.update.Node]`
  - get all leaf nodes (settings, datas, functions)
- `node`
  - Overloaded function.
  - `node(self: csc.update.Group, name: str) -> csc.update.Node`
  - `node(self: csc.update.Group, node: Union[csc.update.GroupId, csc.update.InterfaceId, csc.update.ExternalPropertiesId, csc.update.ConstantDatasId, csc.update.ConstantSettingsId, csc.model.ObjectId, csc.model.HyperedgeId, csc.model.DataId, csc.model.SettingFunctionId, csc.model.SettingId]) -> csc.update.Node`
- `node_deep(self: csc.update.Group, name: str) → csc.update.Node`
  - access node by name or id recursively
- `node_with_type(self: csc.update.Group, type_name: str, name: str) → csc.update.Node`
  - find node with name and type
- `node_with_type_deep(self: csc.update.Group, type_name: str, name: str) → csc.update.Node`
  - find node with name and type recursively
- `nodes(self: csc.update.Group) → set[csc.update.Node]`
  - get all children (their children are not included)
- `output_interface_node(self: csc.update.Group) → csc.update.InterfaceNode`
