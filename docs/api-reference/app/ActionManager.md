# csc.app.ActionManager

> 公式: https://cascadeur.com/python-api/_generate/csc.app.ActionManager.html

`class csc.app.ActionManager`

ActionManager class Represents the ActionManager class that handles actions within the Cascadeur application.

## Methods

- `__init__(*args, **kwargs)`
- `call_action(self: csc.app.ActionManager, arg0: str) -> None`
  - Call action by key.
  - Parameter: key (str) – The key of the action to call.

    ```python
    #This script calls the specified action
    import csc

    def run(scene):
        mp = csc.app.get_application()
        mp.get_action_manager().call_action("Scene.Undo")
    ```
