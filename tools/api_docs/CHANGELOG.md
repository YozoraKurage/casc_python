# Cascadeur Python API ドキュメント 変更履歴

ダンプ間の差分を新しい順に記録する（`diff.py` が自動追記）。各エントリの末尾に
`TODO(AI)` 行が付くので、それを起点に docs/ を更新する。

## 2026-05-30 — 初回ダンプ（ベースライン）

- `https://cascadeur.com/python-api/` の全 209 ページを取得し、Markdown 化（`docs/api-reference/`）。
- 生 HTML 全 213 ファイルを `docs/api-reference/raw-html/` に保持。
- 初回スナップショットを `tools/api_docs/snapshots/` に保存（次回ダンプの比較基準）。
- 以降は `python diff.py` が前回スナップショットとの差分をこの下に追記する。
