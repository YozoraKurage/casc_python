# csc.math.Quaternion

> 公式: https://cascadeur.com/python-api/_generate/csc.math.Quaternion.html

Quaternion class useful to calculate rotation operations.

## Methods

- `__init__(self: csc.math.Quaternion, w: float, x: float, y: float, z: float) → None`
  - Constructor for Quaternion with w, x, y, z components

- `__mul__(*args, **kwargs)`
  - Overloaded multiplication operator
    - `__mul__(self: csc.math.Quaternion, arg0: csc.math.Quaternion) → csc.math.Quaternion` - Quaternion multiplication
    - `__mul__(self: csc.math.Quaternion, arg0: numpy.ndarray[numpy.float32[3, 1]]) → numpy.ndarray[numpy.float32[3, 1]]` - Vector rotation

- `from_two_vectors(arg0: numpy.ndarray[numpy.float32[3, 1]], arg1: numpy.ndarray[numpy.float32[3, 1]]) → csc.math.Quaternion` (static)
  - Creates a quaternion from two vectors

- `identity() → csc.math.Quaternion` (static)
  - Returns identity quaternion

- `inverse(self: csc.math.Quaternion) → csc.math.Quaternion`
  - Returns inverse of quaternion

- `w(self: csc.math.Quaternion) → float`
  - Returns w component

- `x(self: csc.math.Quaternion) → float`
  - Returns x component

- `y(self: csc.math.Quaternion) → float`
  - Returns y component

- `z(self: csc.math.Quaternion) → float`
  - Returns z component
