# csc.view.Scene

> 公式: https://cascadeur.com/python-api/_generate/csc.view.Scene.html

`class csc.view.Scene`

SceneView class

## Methods

- `__init__(*args, **kwargs)`
- `active_viewport(self: csc.view.Scene) -> object`
  - Returns active csc.view.Viewport
  - Returns: Active csc.view.Viewport
  - Return type: csc.view.Viewport
- `animation_boundary(self: csc.view.Scene) -> object`
  - -> csc.view.AnimationBoundary
- `domain_scene(self: csc.view.Scene) -> object`
  - Return current csc.domain.Scene
  - Returns: Current csc.domain.Scene
  - Return type: csc.domain.Scene
- `get_setting_handler(self: csc.view.Scene) -> object`
- `gravity_per_frame(self: csc.view.Scene) -> float`
- `name(self: csc.view.Scene) -> str`
- `save(self: csc.view.Scene, path_name: str) -> None`
  - Save scene to file
  - Parameter: path_name (str) – The path to save the scene
- `viewports(self: csc.view.Scene) -> list[object]`
  - Provides all of csc.view.Viewport objects
  - Returns: List of csc.view.Viewport objects
  - Return type: List[csc.view.Viewport]
