# csc.Direction

> 公式: https://cascadeur.com/python-api/_generate/csc.Direction.html

Direction class Implements direction.

## Methods

- **`__init__(self: csc.Direction, value: csc.DirectionValue = <DirectionValue.Unknown: 2>) → None`**
  - Initializes a Direction instance with an optional DirectionValue parameter.

- **`inverse(self: csc.Direction) → csc.DirectionValue`**
  - Get the inverse direction.
  - Returns: The inverse direction.

- **`to_string(self: csc.Direction) → str`**
  - Get the string representation of the direction.
  - Returns: The string representation of the direction.

- **`value(self: csc.Direction) → csc.DirectionValue`**
  - Get the value of the direction.
  - Returns: The value of the direction.

## Examples

```python
import csc
d = csc.Direction(csc.DirectionValue.In)
print(d.inverse())
```

```python
import csc
d = csc.Direction(csc.DirectionValue.In)
print(d.value())
```
