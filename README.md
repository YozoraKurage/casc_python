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
├── batch_export_fbx/  ← 自作ツール: .casc 一括 FBX 書き出し（git 管理対象）
├── tools/
│   └── api_docs/      ← 公式API定期ダンプ&差分ツール（dump/convert/diff）
└── scripts/           ← Cascadeur 同梱スクリプトのコピー（解析用・git 管理対象外）
    ├── python/        ← csc(内蔵) / pycsc / common / commands / events / samples ...
    ├── parts/         ← プリセットオブジェクト(.partscasc)
    └── python_api_doc/← Sphinx 設定
```

> API ドキュメントの更新（定期ダンプ→差分→整理）は [tools/api_docs/](tools/api_docs/README.md) を参照。

> 実ファイルは `C:\Program Files\Cascadeur\resources\scripts`（読み取り専用）。`scripts/` はその解析用コピーで、**git 管理対象外**（`.gitignore`）です。自作ツール [batch_export_fbx/](batch_export_fbx/README.md) はリポジトリ最上階に置いています。

## 🔗 公式情報源

- Python スクリプティング解説: <https://cascadeur.com/help/tools/animation_tools/python_scripting_in_cascadeur>
- Python API（HTML 自動生成）: <https://cascadeur.com/python-api/>
- ヘルプ全般: <https://cascadeur.com/help/category/215>
