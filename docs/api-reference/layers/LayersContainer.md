# csc.layers.LayersContainer

> 公式: https://cascadeur.com/python-api/_generate/csc.layers.LayersContainer.html

`class csc.layers.LayersContainer`

LayersContainer class

It is the container of layers.

## Methods

- `at(self: csc.layers.LayersContainer, arg0: csc.Guid) -> object`
  - -> Layer
- `has_any_obj_ids(self: csc.layers.LayersContainer) -> bool`
- `has_obj_id(self: csc.layers.LayersContainer, id: common::GenericId<domain::scene::model::ModelObject>) -> bool`
- `layer_id_by_obj_id(self: csc.layers.LayersContainer, id: common::GenericId<domain::scene::model::ModelObject>) -> csc.Guid`
  - -> LayerId
- `layer_id_by_obj_id_or_null(self: csc.layers.LayersContainer, id: common::GenericId<domain::scene::model::ModelObject>) -> csc.Guid`
  - -> LayerId
- `map(self: csc.layers.LayersContainer) -> object`
  - -> <LayerId, Layer>{}
- `obj_ids(self: csc.layers.LayersContainer) -> object`
  - -> <csc.model.ObjectId, LayerId>{}
