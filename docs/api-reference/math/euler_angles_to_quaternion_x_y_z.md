# csc.math.euler_angles_to_quaternion_x_y_z

> 公式: https://cascadeur.com/python-api/_generate/csc.math.euler_angles_to_quaternion_x_y_z.html

Converts Euler angles to a quaternion representation.

## Function

```python
euler_angles_to_quaternion_x_y_z(euler_angles: numpy.ndarray[numpy.float32[3, 1]]) → csc.math.Quaternion
```

- **Parameters:**
  - `euler_angles`: A 3x1 numpy array of float32 values representing rotations around X, Y, and Z axes
- **Returns:** A `csc.math.Quaternion` object representing the equivalent rotation
