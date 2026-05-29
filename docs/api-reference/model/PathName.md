# csc.model.PathName

> 公式: https://cascadeur.com/python-api/_generate/csc.model.PathName.html

`class csc.model.PathName`

## Properties

- **name** — Get Set string
- **path** — Get Set string[]

## Methods

- `__init__(*args, **kwargs)`
  - Overloaded function.
  - `__init__(self: csc.model.PathName) -> None`
    - PathName class
    - Implements a hierarchical name
  - `__init__(self: csc.model.PathName, arg0: str, arg1: list[str]) -> None`
    - PathName class
    - Implements a hierarchical name
    - Get Set string
    - Get Set string[]

- `clear(self: csc.model.PathName) -> None`

- `empty(self: csc.model.PathName) -> bool`

- `full_path(self: csc.model.PathName) -> list[str]`

- `get_namespace(self: csc.model.PathName) -> str`

- `static get_object_path_name(obj_id: csc.model.ObjectId, mv: domain::scene::model::ModelViewer) -> csc.model.PathName`

- `static get_path_name(obj_id: csc.model.ObjectId, mv: domain::scene::model::ModelViewer, beh_name: str = 'Joint') -> csc.model.PathName`

- `static get_path_names(arg0: dict[str, str]) -> dict[str, csc.model.PathName]`

- `static get_path_names_by_behavior(arg0: str, arg1: domain::scene::model::ModelViewer) -> dict[csc.model.PathName, csc.model.ObjectId]`

- `static get_path_names_for_objects(arg0: set[csc.model.ObjectId], arg1: domain::scene::model::ModelViewer) -> dict[csc.model.PathName, csc.model.ObjectId]`

- `set_namespace(self: csc.model.PathName, namespace: str) -> None`

- `to_string(self: csc.model.PathName) -> str`
