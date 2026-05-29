# csc.model.ModelEditor

> 公式: https://cascadeur.com/python-api/_generate/csc.model.ModelEditor.html

ModelEditor class

Represents basic methods to edit the scene model

`class csc.model.ModelEditor`

## Properties

- **add_object** — overridden method by GroupId -> csc.model.ObjectId

## Methods

- `add_object(*args, **kwargs)`
  - Overloaded function.
  - `add_object(self: csc.model.ModelEditor) -> csc.model.ObjectId`
  - `add_object(self: csc.model.ModelEditor, id: csc.model.ObjectId) -> csc.model.ObjectId`

- `behaviour_editor(self: csc.model.ModelEditor) -> csc.model.BehaviourEditor`
  - -> BehaviourEditor

- `data_editor(self: csc.model.ModelEditor) -> csc.model.DataEditor`
  - -> DataEditor

- `delete_objects(self: csc.model.ModelEditor, ids: set[csc.model.ObjectId], close_connections: bool = True) -> None`

- `fit_animation_size_by_layers(self: csc.model.ModelEditor) -> None`

- `get_viewer(self: csc.model.ModelEditor) -> csc.model.ModelViewer`

- `init_default_constants(self: csc.model.ModelEditor) -> None`

- `layers(self: csc.model.ModelEditor) -> object`
  - -> csc.layers.Layers

- `layers_editor(self: csc.model.ModelEditor) -> csc.layers.Editor`
  - -> csc.layers.Editor

- `layers_selector(self: csc.model.ModelEditor) -> object`
  - -> csc.layers.Selector

- `move_obj_ids_in_layers(self: csc.model.ModelEditor, objIds = csc.model.ObjectId[]: list[csc.model.ObjectId], layer_id: csc.Guid) -> None`

- `move_objects_to_layer(self: csc.model.ModelEditor, ids: list[csc.model.ObjectId], target_layer_id: csc.Guid) -> None`

- `set_fixed_interpolation_if_need(self: csc.model.ModelEditor, actuals: set[csc.model.DataId], frame: int, ignore_locked: bool = False) -> None`

- `set_object_name(self: csc.model.ModelEditor, id: csc.model.ObjectId, name: str) -> None`

- `set_object_type_name(self: csc.model.ModelEditor, id: csc.model.ObjectId, name: str) -> None`
