# csc.Guid

> 公式: https://cascadeur.com/python-api/_generate/csc.Guid.html

A class for representing globally unique identifiers in Cascadeur.

## Methods

- `__init__(*args, **kwargs)` - Overloaded constructor. Can initialize from a string or create an empty Guid.
  - `__init__(self: csc.Guid, arg0: str) -> None`
  - `__init__(self: csc.Guid) -> None`

- `__eq__(self: csc.Guid, arg0: csc.Guid) -> bool` - Equality comparison between two Guid objects.

- `__ne__(self: csc.Guid, arg0: csc.Guid) -> bool` - Inequality comparison between two Guid objects.

- `__hash__(self: csc.Guid) -> int` - Returns hash value of the Guid.

- `__cmp__(self: csc.Guid, arg0: csc.Guid) -> int` - Comparison operation between two Guid objects.

- `__str__(self: csc.Guid) -> str` - Returns string representation of the Guid.

- `is_null(self: csc.Guid) -> bool` - Checks whether this Guid is null.

- `null() -> csc.Guid` - Static method that returns a null Guid.

- `to_string(self: csc.Guid) -> str` - Converts the Guid to its string representation.
