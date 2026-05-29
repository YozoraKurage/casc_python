# csc.domain.Selector

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.Selector.html

`class csc.domain.Selector`

Selector class

Contains basic methods and properties to operate current selected scene objects

## Properties

- `ids`
  - Get (csc.model.ObjectId or csc.scene.Tool_object_id){}
- `select`
  - overridden method by Select || Entity3d_id{}, Entity3d_id, SelectorFilter (SelectorFilter.Free), SelectorMode (SelectorMode.NewSelection), string{} (typeFilter)

## Methods

- `__init__(*args, **kwargs)`
- `pivot(self: csc.domain.Selector) -> object`
  - -> Pivot
- `select(*args, **kwargs)`
  - `select(self: csc.domain.Selector, select: csc.domain.Select) -> None`
  - `select(self: csc.domain.Selector, ids: set[Union[csc.model.ObjectId, csc.domain.Tool_object_id]], id: Union[csc.model.ObjectId, csc.domain.Tool_object_id] = <csc.model.ObjectId object at 0x7f6b38d18b30>, filter: csc.domain.SelectorFilter = <SelectorFilter.Free: 0>, mode: csc.domain.SelectorMode = <SelectorMode.NewSelection: 2>, type_filter: set[str] = set(), auto_pivot: bool = False) -> None`
- `selected(self: csc.domain.Selector) -> object`
  - -> Selection
