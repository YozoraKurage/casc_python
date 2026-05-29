# csc.update.RegularFunction

> 公式: https://cascadeur.com/python-api/_generate/csc.update.RegularFunction.html

RegularFunction class represents a node that calculates same operation, done with datas.

`class csc.update.RegularFunction`

## Methods

- `activity(self: csc.update.RegularFunction) → csc.update.ActivityAttribute`
  - activity attributes
- `arguments(self: csc.update.RegularFunction) → list[csc.update.RegularFunctionAttribute]`
  - its input arguments
- `decrease_vector(self: csc.update.RegularFunction, path: str, direction: csc.Direction) → None`
  - method that decreases vector attribute
- `func_id(self: csc.update.RegularFunction) → csc.model.HyperedgeId`
  - its id
- `increase_vector(self: csc.update.RegularFunction, path: str, direction: csc.Direction) → csc.update.RegularFunctionAttribute`
  - method that increases vector attribute
- `is_convertible(self: csc.update.RegularFunction) → bool`
  - check whether this function will make it to the resulting data graph
- `remove_attribute(self: csc.update.RegularFunction, attribute: csc.update.RegularFunctionAttribute) → None`
  - method that removes one in vector attribute
- `resize_vector_inputs(self: csc.update.RegularFunction, count: int, path: str) → None`
  - method that resizes input vector attribute
- `resize_vector_outputs(self: csc.update.RegularFunction, count: int, path: str) → None`
  - method that resizes output vector attribute
- `results(self: csc.update.RegularFunction) → list[csc.update.RegularFunctionAttribute]`
  - its output arguments
- `set_convertible(self: csc.update.RegularFunction, convertible: bool) → None`
  - set the state of the function, whether it will be used or not
- `type_name(self: csc.update.RegularFunction) → str`
  - function name
