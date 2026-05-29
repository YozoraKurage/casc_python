# csc.domain

ドメイン層。`run(scene)` に渡る中心オブジェクト **`Scene`** と、シーン変更・選択・ピボット・更新を司るクラス群です。

### 目次
- [Scene](#scene)（最重要）
- [SceneUpdater](#sceneupdater)
- [Session](#session)
- 選択: [Selector](#selector) / [Selection](#selection) / [Select](#select) / [SelectionChanger](#selectionchanger) / [SelectorFilter](#selectorfilter) / [SelectorMode](#selectormode)
- ピボット: [Pivot](#pivot) / [StatePivot](#statepivot)
- その他: [Asset](#asset) / [Tool_object_id](#tool_object_id) / [ProcessorsStorage / IMessageHandler](#processorsstorage--imessagehandler)

シーン変更の全体像は [シーン変更モデル ガイド](../guides/scene-modification.md) を参照。

---

## Scene

シーンを表すルートクラス。読み取り Viewer の取得と、変更トランザクションの起点。

### 読み取り・情報

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `model_viewer()` | `csc.model.ModelViewer` | モデル Viewer |
| `behaviour_viewer()` | `csc.model.BehaviourViewer` | ビヘイビア Viewer |
| `data_viewer()` | `csc.model.DataViewer` | データ Viewer |
| `layers_viewer()` | `csc.layers.Viewer` | レイヤー Viewer |
| `get_layers_selector()` | `csc.layers.Selector` | レイヤー選択 |
| `selector()` | `Selector` | 選択 Selector |
| `assets_manager()` | AssetsManager | アセット管理 |
| `get_current_frame(clamp_animation=True)` | `int` | 現在フレーム |
| `set_current_frame(frame)` | `None` | 現在フレーム設定 |
| `get_event_log_or_null()` | `object` | イベントログ |
| `set_event_log(handler)` | `None` | イベントログハンドラ設定 |

### ログ

| メソッド | 説明 |
|---|---|
| `info(msg)` | 情報ログ |
| `warning(msg)` | 警告ログ |
| `error(msg)` | エラーログ |

### 変更トランザクション

| メソッド | コールバック引数 | 説明 |
|---|---|---|
| `modify(name, func)` | `(model, update, scene)` | 変更（再計算なし） |
| `modify_update(name, func)` | `(model, update, scene_updater)` | 変更 + 再計算 |
| `modify_with_session(name, func)` | `(model, update, scene, session)` | 変更 + セッション |
| `modify_update_with_session(name, func)` | `(model, update, scene_updater, session)` | 変更 + 再計算 + セッション |

いずれも戻り値 `bool`。

```python
def run(scene):
    frame = scene.get_current_frame()

    def mod(model, update, scene_updater):
        scene_updater.generate_update()
    scene.modify_update('Modify update', mod)

    def mod_session(model, update, scene, session):
        session.take_selector().select({obj_id}, obj_id)
    scene.modify_with_session('With session', mod_session)
```

---

## SceneUpdater

`modify_update*` のコールバックに渡る、更新処理の司令塔。

| メソッド | 説明 |
|---|---|
| `generate_update()` | アップデートグラフを再生成（構造変更後に必須） |
| `run_update(local_ids, frame)` | `Set[DataId]` を指定フレームで再計算 |
| `run_update(local_ids, frames)` | フレーム範囲（`csc.layers.index.FramesIndices`）で再計算 |
| `scene()` | 紐づく `domain.Scene` を返す |

```python
def mod(model, update, scene_updater):
    # ノード追加後
    scene_updater.generate_update()
    scene_updater.run_update({pos_node.data_id()}, 0)
    # 範囲指定
    scene_updater.run_update({pos_node.data_id()},
                             csc.layers.index.FramesIndices.from_range(3, 5))
scene.modify_update('Update', mod)
```

---

## Session

`*_with_session` のコールバックに渡る。選択・フレームの操作。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `set_current_frame(frame)` | `None` | 現在フレーム設定 |
| `take_selector()` | `Selector` 相当 | オブジェクト選択 |
| `take_layers_selector()` | object | レイヤー選択 |

```python
def mod(model, update, scene, session):
    session.set_current_frame(10)
    session.take_selector().select({obj_id}, obj_id)
scene.modify_with_session('Session', mod)
```

---

## Selector

現在の選択を操作する。`scene.selector()` または `session.take_selector()`。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `selected()` | `Selection` | 現在の選択 |
| `select(select)` | `None` | `Select` 構造体で選択 |
| `select(ids, id, filter, mode, type_filter, auto_pivot=False)` | `None` | 詳細指定で選択 |
| `pivot()` | `Pivot` | ピボット |

```python
selected = scene.selector().selected()
obj_ids = [s for s in selected.ids if isinstance(s, csc.model.ObjectId)]
```

---

## Selection

選択中オブジェクトを保持。

| メンバー | 説明 |
|---|---|
| `ids` | 選択中の ID（`ObjectId` または `Tool_object_id`）の集合 |

---

## Select

選択指定の構造体。

| メンバー | 型 | 説明 |
|---|---|---|
| `object_ids` | `ObjectId`/`Tool_object_id` | 対象 |
| `pivot_id` | `ObjectId`/`Tool_object_id` | ピボット |
| `filter` | `SelectorFilter` | フィルタ |
| `mode` | `SelectorMode` | モード |
| `types_filter` | `str` | 型フィルタ |

---

## SelectionChanger

選択の変更操作。

| メソッド | 説明 |
|---|---|
| `clear_selection()` | 選択解除 |
| `refresh_selection()` | 選択を更新 |
| `select(select)` | `Select` で選択 |
| `select(ids, id, filter, mode, types_filter, auto_pivot=False)` | 詳細選択 |

---

## SelectorFilter

選択フィルタ（ビットフラグ）。

| メンバー | 値 | 説明 |
|---|---|---|
| `Free` | 0x00 | 制限なし |
| `Selectable` | 0x01 | 選択可能なものに限定 |
| `ObjectType` | 0x02 | 型で限定 |
| `Layer` | 0x04 | レイヤーで限定 |
| `OnlySingle` | 0x08 | 単一のみ |
| `Standart` | `Selectable\|ObjectType\|Layer` | 標準 |
| `Full` | 0xFF | 全制限 |

---

## SelectorMode

選択モード。

| メンバー | 説明 |
|---|---|
| `SingleSelection` | 新規選択時はリセット、同一再選択は変化なし |
| `MultiSelection` | 複数選択。未選択なら追加、全選択済みなら除外 |
| `NewSelection` | 既存をリセットして新規を強調 |
| `AdditionSelection` | 強調分を現在選択へ追加 |
| `SubtractionSelection` | 強調分を現在選択から除外 |

---

## Pivot

ピボットの操作。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `origin()` / `origin(frame)` / `origin(frame, pivot)` | Vector3 | 原点 |
| `rotation()` / `rotation(frame)` / `rotation(frame, pivot)` | `Quaternion` | 回転 |
| `center_of_top_objects(func)` | Vector3 | 上位オブジェクトの中心 |
| `select(entity_id)` | `None` | エンティティを選択 |
| `remember_current_frame_pivot()` | `None` | 現フレームのピボットを記憶 |
| `clear_current_frame_pivot()` | `None` | 現フレームのピボットをクリア |
| `remember_interval_pivots()` | `None` | 区間のピボットを記憶 |
| `clear_interval_pivots()` | `None` | 区間のピボットをクリア |

---

## StatePivot

ピボット状態。

| メンバー | 値 | 説明 |
|---|---|---|
| `Fixed` | 0 | 固定 |
| `Moving` | 1 | 移動中 |

---

## Asset

メッシュやテクスチャなどのオブジェクトリソース。

| プロパティ | 型 | 説明 |
|---|---|---|
| `id` | `csc.Guid` | 識別子 |

> アセットの実体取得は `scene.assets_manager()`（`AssetsManager`）経由。`am.at(asset_id)` でメッシュ等にアクセス、`am.add(...)` で追加。`csc.domain.assets.AssetsManager.get_cube_mesh(size)` のような静的生成も存在（[`samples/model_cube.py`](../cookbook.md)）。

---

## Tool_object_id

ツールオブジェクトの識別子。選択 ID は `ObjectId` か `Tool_object_id` のいずれか。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_null()` | `bool` | null 判定 |
| `static null()` | `Tool_object_id` | null を返す |
| `to_string()` | `str` | 文字列化 |

---

## ProcessorsStorage / IMessageHandler

- `ProcessorsStorage`: エンティティの 3D プロセッサを格納するクラス。
- `IMessageHandler`: メッセージ処理のインターフェース（`set_event_log` に渡す）。

---

[← API 目次](README.md)
