# csc.view.Camera

> 公式: https://cascadeur.com/python-api/_generate/csc.view.Camera.html

`class csc.view.Camera`

Represents a spherical camera class in the view domain.

## Methods

- `__init__(*args, **kwargs)`
- `set_target(self: csc.view.Camera, arg0: numpy.ndarray[numpy.float32[3, 1]]) -> None`
  - Sets the camera target to a specified point.
  - Parameter: arg0 (numpy.ndarray[numpy.float32[3,1]]) – The target point to set the camera to.
- `zoom_to_points(self: csc.view.Camera, arg0: list[numpy.ndarray[numpy.float32[3, 1]]]) -> None`
  - Zooms the camera to a specified set of points.
  - Args: arg0 (numpy.ndarray[numpy.float32[3,1]]) : The set of points to zoom the camera to.
