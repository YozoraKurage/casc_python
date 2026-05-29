# 概要 — Cascadeur Python API とは

Cascadeur は Python による拡張（アドオン／スクリプト）に対応しており、アプリ内のほぼすべての操作 — シーンの読み取り、オブジェクトの生成・編集、アニメーションのキー操作、リギング、FBX 入出力、UI ダイアログ表示 — を Python から自動化できます。

このページでは、API の全体像と「どこに何があるか」を把握します。

---

## 1. 2層構造: `csc` と `pycsc`

Cascadeur の Python API は大きく2層に分かれています。

```
┌─────────────────────────────────────────────┐
│  あなたのアドオン / スクリプト                  │
├──────────────────────┬──────────────────────┤
│   pycsc（高レベル）    │   common（ヘルパー群） │  ← Python製・読みやすい
│   DomainScene 等       │   selection_operations 等 │
├──────────────────────┴──────────────────────┤
│   csc（低レベル・コア）                          │  ← C++製コンパイル済み
│   csc.app / csc.view / csc.model / csc.domain  │
│   csc.layers / csc.math / csc.update ...        │
└─────────────────────────────────────────────┘
```

### `csc` — コアモジュール（低レベル）

- C++ で実装され、Cascadeur 本体に**コンパイル済みモジュール**として組み込まれています（`.pyd` / `.so`）。
- すべての機能の土台。`import csc` で利用できます。
- ソースは見られませんが、API は同梱の [`samples/api_document.py`](getting-started.md) に全クラス・メソッド・enum と使用例の形でまとまっています（本ドキュメントの API リファレンスはこれを再構成したものです）。
- サブモジュール: `app` / `view` / `model` / `domain` / `layers` / `math` / `parts` / `fbx` / `external.fbx` / `rig` / `tools` / `physics` / `update`。

### `pycsc` — Python ラッパー（高レベル・任意）

- `csc` を Python で包んだ、より読み書きしやすい API。`import pycsc` で利用します。
- `DomainScene`、`ObjectNode`、`TransformUpdate` などのクラスや、`@pycsc.run_update_session` デコレータでボイラープレートを削減します。
- 標準コマンドの一部（例: [`commands/go_to_default_pose.py`](cookbook.md)）も pycsc を使って書かれています。
- 必須ではありません。`csc` だけでもすべて記述できます。詳細は [pycsc ガイド](guides/pycsc.md)。

### `common` — ヘルパー関数群

- `selection_operations`（選択）、`math_operations`（行列変換）、`update_operations`（グラフ接続）など、よく使う処理をまとめた Python モジュール。
- 標準コマンドが内部利用しています。自作アドオンからも `import common.xxx` で使えます。

---

## 2. スクリプトの配置場所

標準のスクリプトはインストール先に置かれています（**読み取り専用**として扱うこと）。

```
C:\Program Files\Cascadeur\resources\scripts\
├── README.md
├── python\                ← Python パッケージのルート（import の基点）
│   ├── csc（コンパイル済みコアモジュール。本体に内蔵）
│   ├── pycsc\             ← 高レベルラッパー
│   ├── common\            ← ヘルパー群
│   ├── commands\          ← 標準コマンド（アドオンの実例集）
│   ├── events\            ← イベントハンドラ
│   ├── samples\           ← サンプルスクリプト（api_document.py を含む）
│   ├── add_function\      ← オブジェクト生成の例
│   ├── rig_gen\ rig_gen2\ rigging\  ← リギング関連
│   ├── prototypes\        ← アクション・プロトタイプ
│   ├── commands_rule.py   ← コマンド自動検出ロジック
│   └── events_rule.py     ← イベント自動検出ロジック
├── parts\                 ← 挿入可能なプリセットオブジェクト(.partscasc)
└── python_api_doc\        ← Sphinx ドキュメント生成設定
```

> 自作コマンドを本番運用する際は、`resources\scripts`（= `Program Files` 配下）を直接編集せず、ユーザー用フォルダ `<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands` に置きます。本作業フォルダの `scripts/` はあくまで「解析・ドキュメント化のためのコピー」です（公式: [Python scripting in Cascadeur](https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur)）。

---

## 3. アドオンの3つの形態

| 形態 | 何を書くか | どこに置くか | 起動契機 |
|---|---|---|---|
| **コマンド** | `run(scene)` を持つモジュール（任意で `command_name()` / `command_description()`） | ユーザー `scripts/python/commands/` | `Commands` メニューから実行 |
| **イベントハンドラ** | `run(scene)` を持つモジュール | `events/<イベント名>/` 配下 | シーンの作成・オープン・保存などで自動実行 |
| **スクリプト** | 任意の関数 | `samples/` など任意 | アプリ内の Python 実行機能から手動呼び出し |

詳しくは [アドオンの基本](guides/addon-basics.md) を参照。

---

## 4. Python から何ができるか（代表例）

- **シーン情報の取得**: オブジェクト一覧、ジョイント、メッシュ統計、選択状態、現在フレーム
- **オブジェクトの生成・削除・親子付け**: ジョイント、ロケーター、ボックス、メッシュ、リグ要素
- **アニメーション編集**: キーの追加・移動、補間・接線、レイヤー、サイクル
- **トランスフォーム操作**: グローバル/ローカルの位置・回転・スケール、ミラー、T ポーズへのリセット
- **リギング**: 自動リグ、リグ要素の追加、IK/FK、コンストレイント
- **入出力**: FBX のインポート／エクスポート（モデル・アニメ・シーン）、独自エクスポータ（Roblox, Daz などの実例あり）
- **UI**: 入力ダイアログ、ボタンダイアログ、ファイル選択ダイアログ、ログ出力（info/warning/error）
- **物理**: 重心・物理計算の補助

---

## 5. 最重要の心構え

Cascadeur の API を理解する上で最初に押さえるべき3点:

1. **読み取りは Viewer、書き込みは Editor**
   シーンを読むには `model_viewer()` などの **Viewer** を使い、書き換えるには `modify(...)` の中で取得する **Editor** を使います。

2. **変更は必ず `modify` / `modify_update` トランザクション内で**
   オブジェクトやデータの変更は `scene.modify_update("名前", 関数)` のようなトランザクションでくるみます。これが Undo/Redo の1単位になります。

3. **値はフレーム単位、計算はアップデートグラフ**
   位置・回転などの値（Data）はフレームごとに保持され、オブジェクト内部の依存グラフ（**Update graph**）によって再計算されます。値を変えたら `run_update(...)` で再計算を促します。

この3点の詳細は [アーキテクチャ](architecture.md) で解説します。

---

次へ: [はじめに（実行方法）](getting-started.md)
