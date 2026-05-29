# csc.view.StandardButton

> 公式: https://cascadeur.com/python-api/_generate/csc.view.StandardButton.html

`class csc.view.StandardButton`

StandardButton enum

This enumerates the basic types of standard buttons. Ok, Cancel, Yes, No

```python
#This script showcases the use of StandardButton in a dialog
import csc
def run(scene):
    dialog_buttons = [csc.view.DialogButton(csc.view.StandardButton.Ok, lambda: scene.success('Pressed Ok')),
                      csc.view.DialogButton(csc.view.StandardButton.Yes, lambda: scene.success('Pressed Yes')),
                      csc.view.DialogButton(csc.view.StandardButton.No, lambda: scene.success('Pressed No')),
                      csc.view.DialogButton(csc.view.StandardButton.Cancel, lambda: scene.success('Pressed Cancel'))]

    csc.view.DialogManager.instance().show_buttons_dialog("Test dialog window", "Press anything", dialog_buttons)
```

## Members

- `Cancel` = 1
- `No` = 3
- `Ok` = 0
- `Yes` = 2

## Properties

- `name`
- `value`

## Methods

- `__init__(self: csc.view.StandardButton, value: int) -> None`
- `__eq__(self: object, other: object) -> bool`
- `__getstate__(self: object) -> int`
- `__hash__(self: object) -> int`
- `__index__(self: csc.view.StandardButton) -> int`
- `__int__(self: csc.view.StandardButton) -> int`
- `__ne__(self: object, other: object) -> bool`
- `__repr__(self: object) -> str`
- `__setstate__(self: csc.view.StandardButton, state: int) -> None`
- `__str__(self: object) -> str`
