# csc.model.ClusterEditor

> 公式: https://cascadeur.com/python-api/_generate/csc.model.ClusterEditor.html

ClusterEditor class

This class lets edit scene data clusters.

`class csc.model.ClusterEditor`

## Methods

- `add_cluster(self: csc.model.ClusterEditor, inserted_ids: list[csc.model.DataId], name: str) -> int`
  - insertedIds : csc.model.DataId[] | name : string (“”) | -> ClusterId

- `add_data_to_cluster(self: csc.model.ClusterEditor, cluster_index: int, inserted_ids: list[csc.model.DataId]) -> None`
  - cluster_index : ClusterId | insertedIds : csc.model.DataId[]

- `bind_clusters(self: csc.model.ClusterEditor, cluster_id_first: int, cluster_id_second: int) -> None`
  - cluster_id_first : ClusterId | cluster_id_second : ClusterId

- `remove_cluster(self: csc.model.ClusterEditor, cluster_id: int) -> None`
  - cluster_id : ClusterId

- `remove_data_from_cluster(self: csc.model.ClusterEditor, data_id: csc.model.DataId) -> None`
  - data_id : csc.model.DataId

- `set_cluster_name(self: csc.model.ClusterEditor, cluster_id: int, name: str) -> None`
  - cluster_id : ClusterId | name : string

- `unbind_cluster(self: csc.model.ClusterEditor, cluster_id: int) -> None`
  - cluster_id : ClusterId

- `unbind_clusters(self: csc.model.ClusterEditor, cluster_id_first: int, cluster_id_second: int) -> None`
  - cluster_id_first : ClusterId | cluster_id_second : ClusterId
