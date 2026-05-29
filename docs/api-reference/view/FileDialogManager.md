# csc.view.FileDialogManager

> 公式: https://cascadeur.com/python-api/_generate/csc.view.FileDialogManager.html

`class csc.view.FileDialogManager`

FileDialogManager class

## Methods

- `__init__(*args, **kwargs)`
- `show_folder_dialog(self: csc.view.FileDialogManager, arg0: str, arg1: Callable) -> None`
  - Shows a folder dialog
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (Callable[List[str]]) – The handler of the dialog
- `show_open_file_dialog(self: csc.view.FileDialogManager, title: str, path: str, filters: list[str], handler: Callable) -> None`
  - Shows an open file dialog
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (str) – The path of the dialog
  - Parameter: arg2 (List[str]) – The list of filters of the dialog
  - Parameter: arg3 (Callable[List[str]]) – The handler of the dialog
- `show_save_file_dialog(self: csc.view.FileDialogManager, title: str, path: str, filters: list[str], handler: Callable) -> None`
  - Shows a save file dialog
  - Parameter: arg0 (str) – The title of the dialog
  - Parameter: arg1 (str) – The path of the dialog
  - Parameter: arg2 (List[str]) – The list of filters of the dialog
  - Parameter: arg3 (Callable[List[str]]) – The handler of the dialog
