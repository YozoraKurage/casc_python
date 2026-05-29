# pycsc — 高レベル Python ラッパー

`pycsc` は、低レベルの `csc` を Python らしく包んだラッパーライブラリです。**必須ではありません**が、ボイラープレート（`modify_update_with_session` の入れ子、Viewer/Editor の取り回し、ID 経由のスロットアクセス）を大きく減らせます。

> 作者・バージョン: `pycsc/__init__.py` に `__author__ = "Nathaniel Albright"`、`VERSION = (0, 6, 0)`。標準コマンドの一部（例: [`commands/go_to_default_pose.py`](../cookbook.md)、`commands/add/add_locator.py`）が pycsc を使っています。

---

## いつ pycsc を使うか

| 状況 | 推奨 |
|---|---|
| シーンを軽く読むだけ | 素の `csc` で十分 |
| 大量のオブジェクト走査・トランスフォーム計算 | `pycsc` が読みやすい |
| 新規オブジェクト生成やノード操作 | どちらでも可（`csc` の方が低レベルで明示的） |
| 既存の標準コマンドを改造 | そのコマンドが使っている流儀に合わせる |

`pycsc` は内部で `csc` を呼ぶだけなので、両者を混在させても構いません（`pycsc.wrap` / `.unwrap()` で相互変換）。

---

## 中核の考え方: ラッパーと unwrap

`pycsc` のオブジェクトは `CscWrapper` で、内部に生の `csc` オブジェクト（handle）を保持します。

```python
import pycsc

py_scene = pycsc.wrap(scene)        # csc.domain.Scene → DomainScene
raw = py_scene.unwrap()             # 生の csc.domain.Scene に戻す（.handle でも可）
```

ラッパーはメソッド呼び出しや属性アクセスを生オブジェクトへ委譲し、戻り値も自動でラップします。`is_null()` な ID は `None` に変換されるなど、Python的な扱いになります。

---

## デコレータで modify を省略する

最頻出のパターン。`@pycsc.run_update_session` を付けた関数は、自動的に `modify_update_with_session` トランザクションの中で実行され、終了時に `generate_update()` まで呼ばれます。関数の第1引数には `DomainScene`（pycsc 版）が渡ります。

```python
import csc, pycsc

def run(scene):
    @pycsc.run_update_session
    def go(py_scene: pycsc.DomainScene):
        # ここはすでに modify_update_with_session の中
        objs = py_scene.get_scene_objects(selected=True, with_behaviour="BoxView")
        if not objs:
            raise Exception("ボックスコントローラを選択してください")
        frame = py_scene.get_current_frame()
        ...
        py_scene.su.handle.run_update(actuals, frame)   # 生の SceneUpdater へ

    go()    # ← ここで実際に実行される
```

（[`commands/go_to_default_pose.py`](../cookbook.md) がまさにこの形。）

関連デコレータ:

| デコレータ | 第1引数 | 内部で呼ぶ | 用途 |
|---|---|---|---|
| `run_update_session` | 現在シーン（自動取得） | `modify_update_with_session` + `generate_update` | 現在シーンを編集 |
| `run_generate_update` | 現在シーン | 同上 | 同上（別名的） |
| `run_edit_update` | 引数で渡した `scene` | `modify_update_with_session` + `generate_update` | scene を明示的に渡す |

---

## 既存の modify コールバック内で pycsc を使う

すでに `csc` の `modify*` を開始している場合は、`set_modifiers(...)` でラッパーに Editor 群を渡してから使います。

```python
def add_locator_mod(model, update, sc, session):
    py_scene = pycsc.wrap(sc)
    py_scene.set_modifiers(model, update, sc, session)   # ← Editor を引き渡す
    py_obj = pycsc.wrap(obj_id, py_scene)
    py_obj.name = "Locator"                              # 属性で名前設定
```

（[`commands/add/add_locator.py`](../cookbook.md) の手法。）

---

## シーンオブジェクトの取得とフィルタ

`DomainScene.get_scene_objects(...)` は強力なフィルタ付きでオブジェクトを返します。

```python
py_scene.get_scene_objects(
    names=[],            # 特定の名前のみ
    selected=False,      # 選択中のみ
    of_type="",          # アウトライナ上の型名で絞る
    only_roots=False,    # 親を持たないルートのみ
    with_behaviour="",   # 指定ビヘイビアを持つもののみ（例 "BoxView", "Joint"）
)
```

例:

```python
# 選択中の BoxView コントローラだけ
boxes = py_scene.get_scene_objects(selected=True, with_behaviour="BoxView")

# ルートのジョイントだけ
roots = py_scene.get_scene_objects(only_roots=True, with_behaviour="Joint")
```

`pycsc.get_scene_objects(...)`（モジュール関数）は現在シーンに対する同等のショートカットです。

---

## ノードとトランスフォーム

`DomainScene.update_node(obj)` で `ObjectNode` を、`pycsc.TransformUpdate(obj_id, py_scene)` でトランスフォーム操作用ノードを得られます。

```python
node = py_scene.update_node(obj_id)             # ObjectNode
if node.has_behaviour("Transform"):
    tr = pycsc.TransformUpdate(obj_id, py_scene)
    parent = tr.parent_obj()                    # 親 TransformUpdate
    has_parent = tr.has_transform_parent()
    g = tr.get_global_orto_transform()          # csc.math.OrthogonalTransform
    # ローカル位置/回転データへ
    tr.local_pos_data.set_value(pos, frame)
    tr.local_rot_data.set_value(rot, frame)
```

属性経由でビヘイビアのプロパティにアクセスする糖衣も用意されています。

```python
# Untwist ビヘイビアの各プロパティをフレーム指定で取得
axis   = node.id.Untwist.axis.get(frame=frame)
weight = node.id.Untwist.weight.get(frame=frame)
```

> これらは `pycsc` の高水準 API です。内部的には `csc` の `BehaviourViewer/DataViewer/Editor` 呼び出しに展開されます。型や利用可能メンバーは `pycsc/datatypes/domain/...` のソースで確認できます。

---

## ヘルパーモジュール（`common`）

`pycsc` と並んで、`common` パッケージにも実用的なヘルパーがあります（pycsc 非依存のものも多い）。

| モジュール | 主な関数 |
|---|---|
| `common.selection_operations` | `selected_obj_ids(scene)`, `select_all`, `clear_selection`, `find_object_by_behaviour_type` |
| `common.math_operations` | `to_matrix4`, `to_ortho_transform` など行列変換 |
| `common.update_operations` | `connect_regular_function(func, attrs)`, `get_data_id_by_node_deep`, カスタム enum 記述の生成 |
| `common.objects_names` | `increment_object_name(scene, base)` 連番名生成 |

```python
import common.selection_operations as so
selected = so.selected_obj_ids(scene)    # 選択中の ObjectId リスト
```

---

## 素の csc と pycsc の対応（チートシート）

| やること | 素の csc | pycsc |
|---|---|---|
| 変更トランザクション | `scene.modify_update_with_session(name, fn)` | `@pycsc.run_update_session` |
| 選択オブジェクト | `scene.selector().selected().ids` を型で絞る | `py_scene.get_scene_objects(selected=True)` |
| 現在フレーム | `scene.get_current_frame()` | `py_scene.get_current_frame()` |
| 名前設定 | `BehaviourEditor` 経由（複雑） | `py_obj.name = "..."` |
| 生に戻す | — | `obj.unwrap()` / `obj.handle` |

---

関連: [シーン変更モデル](scene-modification.md) / [発展的なアドオン](advanced-addons.md) / [クックブック](../cookbook.md)
