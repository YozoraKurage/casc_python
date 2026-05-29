# csc.math.transform_point

> 公式: https://cascadeur.com/python-api/_generate/csc.math.transform_point.html

Applies a geometric transformation to a 3D point.

## Overloads

1. `transform_point(transform: math::OrthogonalTransform, point: numpy.ndarray[numpy.float32[3, 1]]) -> numpy.ndarray[numpy.float32[3, 1]]`
   - Transforms a point using an orthogonal transformation

2. `transform_point(matrix: numpy.ndarray[numpy.float32[4, 4]], point: numpy.ndarray[numpy.float32[3, 1]]) -> numpy.ndarray[numpy.float32[3, 1]]`
   - Transforms a point using a 4x4 matrix
