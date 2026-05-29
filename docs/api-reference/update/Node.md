# csc.update.Node

> 公式: https://cascadeur.com/python-api/_generate/csc.update.Node.html

Node class represents a generic Node and implements methods that are common for all nodes

`class csc.update.Node`

## Methods

- `attributes(self: csc.update.Node, d: csc.Direction) → list[csc.update.NodeAttribute]`
  - array of all input and output attributes
- `equal_to(self: csc.update.Node, arg0: csc.update.Node) → bool`
- `full_name(self: csc.update.Node) → str`
  - name with all the parent nodes
- `has_input(self: csc.update.Node, name: str) → bool`
  - check if there is an input with such a name
- `has_output(self: csc.update.Node, name: str) → bool`
  - check if there is an output with such a name
- `id(self: csc.update.Node) → csc.update.GroupId | csc.update.InterfaceId | csc.update.ExternalPropertiesId | csc.update.ConstantDatasId | csc.update.ConstantSettingsId | csc.model.ObjectId | csc.model.HyperedgeId | csc.model.DataId | csc.model.SettingFunctionId | csc.model.SettingId`
  - get uniqui id
- `input(self: csc.update.Node, name: str) → csc.update.NodeAttribute`
  - shortcut if node has only one input attribute
- `inputs(self: csc.update.Node) → list[csc.update.NodeAttribute]`
  - array of all the inputes attributes
- `is_active(self: csc.update.Node) → bool`
  - check whether it is active for current actualities states (see Additional functionality in csc.update.UpdateEditor)
- `is_fictive(self: csc.update.Node) → bool`
  - whether it is a fictive node (constants, inputs, outputs of a group or external properties)
- `name(self: csc.update.Node) → str`
  - get name
- `output(self: csc.update.Node, name: str) → csc.update.NodeAttribute`
  - shortcut if node has only one output attribute
- `outputs(self: csc.update.Node) → list[csc.update.NodeAttribute]`
  - array of all the outputs attributes
- `parent_group(self: csc.update.Node) → domain::update_editor::Group`
  - return parent group (where this group node is located)
- `parent_object(self: csc.update.Node) → domain::update_editor::Object`
  - return object of the node. Will return null if this is not an update group
- `set_name(self: csc.update.Node, name: str) → None`
  - rename node
