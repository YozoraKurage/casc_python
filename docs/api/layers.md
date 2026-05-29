# csc.layers

タイムライン構造（フォルダ・レイヤー＝トラック・キー・補間・サイクル）を扱います。アニメーションのキーフレームや補間を Python から操作する際の中心モジュールです。

### 概念
```
Layers（ルート階層）
└─ Folder（フォルダ）           ← Header(id/name/parent) を持つ
     └─ Layer（= トラック）       ← obj_ids, is_visible, is_locked, sections
          └─ Section（区間）       = Key（キー） + Interval（補間区間）
               ├─ Interpolation（BEZIER/LINEAR/STEP/FIXED ...）
               └─ Common（ik_fk, fixation）
```
- フレーム範囲は `index.FramesIndices` / `index.FramesInterval` で表す。
- ループは `Cycle`（`CyclesViewer` / `CyclesEditor`）。

### 取得経路
- 読み取り: `scene.layers_viewer()` → [Viewer](#viewer)
- 書き込み: `model.layers_editor()` → [Editor](#editor)（`modify*` 内）
- 選択: `model.layers_selector()` / `scene.get_layers_selector()` → [Selector](#selector)
- 全体: `model.layers()` → [Layers](#layers)

### 目次
[Viewer](#viewer) ・ [Editor](#editor) ・ [Selector](#selector) ・ [LayersSelectionChanger](#layersselectionchanger) ・ [Layers](#layers) ・ [LayersContainer](#layerscontainer) ・ [Layer](#layer) ・ [Folder](#folder) ・ [Header](#header) ・ [ItemVariant](#itemvariant) ・ [layer.* 列挙/構造](#layer-列挙構造) ・ [index.* フレーム](#index-フレーム) ・ [Cycle 系](#cycle-系)

---

## Viewer

レイヤー階層の読み取り。`scene.layers_viewer()`。

主なメソッド:

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `root_id()` | `Guid` | ルートフォルダ ID |
| `default_layer_id()` | `Guid` | 既定レイヤー ID |
| `all_layer_ids()` | `List[Guid]` | 全レイヤー ID |
| `layer(id)` / `find_layer(id)` | `Layer` | レイヤー取得 |
| `folder(id)` / `find_folder(id)` | `Folder` | フォルダ取得 |
| `item(id)` | `ItemVariant` | レイヤー/フォルダの抽象 |
| `header(id)` | `Header` | ヘッダ |
| `layers_map()` | `Dict[Guid, Layer]` | レイヤー一覧 |
| `folders_map()` | `Dict[Guid, Folder]` | フォルダ一覧 |
| `all_child_ids(id)` | `List[Guid]` | 子 ID |
| `all_parent_ids(id)` | `List[Guid]` | 親 ID |
| `all_included_layer_ids(items, ignore_locked=False)` | `List[Guid]` | 含まれるレイヤー ID |
| `layer_id_by_obj_id(obj_id)` / `..._or_null` | `Guid` | オブジェクトの所属レイヤー |
| `layer_ids_by_obj_ids(ids)` | `Set[Guid]` | 複数オブジェクトの所属 |
| `obj_ids_by_layer_ids(ids)` | `List[ObjectId]` | レイヤーに属すオブジェクト |
| `frames_count()` / `frames_count(ids)` | `int` | フレーム数 |
| `last_key_pos(ids)` | `int` | 最終キー位置 |
| `actual_key_pos(pos)` | `int` | 実キー位置 |
| `significant_frames([ids])` | `FramesIndices` | 重要フレーム |
| `merged_layer(ids)` / `static merged_layer_s(layers)` | `Layer` | レイヤー結合 |
| `top_layer_id([id])` | `Guid` | 最上位レイヤー |
| `pos_in_parent(id)` | `int` | 親内の位置 |
| `is_deep_child(item_id, folder_id)` | `bool` | 深い子か |
| `has_item(id)` | `bool` | 存在確認 |
| `for_all_ordered_items(callback)` | `None` | 全順序アイテムを走査 |

```python
lv = scene.layers_viewer()
for layer_id in lv.all_included_layer_ids([lv.root_id()]):
    layer = lv.layer(layer_id)
    print(layer.header.name, layer.is_visible, list(layer.obj_ids))
```

---

## Editor

レイヤーの編集。`model.layers_editor()`（`modify*` 内）。

| メソッド | 説明 |
|---|---|
| `create_folder(name, parent, with_default_layer=True, pos=None)` → `Guid` | フォルダ作成 |
| `create_layer(name, parent, pos=None)` → `Guid` | レイヤー（トラック）作成 |
| `delete_folder(id)` / `delete_layer(id)` | 削除（トラック→フォルダの順で） |
| `delete_empty_folders()` / `delete_empty_layers()` | 空の一括削除 |
| `insert_layer(layer, pos)` | レイヤー挿入 |
| `move_item(item_id, folder_id, pos=None)` | アイテム移動 |
| `set_name(name, id)` | 名前設定 |
| `set_visible_for_layer(is_v, id)` / `set_visible_for_item(is_v, id)` | 表示切替 |
| `set_locked_for_layer(is_l, id)` / `set_locked_for_item(is_l, id)` | ロック切替 |
| `set_fixed_interpolation_or_key_if_need(id, frame, set_key)` → `bool` | キー/固定補間を設定 |
| `set_fixed_interpolation_if_need(...)` | 固定補間を設定（オーバーロード） |
| `change_section(pos, id, func)` | 区間を変更（`func(section)` で編集） |
| `set_section(section, pos, id)` / `set_sections(map, id)` / `unset_section(pos, id)` | 区間の設定/解除 |
| `normalize_sections()` | 区間を正規化 |
| `find_header(id)` | ヘッダ取得 |
| `clear()` / `set_default()` | クリア / 既定状態へ |

```python
def mod(model, update, scene):
    le = model.layers_editor()
    lv = scene.layers_viewer()
    track = lv.layer_id_by_obj_id(obj_id)
    le.set_fixed_interpolation_or_key_if_need(track, 5, True)   # フレーム5にキー
    def mod_section(section):
        section.interval.interpolation = csc.layers.layer.Interpolation.BEZIER
    le.change_section(0, track, mod_section)                   # フレーム0からの補間を変更
scene.modify('Set interpolation', mod)
```

---

## Selector

選択中のレイヤー／フォルダの観察と設定。`model.layers_selector()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `all_included_layer_ids(ignore_locked=False)` | `List[Guid]` | 選択に含まれるレイヤー |
| `all_included_layer_indices(ignore_locked=False)` | `IndicesContainer` | 選択インデックス |
| `selection()` | `IndicesContainer` | 現在の選択 |
| `is_selected(id)` | `bool` | 選択中か |
| `select_default()` | `None` | 既定を選択 |
| `set_full_selection_by_parts(inds)` / `(itms, first, last)` | `None` | 全選択を設定 |
| `set_uncheckable_folder_id(id, uncheckable)` | `None` | チェック不可フォルダ設定 |
| `top_layer_id()` | `Guid` | 最上位レイヤー |

```python
def mod(model, update, scene):
    ls = model.layers_selector()
    interval = ls.selection().frames_interval()      # 選択タイムライン範囲
    print(interval.first, interval.last)
scene.modify('Get selection', mod)
```

---

## LayersSelectionChanger

レイヤー選択の変更。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `refresh()` | `bool` | 更新 |
| `selectDefault()` | `bool` | 既定を選択 |
| `set_full_selection_by_parts(inds)` / `(itms, first, last)` | `None`/`bool` | 全選択設定 |

---

## Layers

シーンのレイヤー階層のルート。`model.layers()`。

| プロパティ/メソッド | 戻り値 | 説明 |
|---|---|---|
| `root_id` | `Guid` | ルート ID |
| `folders()` | `Dict[FolderId, Folder]` | フォルダ一覧 |
| `layers()` | `LayersContainer` | レイヤーコンテナ |

---

## LayersContainer

レイヤーの集合。`layers_obj.layers()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `at(guid)` | `Layer` | レイヤー取得 |
| `map()` | `Dict[LayerId, Layer]` | レイヤー一覧 |
| `obj_ids()` | `Dict[ObjectId, LayerId]` | オブジェクト→レイヤー |
| `has_any_obj_ids()` | `bool` | オブジェクトを含むか |
| `has_obj_id(id)` | `bool` | 指定を含むか |
| `layer_id_by_obj_id(id)` / `..._or_null` | `Guid` | 所属レイヤー |

---

## Layer

トラック（補間特性を定義する単位）。

プロパティ: `header`（`Header`）, `is_locked`, `is_visible`, `obj_ids`（`Set[ObjectId]`）, `sections`（`Dict[Pos, Section]`）。

主なメソッド:

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_key(pos)` / `is_key_or_fixed(pos)` | `bool` | キー/固定か |
| `key(pos)` / `actual_key(pos)` | `Key` | キー取得 |
| `actual_key_pos(pos)` | `int` | 実キー位置 |
| `section(pos)` / `actual_section(pos)` / `find_section(pos)` | `Section` | 区間取得 |
| `actual_section_pos(pos)` | `int` | 実区間位置 |
| `interval(pos)` | `Interval` | 区間 |
| `cell(pos)` | `Cell` | セル |
| `key_frame_indices()` | `FramesIndices` | キーのあるフレーム |
| `last_key_pos()` | `int` | 最終キー位置 |

---

## Folder

レイヤー階層内のフォルダ。プロパティ `header`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `children_ids()` / `children_ordered()` | `List[Guid]` | 子 ID |
| `children_cnt()` | `int` | 子の数 |
| `child_by_id(id)` / `child_by_pos(pos)` | `Guid` | 子取得 |
| `child_pos(id)` | `int` | 子の位置 |
| `has_child(id)` | `bool` | 子を持つか |
| `is_empty()` | `bool` | 空か |

---

## Header

フォルダ/レイヤーのヘッダ情報。

| プロパティ | 型 | 説明 |
|---|---|---|
| `id` | `Guid` | 識別子 |
| `name` | `str` | 名前 |
| `parent` | `Guid` | 親 ID |

---

## ItemVariant

フォルダかレイヤーのどちらかを表す抽象。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_folder()` / `is_layer()` | `bool` | 種別判定 |
| `folder()` / `layer()` | `Folder`/`Layer` | 実体取得 |
| `header()` | `Header` | ヘッダ |

```python
item = lv.item(some_id)
if item.is_folder():
    print(item.header().name, "はフォルダ")
```

---

## layer.* 列挙/構造

`csc.layers.layer` 名前空間のキー・区間関連。

### Interpolation（補間）

| メンバー | 値 |
|---|---|
| `BEZIER` | 0 |
| `LOW_AMPLITUDE_BEZIER` | 1 |
| `LINEAR` | 2 |
| `STEP` | 3 |
| `FIXED` | 4 |
| `NONE` | 5 |
| `CLAMPED_BEZIER` | 6 |

### Tangents

`Continuous`(0) / `UserDefined`(1)。

### Label

`NONE`(0) / `SIGNIFICANT`(1)。

### IkFk

`IK`(0) / `FK`(1)。

### Fixation

`Free`(0) / `Fulcrum`(2)。

### Common
区間/キー共通プロパティ。`ik_fk`（`IkFk`）、`fixation`（`Fixation`）。

### Key
キーフレーム。`common`（`Common`）、`label`（`str`）、`tangents`（`Tangents`）。

### Interval
補間区間。`common`（`Common`）、`interpolation`（`Interpolation`）。

### Section
区間の補間特性。`key`（`Key`）と `interval`（`Interval`）を持つ。`change_section` のコールバックで受け取り、`section.interval.interpolation` や `section.key.common.ik_fk` を編集する。

### Cell
区間上のフレーム特性。`key`（`Key`）、`interval`（`FramesInterval`）。

```python
def mod_section(section):
    section.interval.interpolation = csc.layers.layer.Interpolation.LINEAR
    section.interval.common.ik_fk = csc.layers.layer.IkFk.FK
    section.interval.common.fixation = csc.layers.layer.Fixation.Fulcrum
    section.key.common.ik_fk = csc.layers.layer.IkFk.FK
le.change_section(0, track, mod_section)
```

---

## index.* フレーム

`csc.layers.index` 名前空間。フレーム範囲・選択インデックス。

### FramesInterval
連続フレーム区間。プロパティ `first` / `last`（および `start` / `end`）。メソッド `distance()`（フレーム数）、`valid()`。

### FramesIndices
フレーム集合（`run_update` のフレーム引数にも使用）。

| メソッド / 静的 | 説明 |
|---|---|
| `static from_range(min, max)` | 範囲から生成 |
| `add(index/other/set/list)` | 追加 |
| `clamp(min, max)` | 範囲内に丸める |
| `first()` / `last()` / `size()` / `empty()` | 情報 |
| `static intersect_indices(l, r)` | 積集合 |
| `static union_indices(l, r)` | 和集合 |
| `static to_intervals(indices)` | `List[FramesInterval]` へ |

```python
fi = csc.layers.index.FramesIndices.from_range(3, 5)
scene_updater.run_update({pos_id}, fi)
```

### CellIndex
フレーム×アイテムのインデックス。`frame_index`（`int`）、`item_id`（`Guid`）、`is_valid()`。

### RectIndicesContainer
矩形選択のコンテナ。`item_ids()` / `set_item_ids(...)` / `add_item_id(id)` / `contains(id)` / `frames_indices()` / `set_frames_indices(...)`。

### IndicesContainer
`ItemId → FramesIndices` のマップ。タイムライン選択の表現。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `all_frame_indices([size_limit])` | `FramesIndices` | 全フレーム |
| `frames_interval([size_limit])` | `FramesInterval` | フレーム区間 |
| `cell_indices()` | `List[CellIndex]` | セルインデックス |
| `item_ids()` | `List[Guid]` | アイテム ID |
| `item_indices(id)` | `FramesIndices` | 指定アイテムの範囲 |
| `direct_indices()` | `Dict[Guid, FramesIndices]` | 直接インデックス |
| `rect()` | `RectIndicesContainer` | 矩形 |
| `set_frame_indices(start, end)` | `None` | 範囲設定 |
| `add(...)` / `add_frame_indices(...)` / `add_item(...)` | `None` | 追加 |
| `is_empty()` / `delete_empty_items()` | — | 判定/掃除 |

---

## Cycle 系

ループ（サイクル）の表現と編集。

### Cycle
プロパティ: `first_active_frame_index` / `last_active_frame_index` / `left_inactive_frame_index` / `right_inactive_frame_index` / `following_interval`。
メソッド: `left_frame_index()` / `right_frame_index()` / `is_the_same_frames_as(other)`、静的 `get_no_pos()`。

### CyclesEditor

| メソッド | 説明 |
|---|---|
| `create_cycle(a, b)` | サイクル作成 |
| `delete_cycle(pos)` | 削除 |
| `change_inactive_parts(a, b, c)` | 非アクティブ部の変更 |
| `get_cycle_or_null(pos)` | 取得 |
| `normalize()` | 正規化 |

### CyclesViewer

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `get_cycles_in_frames(a, b)` | `List[Cycle]` | 範囲内のサイクル |
| `any_cycles_exist_in_frames(a, b)` | `bool` | 存在判定 |
| `cycle_contains_frame_index(cycle, idx)` | `bool` | 含有判定 |
| `get_active_pos(frame)` / `get_active_section_pos(frame)` | `int` | アクティブ位置 |
| `get_cell(idx)` | `Cell` | セル取得 |
| `is_pos_in_active_cycle_zone(pos)` / `is_pos_in_inactive_cycle_zone(pos)` | `bool` | ゾーン判定 |
| `get_most_left_and_right_frame_indices_of_cycle(cycle)` | `Tuple[int,int]` | 左右端 |
| `last_pos()` | `int` | 最終位置 |

---

[← API 目次](README.md)
