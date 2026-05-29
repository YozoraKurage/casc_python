# csc.app.ProjectLoader

> 公式: https://cascadeur.com/python-api/_generate/csc.app.ProjectLoader.html

`class csc.app.ProjectLoader`

ProjectLoader class

Provides methods to load domain scene.

## Methods

- `__init__(*args, **kwargs)`
- `static load_from(arg0: str, arg1: csc.domain.Scene) -> None`
  - Minimal Load. This method doesn’t load selection groups, control picker and etc. Better use data_source_manager’s load_scene method.
  - Parameter: file_path (str) – The path to the file to load
  - Parameter: scene (csc.domain.Scene) – The scene to load the file into

    ```python
    import csc
    csc.app.ProjectLoader.load_from(file_path, scene)
    ```
