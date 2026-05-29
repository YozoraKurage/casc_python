# csc.app.SettingsManager

> 公式: https://cascadeur.com/python-api/_generate/csc.app.SettingsManager.html

`class csc.app.SettingsManager`

SettingsManager class provides methods to get various settings values.

## Methods

- `__init__(*args, **kwargs)`
- `get_bool_value(self: csc.app.SettingsManager, arg0: str) -> bool`
  - Get the boolean value of the specified key
  - Parameter: arg0 (str) – The key to get the boolean value from
  - Returns: The boolean value of the specified key
  - Return type: bool
- `get_color_value(self: csc.app.SettingsManager, arg0: str) -> numpy.ndarray[numpy.float32[3, 1]]`
  - Get the color value of the specified key
  - Parameter: arg0 (str) – The key to get the color value from
  - Returns: The color value of the specified key
  - Return type: Tuple[float, float, float]
- `get_float_value(self: csc.app.SettingsManager, arg0: str) -> float`
  - Get the float value of the specified key
  - Parameter: key (str) – The key to get the float value from
  - Returns: The float value of the specified key
  - Return type: float
