# csc.fbx.FbxLoader

> 公式: https://cascadeur.com/python-api/_generate/csc.fbx.FbxLoader.html

FbxLoader class. Provides methods to import and export FBX files.

## Methods

- `__init__(self: csc.fbx.FbxLoader, fps: float, handler: csc.domain.IMessageHandler, scene: csc.view.Scene) → None`

- `add_model(self: csc.fbx.FbxLoader, file_name: csc.Path) → None`
  - Adds the model from the specified file.
  - Parameters: **file_name** (str) – The name of the file to add the model from

- `add_model_to_selected(self: csc.fbx.FbxLoader, file_name: csc.Path) → None`
  - Adds the model to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to add the model from

- `export_all_objects(self: csc.fbx.FbxLoader, file_name: csc.Path) → None`
  - Exports all objects to the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the objects to

- `export_joints(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the joints to the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the joints to

- `export_joints_selected(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the joints to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the joints to

- `export_joints_selected_frames(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the joints to the selected frames from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the joints to

- `export_joints_selected_objects(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the joints to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the joints to

- `export_model(self: csc.fbx.FbxLoader, file_name: csc.Path) → None`
  - Exports the model to the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the model to

- `export_scene_selected(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the scene to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the scene to

- `export_scene_selected_frames(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the scene to the selected frames from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the scene to

- `export_scene_selected_objects(self: csc.fbx.FbxLoader, file_name: str) → None`
  - Exports the scene to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to export the scene to

- `get_takes(self: csc.fbx.FbxLoader, file_name: csc.Path) → list[str]`
  - Get animation takes the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the animation from

- `import_animation(self: csc.fbx.FbxLoader, file_name: csc.Path, num_take: int = -1) → None`
  - Imports the animation from the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the animation from; **num_take** (int) – Take number from the list received from get_takes

- `import_animation_to_selected_frames(self: csc.fbx.FbxLoader, file_name: csc.Path, num_take: int = -1) → None`
  - Imports the animation to the selected frames from the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the animation from; **num_take** (int) – Take number from the list received from get_takes

- `import_animation_to_selected_objects(self: csc.fbx.FbxLoader, file_name: csc.Path, num_take: int = -1) → None`
  - Imports the animation to the selected objects from the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the animation from; **num_take** (int) – Take number from the list received from get_takes

- `import_model(self: csc.fbx.FbxLoader, file_name: csc.Path) → None`
  - Imports the model from the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the model from

- `import_scene(self: csc.fbx.FbxLoader, file_name: csc.Path, num_take: int = -1, is_set_offset: bool = True) → None`
  - Imports the scene from the specified file.
  - Parameters: **file_name** (str) – The name of the file to import the scene from; **num_take** (int) – Take number from the list received from get_takes

- `set_settings(self: csc.fbx.FbxLoader, settings: csc.fbx.FbxSettings) → None`
  - Sets the settings.
  - Parameters: **settings** (csc.fbx.FbxSettings) – The settings

## Examples

```python
# This script imports a specified FBX file into the current scene
import csc

def run(scene):
    app = csc.app.get_application()

    def import_scene(folder_path: str):
        file_ = folder_path.replace('\\', '/')
        scene_manager = app.get_scene_manager()
        tools_manager = app.get_tools_manager()
        # Get current scene tab
        current_scene = scene_manager.current_scene()
        # Get FbxSceneLoader tool
        fbx_scene_loader_tool = tools_manager.get_tool("FbxSceneLoader")
        # Get FbxLoader
        fbx_scene_loader = fbx_scene_loader_tool.get_fbx_loader(current_scene)
        # Import fbx file as a scene
        fbx_scene_loader.import_scene(file_)

    app.get_file_dialog_manager().show_open_file_dialog(
        "Select .fbx file", "", ["*.fbx"], import_scene
    )
```

```python
# This script imports animation data from the specified FBX file
import csc

def run(scene):
    app = csc.app.get_application()

    def import_animation(folder_path: str):
        file_ = folder_path.replace('\\', '/')
        scene_manager = app.get_scene_manager()
        tools_manager = app.get_tools_manager()
        # Get current scene tab
        current_scene = scene_manager.current_scene()
        # Get FbxSceneLoader tool
        fbx_scene_loader_tool = tools_manager.get_tool("FbxSceneLoader")
        # Get FbxLoader
        fbx_scene_loader = fbx_scene_loader_tool.get_fbx_loader(current_scene)
        # Import fbx file as a scene
        fbx_scene_loader.import_animation(file_)

    app.get_file_dialog_manager().show_open_file_dialog(
        "Select .fbx file", "", ["*.fbx"], import_animation
    )
```
