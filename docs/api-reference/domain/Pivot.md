# csc.domain.Pivot

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.Pivot.html

`class csc.domain.Pivot`

Pivot class

Represents basic Pivot methods.

## Properties

- `position`
  - overridden method by … || int (frame) || int, StatePivot (pivot)
- `rotation`
  - overridden method by … || int (frame) || int, StatePivot (pivot)

## Methods

- `__init__(*args, **kwargs)`
- `center_of_top_objects(self: csc.domain.Pivot, arg0: Callable[[csc.model.ObjectId | csc.domain.Tool_object_id], numpy.ndarray[numpy.float32[3, 1]]]) -> numpy.ndarray[numpy.float32[3, 1]]`
- `position(*args, **kwargs)`
  - `position(self: csc.domain.Pivot) -> numpy.ndarray[numpy.float32[3, 1]]`
  - `position(self: csc.domain.Pivot, frame: int) -> numpy.ndarray[numpy.float32[3, 1]]`
  - `position(self: csc.domain.Pivot, frame: int, pivot: csc.domain.StatePivot) -> numpy.ndarray[numpy.float32[3, 1]]`
- `rotation(*args, **kwargs)`
  - `rotation(self: csc.domain.Pivot) -> csc.math.Quaternion`
  - `rotation(self: csc.domain.Pivot, frame: int) -> csc.math.Quaternion`
  - `rotation(self: csc.domain.Pivot, frame: int, pivot: csc.domain.StatePivot) -> csc.math.Quaternion`
- `select(self: csc.domain.Pivot, entity_id: csc.model.ObjectId | csc.domain.Tool_object_id) -> None`
