# csc.math.SizesInterval

> 公式: https://cascadeur.com/python-api/_generate/csc.math.SizesInterval.html

Implements the sizes interval basic methods

## Methods

- `__init__(*args, **kwargs)` → None
  - Overloaded function.
  - `__init__(self: csc.math.SizesInterval) -> None`
  - `__init__(self: csc.math.SizesInterval, start: int, end: int) -> None`

- `construct_in_right_order(first: int, second: int)` → csc.math.SizesInterval
  - Static method

- `contains(self: csc.math.SizesInterval, i: int)` → bool

- `empty(self: csc.math.SizesInterval)` → bool

- `end(self: csc.math.SizesInterval)` → int

- `inside_interval_inclusive(self: csc.math.SizesInterval, number: int)` → bool

- `intersect_intervals(first: csc.math.SizesInterval, second: csc.math.SizesInterval)` → csc.math.SizesInterval
  - Static method

- `safe_construct(first: int, second: int)` → csc.math.SizesInterval
  - Static method

- `start(self: csc.math.SizesInterval)` → int

- `union_overlaping_intervals(first: csc.math.SizesInterval, second: csc.math.SizesInterval)` → csc.math.SizesInterval
  - Static method

## Attributes

- `__annotations__` = {}
- `__module__` = 'csc.math'
- `__hash__` = None
