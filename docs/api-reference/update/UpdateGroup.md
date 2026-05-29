# csc.update.UpdateGroup

> 公式: https://cascadeur.com/python-api/_generate/csc.update.UpdateGroup.html

UpdateGroup class represents update group node

`class csc.update.UpdateGroup`

## Methods

- `create_regular_data(self: csc.update.UpdateGroup, name: str, value: Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]], mode: csc.model.DataMode = <DataMode.Static: 0>) → csc.update.RegularData`
- `create_regular_function(self: csc.update.UpdateGroup, name: str, function: str) → csc.update.RegularFunction`
- `create_setting_data(self: csc.update.UpdateGroup, name: str, value: Union[bool, int], mode: csc.model.SettingMode = <SettingMode.Static: 0>) → csc.update.SettingData`
- `create_setting_function(self: csc.update.UpdateGroup, name: str, function_name: str) → csc.update.SettingFunction`
- `create_sub_update_group(self: csc.update.UpdateGroup, arg0: str) → csc.update.UpdateGroup`
- `create_sub_update_group2(self: csc.update.UpdateGroup, name: str, group_id: csc.update.GroupId) → csc.update.UpdateGroup`
  - -> UpdateGroup
- `external_properties(self: csc.update.UpdateGroup) → csc.update.ExternalProperties`
  - -> ExternalProperties
- `groups(self: csc.update.UpdateGroup) → set[csc.update.UpdateGroup]`
  - -> UpdateGroup{}
- `regular_datas(self: csc.update.UpdateGroup) → set[csc.update.RegularData]`
  - -> RegularData{}
- `regular_functions(self: csc.update.UpdateGroup) → set[csc.update.RegularFunction]`
  - -> RegularFunction{}
- `setting_functions(self: csc.update.UpdateGroup) → set[csc.update.SettingFunction]`
  - -> SettingFunction{}
- `settings_datas(self: csc.update.UpdateGroup) → set[csc.update.SettingData]`
  - -> SettingsData{}
