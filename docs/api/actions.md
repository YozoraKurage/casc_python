# アクション ID 一覧（call_action）

`csc.app.ActionManager.call_action(name)` に渡せる **アクション ID 文字列** の一覧です。メニュー項目やツール操作を Python から名前で実行できます。

```python
import csc
def run(scene):
    am = csc.app.get_application().get_action_manager()
    am.call_action("Scene.Undo")
```

> ⚠️ **将来の非推奨予定（公式注記）**: 「この方式の機能は今後段階的に削除予定。よく使われるツールは API 側に拡張機能付きで提供していく」とされています。可能なら専用 API（`csc.tools` の各ツールや `csc.fbx` など）を優先し、`call_action` は API 未提供の操作に限定するのが安全です。
>
> 公式の完全な一覧: [python-api-actions-id-list（category/301）](https://cascadeur.com/help/category/301)

ID は `カテゴリ.操作`（一部 `カテゴリ.サブ.操作`）のドット区切り命名です。以下は主要カテゴリと代表 ID（網羅ではありません。最新・完全版は公式ページ参照）。

---

## Application / Settings

| ID | 内容 |
|---|---|
| `Application.New scene` | 新規シーン |
| `Application.Next scene` / `Application.Previous scene` | シーン切替 |
| `Application.Select all` | 全選択 |
| `Application.Repeat last action` | 直前の操作を繰り返す |
| `Application.Fix scene` | シーン修復 |
| `Application.Logs folder` / `Application.Home` / `Application.Exit` | ログフォルダ / ホーム / 終了 |
| `Settings.Reset all to factory settings` | 設定を工場出荷時へ |
| `Settings.Save current settings as default` | 現設定を既定に保存 |
| `Settings.Reset workspace changes` | ワークスペース変更を破棄 |

## Scene（編集・Undo/Redo）

| ID | 内容 |
|---|---|
| `Scene.Undo` / `Scene.Redo` | 元に戻す / やり直し |
| `Scene.Delete objects` | オブジェクト削除 |
| `Scene.Change fix in objects` | 固定状態の切替 |
| `Scene.Edit mode.Change` / `.Current frame` / `.Neighbors` / `.Selection` | 編集モード |
| `Scene.Pivot mode.Change` / `.Fixed pivot` / `.Moving pivot` | ピボットモード |
| `Scene.Set fixed interpolation on change` / `Scene.Set key on change` | 補間/キーの自動設定 |
| `Scene.Inbetween interpolation switcher` | 中割り補間切替 |

## File（インポート／エクスポート）

代表例（FBX / USD / GLB / 動画など多数）:

| ID | 内容 |
|---|---|
| `File.Open...` / `File.Open autosave file...` | 開く / 自動保存を開く |
| `File.Save` / `File.Save as...` / `File.Save as new version` / `File.Save as (no assets)` | 保存系 |
| `File.Import.Scene.Fbx...` / `File.Import.Scene.Usd...` | シーン取込 |
| `File.Import.Model.Fbx...` / `File.Import.Animation.Fbx...` | モデル/アニメ取込 |
| `File.Import.Animation to selected objects.Fbx...` | 選択へアニメ取込 |
| `File.Export.Scene.Fbx...` / `File.Export.Model.Fbx...` / `File.Export.Glb` | エクスポート |
| `File.Export.Animation.Fbx...` / `File.Export.Video...` | アニメ/動画出力 |
| `File.Export.Selection groups...` / `File.Import.Selection groups...` | 選択グループ I/O |

> FBX 入出力は専用 API（[csc.fbx](fbx.md) / [FBX ガイド](../guides/fbx-io.md)）の利用が推奨です。

## ツール操作

| カテゴリ | 代表 ID |
|---|---|
| AutoPhysics | `AutoPhysicsTool.Switch Auto Physics`, `AutoPhysicsTool.Snap to Auto Physics`, `AutoPhysicsTool.Set priority frame` |
| AutoPosing | `AutoPosingTool.AutoPosing`, `AutoPosingTool.SwitchLock`, `AutoPosingTool.Update` |
| Ballistic Trajectory | `BallisticTrajectoryTool.Add ballistic trajectory`, `BallisticTrajectoryTool.Switch ballistic ghosts` |
| Ghost | `GhostTool.Keyframe ghosts`, `GhostTool.Neighbor frame ghosts`, `GhostTool.Disable ghost` |
| Mirror | `MirrorTool.Mirror on current frame`, `MirrorTool.Mirror on interval`, `MirrorTool.Planes.XY/.XZ/.YZ`, `MirrorTool.Planes.Set by 3 objects` |
| Trajectory | `TrajectoryTool.All trajectories`, `TrajectoryTool.Translate mode`, `TrajectoryTool.Rotate mode`, `TrajectoryTool.Trajectory edit mode` ほか多数 |
| Object Watching | `ObjectWatchingTool.Track object with camera`, `ObjectWatchingTool.Switch camera mode` |
| Default FBX Sync | `DefaultFbxSynchronization.Export scene to default FBX`, `.Import animation from default FBX` |
| Tween Machine | 多数（位置モード×フレーム選択の組合せ） |
| Selection Groups | bind/multiselection/single-selection 各30 グループ（main/additional） |

## View / Viewport / Window

| ID | 内容 |
|---|---|
| `View.Center camera` / `View.Align to camera` | カメラ |
| `View.Hide selected` / `View.Hide not selected` / `View.Make all visible` | 表示 |
| `View.Silhouette mode` / `View.Isometric Grid` / `View.Composition` | 表示モード |
| `Viewport.One Viewport` / `.Two Viewports` / `.Four Viewports` | ビューポート分割 |
| `Viewport.FOV increase` / `.FOV decrease` / `.Set default FOV` | FOV |
| `Window.Python console` | Python コンソール |
| `Window.Node editor` / `.Graph editor` / `.Timeline` / `.Outliner` | 各ウィンドウ |
| `Window.Rigging tools` / `.Tween Machine` / `.Object properties` | ツールウィンドウ |

## Camera Orientation

`CameraOrientationTool.Look from above` / `.below` / `.left` / `.right`、`CameraOrientationTool.Switch projection`。

## Copier（コピー＆ペースト）

`Copier.Copy` / `Copier.Paste`、`Copier.Copy interval` / `Copier.Paste interval`、`Copier.Copy timeline interval`、`Copier.Copy tracks hierarchy` / `Copier.Paste tracks hierarchy` など。

## Manipulators Controller

`ManipulatorsController.Translate` / `.Rotate` / `.Scale` / `.Select`、座標系 `ManipulatorsController.Global` / `.Local` / `.Relative`、軸選択 `.Select axis X/Y/Z`、半径・感度の増減など。

## Selectable / Visible（選択可否・表示切替）

オブジェクト種別ごとに2系統。

- `Selectable.Joints` / `Selectable.Boxes` / `Selectable.Points` / `Selectable.Colliders` / `Selectable.Centers of Mass` / `Selectable.Edges` / `Selectable.Camera Objects` / `Selectable.Shaded Meshes` …
- `Visible.Joints` / `Visible.Boxes` / `Visible.Points` / `Visible.Manipulators` / `Visible.Pivot` / `Visible.Textures` / `Visible.Wireframe Meshes` / `Visible.X-Ray` …

## Timeline

キーフレーム・補間・IK/FK・サイクル・トラック・再生など80以上のアクション（`Timeline.Clear custom tangents on current frame` ほか）。

## Visualizer State Controller（編集モード切替）

`VisualizerStateController.AllModes.AutoPosing mode` / `.Box controller mode` / `.Joint mode` / `.Mesh mode` / `.Point controller mode` / `.Rigging view mode` / `.View mode`、`VisualizerStateController.GroupModes.Switch edit modes` など。

---

[← API 目次](README.md)
