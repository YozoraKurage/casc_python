# csc.math.Rotation

> 公式: https://cascadeur.com/python-api/_generate/csc.math.Rotation.html

Rotation class for Euler angles implementation.

## Methods

- `__init__(self: csc.math.Rotation) → None`
  - Constructor for Rotation object

- `__mul__(self: csc.math.Rotation, arg0: csc.math.Rotation) → csc.math.Rotation`
  - Multiplies two rotation objects

- `from_angle_axis(*args, **kwargs)` (static, overloaded)
  - `from_angle_axis(arg0: float, arg1: numpy.ndarray[numpy.float32[3, 1]]) -> csc.math.Rotation`
  - `from_angle_axis(arg0: csc.math.AngleAxis) -> csc.math.Rotation`
  - Creates rotation from angle and axis representation

- `from_euler(*args, **kwargs)` (static, overloaded)
  - `from_euler(x: float, y: float, z: float) -> csc.math.Rotation`
  - `from_euler(vec3f: numpy.ndarray[numpy.float32[3, 1]]) -> csc.math.Rotation`
  - Creates rotation from Euler angles

- `from_quaternion(*args, **kwargs)` (static, overloaded)
  - `from_quaternion(w: float, x: float, y: float, z: float) -> csc.math.Rotation`
  - `from_quaternion(quaternion: csc.math.Quaternion) -> csc.math.Rotation`
  - Creates rotation from quaternion representation

- `from_rotation_matrix(arg0: numpy.ndarray[numpy.float32[3, 3]]) → csc.math.Rotation` (static)
  - Creates rotation from a 3x3 rotation matrix

- `inverse(self: csc.math.Rotation) → csc.math.Rotation`
  - Returns the inverse rotation

- `to_angle_axis(self: csc.math.Rotation) → csc.math.AngleAxis`
  - Converts rotation to angle-axis representation

- `to_euler_angles(self: csc.math.Rotation) → numpy.ndarray[numpy.float32[3, 1]]`
  - Converts rotation to Euler angles

- `to_euler_angles_x_y_z(self: csc.math.Rotation) → numpy.ndarray[numpy.float32[3, 1]]`
  - Converts rotation to X-Y-Z Euler angles

- `to_quaternion(self: csc.math.Rotation) → csc.math.Quaternion`
  - Converts rotation to quaternion representation

- `to_rotation_matrix(self: csc.math.Rotation) → numpy.ndarray[numpy.float32[3, 3]]`
  - Converts rotation to a 3x3 rotation matrix
