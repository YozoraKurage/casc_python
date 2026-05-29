# csc.rig

リギング（自動リグ生成・リグ要素追加）用のデータ構造です。これらは設定値の入れ物で、実際の生成処理は `rig_gen` / `rig_gen2` / `rigging` パッケージや各種コマンドが担います（[リギング ガイド](../guides/rigging.md)）。

### 目次
[AutoRigData](#autorigdata) ・ [AddElementData](#addelementdata) ・ [NamesInfo](#namesinfo) ・ [RigValues](#rigvalues)

---

## AutoRigData

自動リグ生成の設定一式。各ボディパーツや名前リストを保持。

| プロパティ | 型 | 説明 |
|---|---|---|
| `names` | `list` | 名前 |
| `arms` / `hands` / `foots` / `thighs` / `toes` | `list` | 各部位の要素 |
| `neck` / `pelvis` | `list` | 首・骨盤 |
| `spine_names` / `finger_names` / `hinge_names` / `straighten_names` | `list` | 各種名前 |
| `directions` | `list` | 方向 |
| `fulcrum_groups` | `list` | 支点グループ |
| `additionals` | `list` | 追加要素 |
| `values` | `list` | 設定値 |

---

## AddElementData

リグ要素（コントローラ）追加時の設定。

| プロパティ | 型 | 説明 |
|---|---|---|
| `box_multiplier` | `float` | ボックスサイズ倍率 |
| `joint_size_without_child` | `float` | 子なしジョイントのサイズ |
| `only_box_controller` | `bool` | ボックスコントローラのみ |
| `orthogonal_with_parent` | `bool` | 親と直交させるか |
| `use_global_axis` | `bool` | グローバル軸を使うか |
| `is_multiple` | `bool` | 複数追加か |
| `point_color` | `tuple` | ポイント色 |
| `axis_point_controller` | `Any` | 軸ポイントコントローラ |
| `offset_point_controller` | `Any` | オフセットポイントコントローラ |

---

## NamesInfo

ジョイント名と影響範囲。

| プロパティ | 型 | 説明 |
|---|---|---|
| `begin_joint` | `str` | 開始ジョイント |
| `end_joint` | `str` | 終了ジョイント |
| `is_left` | `bool` | 左側か |
| `is_inverse` | `bool` | 反転か |
| `is_affect_parent` | `bool` | 親に影響するか |

---

## RigValues

リグの寸法・質量系の値。

| プロパティ | 型 | 説明 |
|---|---|---|
| `box_global_offset` | `float` | ボックスのグローバルオフセット |
| `box_scale_width` | `float` | 幅スケール |
| `box_scale_depth` | `float` | 奥行スケール |
| `additional_point_global_offset` | `float` | 追加ポイントのオフセット |
| `mass` | `float` | 質量 |
| `width` | `float` | 幅 |

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_names()` | `Dict[str, str]` | 関連する名前 |

---

[← API 目次](README.md)
