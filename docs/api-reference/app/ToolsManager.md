# csc.app.ToolsManager

> 公式: https://cascadeur.com/python-api/_generate/csc.app.ToolsManager.html

`class csc.app.ToolsManager`

ToolsManager class provides access to various tools within the application.

```python
# This script gets the FbxSceneLoader tool
import csc

def run(scene):
    app = csc.app.get_application()
    tools_manager = app.get_tools_manager()
    # Get specified tool object
    tools_manager.get_tool("FbxSceneLoader")
```

## Methods

- `__init__(*args, **kwargs)`
- `get_tool(self: csc.app.ToolsManager, arg0: str) -> object`
  - Returns the specified tool based on its name.
  - Parameter: arg0 (str) – The name of the tool to get
  - Returns: The specified tool object
  - Return type: csc.app.CascadeurTool
- `tools(self: csc.app.ToolsManager) -> list[object]`
