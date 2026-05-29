# csc.update.Update

> 公式: https://cascadeur.com/python-api/_generate/csc.update.Update.html

Update class represents the whole update editor

`class csc.update.Update`

## Methods

- `delete_node(self: csc.update.Update, id: csc.update.GroupId | csc.update.InterfaceId | csc.update.ExternalPropertiesId | csc.update.ConstantDatasId | csc.update.ConstantSettingsId | csc.model.ObjectId | csc.model.HyperedgeId | csc.model.DataId | csc.model.SettingFunctionId | csc.model.SettingId) → None`
- `get_node_by_id(self: csc.update.Update, id: csc.update.GroupId | csc.update.InterfaceId | csc.update.ExternalPropertiesId | csc.update.ConstantDatasId | csc.update.ConstantSettingsId | csc.model.ObjectId | csc.model.HyperedgeId | csc.model.DataId | csc.model.SettingFunctionId | csc.model.SettingId) → csc.update.Node`
- `get_object_by_id(self: csc.update.Update, arg0: csc.model.ObjectId) → csc.update.Object`
- `root(self: csc.update.Update) → csc.update.ObjectGroup`
  - -> ObjectGroup
- `ungroup(self: csc.update.Update, group: csc.update.Group) → None`
