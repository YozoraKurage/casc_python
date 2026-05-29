# csc.fbx.FbxSettings

> 公式: https://cascadeur.com/python-api/_generate/csc.fbx.FbxSettings.html

Class for configuring FBX import/export options.

## Properties

- **mode**: `csc.fbx.FbxSettingsMode` - The FBX type (Ascii or Binary)
- **up_axis**: `csc.fbx.FbxSettingsAxis` - The up axis (X, Y, or Z)
- **bake_animation**: `bool` - Whether to bake animation during export
- **apply_euler_filter**: `bool` - Whether to apply euler filter to exported animation

## Methods

- **`__init__(self: csc.fbx.FbxSettings) → None`** - Initialize FbxSettings

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
        settings.mode = fbx.FbxSettingsMode.Ascii
        # Turn on or off the euler filter being applied on the exported animation
        settings.apply_euler_filter = False
        # Set up the up axis (X, Y or Z)
        settings.up_axis = fbx.FbxSettingsAxis.Y

        scene_manager = app.get_scene_manager()
        tools_manager = app.get_tools_manager()
        current_scene = scene_manager.current_scene()

        fbx_scene_loader_tool = tools_manager.get_tool("FbxSceneLoader")
        fbx_scene_loader = fbx_scene_loader_tool.get_fbx_loader(current_scene)
        fbx_scene_loader.set_settings(settings)
        fbx_scene_loader.export_all_objects(file_name)

        fd_m.show_save_file_dialog("Choose filename fbx", "", ["*.fbx"], export_scene)
```
