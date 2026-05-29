# csc.app.SceneManager

> 公式: https://cascadeur.com/python-api/_generate/csc.app.SceneManager.html

`class csc.app.SceneManager`

SceneManager class. SceneManager class provides functionalities to manage scenes within the application.

## Methods

- `__init__(*args, **kwargs)`
- `create_application_scene(self: csc.app.SceneManager) -> object`
  - Create a new scene tab
  - Returns: The new scene tab
  - Return type: csc.view.Scene
- `current_scene(self: csc.app.SceneManager) -> object`
  - Get the current scene tab
  - Returns: The current scene tab
  - Return type: csc.view.Scene
- `remove_application_scene(self: csc.app.SceneManager, arg0: csc.view.Scene) -> None`
  - Close the specified scene tab
  - Parameter: arg0 (csc.view.Scene) – The scene tab to close
- `scenes(self: csc.app.SceneManager) -> list[object]`
  - Get a list of all scene tabs
  - Returns: The list of all scene tabs
  - Return type: List[csc.view.Scene]
- `set_current_scene(self: csc.app.SceneManager, arg0: csc.view.Scene) -> None`
  - Set the specified scene tab as active
  - Parameter: arg0 (csc.view.Scene) – The scene tab to set as active
