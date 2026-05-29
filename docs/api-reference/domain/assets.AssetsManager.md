# csc.domain.assets.AssetsManager

> 公式: https://cascadeur.com/python-api/_generate/csc.domain.assets.AssetsManager.html

`class csc.domain.assets.AssetsManager`

AssetsManager class

This class implements basic methods to manage assets

## Methods

- `__init__(*args, **kwargs)`
- `add(*args, **kwargs)`
  - `add(self: csc.domain.assets.AssetsManager, asset: csc.domain.assets.MeshBlendshape) -> csc.domain.AssetId`
  - `add(self: csc.domain.assets.AssetsManager, asset: csc.domain.assets.Mesh) -> csc.domain.AssetId`
  - `add(self: csc.domain.assets.AssetsManager, asset: csc.domain.assets.MeshDependency) -> csc.domain.AssetId`
  - `add(self: csc.domain.assets.AssetsManager, asset: csc.domain.assets.Texture) -> csc.domain.AssetId`
- `all_ids(self: csc.domain.assets.AssetsManager) -> list[csc.domain.AssetId]`
  - -> csc.domain.AssetId[]
- `at(self: csc.domain.assets.AssetsManager, arg0: csc.domain.AssetId) -> object`
  - -> Asset
- `erase(self: csc.domain.assets.AssetsManager, ids: set[csc.domain.AssetId]) -> None`
- `erase_link(self: csc.domain.assets.AssetsManager, ids: set[csc.domain.AssetId]) -> None`
- `find_link()`
  - find_link(self: csc.domain.assets.AssetsManager, id
  - -> string
  - : csc.domain.AssetId) -> str
- `static get_cube_mesh(arg0: float) -> csc.domain.assets.Mesh`
  - -> Mesh
- `static get_plane_mesh(arg0: float) -> csc.domain.assets.Mesh`
  - -> Mesh
- `link_ids(self: csc.domain.assets.AssetsManager) -> list[csc.domain.AssetId]`
  - -> csc.domain.AssetId[]
- `set_link(self: csc.domain.assets.AssetsManager, ids: set[csc.domain.AssetId], file_name: str) -> None`
