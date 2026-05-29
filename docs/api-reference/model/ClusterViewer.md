# csc.model.ClusterViewer

> 公式: https://cascadeur.com/python-api/_generate/csc.model.ClusterViewer.html

ClusterViewer class

This class lets read scene data clusters.

`class csc.model.ClusterViewer`

## Methods

- `cluster_by_data(self: csc.model.ClusterViewer, data_id: csc.model.DataId) -> int`
  - data_id : csc.model.DataId | -> ClusterId

- `cluster_datas(self: csc.model.ClusterViewer, cluster_id: int) -> list[csc.model.DataId]`
  - cluster_id : ClusterId | -> csc.model.DataId[]

- `cluster_name(self: csc.model.ClusterViewer, cluster_id: int) -> str`
  - cluster_id : ClusterId | -> string

- `clusters(self: csc.model.ClusterViewer) -> list[int]`
  - -> ClusterId[]

- `clusters_bindings(self: csc.model.ClusterViewer) -> list[csc.model.ClustersEdge]`
  - -> (ClusterId,ClusterId)[]
