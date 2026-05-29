# csc.physics.inertia_tensor

> 公式: https://cascadeur.com/python-api/_generate/csc.physics.inertia_tensor.html

## Function

```python
inertia_tensor(mass_and_poses: list[csc.physics.PosMass], center: numpy.ndarray[numpy.float32[3, 1]]) → numpy.ndarray[numpy.float32[3, 3]]
```

Calculates the inertia tensor matrix from a list of mass positions and a center point.

- **mass_and_poses**: A list of `csc.physics.PosMass` objects containing mass and position data
- **center**: The center point as a 3x1 numpy float32 array
- **Returns**: A 3x3 numpy float32 array representing the inertia tensor (Matrix3f)
