# csc.tools.AttractorTool

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.AttractorTool.html

Attractor tool class

## Methods

- **`__init__`**(*args, **kwargs)
  - Initializes the AttractorTool instance

- **`get_general_settings`**(self) → csc.tools.attractor.AttractorGeneralSettings
  - Retrieves the general settings of the attractor tool

- **`is_only_key_frames`**(self) → bool
  - Checks if the attractor tool is only operating on key frames
  - Returns: True if operating only on key frames, False otherwise

## Attributes

- **`__annotations__`** = {}
- **`__module__`** = 'csc.tools'

## Example

```python
import csc
scene_manager: csc.view.Scene = csc.app.get_application().get_scene_manager()
app_scene = scene_manager.current_scene()
attractor_tool = csc.app.get_application().get_tools_manager().get_tool('AttractorTool').editor(app_scene)
print(attractor_tool.is_only_key_frames())
```
