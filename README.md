# vibe codingだよ

# casc_python — Cascadeur Python アドオン作業場

Cascadeur の Python アドオン開発のための作業フォルダです。

> **対象バージョン**: このドキュメントは **Cascadeur v2026.1.2**（2026-05-29 時点の最新）に基づいています。`csc` はコンパイル済みモジュールのため、API のメンバーや UI の名称はバージョンにより増減・変更されることがあります。最終的には実環境で `dir(...)` / `help(...)` や公式ヘルプで確認してください。

## 📚 ドキュメント

非公式・包括的な日本語ドキュメントを [`docs/`](docs/README.md) に整備しています。

**➡️ まずは [docs/README.md](docs/README.md) を開いてください。**

- [概要](docs/overview.md) / [はじめに](docs/getting-started.md) / [アーキテクチャ](docs/architecture.md)
- ガイド: [アドオンの基本](docs/guides/addon-basics.md)・[コマンド](docs/guides/commands.md)・[イベント](docs/guides/events.md)・[シーン変更](docs/guides/scene-modification.md)・[ビヘイビア/データ](docs/guides/behaviours-and-data.md)・[UI](docs/guides/ui-dialogs.md)・[pycsc](docs/guides/pycsc.md)・[発展](docs/guides/advanced-addons.md)・[FBX](docs/guides/fbx-io.md)・[リギング](docs/guides/rigging.md)
- [API リファレンス](docs/api/README.md)（`csc` 全モジュール網羅）
- [クックブック](docs/cookbook.md)（サンプル・標準コマンド解説）

## 📁 フォルダ構成

```
casc_python/
├── README.md          ← このファイル
├── docs/              ← 日本語ドキュメント（本体）
│   ├── api/           ← 手書きAPIリファレンス（要点・解説）
│   └── api-reference/ ← 公式サイトのクローン（全209ページ md + raw-html ダンプ）
├── commands/
│   └── yozolab/       ← 自作コマンドの名前空間（インストール先と同じ構成）
│       └── batch_export_fbx/  ← .casc 一括 FBX 書き出し（GUIコマンド）
├── tools/
│   └── api_docs/      ← 公式API定期ダンプ&差分ツール（dump/convert/diff）
└── scripts/           ← Cascadeur 同梱スクリプトのコピー（解析用・git 管理対象外）
    ├── python/        ← csc(内蔵) / pycsc / common / commands / events / samples ...
    ├── parts/         ← プリセットオブジェクト(.partscasc)
    └── python_api_doc/← Sphinx 設定
```

> API ドキュメントの更新（定期ダンプ→差分→整理）は [tools/api_docs/](tools/api_docs/README.md) を参照。

> 実ファイルは `C:\Program Files\Cascadeur\resources\scripts`（読み取り専用）。`scripts/` はその解析用コピーで、**git 管理対象外**（`.gitignore`）です。自作コマンドは [commands/yozolab/](commands/yozolab/) 名前空間（インストール先と同じ構成）に置いています（例: [batch_export_fbx](commands/yozolab/batch_export_fbx/README.md)）。

## 🧩 commands（自作コマンド）の使い方

自作コマンドはすべて **`commands/yozolab/<機能名>/`** に置いています。Cascadeur は
`commands/` 配下を再帰スキャンし、`run(scene)` を持つモジュールを `Commands` メニューへ
自動登録します（メニュー表示名は各コマンドの `command_name()` のドット区切りで決まる）。

### インストール（基本は yozolab フォルダをコピペするだけ）

このリポジトリの **`commands/yozolab/` フォルダごと**、Cascadeur のコマンドフォルダにコピーします。

```
コピー元: casc_python/commands/yozolab/
コピー先: C:\Program Files\Cascadeur\resources\scripts\python\commands\yozolab\
```

その後、Cascadeur で **`Commands > Reload scripts`**（または再起動）。これで
`commands/yozolab/` 配下の全コマンドがメニューに出ます。新しい機能を足したいときも、
`yozolab/` を上書きコピーするだけです。

> 配置先は、書き込み権限のある **ユーザースクリプトフォルダ**
> `<Cascadeurインストールフォルダ>\users\<ユーザー名>\scripts\python\commands\yozolab\`
> でも構いません（公式の推奨はこちら）。どちらか一方に置きます。

### 更新するとき（先に yozolab フォルダを消す）

**更新は「上書き」ではなく、いったん削除してから入れ直す**のが安全です。古いファイルの
残骸（リネーム前の `.py`、不要になったサブフォルダ等）が残ると、二重登録やエラーの原因に
なります。

1. コピー先の **`commands\yozolab\` フォルダを丸ごと削除**
2. 新しい `commands/yozolab/` をコピー
3. `Commands > Reload scripts`（または再起動）

### 自作コマンドを作るときの決まり

- **置き場所**: `commands/yozolab/<機能名>/`（さらにサブフォルダで階層化も可）。
- **各フォルダに `__init__.py` 必須**（無いとそのフォルダはスキャンされない）。
- **名前は Python 識別子**（ASCII 英数字と `_`。スペース・ハイフン・日本語・先頭数字は不可）。
- **`.py` の中身は ASCII のみ**（日本語コメントを入れると Cascadeur のローダが
  `UnicodeDecodeError` で読み込みに失敗する）。日本語の説明は `README.md` 等の
  import されないファイルに置く。
- **コマンド本体**は `run(scene)` を定義（任意で `command_name()` / `command_description()`）。
- メニューの階層は `command_name()` のドット（例 `"Export.Batch casc to FBX"`）で決まる。

## 🔗 公式情報源

- Python スクリプティング解説: <https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur>
- Python API（HTML 自動生成）: <https://cascadeur.com/python-api/>
- ヘルプ全般: <https://cascadeur.com/help/category/215>
