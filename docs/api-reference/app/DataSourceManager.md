# csc.app.DataSourceManager

> 公式: https://cascadeur.com/python-api/_generate/csc.app.DataSourceManager.html

`class csc.app.DataSourceManager`

DataSourceManager class. Represents the DataSourceManager class used for managing data sources and scenes within the application.

## Methods

- `__init__(*args, **kwargs)`
- `close_scene(self: csc.app.DataSourceManager, scene: csc.view.Scene) -> None`
  - Close scene
  - Parameter: scene (csc.view.Scene) – The scene to close
- `load_scene(self: csc.app.DataSourceManager, file_name: str) -> bool`
  - Load scene and all additional datas (selection groups etc) .. Example: .. code-block:: python
  - import csc ds_m = csc.app.get_application().get_data_source_manager() ds_m.load_scene(file_path)
- `save_current_scene(*args, **kwargs)`
  - Overloaded function.
  - `save_current_scene(self: csc.app.DataSourceManager, handler: Callable[[bool], None]) -> None`
  - Save current scene
  - handler (Callable[[bool], None]) : The handler
  - `save_current_scene(self: csc.app.DataSourceManager) -> None`
  - Save current scene
- `save_scene(*args, **kwargs)`
  - Overloaded function.
  - `save_scene(self: csc.app.DataSourceManager, scene_view: csc.view.Scene, handler: Callable[[bool], None]) -> None`
  - Save scene and all additional datas (selection groups etc)
  - scene_view (csc.view.Scene) : The scene to save handler (Callable[[bool], None]) : The handler
  - `save_scene(self: csc.app.DataSourceManager, scene_view: csc.view.Scene) -> None`
  - Save scene and all additional datas (selection groups etc)
  - scene_view (csc.view.Scene) : The scene to save
- `save_scene_as(self: csc.app.DataSourceManager, scene_view: csc.view.Scene, full_file_name: str) -> None`
  - Save scene as
  - Parameter: scene_view (csc.view.Scene) – The scene to save
  - Parameter: full_file_name (str) – The full file name
