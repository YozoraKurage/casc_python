# csc.model.DataViewer

> 公式: https://cascadeur.com/python-api/_generate/csc.model.DataViewer.html

DataViewer class

This class allows to view scene data and their properties.

`class csc.model.DataViewer`

## Properties

- **get_data_value** — overridden method by id : csc.model.DataId || csc.model.DataId, int (frame) -> Data.Value
- **get_behaviour_property** — overridden method by : csc.model.BehaviourId, string -> Data.Value || csc.model.BehaviourId, string, int (frame) -> Setiing.Value

## Methods

- `cluster_viewer(self: csc.model.DataViewer) -> csc.model.ClusterViewer`
  - -> ClusterViewer

- `get_all_data_id(self: csc.model.DataViewer, object_id: csc.model.ObjectId) -> list[csc.model.DataId]`
  - -> csc.model.DataId[]

- `get_all_settings_id(self: csc.model.DataViewer, object_id: csc.model.ObjectId) -> list[csc.model.SettingId]`
  - -> csc.model.SettingId[]

- `get_animation_size(self: csc.model.DataViewer) -> int`
  - -> int

- `get_data(self: csc.model.DataViewer, id: csc.model.DataId) -> csc.model.Data`
  - id : csc.model.DataId | -> Data

- `get_data_id(self: csc.model.DataViewer, id: csc.model.ObjectId, name: str) -> csc.model.DataId`
  - id : csc.model.ObjectId | name : string | -> csc.model.DataId

- `get_data_name(self: csc.model.DataViewer, arg0: csc.model.DataId) -> str`
  - id : csc.model.DataId | -> string

- `get_data_value(*args, **kwargs)`
  - Overloaded function.
  - `get_data_value(self: csc.model.DataViewer, id: csc.model.DataId) -> Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]`
  - `get_data_value(self: csc.model.DataViewer, arg0: csc.model.DataId, arg1: int) -> Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]`

- `get_description_by_name(self: csc.model.DataViewer, arg0: str) -> str`
  - -> string

- `get_description_names(self: csc.model.DataViewer) -> list[str]`
  - -> string[]

- `get_description_value(*args, **kwargs)`
  - Overloaded function.
  - `get_description_value(self: csc.model.DataViewer, id: csc.model.DataId) -> str`
    - id : csc.model.DataId -> string
  - `get_description_value(self: csc.model.DataViewer, id: csc.model.SettingId) -> str`
    - id : csc.model.SettingId -> string

- `get_setting(self: csc.model.DataViewer, id: csc.model.SettingId) -> csc.model.Setting`
  - id : csc.model.SettingId | -> Setting

- `get_setting_id(self: csc.model.DataViewer, id: csc.model.ObjectId, name: str) -> csc.model.SettingId`
  - id : csc.model.ObjectId | name : string | -> csc.model.DataId

- `get_setting_name(self: csc.model.DataViewer, arg0: csc.model.SettingId) -> str`
  - id : csc.model.SettingId | -> string

- `get_setting_value(*args, **kwargs)`
  - Overloaded function.
  - `get_setting_value(self: csc.model.DataViewer, id: csc.model.SettingId) -> Union[bool, int]`
    - id : csc.model.SettingId | -> Setting.Value
  - `get_setting_value(self: csc.model.DataViewer, setting_id: csc.model.SettingId, position: int) -> Union[bool, int]`
    - id : csc.model.SettingId, position : int | -> Setting.Value

- `has_data(self: csc.model.DataViewer, arg0: csc.model.DataId) -> bool`
  - id : csc.model.DataId | -> bool

- `has_setting(self: csc.model.DataViewer, arg0: csc.model.SettingId) -> bool`
  - id : csc.model.SettingId | -> bool

- `union_get_data_value(self: csc.model.DataViewer, data_id: csc.model.DataId, frame: int = 0) -> bool | int | float | numpy.ndarray[numpy.float32[3, 1]] | numpy.ndarray[numpy.float32[4, 1]] | csc.math.Rotation | numpy.ndarray[numpy.float32[3, 3]] | numpy.ndarray[numpy.float32[4, 4]] | csc.math.Quaternion | str | numpy.ndarray[bool[3, 1]]`
  - id : csc.model.DataId | -> Data.Value
