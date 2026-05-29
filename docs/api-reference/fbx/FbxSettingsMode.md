# csc.fbx.FbxSettingsMode

> 公式: https://cascadeur.com/python-api/_generate/csc.fbx.FbxSettingsMode.html

Enumeration for FBX file format settings: Binary or Ascii mode.

## Members

- **Binary** = 0
- **Ascii** = 1

## Methods

- `__init__(self: csc.fbx.FbxSettingsMode, value: int) → None`
- `__eq__(self: object, other: object) → bool`
- `__getstate__(self: object) → int`
- `__hash__(self: object) → int`
- `__index__(self: csc.fbx.FbxSettingsMode) → int`
- `__int__(self: csc.fbx.FbxSettingsMode) → int`
- `__ne__(self: object, other: object) → bool`
- `__repr__(self: object) → str`
- `__setstate__(self: csc.fbx.FbxSettingsMode, state: int) → None`
- `__str__(self: object) → str`

## Properties

- `name`
- `value`

## Example

```python
import csc
from csc import fbx

def run(scene):
    app = csc.app.get_application()
    fd_m = app.get_file_dialog_manager()

    def export_scene(file_name):
        # Initialize FbxSettings
        settings = fbx.FbxSettings()
        # Set the Fbx type - Ascii or Binary
        settings.mode = fbx.FbxSettingsMode.Binary

        scene_manager = app.get_scene_manager()
        tools_manager = app.get_tools_manager()
        current_scene = scene_manager.current_scene()

        fbx_scene_loader_tool = tools_manager.get_tool("FbxSceneLoader")
        fbx_scene_loader = fbx_scene_loader_tool.get_fbx_loader(current_scene)
        fbx_scene_loader.set_settings(settings)
        fbx_scene_loader.export_all_objects(file_name)

    fd_m.show_save_file_dialog("Choose filename fbx", "", ["*.fbx"], export_scene)
```
