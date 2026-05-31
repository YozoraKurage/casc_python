# クックブック（実例集）

同梱の **サンプル** と **標準コマンド** をテーマ別に解説します。これらは「動く実例」であり、自作アドオンの最良の出発点です。パスは `scripts/python/` 基準です。

> 学習の順番のおすすめ:
> 1. `samples/`（小さく明快） → 2. `commands/add/`・`commands/animation_scripts/`（実用コマンド） → 3. `commands/ik/`・`rig_additional/`・`rig_gen2/`（発展）

---

## 1. サンプル（samples/）

| ファイル | テーマ | 学べること |
|---|---|---|
| [api_document.py](../scripts/python/samples/api_document.py) | API 全リファレンス | `csc` 全クラスの説明と使用例（本ドキュメントの元データ） |
| [iterate_joints.py](../scripts/python/samples/iterate_joints.py) | 読み取り | ジョイント列挙、`behaviour_viewer` / `data_viewer` の基本 |
| [move_joints.py](../scripts/python/samples/move_joints.py) | 書き込み | `modify_update` + `data_editor.set_data_value` + `run_update` |
| [show_inputs_dialog.py](../scripts/python/samples/show_inputs_dialog.py) | UI | 入力ダイアログとコールバック |
| [model_cube.py](../scripts/python/samples/model_cube.py) | 生成（上級） | アップデートグラフを一から構築（ビヘイビア・データ・関数・接続） |
| [delete_joints.py](../scripts/python/samples/delete_joints.py) | 削除 | 選択ジョイントを `model_editor.delete_objects` で削除 |
| [reparent_joints.py](../scripts/python/samples/reparent_joints.py) | 階層 | `pycsc` + `common.hierarchy.set_parent_by_id` で親子付け |
| [casc_import_export.py](../scripts/python/samples/casc_import_export.py) | バッチ処理 | フォルダ内 .casc を一括処理し FBX 出力（`rig_mode.on/off` の利用） |
| [read_rig_json.py](../scripts/python/samples/read_rig_json.py) | リグ I/O | リグコンテキストの JSON エンコード/デコード |
| [change_visibility_data_type.py](../scripts/python/samples/change_visibility_data_type.py) | データ変換 | Static データを Animation データへ置換（フォルダ一括） |
| [get_skinned_joint.py](../scripts/python/samples/get_skinned_joint.py) | テスト連携 | `test.test_cases.rigging_tool` の呼び出し |

### 例: 読み取り（iterate_joints.py）
```python
def iterate_through_joints(scene):
    mv = scene.model_viewer()
    dw = mv.data_viewer()
    bw = mv.behaviour_viewer()
    for bh_joint_id in bw.get_behaviours('Joint'):
        owner = bw.get_behaviour_owner(bh_joint_id)
        gmat_id = bw.get_behaviour_data(bh_joint_id, 'global_matrix')
        scene.info(mv.get_object_name(owner) + ' : ' + str(dw.get_data_value(gmat_id, 0)))
```
→ 関連ガイド: [ビヘイビアとデータ](guides/behaviours-and-data.md)

### 例: 書き込み（move_joints.py）
全ジョイント位置を `[1,1,1]` 平行移動。変更 `DataId` を集めて一括 `run_update`。
→ 関連ガイド: [シーン変更モデル](guides/scene-modification.md)

### 例: 生成（model_cube.py）
グローバル/ローカル変換が相互計算されるオブジェクトを構築。アップデートグラフ学習の決定版。
→ 関連ガイド: [発展的なアドオン #3](guides/advanced-addons.md#3-アップデートグラフの構築model_cubepy-の解剖)

---

## 2. オブジェクト追加（commands/add/）

最も読みやすい「生成系コマンド」の宝庫。`modify_with_session` + `parts` 挿入 + 選択のパターン。

| コマンド | 内容 |
|---|---|
| `add/add_transform.py` | Transform オブジェクトの基礎（他コマンドが部品として再利用） |
| `add/add_locator.py` | ロケーター（[コマンドガイドで詳説](guides/commands.md#実例2-オブジェクトを追加書き込み--セッション)） |
| `add/add_joint.py` | ジョイント |
| `add/add_point_light.py` / `add_spot_light.py` | ライト |
| `add/add_ruler.py` | ルーラー |
| `add/camera/*.py` | カメラ各種（ビューポートから生成等） |
| `add/primitives/*.py` | プリミティブ（cube / cylinder / plane / sphere） |

→ 関連: [コマンドアドオン](guides/commands.md) / [csc.parts](api/parts.md)

---

## 3. アニメーション操作（commands/animation_scripts/）

| コマンド | 内容 |
|---|---|
| `go_to_bind_pose.py` / `go_to_origin.py` | ポーズリセット系 |
| `invert_selection.py` | 選択反転 |
| `keyframe_reduction.py` | キーフレーム削減 |
| `remove_step_interpolation.py` | ステップ補間の除去 |
| `reverse_animation.py` | アニメ逆再生化 |
| `add_noise_to_selected_objs.py` | ノイズ付与 |
| `untwist_animation.py` | ツイスト補正 |

→ 関連: [csc.layers](api/layers.md)（補間・キー）

---

## 4. トランスフォーム・親子（commands/transform/, go_to_default_pose.py）

| コマンド | 内容 |
|---|---|
| `transform/set_parent.py` / `remove_parent.py` | 親子付け／解除 |
| `transform/set_model_pose.py` / `go_to_model_pose.py` | モデルポーズの保存/復帰 |
| `go_to_default_pose.py` | T ポーズへリセット（[リギングガイドで詳説](guides/rigging.md#実例-t-ポーズへのリセットgo_to_default_posepy)） |

→ 関連: [csc.math](api/math.md)（`transforms_difference` 等） / [pycsc](guides/pycsc.md)

---

## 5. リギング（commands/ik/, rig_additional/, rig_info/, center_of_mass/, constrain/）

| グループ | 代表コマンド | 内容 |
|---|---|---|
| `ik/` | `add_ik.py`, `add_pole.py`, `add_proportional_*` | IK・ポール・比例角度 |
| `rig_additional/` | `bind_additional_joint.py`, `batch_rename.py`, `change_character_mass.py`, `correct_daz_rig.py`, `correct_autorig_pro_rig.py` | 追加ジョイント・バインド・リネーム・他ツール由来リグの補正 |
| `rig_info/` | `create.py`, `add_joints.py`, `save_json.py`, `remove.py` | RigInfo の生成・保存 |
| `center_of_mass/` | `create_by_rigids.py`, `create_composite.py`, `snap_mesh_to_cm.py` | 重心オブジェクト |
| `constrain/` | `add_constraint.py`, `add_look_at_constraint.py`, `add_transform_constraint.py` | 各種コンストレイント |
| `collision/` | `add_box.py`, `add_capsule.py`, `generate_convex_mesh.py` | コリジョン形状 |

→ 関連: [リギング](guides/rigging.md) / [csc.rig](api/rig.md) / [csc.tools](api/tools.md)

---

## 6. 入出力・エクスポート（commands/export_to_*, quick_export/, custom_export/）

| コマンド | 内容 |
|---|---|
| `export_to_roblox.py` | Roblox 向けエクスポータ |
| `expotr_to_daz.py` | Daz 向けエクスポータ（ファイル名は原文ママ） |
| `quick_export/*` | 既定フォルダへの素早い再エクスポート、エクスポートパス管理 |
| `custom_export/export_inplace_animation.py` | インプレースアニメの出力 |
| `custom_export/tracks_hierarchy/*` | トラック階層の入出力 |
| **`commands/yozolab/batch_export_fbx/`** | **自作コマンド**: フォルダ以下の全 `.casc` を同じ場所・同じ名前で FBX 一括書き出し（GUIコマンド＋コンソールヘルパー）。[README](../commands/yozolab/batch_export_fbx/README.md) |

→ 関連: [FBX 入出力](guides/fbx-io.md) / [csc.fbx](api/fbx.md)

### バッチ書き出しの最小コア（batch_export_fbx の要点）
```python
import os, csc

def export_folder(folder):                     # folder 以下の *.casc を再帰探索
    app = csc.app.get_application()
    sm = app.get_scene_manager(); tm = app.get_tools_manager()
    for root, _d, files in os.walk(folder):
        for f in files:
            if not f.lower().endswith(".casc"):
                continue
            casc = os.path.join(root, f).replace("\\", "/")     # パスは / に正規化
            out = os.path.splitext(casc)[0] + ".fbx"            # 同じ場所・同じ名前
            sc = sm.create_application_scene(); sm.set_current_scene(sc)
            try:
                csc.app.ProjectLoader.load_from(casc, sc.domain_scene())
                tm.get_tool("FbxSceneLoader").get_fbx_loader(sc).export_all_objects(out)
                # export_* は失敗しても例外を出さないことがある -> 実ファイルを検証
                if not os.path.exists(out):
                    print("WARN: not written:", out)
            finally:
                sm.remove_application_scene(sc)        # 作業タブを必ず閉じる
```
`samples/casc_import_export.py`（処理付きバッチ）が原型。実用版は [commands/yozolab/batch_export_fbx](../commands/yozolab/batch_export_fbx/README.md) を参照。

> ⚠️ ハマりどころ: (1) パスは**フォワードスラッシュ**に正規化する（バックスラッシュだとエクスポータがサイレント失敗し得る）。(2) `export_*` は失敗時も例外を出さないことがあるため**書き出し後に実ファイルを検証**する。(3) アドオンの `.py` は **ASCII のみ**で書く（日本語コメント等を入れると Cascadeur のローダが `UnicodeDecodeError` で読み込みに失敗する）。

---

## 7. ユーティリティ・その他

| コマンド | 内容 |
|---|---|
| `print_mesh_info.py` | メッシュ統計（[コマンドガイドで詳説](guides/commands.md#実例1-ログ出力だけ読み取り)） |
| `change_namespace.py` | 名前空間の変更 |
| `restore_values.py` | デフォルト値の復元（一時部品の活用） |
| `copy_paste_objects/*` | オブジェクトのコピー/複製/ペースト |
| `debug/select_object_by_id.py` | ID で選択（デバッグ） |
| `debug/run_tests.py` | テスト実行 |
| `nekki/Spine/*` | 武器スロット・装備など製品固有の応用例 |

---

## 8. ヘルパー（common/）

自作アドオンから `import common.xxx` で使えるユーティリティ。

| モジュール | 主な関数 |
|---|---|
| `common.selection_operations` | `selected_obj_ids`, `selected_objects_by_type`, `select_all`, `clear_selection`, `get_rig_info` |
| `common.math_operations` | `to_matrix4`, `to_ortho_transform` 等の行列変換 |
| `common.update_operations` | `connect_regular_function`, `get_data_id_by_node_deep`, カスタム enum 記述 |
| `common.objects_names` | `increment_object_name` |
| `common.hierarchy` | `set_parent_by_id` 等の階層操作 |
| `common.layers_operation` | `move_to_new_layer` 等 |
| `common.mesh` / `common.camera` / `common.constraints` | メッシュ・カメラ・コンストレイント補助 |

→ 関連: [pycsc ガイド #ヘルパーモジュール](guides/pycsc.md#ヘルパーモジュールcommon)

---

## 9. リグ生成エンジン（rig_gen/, rig_gen2/, rigging/）

大規模な内部実装。フルスクラッチ再実装より、改造の参照元として使うのが現実的です。

| パッケージ | 内容 |
|---|---|
| `rig_gen2/` | ボックスコントローラ・IK・重心・ポイント・リジッドのファクトリ群（`generation.py`, `rig_object_factory.py` 等） |
| `rigging/rig_builders/` | units / fulcrum_groups / center_of_mass のビルダー |
| `rig_gen/rig_context_gen/` | リグコンテキストの JSON エンコード/デコード |
| `rig_mode/` | リギングモードの on/off（`rig_mode.on` / `rig_mode.off`） |

→ 関連: [リギング](guides/rigging.md)

---

[← ドキュメントトップへ戻る](README.md)
