# csc.tools.selection.Group

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.selection.Group.html

Group class for managing object selections with a pivot point.

## Properties

- **objects**: `std::set<ModelObjectId>` - Set of selected model object IDs
- **pivot**: `ModelObjectId` - The pivot object ID for the selection group

## Methods

- **`__init__()`** - Overloaded constructor
  - `__init__(self: csc.tools.selection.Group) -> None` - Creates an empty Group
  - `__init__(self: csc.tools.selection.Group, arg0: set[Union[csc.model.ObjectId, csc.domain.Tool_object_id]], arg1: Union[csc.model.ObjectId, csc.domain.Tool_object_id]) -> None` - Creates a Group with specified objects and pivot
