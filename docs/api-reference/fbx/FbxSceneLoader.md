# csc.fbx.FbxSceneLoader

> 公式: https://cascadeur.com/python-api/_generate/csc.fbx.FbxSceneLoader.html

Provides methods to import and export FBX scenes.

## Methods

- **`__init__(*args, **kwargs)`**
  - Initializes the FbxSceneLoader instance

- **`editor(self, arg0)`**
  - Get the editor of the tool

- **`export_fbx_scene(self, scene: csc.view.Scene, file_name: str) → None`**
  - Exports the scene to the specified file
  - **Parameters:**
    - `scene`: The scene
    - `file_name`: The name of the file to export the scene to

- **`get_fbx_loader(self, scene: csc.view.Scene) → csc.fbx.FbxLoader`**
  - Gets the FbxLoader
  - **Parameters:**
    - `scene`: The scene
  - **Returns:** csc.fbx.FbxLoader

- **`import_fbx_animation(self, scene: csc.view.Scene, file_name: str) → None`**
  - Imports the animation from the specified file
  - **Parameters:**
    - `scene`: The scene
    - `file_name`: The name of the file to import the animation from

- **`import_fbx_scene(self, scene: csc.view.Scene, file_name: str) → None`**
  - Imports the scene from the specified file
  - **Parameters:**
    - `scene`: The scene
    - `file_name`: The name of the file to import the scene from

- **`name(self)`**
  - Get the name of the tool

## Example

```python
import csc

def run(scene):
    app = csc.app.get_application()
    scene_manager = app.get_scene_manager()
    tools_manager = app.get_tools_manager()
    current_scene = scene_manager.current_scene()
    fbx_scene_loader_tool = tools_manager.get_tool("FbxSceneLoader")
    fbx_scene_loader = fbx_scene_loader_tool.get_fbx_loader(current_scene)
```
