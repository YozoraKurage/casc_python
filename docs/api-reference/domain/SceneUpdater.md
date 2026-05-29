# csc.domain.SceneUpdater

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.SceneUpdater.html

`class csc.domain.SceneUpdater`

SceneUpdater class

The SceneUpdater serves to rule the scene modify.
If we changed the update, we should regenerate it, also it has the possible to run the update with certain data.

## Methods

- `__init__(*args, **kwargs)`
- `generate_update(self: csc.domain.SceneUpdater) -> None`
- `get_interpolator(self: csc.domain.SceneUpdater) -> csc.domain.LocalInterpolator`
- `run_update(*args, **kwargs)`
  - `run_update(self: csc.domain.SceneUpdater, local_ids: set[csc.model.DataId], frame: int) -> None`
  - `run_update(self: csc.domain.SceneUpdater, local_ids: set[csc.model.DataId], frames: csc.layers.index.FramesIndices) -> None`
- `scene(self: csc.domain.SceneUpdater) -> object`
