# csc.tools.selection.Core

> 公式: https://cascadeur.com/python-api/_generate/csc.tools.selection.Core.html

Core class for selection handling in Cascadeur.

## Methods

- `__init__(*args, **kwargs)` - Initialize the Core instance
- `get_group(self: csc.tools.selection.Core, idx: int) → csc.tools.selection.Group` - Retrieve a selection group by index
- `get_groups(self: csc.tools.selection.Core) → dict[int, csc.tools.selection.Group]` - Retrieve all selection groups as a dictionary mapping group indices to Group objects
- `process(self: csc.tools.selection.Core, index: int, mode: csc.tools.selection.Mode) → None` - Process a selection action with the specified index and mode
- `set_group(self: csc.tools.selection.Core, index: int, group: csc.tools.selection.Group) → None` - Set a selection group at the specified index
- `set_groups(self: csc.tools.selection.Core, groups: dict[int, csc.tools.selection.Group]) → None` - Set multiple selection groups from a dictionary
