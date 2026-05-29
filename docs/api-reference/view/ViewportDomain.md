# csc.view.ViewportDomain

> 公式: https://cascadeur.com/python-api/_generate/csc.view.ViewportDomain.html

`class csc.view.ViewportDomain`

Domain Viewport class. Represents the Domain ViewPort class that manages properties and functionalities of a viewport in the scene.

Args: camera_struct (csc.view.SphericalCameraStruct) : The camera structure associated with the viewport.

## Methods

- `__init__(*args, **kwargs)`
- `camera(self: csc.view.ViewportDomain) -> object`
  - Get the camera associated with the viewport.
  - Returns: The camera associated with the viewport.
  - Return type: csc.view.Camera
- `camera_struct(self: csc.view.ViewportDomain) -> csc.view.SphericalCameraStruct`
  - Get the camera structure associated with the viewport.
  - Returns: The camera structure associated with the viewport.
  - Return type: csc.view.SphericalCameraStruct
- `id(self: csc.view.ViewportDomain) -> csc.Guid`
  - Get the ID of the viewport.
  - Returns: The ID of the viewport.
  - Return type: csc.Guid
- `is_main(self: csc.view.ViewportDomain) -> bool`
- `mode_visualizers(self: csc.view.ViewportDomain) -> csc.view.ViewportMode`
  - Get the mode visualizers of the viewport.
  - Returns: The mode visualizers of the viewport.
  - Return type: csc.view.ViewportMode
- `set_camera_struct(self: csc.view.ViewportDomain, camera_struct: csc.view.SphericalCameraStruct) -> None`
  - Set the camera structure associated with the viewport.
  - Parameter: arg0 (csc.view.SphericalCameraStruct) – The camera structure to set.
- `set_mode_visualizers(self: csc.view.ViewportDomain, mode: csc.view.ViewportMode) -> None`
  - Set the mode visualizers of the viewport.
  - Parameter: arg0 (csc.view.ViewportMode) – The mode visualizers to set.
