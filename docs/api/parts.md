# csc.parts

パーツ（プリセットオブジェクト `.partscasc`）の挿入と、シーンクリップボードを扱います。ゼロからオブジェクトを組むより、既製部品を挿入する方が手軽です（[発展的なアドオン](../guides/advanced-addons.md#1-パーツプリセットを挿入する最も手軽な生成)）。

`parts/` フォルダには `objects/`, `points/`, `boxes/`, `constraints/`, `3d node/`, `spline helpers/`, `final_rig/` などのプリセットがあります。

### 目次
[Buffer](#buffer) ・ [Type](#type) ・ [Info](#info) ・ [GroupInfo](#groupinfo) ・ [SceneClipboard](#sceneclipboard)

---

## Buffer

パーツをシーンへ挿入する。`csc.parts.Buffer.get()` で取得。挿入系は `modify*` 内で呼ぶ。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `static get(source_dir='')` | `Buffer` | バッファ取得 |
| `insert_object_by_path(path, group_id, model, assets)` | `ObjectId` | パスから1オブジェクト挿入 |
| `insert_object_by_id(obj_id, group_id, model, assets)` | `ObjectId` | ID から1オブジェクト挿入 |
| `insert_objects_by_path(path, group_id, model, assets)` | `Tuple[Set[ObjectId], Set[GroupId]]` | パスから複数挿入 |
| `insert_objects_by_id(obj_id, group_id, model, assets)` | `Tuple[Set[ObjectId], Set[GroupId]]` | ID から複数挿入 |
| `insert_selected_objects_by_path(path, group_id, model, assets)` | `Set[ObjectId]` | 選択分を挿入 |
| `insert_elementary_by_path(path, group_id, model)` | `GroupInfo` | エレメンタリ挿入（パス） |
| `insert_elementary_by_id(obj_id, group_id, model)` | `GroupInfo` | エレメンタリ挿入（ID） |
| `insert_update_group_by_path(path, group_id, model)` | `Tuple[GroupInfo, Dict[GroupId, GroupInfo]]` | アップデートグループ挿入（パス） |
| `insert_update_group_by_id(obj_id, group_id, model)` | `Tuple[GroupInfo, Dict[GroupId, GroupInfo]]` | アップデートグループ挿入（ID） |
| `refresh()` | `None` | バッファ更新 |

```python
def run(scene):
    def mod(model, update, scene_updater):
        new_id = csc.parts.Buffer.get().insert_object_by_path(
            'objects/locator.partscasc',
            update.root().group_id(), model, scene_updater.scene().assets_manager())
        scene_updater.generate_update()
        scene.info(f'Added: {new_id}')
    scene.modify_update("Insert object by path", mod)
```

---

## Type

パーツの種類（enum）。挿入の単位を表す。

| メンバー | 値 | 説明 |
|---|---|---|
| `Elementary` | 0 | 通常/設定の関数・データと、それらをつなぐ接続のみ |
| `UpdateGroup` | 1 | サブアップデートグループとそのエレメンタリ、接続 |
| `Object` | 2 | あるオブジェクトの関連エンティティ一式 |
| `ObjectGroup` | 3 | 全オブジェクト・サブグループと関連エンティティ |
| `SelectedObjects` | 4 | 異なるグループからの選択オブジェクト |

プロパティ: `name` / `value`。

---

## Info

パーツの基本情報。

| プロパティ | 型 | 説明 |
|---|---|---|
| `name` | `str` | 名前 |
| `object_id` | `ObjectId` | オブジェクト ID |
| `path` | `str` | パス |
| `type` | `Type` | 種類 |

---

## GroupInfo

シーンバッファ内のグループ情報。

| プロパティ | 型 | 説明 |
|---|---|---|
| `datas` | `List` | データ |
| `regular_funcs` | `List` | 通常関数 |
| `settings` | `List` | 設定 |
| `settings_funcs` | `List` | 設定関数 |

---

## SceneClipboard

シーンのコピー＆ペースト。`csc.app.get_application().get_scene_clipboard()`。

| メソッド | 説明 |
|---|---|
| `copy(view_scene)` | シーンをクリップボードへコピー |
| `paste(view_scene)` | クリップボードからペースト |
| `copy_image_to_clipboard(view_scene)` | シーン画像をコピー |

---

[← API 目次](README.md)
