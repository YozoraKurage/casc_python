# csc.model.BehaviourViewer

> 公式: https://cascadeur.com/python-api/_generate/csc.model.BehaviourViewer.html

BehaviourViewer class

This class allows viewing of scene behaviours and their properties.

`class csc.model.BehaviourViewer`

## Methods

- `behaviour_id(self: csc.model.BehaviourViewer, object_id: csc.model.ObjectId, behaviour_name: str) -> csc.model.BehaviourId`
  - objectId : csc.model.ObjectId | behaviour_name : string | -> csc.model.BehaviourId

- `get_behaviour_asset(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> common::GenericId<domain::scene::assets::Asset>`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.BehaviourId

- `get_behaviour_asset_range(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> list[common::GenericId<domain::scene::assets::Asset>]`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.BehaviourId[]

- `get_behaviour_by_name(self: csc.model.BehaviourViewer, object_id: csc.model.ObjectId, behaviour_name: str) -> csc.model.BehaviourId`
  - objectId : csc.model.ObjectId | behaviour_name : string | -> csc.model.BehaviourId

- `get_behaviour_data(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> csc.model.DataId`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.DataId

- `get_behaviour_data_range(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> list[csc.model.DataId]`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.DataId[]

- `get_behaviour_data_subtype(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviour_data_subtype(self: csc.model.BehaviourViewer, behaviour_name: str, property_name: str) -> str`
  - `get_behaviour_data_subtype(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, property_name: str) -> str`

- `get_behaviour_default_data_value(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviour_default_data_value(self: csc.model.BehaviourViewer, behaviour_name: str, property_name: str) -> Optional[Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]]`
  - `get_behaviour_default_data_value(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, property_name: str) -> Optional[Union[bool, int, float, numpy.ndarray[numpy.float32[3, 1]], numpy.ndarray[numpy.float32[4, 1]], csc.math.Rotation, numpy.ndarray[numpy.float32[3, 3]], numpy.ndarray[numpy.float32[4, 4]], csc.math.Quaternion, str, numpy.ndarray[bool[3, 1]]]]`

- `get_behaviour_default_setting_value(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviour_default_setting_value(self: csc.model.BehaviourViewer, behaviour_name: str, property_name: str) -> Optional[Union[bool, int]]`
  - `get_behaviour_default_setting_value(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, property_name: str) -> Optional[Union[bool, int]]`

- `get_behaviour_name(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId) -> str`
  - behaviour_id : csc.model.BehaviourId | -> string

- `get_behaviour_object(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> csc.model.ObjectId`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.ObjectId

- `get_behaviour_objects_range(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> list[csc.model.ObjectId]`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.ObjectId[]

- `get_behaviour_owner(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId) -> csc.model.ObjectId`
  - behaviour_id : csc.model.BehaviourId | -> csc.model.ObjectId

- `get_behaviour_property_names(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId) -> list[str]`
  - -> string[]

- `get_behaviour_reference(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> csc.model.BehaviourId`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.BehaviourId

- `get_behaviour_reference_range(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> list[csc.model.BehaviourId]`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.BehaviourId[]

- `get_behaviour_reference_subtype(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviour_reference_subtype(self: csc.model.BehaviourViewer, behaviour_name: str, property_name: str) -> str`
  - `get_behaviour_reference_subtype(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, property_name: str) -> str`

- `get_behaviour_setting(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> csc.model.SettingId`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.SettingId

- `get_behaviour_setting_subtype(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviour_setting_subtype(self: csc.model.BehaviourViewer, behaviour_name: str, property_name: str) -> str`
  - `get_behaviour_setting_subtype(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, property_name: str) -> str`

- `get_behaviour_settings_range(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> list[csc.model.SettingId]`
  - behaviour_id : csc.model.BehaviourId | name : string | -> csc.model.SettingId[]

- `get_behaviour_string(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> str`
  - behaviour_id : csc.model.BehaviourId | name : string | -> string

- `get_behaviours(*args, **kwargs)`
  - Overloaded function.
  - `get_behaviours(self: csc.model.BehaviourViewer, type_name: str) -> list[csc.model.BehaviourId]`
    - typeName : string | -> csc.model.BehaviourId[]
  - `get_behaviours(self: csc.model.BehaviourViewer, object_id: csc.model.ObjectId) -> list[csc.model.BehaviourId]`
    - objectId : csc.model.ObjectId | -> csc.model.BehaviourId[]

- `get_behaviours_by_name(self: csc.model.BehaviourViewer, object_id: csc.model.ObjectId, behaviour_name: str) -> list[csc.model.BehaviourId]`
  - objectId : csc.model.ObjectId | behaviour_name : string | -> csc.model.BehaviourId[]

- `get_children(self: csc.model.BehaviourViewer, object_id: csc.model.ObjectId) -> list[csc.model.BehaviourId]`
  - -> Children behs ids

- `get_property_type(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId, name: str) -> csc.model.PropertyType`
  - behaviour_id : csc.model.BehaviourId | name : string | -> Type[]

- `is_hidden(self: csc.model.BehaviourViewer, behaviour_id: csc.model.BehaviourId) -> bool`
  - -> bool

- `is_valid_behaviour_type(self: csc.model.BehaviourViewer, behaviour_name: str) -> bool`
  - behaviour_name : string | -> bool
