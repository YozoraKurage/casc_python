# Cascadeur Python API 日本語ドキュメント

Cascadeur（3Dキャラクターアニメーションソフト）の Python アドオン開発のための、非公式・包括的な日本語ドキュメントです。
`C:\Program Files\Cascadeur\resources\scripts` に同梱されている実際のスクリプト群（`csc` モジュールの API ドキュメント・サンプル・標準コマンド・`pycsc` ラッパー）を解析して作成しています。

> 公式情報源
> - Python スクリプティング解説: <https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur>
> - Python API リファレンス（HTML自動生成）: <https://cascadeur.com/python-api/>
> - ヘルプ全般: <https://cascadeur.com/help/category/215>
>
> 本ドキュメントはそれらを読みやすく再構成し、実コードに基づく解説・サンプルを加えたものです。
>
> **対象バージョン**: Cascadeur **v2026.1.2**（2026-05-29 時点）。バージョン差により API・UI 名称が変わる場合があります。

---

## このドキュメントの読み方

はじめての方は **概要 → はじめに → アーキテクチャ → アドオンの基本** の順に読むことを推奨します。
API の細部を調べたいときは **API リファレンス** を辞書的に参照してください。

### 1. 全体を理解する

| ドキュメント | 内容 |
|---|---|
| [概要](overview.md) | Cascadeur Python API とは何か。2層構造（`csc` / `pycsc`）、スクリプト配置、できること |
| [はじめに](getting-started.md) | スクリプトの実行方法、最初のスクリプト、開発環境とデバッグ |
| [アーキテクチャ](architecture.md) | Scene / Viewer / Editor、`modify` トランザクション、アップデートグラフ、ビヘイビア・データという中核モデル |

### 2. アドオンを作る（ガイド）

| ガイド | 内容 |
|---|---|
| [アドオンの基本](guides/addon-basics.md) | アドオンの3形態（コマンド・イベント・スクリプト）と最小実装 |
| [コマンドアドオン](guides/commands.md) | `run` / `command_name` / `command_description`、登録の仕組み、メニュー登録 |
| [イベントハンドラ](guides/events.md) | `scene_opened` などシーンイベントへのフック |
| [シーン変更モデル](guides/scene-modification.md) | `modify` / `modify_update` / `*_with_session` の違いと使い分け、Undo/Redo |
| [ビヘイビアとデータ](guides/behaviours-and-data.md) | オブジェクト・ビヘイビア・データ・設定の関係、読み書きの実践 |
| [UI・ダイアログ](guides/ui-dialogs.md) | 入力ダイアログ、ボタンダイアログ、ファイルダイアログ |
| [pycsc 高レベルAPI](guides/pycsc.md) | `DomainScene` / `TransformUpdate` / `run_update_session` による簡潔な記述 |
| [発展的なアドオン](guides/advanced-addons.md) | オブジェクト生成、アップデートグラフ構築、クラスタ、選択操作 |
| [FBX 入出力](guides/fbx-io.md) | FBX のインポート・エクスポート、設定 |
| [リギング](guides/rigging.md) | 自動リグ・リグ要素・T ポーズ関連 |

### 3. API リファレンス（モジュール別）

[API リファレンス目次](api/README.md) を参照してください。`csc` の全サブモジュールを網羅しています。

| モジュール | 役割 |
|---|---|
| [csc](api/csc.md) | トップレベル（`Guid` / `Version` / `Direction` など共通型） |
| [csc.app](api/app.md) | アプリケーション・各種マネージャ（エントリポイント `get_application`） |
| [csc.view](api/view.md) | ビュー層（`Scene` タブ、カメラ、ダイアログ） |
| [csc.domain](api/domain.md) | ドメインの `Scene`、選択、ピボット、`SceneUpdater` |
| [csc.model](api/model.md) | モデル層（Viewer/Editor、ビヘイビア、データ、設定） |
| [csc.layers](api/layers.md) | タイムライン・レイヤー・キー・補間 |
| [csc.math](api/math.md) | 数学型（行列・回転・クォータニオン）と関数 |
| [csc.parts](api/parts.md) | パーツ（プリセットオブジェクト）の挿入、クリップボード |
| [csc.fbx](api/fbx.md) | FBX ローダーと設定（`csc.external.fbx` 含む） |
| [csc.rig](api/rig.md) | リギング用データ構造 |
| [csc.tools](api/tools.md) | ツール（ミラー・アトラクタ・選択グループ・リグモード） |
| [csc.physics](api/physics.md) | 物理（`PosMass`） |
| [csc.update](api/update.md) | アップデートグラフ（ノード・グループ・データ・関数） |

### 4. 実例集

| ドキュメント | 内容 |
|---|---|
| [クックブック](cookbook.md) | 同梱サンプル・標準コマンドをテーマ別に解説 |

---

## 用語クイックリファレンス

| 用語 | 意味 |
|---|---|
| `csc` | C++ 実装のコンパイル済みコアモジュール（低レベル API） |
| `pycsc` | `csc` を Python で包んだ高レベルラッパー（任意利用） |
| Scene | シーン。`csc.view.Scene`（UIタブ）と `csc.domain.Scene`（中身）の2種類がある |
| Viewer | シーンを**読み取る**ためのオブジェクト（`ModelViewer` 等） |
| Editor | シーンを**書き換える**ためのオブジェクト（`modify` 内でのみ取得） |
| modify / modify_update | シーン変更を1つの Undo 単位として実行するトランザクション |
| Behaviour（ビヘイビア） | オブジェクトに付く機能部品（`Joint`、`Transform`、`MeshObject` など） |
| Data / Setting | ビヘイビアが参照する値（アニメ／静的）。フレーム単位で保持 |
| Update graph | オブジェクト内部の依存計算グラフ（`csc.update`） |
| Command | メニューから呼べるアドオン。`run(scene)` を持つモジュール |

---

> ⚠️ 注意: `csc` はコンパイル済みモジュールのため、シグネチャは Cascadeur のバージョンによって増減します。本ドキュメントは同梱の `samples/api_document.py` を基準にしています。実環境では `print(dir(csc.xxx))` や `help(...)` で最新の定義を確認してください。
