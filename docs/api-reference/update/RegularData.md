# csc.update.RegularData

> 公式: https://cascadeur.com/python-api/_generate/csc.update.RegularData.html

RegularData class represents a node of a data.

`class csc.update.RegularData`

## Properties

- `value`
  - overridden method by frame, get data value (requires frame if Animation data)
- `set_value`
  - overridden method by frame, set data value (requires frame if Animation data)

## Methods

- `actuality(self: csc.update.RegularData) → csc.update.ActualityAttribute`
  - output attribute, that provides actuality status
- `attribute(self: csc.update.RegularData, d: csc.Direction) → csc.update.RegularDataAttribute`
  - get attribute by direction
- `data_id(self: csc.update.RegularData) → csc.model.DataId`
- `get_apply_euler_filter(self: csc.update.RegularData) → bool`
  - get apply euler filter
- `get_explicit_linear(self: csc.update.RegularData) → bool`
  - get explicit linear
- `get_lerp_mode(self: csc.update.RegularData) → csc.model.LerpMode`
  - get lerp mode
- `get_period(self: csc.update.RegularData) → float | None`
  - in interpolation, get period
- `input(self: csc.update.RegularData) → csc.update.RegularDataAttribute`
  - input attribute
- `is_actual(self: csc.update.RegularData) → bool`
  - check if this data is set to actual (see Additional functionality in csc.update.UpdateEditor)
- `mode(self: csc.update.RegularData) → csc.model.DataMode`
  - Check if data is Animation or Static
- `output(self: csc.update.RegularData) → csc.update.RegularDataAttribute`
  - output attribute
- `remove_period(self: csc.update.RegularData) → None`
  - in interpolation, remove period
- `set_actual(self: csc.update.RegularData, act: bool) → None`
  - set this data as actual (see Additional functionality in csc.update.UpdateEditor)
- `set_apply_euler_filter(self: csc.update.RegularData, apply_euler_filter: bool) → None`
  - set apply euler filter
- `set_description_value(self: csc.update.RegularData, name: str) → None`
  - setDescriptionValue
- `set_explicit_linear(self: csc.update.RegularData, explicit_linear: bool) → None`
  - set explicit linear
- `set_lerp_mode(self: csc.update.RegularData, mode: csc.model.LerpMode) → None`
  - can be slerp for Vector3 datas. Used in interpolation
- `set_period(self: csc.update.RegularData, period: float) → None`
  - in interpolation, if perion is provided, the data will be “fixed” to provide smoothness
- `set_value`
  - Overloaded function.
  - `set_value(self: csc.update.RegularData, v: Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]) -> None`
  - `set_value(self: csc.update.RegularData, v: Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]], frame: int) -> None`
- `value`
  - Overloaded function.
  - `value(self: csc.update.RegularData) -> Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]`
  - `value(self: csc.update.RegularData, frame: int) -> Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]`
