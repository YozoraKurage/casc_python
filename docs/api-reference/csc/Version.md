# csc.Version

> 公式: https://cascadeur.com/python-api/_generate/csc.Version.html

Version class that implements version management with major, minor, and patch components.

## Properties

- **major**: Get/set int
- **minor**: Get/set int
- **patch**: Get/set int

## Methods

- `__init__(self: csc.Version, major: int, minor: int, patch: int) → None`
  - Initialize a Version object with major, minor, and patch numbers

- `from_string(arg0: str) → csc.Version`
  - Create a Version object from a string representation
  - Parameters: **version** (str) – The version string
  - Returns: The Version object

- `to_string(self: csc.Version) → str`
  - Get the string representation of the version
  - Returns: The string representation of the version

- `__eq__(self: csc.Version, arg0: csc.Version) → bool`
  - Equality comparison between Version objects

- `__ne__(self: csc.Version, arg0: csc.Version) → bool`
  - Inequality comparison between Version objects

- `__lt__(self: csc.Version, arg0: csc.Version) → bool`
  - Less-than comparison between Version objects

- `__cmp__(self: csc.Version, arg0: csc.Version) → int`
  - Compare two Version objects

## Example

```python
import csc
version = csc.Version.from_string("4.2.1")
print(version.major)
print(version.minor)
print(version.patch)
print(version.to_string())
```
