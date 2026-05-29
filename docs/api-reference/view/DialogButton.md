# csc.view.DialogButton

> 公式: https://cascadeur.com/python-api/_generate/csc.view.DialogButton.html

`class csc.view.DialogButton`

DialogButton class

## Methods

- `__init__(*args, **kwargs)`
  - Overloaded function.
  - `__init__(self: csc.view.DialogButton) -> None`
  - `__init__(self: csc.view.DialogButton, arg0: str) -> None`
  - `__init__(self: csc.view.DialogButton, text: str, handler: Callable, force_active_focus: bool = False, accent: bool = False) -> None`
  - `__init__(self: csc.view.DialogButton, arg0: csc.view.StandardButton) -> None`
  - `__init__(self: csc.view.DialogButton, button: csc.view.StandardButton, handler: Callable, force_active_focus: bool = False, accent: bool = False) -> None`
- `force_active_focus(self: csc.view.DialogButton) -> bool`
  - Returns whether the button should force active focus
  - Returns: True if the button should force active focus, False otherwise
  - Return type: bool
- `text(self: csc.view.DialogButton) -> str`
  - Returns the text of the button
  - Returns: The text of the button
  - Return type: str
