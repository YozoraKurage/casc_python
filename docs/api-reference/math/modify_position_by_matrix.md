# csc.math.modify_position_by_matrix

> 公式: https://cascadeur.com/python-api/_generate/csc.math.modify_position_by_matrix.html

Applies a 3x3 matrix transformation to a 3D position vector.

## Function

`modify_position_by_matrix(matrix: numpy.ndarray[numpy.float32[3, 3]], position: numpy.ndarray[numpy.float32[3, 1]]) → numpy.ndarray[numpy.float32[3, 1]]`

- **matrix**: A 3x3 float32 transformation matrix
- **position**: A 3D position vector as a float32 array
- **Returns**: The transformed position vector (Vector3f)
