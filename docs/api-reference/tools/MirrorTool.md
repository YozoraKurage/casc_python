# csc.tools.MirrorTool

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.MirrorTool.html

Mirror tool class. Represents the mirror tool class used to handle symmetry operations in Cascadeur.

## Methods

- **`__init__(*args, **kwargs)`**
  - Initializes the MirrorTool instance.

- **`core(self: csc.tools.MirrorTool) → object`**
  - Retrieves the core of the mirror tool.
  - Returns: The core of the mirror tool (csc.tools.mirror.Core)

## Example

```python
import csc
scene_manager = csc.app.get_application().get_scene_manager()
app_scene = scene_manager.current_scene()
mirror_tool = csc.app.get_application().get_tools_manager().get_tool('MirrorTool').editor(app_scene)
core = mirror_tool.core()
core.set_plane(csc.math.Plane([1.0, 0.0, 0.0], [0.0,0.0,0.0]))
```
