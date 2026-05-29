# csc.math.inverse_transform_point

> 公式: https://cascadeur.com/python-api/_generate/csc.math.inverse_transform_point.html

Applies the inverse transformation to a point using an orthogonal transform.

## Function

```python
csc.math.inverse_transform_point(transform: math::OrthogonalTransform, point: numpy.ndarray[numpy.float32[3, 1]]) → numpy.ndarray[numpy.float32[3, 1]]
```

- **transform**: An `OrthogonalTransform` object defining the inverse transformation
- **point**: A 3D point as a numpy array
- **Returns**: The transformed point as a `Vector3f`
