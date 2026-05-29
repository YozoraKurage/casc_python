# アーキテクチャ — Cascadeur の中核モデル

このページは本ドキュメントで最も重要です。Cascadeur のシーンがどう構成され、Python からどう触るのかという**全体像**を説明します。ここを理解すれば、API リファレンスの各クラスが「どこに位置するか」が分かるようになります。

---

## 1. 2つの Scene: `view.Scene` と `domain.Scene`

「Scene」という語は2つの異なるオブジェクトを指します。混同しやすいので最初に整理します。

| | `csc.view.Scene` | `csc.domain.Scene` |
|---|---|---|
| 何を表すか | UI 上の**シーンタブ**（ビュー） | シーンの**中身**（ドメインモデル） |
| 取得元 | `scene_manager.current_scene()` | `view_scene.domain_scene()` / `run(scene)` の引数 |
| 主な役割 | 保存、ビューポート、カメラ | オブジェクト・データの読み書き、変更トランザクション |

```python
import csc

def run(scene):                       # scene は csc.domain.Scene
    app = csc.app.get_application()
    view_scene = app.get_scene_manager().current_scene()   # csc.view.Scene
    same_domain = view_scene.domain_scene()                # ← run の scene と同じ中身
```

アドオンの `run(scene)` に渡るのは **`csc.domain.Scene`**。以降「scene」と書いたらこちらを指します。

---

## 2. Viewer と Editor — 読み取りと書き込みの分離

Cascadeur API の根本原則です。

- **Viewer = 読み取り専用**。いつでも取得・呼び出し可能。
- **Editor = 書き込み**。`scene.modify*(...)` トランザクションの**中でだけ**取得できる。

```
csc.domain.Scene
├── model_viewer()  → csc.model.ModelViewer        （読み取り）
│     ├── behaviour_viewer() → BehaviourViewer
│     └── data_viewer()      → DataViewer
├── layers_viewer() → csc.layers.Viewer            （読み取り）
├── selector()      → 選択状態の取得                （読み取り）
└── modify_update(name, fn) のコールバック内で:
      model_editor: csc.model.ModelEditor          （書き込み）
        ├── behaviour_editor() → BehaviourEditor
        ├── data_editor()      → DataEditor
        └── layers_editor()    → csc.layers.Editor
```

読み取りと書き込みでクラスが分かれている（`BehaviourViewer` / `BehaviourEditor`、`DataViewer` / `DataEditor` など）のがポイントです。

```python
def run(scene):
    # 読み取り: Viewer はそのまま使える
    mv = scene.model_viewer()
    bv = mv.behaviour_viewer()
    objs = mv.get_objects()

    # 書き込み: Editor は modify の中でだけ
    def mod(model, update, scene_updater):
        de = model.data_editor()       # ここでしか取れない
        ...
    scene.modify_update("変更名", mod)
```

---

## 3. 変更トランザクション `modify` 系

シーンの変更は必ずトランザクションでくるみます。これが **Undo/Redo の1単位**になり、内部状態の整合性も保たれます。4種類あります。

| メソッド | コールバック引数 | 用途 |
|---|---|---|
| `modify(name, fn)` | `(model, update, scene)` | データ・ビヘイビアの変更（再計算を伴わない／自前で扱う） |
| `modify_update(name, fn)` | `(model, update, scene_updater)` | 変更後にアップデートグラフの**再計算**まで行う（最も一般的） |
| `modify_with_session(name, fn)` | `(model, update, scene, session)` | 選択など**セッション**を伴う操作 |
| `modify_update_with_session(name, fn)` | `(model, update, scene_updater, session)` | 上記 + 再計算 |

コールバックに渡る主なオブジェクト:
- `model`（`csc.model.ModelEditor`）: ビヘイビア・データの Editor を取得（`behaviour_editor()`, `data_editor()`, `layers_editor()`）。
- `update`（`csc.update.Update`）: アップデートグラフの編集（`root()`, `get_object_by_id(...)`、オブジェクト/グループ/データ/関数の生成）。
- `scene_updater`（`csc.domain.SceneUpdater`）: `generate_update()` でグラフ再構築、`run_update(data_ids, frame)` で値の再計算。
- `session`（`csc.domain.Session`）: `take_selector()` などで選択を変更。

```python
def run(scene):
    def mod(model, update, scene_updater):
        de = model.data_editor()
        # ... データを書き換える ...
        scene_updater.run_update(changed_data_ids, frame)
    scene.modify_update("My change", mod)
```

詳細・使い分けは [シーン変更モデル](guides/scene-modification.md) を参照。

---

## 4. オブジェクト・ビヘイビア・データの3層

シーン内の「もの」は次の階層で表現されます。

```
Object（オブジェクト）  ← csc.model.ObjectId で識別
  └─ Behaviour（ビヘイビア）複数  ← csc.Guid で識別、型名を持つ（'Joint','Transform',...）
       └─ 名前付きスロット → Data / Setting / 別オブジェクト / 別ビヘイビア を参照
                              ↑ Data は csc.model.DataId、Setting は SettingId で識別
```

- **Object**: シーン内の1個の要素（ジョイント、ロケーター、メッシュ、リグ要素…）。実体は ID（`ObjectId`）。
- **Behaviour**: オブジェクトに付く「機能部品」。1オブジェクトが複数のビヘイビアを持つ。
  - 例: ジョイントは `Basic` + `Transform` + `Joint` + `BoxView` + `Point` などを併せ持つ。
  - ビヘイビアは**名前付きスロット**を持ち、そこに Data や別オブジェクトを差し込む。
    - 例: `Transform` ビヘイビアの `global_position` スロット → 位置を保持する Data を参照。
    - 例: `Basic` ビヘイビアの `parent` スロット → 親オブジェクトを参照。
- **Data / Setting**: 実際の値。`Data` はベクトル・回転・行列などの**フレーム単位**の値。`Setting` は bool/int の設定値。

代表的なビヘイビアと型名:

| 型名 | 役割 |
|---|---|
| `Basic` | 基本属性（親 `parent`、選択可否など） |
| `Transform` | グローバル/ローカルの位置・回転・スケール |
| `Joint` | ジョイント（`global_matrix` など） |
| `BoxView` | ボックスコントローラの見た目（`size`, `offset`） |
| `Point` | ポイント表示 |
| `EdgeView` | 2オブジェクト間のエッジ表示 |
| `MeshObject` | メッシュ（`mesh` アセット、`linked_objects`） |
| `RigInfo` | リグ情報（`rig_objects`, `related_joints`） |

### 読み取りの基本パターン

```python
def run(scene):
    mv = scene.model_viewer()
    bv = mv.behaviour_viewer()
    dv = mv.data_viewer()

    obj = mv.get_objects()[0]
    tr  = bv.get_behaviour_by_name(obj, "Transform")     # ビヘイビアID(Guid)
    pos_id = bv.get_behaviour_data(tr, "global_position") # データID(DataId)
    pos = dv.get_data_value(pos_id, 0)                    # フレーム0の値
    scene.info(f"{mv.get_object_name(obj)} の位置: {pos}")
```

### 書き込みの基本パターン

```python
def run(scene):
    mv = scene.model_viewer(); bv = mv.behaviour_viewer()
    obj = mv.get_objects()[0]
    tr  = bv.get_behaviour_by_name(obj, "Transform")
    pos_id = bv.get_behaviour_data(tr, "global_position")

    def mod(model, update, scene_updater):
        de = model.data_editor()
        de.set_data_value(pos_id, 0, [10.0, 0.0, 0.0])
        scene_updater.run_update({pos_id}, 0)
    scene.modify_update("Set position", mod)
```

詳細は [ビヘイビアとデータ](guides/behaviours-and-data.md)。

---

## 5. アップデートグラフ（`csc.update`）

ここが Cascadeur 独特の部分です。各オブジェクトの内部は、**ノードの依存計算グラフ**として実装されています。たとえば「ローカル位置」と「親のトランスフォーム」から「グローバル位置」が計算される、という関係がグラフのエッジで表現されます。

主な構成要素（[csc.update リファレンス](api/update.md) 参照）:

- **Object / ObjectGroup / Group / UpdateGroup**: ノードの入れ物（階層）。`update.root()` が最上位。
- **RegularData / SettingData**: グラフ上のデータノード（値を保持）。
- **RegularFunction / SettingFunction**: 計算ノード（`CombineTransforms`、`Or`、`BinarySwitcher` など）。
- **Node / NodeAttribute / Connection / Interface**: ノードとその入出力端子、接続。
- **GroupId / DataId / SettingId** など: 各要素の ID。

通常のアニメーション編集（既存オブジェクトの値変更）では、このグラフを意識する必要はほぼありません。
グラフを直接組むのは「**新しいオブジェクトを一から生成する**」「**カスタムの計算ノードを差し込む**」ような発展的ケースです（[`samples/model_cube.py`](cookbook.md) が良い実例）。

### 再計算のサイクル

```
値を変更（data_editor.set_data_value）
        ↓
グラフ構造を変えたら scene_updater.generate_update()
        ↓
scene_updater.run_update({変更したDataId}, frame)   ← 依存先が再計算される
```

- 既存の値だけ変えた → `run_update(...)` だけでよい。
- ノードやオブジェクトを追加・接続変更した → 先に `generate_update()`、その後 `run_update(...)`。

---

## 6. タイムラインとレイヤー（`csc.layers`）

アニメーションはレイヤー（トラック）とキーフレームで構成されます。

- `scene.layers_viewer()` → `csc.layers.Viewer`（読み取り）
- `model.layers_editor()` → `csc.layers.Editor`（書き込み）
- キー・補間・接線・サイクル（ループ）・フィクセーション・IK/FK などを操作。
- フレーム範囲は `csc.layers.index.FramesIndices` / `FramesInterval` で表現。

詳細は [csc.layers リファレンス](api/layers.md)。

---

## 7. 全体像（1枚図）

```
                 csc.app.get_application()  → Application
                      │  get_scene_manager / get_tools_manager / get_action_manager ...
                      ▼
        SceneManager.current_scene()  → csc.view.Scene （UIタブ）
                      │  .domain_scene()
                      ▼
        ┌──────────────  csc.domain.Scene  ──────────────┐
        │  （= run(scene) の引数。読み書きの中心）           │
        │                                                  │
        │  読取: model_viewer() / layers_viewer()          │
        │        / selector() / assets_manager()           │
        │                                                  │
        │  書込: modify_update("名前", fn)                  │
        │         fn(model, update, scene_updater)         │
        │           model  → ModelEditor                   │
        │             ├ behaviour_editor()                 │
        │             ├ data_editor()                      │
        │             └ layers_editor()                    │
        │           update → アップデートグラフ編集          │
        │           scene_updater → generate/run_update    │
        └──────────────────────────────────────────────────┘

   オブジェクト = ObjectId
       └ ビヘイビア(Guid){Basic,Transform,Joint,BoxView,...}
            └ 名前付きスロット → Data(DataId)/Setting(SettingId)/別Object
```

---

## 次に読むべきもの

- アドオンを作り始める → [アドオンの基本](guides/addon-basics.md)
- 変更トランザクションを深く → [シーン変更モデル](guides/scene-modification.md)
- ビヘイビア/データ操作を深く → [ビヘイビアとデータ](guides/behaviours-and-data.md)
- API を辞書的に引く → [API リファレンス目次](api/README.md)
