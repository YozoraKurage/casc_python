# Cascadeur Python API リファレンス（公式サイト クローン）

公式の自動生成APIドキュメント <https://cascadeur.com/python-api/> を **1ページ=1md** で丸ごとクローンしたものです。各 `csc.*` クラス／関数ページを Markdown 化しています。

> - 取得元: `https://cascadeur.com/python-api/_generate/<名前>.html`
> - 対象バージョン: Cascadeur v2026.1.2（2026-05時点の公式サイト）
> - これは**公式ページの忠実な写し**です。日本語の解説・ガイドは [../README.md](../README.md)（手書きドキュメント）を参照してください。
> - `csc` はコンパイル済みモジュールのため、実環境では `dir()` / `help()` も併用してください。
>
> **更新方法**: このフォルダは [`tools/api_docs/`](../../tools/api_docs/README.md) のツールチェイン（dump → convert → diff）で生成・更新します。定期ダンプして差分を `tools/api_docs/CHANGELOG.md` に記録し、それを起点にドキュメントを整理する運用です。生HTMLは [`raw-html/`](raw-html/) に保持。

## モジュール別インデックス

| モジュール | 内容 | フォルダ |
|---|---|---|
| `csc` | トップレベル共通型（Guid/Version/Direction 等） | [csc/](csc/) |
| `csc.math` | 数学型・関数 | [math/](math/) |
| `csc.physics` | 物理（PosMass, inertia_tensor） | [physics/](physics/) |
| `csc.parts` | パーツ挿入・クリップボード | [parts/](parts/) |
| `csc.fbx` | FBX ローダー・設定 | [fbx/](fbx/) |
| `csc.external` | FBX 付加データ | [external/](external/) |
| `csc.view` | ビュー・ダイアログ・カメラ | [view/](view/) |
| `csc.app` | アプリ・各種マネージャ（StatusManager 等） | [app/](app/) |
| `csc.tools` | ツール（mirror/attractor/selection 等） | [tools/](tools/) |
| `csc.rig` | リギング用データ | [rig/](rig/) |
| `csc.layers` | タイムライン・レイヤー | [layers/](layers/) |
| `csc.model` | モデル（Viewer/Editor/ビヘイビア/データ） | [model/](model/) |
| `csc.domain` | ドメイン（Scene/選択/アセット 等） | [domain/](domain/) |
| `csc.update` | アップデートグラフ | [update/](update/) |

各フォルダ内の `_index.md` にそのモジュールのクラス一覧があります。
