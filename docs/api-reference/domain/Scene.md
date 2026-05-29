# csc.domain.Scene

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.Scene.html

`class csc.domain.Scene`

Scene class

Root class that represents a scene and its methods for modifying or observing it.

Modify scene by func modify:

## Methods

- `__init__(self: csc.domain.Scene) -> None`
- `assets_manager(self: csc.domain.Scene) -> domain::scene::AssetsManager`
  - -> AssetsManager
- `behaviour_viewer(self: csc.domain.Scene) -> csc.model.BehaviourViewer`
  - -> csc.model.BehaviourViewer
- `data_viewer(self: csc.domain.Scene) -> csc.model.DataViewer`
  - -> csc.model.DataViewer
- `error(self: csc.domain.Scene, arg0: str) -> None`
- `get_current_frame(self: csc.domain.Scene, clamp_animation: bool = True) -> int`
- `get_event_log_or_null(self: csc.domain.Scene) -> object`
- `get_layers_selector(self: csc.domain.Scene) -> object`
  - -> csc.layers.Selector
- `info(self: csc.domain.Scene, arg0: str) -> None`
- `layers_viewer(self: csc.domain.Scene) -> csc.layers.Viewer`
  - -> csc.layers.Viewer
- `model_viewer(self: csc.domain.Scene) -> csc.model.ModelViewer`
  - -> csc.model.ModelViewer
- `modify(self: csc.domain.Scene, arg0: str, arg1: Callable) -> bool`
  - -> bool
- `modify_update(self: csc.domain.Scene, arg0: str, arg1: Callable) -> bool`
  - -> bool
- `modify_update_with_session(self: csc.domain.Scene, arg0: str, arg1: Callable) -> bool`
  - -> bool
- `modify_with_session(self: csc.domain.Scene, arg0: str, arg1: Callable) -> bool`
  - -> bool
- `selector(self: csc.domain.Scene) -> object`
  - -> Selector
- `set_current_frame(self: csc.domain.Scene, frame: int) -> None`
- `set_event_log(self: csc.domain.Scene, message_handler: csc.domain.IMessageHandler) -> None`
- `success(self: csc.domain.Scene, arg0: str) -> None`
- `warning(self: csc.domain.Scene, arg0: str) -> None`
