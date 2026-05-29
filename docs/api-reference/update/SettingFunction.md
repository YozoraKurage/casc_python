# csc.update.SettingFunction

> 公式: https://cascadeur.com/python-api/_generate/csc.update.SettingFunction.html

SettingFunction class

`class csc.update.SettingFunction`

## Methods

- `arguments(self: csc.update.SettingFunction) → list[csc.update.SettingFunctionAttribute]`
  - input attributes
- `decrease_input_vector(self: csc.update.SettingFunction, index: int) → None`
  - method that decreases input vector attribute
- `func_id(self: csc.update.SettingFunction) → csc.model.SettingFunctionId`
  - its id
- `increase_input_vector(self: csc.update.SettingFunction, index: int) → csc.update.SettingFunctionAttribute`
  - method that increases input vector attribute
- `is_convertible(self: csc.update.SettingFunction) → bool`
  - check whether this function will make it to the resulting setting graph
- `remove_attribute(self: csc.update.SettingFunction, attribute: csc.update.SettingFunctionAttribute) → None`
  - method that removes one in input vector attribute
- `resize_vector_inputs(self: csc.update.SettingFunction, index: int, count: int) → None`
  - method that resizes input vector attribute
- `results(self: csc.update.SettingFunction) → list[csc.update.SettingFunctionAttribute]`
  - output attributes
- `set_convertible(self: csc.update.SettingFunction, convertible: bool) → None`
  - set the state of the function, whether it will be used or not
- `type_name(self: csc.update.SettingFunction) → str`
  - function name
