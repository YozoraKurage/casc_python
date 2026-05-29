# csc.view.DialogManager

> 公式: https://cascadeur.com/python-api/_generate/csc.view.DialogManager.html

`class csc.view.DialogManager`

DialogManager class

```python
import csc
 def run(scene):
     def callback_button():
         def input_callback(input_values):
             values = ''.join(input_values)
             csc.view.DialogManager.instance().show_info("Input values", values)

         input_field_count = 5
         input_field_names = ["f1", "f2", "f3"]
         input_field_fills = ["v1", "v2", "v3", "v4"]
         csc.view.DialogManager.instance().show_inputs_dialog("Test1", input_field_names, input_field_fills,
                                                              input_field_count, input_callback)

     dialog_buttons = [csc.view.DialogButton('ButtonName', callback_button),
                       csc.view.DialogButton(csc.view.StandardButton.Cancel)]

     csc.view.DialogManager.instance().show_buttons_dialog("Test dialog window", "Press anything", dialog_buttons)
```

## Methods

- `__init__(*args, **kwargs)`
- `static instance() -> object`
  - Returns the instance of the dialog manager
  - Returns: The instance of the dialog manager
  - Return type: csc.view.DialogManager
- `show_buttons_dialog(self: csc.view.DialogManager, arg0: str, arg1: str, arg2: list[csc.view.DialogButton]) -> None`
  - Shows a dialog with buttons
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (str) – The text of the dialog
  - Parameter: arg2 (List[csc.view.DialogButton]) – The list of buttons to show
- `show_info(self: csc.view.DialogManager, arg0: str, arg1: str) -> None`
  - Shows an info dialog
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (str) – The text of the dialog
- `show_input_dialog(*args, **kwargs)`
  - Overloaded function.
  - `show_input_dialog(self: csc.view.DialogManager, arg0: str, arg1: str, arg2: str, arg3: Callable) -> None`
  - Shows an input dialog
  - arg0 (str) : The title of the dialog arg1 (str) : The text of the dialog arg2 (str) : The hint of the dialog arg3 (Callable[List[str]]) : The handler of the dialog
  - `show_input_dialog(self: csc.view.DialogManager, arg0: str, arg1: str, arg2: str, arg3: Callable, arg4: Callable) -> None`
  - Shows an input dialog
  - arg0 (str) : The title of the dialog arg1 (str) : The text of the dialog arg2 (str) : The hint of the dialog arg3 (Callable[List[str]]) : The handler of the dialog arg4 (Callable[List[str]]) : The validator of the dialog
- `show_inputs_dialog(self: csc.view.DialogManager, arg0: str, arg1: list[str], arg2: list[str], arg3: int, arg4: Callable) -> None`
  - Shows an input dialog
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (List[str]) – The list of texts of the dialog
  - Parameter: arg2 (List[str]) – The list of hints of the dialog
  - Parameter: arg3 (int) – The size of the dialog
  - Parameter: arg4 (Callable[List[str]]) – The handler of the dialog
- `show_styled_buttons_dialog(self: csc.view.DialogManager, arg0: str, arg1: str, arg2: list[csc.view.DialogButton]) -> None`
  - Shows a dialog with styled buttons
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (str) – The text of the dialog
  - Parameter: arg2 (List[csc.view.DialogButton]) – The list of buttons to show
