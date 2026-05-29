# csc.DirectionValue

> 公式: https://cascadeur.com/python-api/_generate/csc.DirectionValue.html

DirectionValue enumeration. Represents a DirectionValue enumeration for defining In, Out, and Unknown directions.

## Members

- `In` = 0
- `Out` = 1
- `Unknown` = 2

## Methods

- `__init__(self, value: int) -> None`
- `__eq__(self, other: object) -> bool`
- `__getstate__(self) -> int`
- `__hash__(self) -> int`
- `__index__(self) -> int`
- `__int__(self) -> int`
- `__ne__(self, other: object) -> bool`
- `__repr__(self) -> str`
- `__setstate__(self, state: int) -> None`
- `__str__(self) -> str`

## Properties

- `name`
- `value`

## Example

```python
import csc
print(csc.DirectionValue.In)
print(csc.DirectionValue.In.value)
```
