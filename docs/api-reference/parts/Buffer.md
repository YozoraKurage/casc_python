# csc.parts.Buffer

> 公式: https://cascadeur.com/python-api/_generate/csc.parts.Buffer.html

Buffer class that provides methods to operate parts of the scene.

## Methods

- `__init__(*args, **kwargs)` - Constructor
- `get() → object` - Static method to get buffer instance
- `insert_elementary_by_id(self: csc.parts.Buffer, arg0: csc.model.ObjectId, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor) → csc.parts.GroupInfo` - Insert elementary part by object ID
- `insert_elementary_by_path(self: csc.parts.Buffer, arg0: str, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor) → csc.parts.GroupInfo` - Insert elementary part by path
- `insert_object_by_id(self: csc.parts.Buffer, arg0: csc.model.ObjectId, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor, arg3: csc.domain.assets.AssetsManager) → csc.model.ObjectId` - Insert object by ID
- `insert_object_by_path(self: csc.parts.Buffer, arg0: str, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor, arg3: csc.domain.assets.AssetsManager) → csc.model.ObjectId` - Insert object by path
- `insert_objects_by_id(self: csc.parts.Buffer, arg0: csc.model.ObjectId, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor, arg3: csc.domain.assets.AssetsManager) → tuple[set[csc.model.ObjectId], set[csc.update.GroupId]]` - Insert multiple objects by ID
- `insert_objects_by_path(self: csc.parts.Buffer, arg0: str, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor, arg3: csc.domain.assets.AssetsManager) → tuple[set[csc.model.ObjectId], set[csc.update.GroupId]]` - Insert multiple objects by path
- `insert_selected_objects_by_path(self: csc.parts.Buffer, arg0: str, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor, arg3: csc.domain.assets.AssetsManager) → set[csc.model.ObjectId]` - Insert selected objects by path
- `insert_update_group_by_id(self: csc.parts.Buffer, arg0: csc.model.ObjectId, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor) → tuple[csc.parts.GroupInfo, dict[csc.update.GroupId, csc.parts.GroupInfo]]` - Insert update group by ID
- `insert_update_group_by_path(self: csc.parts.Buffer, arg0: str, arg1: csc.update.GroupId, arg2: csc.model.ModelEditor) → tuple[csc.parts.GroupInfo, dict[csc.update.GroupId, csc.parts.GroupInfo]]` - Insert update group by path
- `refresh(self: csc.parts.Buffer) → None` - Refresh the buffer
