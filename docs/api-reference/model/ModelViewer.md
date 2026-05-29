# csc.model.ModelViewer

> 公式: https://cascadeur.com/python-api/_generate/csc.model.ModelViewer.html

ModelViewer class

Represents basic methods to view the scene model

`class csc.model.ModelViewer`

## Properties

- **get_objects** — overridden method by string -> csc.model.ObjectId[]

## Methods

- `behaviour_viewer(self: csc.model.ModelViewer) -> csc.model.BehaviourViewer`
  - -> BehaviourViewer

- `data_viewer(self: csc.model.ModelViewer) -> csc.model.DataViewer`
  - -> DataViewer

- `get_object_name(self: csc.model.ModelViewer, id: csc.model.ObjectId) -> str`

- `get_object_type_name(self: csc.model.ModelViewer, id: csc.model.ObjectId) -> str`

- `get_objects(*args, **kwargs)`
  - Overloaded function.
  - `get_objects(self: csc.model.ModelViewer) -> list[csc.model.ObjectId]`
  - `get_objects(self: csc.model.ModelViewer, name: str) -> list[csc.model.ObjectId]`
