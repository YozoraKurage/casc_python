# csc.app.Application

> 公式: https://cascadeur.com/python-api/_generate/csc.app.Application.html

`class csc.app.Application`

Application class. Represents the Application class that serves as the central point for accessing various managers and scene-related operations.

## Methods

- `__init__(*args, **kwargs)`
- `current_scene(self: csc.app.Application) -> object`
  - Get the current scene
  - Returns: The current scene
  - Return type: csc.view.Scene
- `get_action_manager(self: csc.app.Application) -> object`
  - Get the action manager
  - Returns: The action manager
  - Return type: csc.app.ActionManager
- `get_data_source_manager(self: csc.app.Application) -> object`
  - Get the data source manager
  - Returns: The data source manager
  - Return type: csc.app.DataSourceManager
- `get_file_dialog_manager(self: csc.app.Application) -> object`
- `get_scene_clipboard(self: csc.app.Application) -> object`
  - Get the scene clipboard
  - Returns: The scene clipboard
  - Return type: csc.view.SceneClipboard
- `get_scene_manager(self: csc.app.Application) -> object`
  - Get the scene manager
  - Returns: The scene manager
  - Return type: csc.app.SceneManager
- `get_setting_manager(self: csc.app.Application) -> object`
  - Get the settings manager
  - Returns: The settings manager
  - Return type: csc.app.SettingsManager
- `get_status_manager(self: csc.app.Application) -> object`
  - Get the status manager
  - Returns: The status manager
  - Return type: csc.app.StatusManager
- `get_tools_manager(self: csc.app.Application) -> object`
  - Get the tools manager
  - Returns: The tools manager
  - Return type: csc.app.ToolsManager
