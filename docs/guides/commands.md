# コマンドアドオン

> 公式ヘルプ: [Python scripting in Cascadeur](https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur)

コマンドは、ユーザーが手動で実行する最も一般的なアドオン形態です。ユーザー用コマンドフォルダに `run(scene)` を持つモジュールを置くと、Cascadeur が起動時に自動検出し、**`Commands` メニュー**に並べます。

```
<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands
```

編集後は **`Commands > Reload scripts`** で再読込できます（再起動不要）。

---

## モジュールの構成

```python
import csc

def command_name():
    return "My Tool"                     # 省略可。コマンド一覧の表示名

def command_description():
    return "選択オブジェクトに対して○○する"  # 省略可。説明文

def run(scene):                          # 必須。実行本体
    ...
```

| 関数 | 必須 | 役割 |
|---|---|---|
| `run(scene)` | ✅ | 実行本体。`scene` は `csc.domain.Scene` |
| `command_name()` | ⬜ | 表示名。無い場合は登録名が空になるため、付けるのが推奨 |
| `command_description()` | ⬜ | 説明文（ツールチップ等） |

---

## 命名規則とメニュー階層

標準コマンドは `command_name()` を**ドット区切り**で返し、メニューの階層を表現しています。

```python
def command_name():
    return "Add.Locator"     # 「Add」グループの中の「Locator」
```

例（同梱の標準コマンド `commands/add/` より）:
- `Add.Locator`、`Add.Joint`、`Add.Transform`、`Add.PointLight` …

この規約に従うと、関連コマンドがメニュー上でまとまり、見つけやすくなります。

---

## 実例1: ログ出力だけ（読み取り）

[`commands/print_mesh_info.py`](../cookbook.md) は、シーン内の全メッシュの頂点・三角形・四角形数を集計してログ出力します。**読み取りのみ**なのでトランザクションは不要です。

```python
import csc

def command_name():
    return "Print mesh info"

def command_description():
    return ("Prints detailed mesh statistics for all MeshObjects in the scene, "
            "including the number of vertices, triangles, and quads for each mesh")

def run(scene):
    mv = scene.model_viewer()
    am = scene.assets_manager()
    bv = mv.behaviour_viewer()

    for bh_mesh in bv.get_behaviours('MeshObject'):
        owner = bv.get_behaviour_owner(bh_mesh)
        mesh = bv.get_behaviour_asset(bh_mesh, 'mesh')   # メッシュアセットを取得
        positions = len(am.at(mesh).positions())
        scene.info(f'Mesh {mv.get_object_name(owner)} has {positions} vertices.')
```

ポイント:
- `scene.assets_manager()` でアセットマネージャを取得し、`am.at(mesh)` でメッシュ本体へアクセス。
- `bv.get_behaviour_asset(behaviour_id, "mesh")` でビヘイビアが参照するアセット ID を取得。

---

## 実例2: オブジェクトを追加（書き込み + セッション）

[`commands/add/add_locator.py`](../cookbook.md) はロケーターを生成し、選択状態にします。オブジェクト生成＋選択変更なので `modify_with_session` を使います。

```python
import csc
import pycsc
import common.objects_names
from commands.add.add_transform import add_transform_object as add_tr

def command_name():
    return "Add.Locator"

def command_description():
    return "Adds a locator object"

def add_locator_mod(model, update, sc, session):
    be = model.behaviour_editor()

    obj_id = add_tr(model, update, sc)        # まず Transform オブジェクトを作る
    be.add_behaviour(obj_id, 'Locator')       # Locator ビヘイビアを付与

    # pycsc で名前を付ける
    py_scene = pycsc.wrap(sc)
    py_scene.set_modifiers(model, update, sc, session)
    py_obj = pycsc.wrap(obj_id, py_scene)
    py_obj.name = common.objects_names.increment_object_name(sc, 'Locator')

    # 生成したオブジェクトを選択
    session.take_selector().select({obj_id}, obj_id)
    return obj_id

def run(scene):
    scene.modify_with_session(command_name(), add_locator_mod)
```

ポイント:
- 生成系コマンドは「他のコマンド関数を部品として再利用」する（`add_transform_object` を import して使う）のが定石。
- `session.take_selector().select({obj_id}, obj_id)` で、生成直後に選択状態へ。
- 名前付けには `pycsc` や `common.objects_names` のヘルパーを使うと楽。

---

## 実例3: 前提チェックと一時オブジェクトの利用

[`commands/restore_values.py`](../cookbook.md) は、一時的に部品オブジェクトを差し込んでデフォルト値を読み出し、対象に書き戻して、最後に一時オブジェクトを削除します。

```python
def restore_auto_physics_values(scene, cm_obj_id, points_obj_ids):
    def mod(model, update, sc):
        bv = scene.model_viewer().behaviour_viewer()
        dv = scene.model_viewer().data_viewer()
        de = model.data_editor()

        # parts から一時オブジェクトを挿入してデフォルト値を取得
        temp = csc.parts.Buffer.get().insert_object_by_path(
            'points/basic_point.partscasc',
            update.root().group_id(), model, sc.assets_manager())
        ...
        model.delete_objects({temp})   # 後始末
    scene.modify("Restore default values", mod)
```

ポイント:
- `csc.parts.Buffer.get().insert_object_by_path("...", update.root().group_id(), model, sc.assets_manager())` でプリセット部品をシーンに挿入できる。
- 値の取得・比較に「デフォルト部品」を使うテクニック。
- 一時オブジェクトは `model.delete_objects({...})` で確実に削除。
- データには `Static`（静的）と `Animation`（フレーム単位）があり、書き込み方が異なる（後述）。

---

## どの `modify` を使うか

| やること | 使うメソッド |
|---|---|
| データ・ビヘイビアを変えるだけ | `modify` |
| 変更後に依存計算を反映したい | `modify_update`（最も一般的） |
| 選択を変える | `*_with_session` |
| オブジェクト生成 + 選択 + 再計算 | `modify_update_with_session` |

詳細な使い分けは [シーン変更モデル](scene-modification.md) を参照。

---

## チェックリスト

- [ ] `commands/` 配下に置いたか
- [ ] `run(scene)` を定義したか
- [ ] 表示名のため `command_name()` を付けたか（推奨）
- [ ] 書き込みは `scene.modify*` の中で行っているか
- [ ] 前提条件が満たされない場合に `raise Exception(...)` で通知しているか
- [ ] 一時オブジェクトを作ったら削除しているか

---

関連: [イベントハンドラ](events.md) / [シーン変更モデル](scene-modification.md) / [ビヘイビアとデータ](behaviours-and-data.md) / [クックブック](../cookbook.md)
