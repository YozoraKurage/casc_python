# csc.tools.RiggingModeTool

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.RiggingModeTool.html

Rigging mode tool class

## Methods

- `__init__(*args, **kwargs)` – Constructor for RiggingModeTool
- `erase_joints_data(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases joint data for the specified session
- `erase_layer_id_by_object_ids(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases layer ID mapped by object IDs for the specified session
- `erase_layers_ids(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases layer IDs for the specified session
- `erase_preserved_data(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases preserved data for the specified session
- `erase_preserved_object_ids(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases preserved object IDs for the specified session
- `erase_preserved_setting(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session) → None` – Erases preserved setting for the specified session
- `get_joints_data(self: csc.tools.RiggingModeTool) → dict[csc.model.ObjectId, list[csc.tools.JointData]]` – Retrieves joint data mapped by object ID
- `get_layer_id_by_object_ids(self: csc.tools.RiggingModeTool) → dict[csc.Guid, list[csc.model.ObjectId]]` – Retrieves layer ID mapped by object IDs
- `get_layers_ids(self: csc.tools.RiggingModeTool) → set[csc.Guid]` – Retrieves layer IDs as a set of GUIDs
- `get_preserved_data(self: csc.tools.RiggingModeTool) → dict[csc.tools.DataKey, list[...]]` – Retrieves preserved data stored in a dictionary structure
- `get_preserved_object_ids(self: csc.tools.RiggingModeTool) → dict[csc.model.PathName, csc.model.ObjectId]` – Retrieves preserved object IDs stored in a set
- `get_preserved_setting(self: csc.tools.RiggingModeTool) → dict[csc.tools.DataKey, list[bool | int]]` – Retrieves preserved setting stored in a dictionary structure
- `set_joints_data(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: dict[csc.model.ObjectId, list[csc.tools.JointData]]) → None` – Sets joint data for the specified session
- `set_layers_ids(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: set[csc.Guid]) → None` – Sets layer IDs for the specified session
- `set_preserved_data(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: dict[csc.tools.DataKey, list[...]]) → None` – Sets preserved data for the specified session
- `set_preserved_object_ids(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: dict[csc.model.PathName, csc.model.ObjectId]) → None` – Sets preserved object IDs for the specified session
- `set_preserved_setting(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: dict[csc.tools.DataKey, list[bool | int]]) → None` – Sets preserved setting for the specified session
- `set_undo_redo_context(self: csc.tools.RiggingModeTool, arg0: csc.domain.Session, arg1: Callable, arg2: object, arg3: object) → None` – Sets undo and redo context for the specified session
