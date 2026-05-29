# csc.model.BehaviourEditor

> 公式: https://cascadeur.com/python-api/_generate/csc.model.BehaviourEditor.html

BehaviourEditor class

This class allows editing of scene behaviours and their properties.

`class csc.model.BehaviourEditor`

## Methods

- `add_behaviour(*args, **kwargs)`
  - Overloaded function.
  - `add_behaviour(self: csc.model.BehaviourEditor, arg0: csc.model.ObjectId, arg1: str) -> csc.model.BehaviourId`
    - object_id : csc.model.ObjectId | behaviour_type : string | -> csc.model.BehaviourId
  - `add_behaviour(self: csc.model.BehaviourEditor, object_id: csc.model.ObjectId, behaviour_type: str, behaviour_id: csc.model.BehaviourId) -> csc.model.BehaviourId`
    - object_id : csc.model.ObjectId | behaviour_type : string | behaviour_id : csc.model.BehaviourId | -> csc.model.BehaviourId

- `add_behaviour_asset_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, asset_id: common::GenericId<domain::scene::assets::Asset>) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | asset_id : csc.domain.AssetId

- `add_behaviour_data_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, data_id: csc.model.DataId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | data_id : csc.model.DataId

- `add_behaviour_model_object_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, mo_id: csc.model.ObjectId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | mo_id : csc.model.ObjectId

- `add_behaviour_reference_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, beh_id: csc.model.BehaviourId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | beh_id : csc.model.BehaviourId

- `add_behaviour_setting_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, setting_id: csc.model.SettingId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | setting_id : csc.model.SettingId

- `delete_behaviour(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId) -> None`
  - behaviour_id : csc.model.BehaviourId

- `delete_behaviours(self: csc.model.BehaviourEditor, objects_id: set[csc.model.ObjectId]) -> None`
  - objectsId : {csc.model.ObjectId}

- `erase_behaviour_data_from_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, data_id: csc.model.DataId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | data_id : csc.model.DataId

- `erase_behaviour_model_object_from_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, mo_id: csc.model.ObjectId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | mo_id : csc.model.ObjectId

- `erase_behaviour_reference_from_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, beh_id: csc.model.BehaviourId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | beh_id : csc.model.BehaviourId

- `erase_behaviour_setting_from_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, setting_id: csc.model.SettingId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | setting_id : csc.model.SettingId

- `get_viewer(self: csc.model.BehaviourEditor) -> csc.model.BehaviourViewer`

- `hide_behaviour(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, hidden: bool = True) -> bool`
  - behaviour_id : csc.model.BehaviourId | hidden : bool(true) -> bool

- `set_behaviour_asset(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, asset_id: common::GenericId<domain::scene::assets::Asset>) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | asset_id : csc.domain.AssetId

- `set_behaviour_data(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, data_id: csc.model.DataId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | dataId : csc.model.DataId

- `set_behaviour_data_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, inserted_ids: list[csc.model.DataId]) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | inserted_ids : csc.model.DataId

- `set_behaviour_field_value(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, name_value: str) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | name_value : string

- `set_behaviour_model_object(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, mo_id: csc.model.ObjectId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | mo_id : csc.model.ObjectId

- `set_behaviour_model_objects_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, inserted_ids: list[csc.model.ObjectId]) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | inserted_ids : csc.model.ObjectId[]

- `set_behaviour_reference(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, beh_id: csc.model.BehaviourId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | beh_id : csc.model.BehaviourId

- `set_behaviour_references_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, inserted_ids: list[csc.model.BehaviourId]) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | inserted_ids : csc.model.BehaviourId[]

- `set_behaviour_setting(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, setting_id: csc.model.SettingId) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | setting_id : csc.model.SettingId

- `set_behaviour_settings_to_range(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, inserted_ids: list[csc.model.SettingId]) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | inserted_ids : csc.model.SettingId[]

- `set_behaviour_string(self: csc.model.BehaviourEditor, behaviour_id: csc.model.BehaviourId, name: str, str: str) -> bool`
  - behaviour_id : csc.model.BehaviourId | name : string | str : string
