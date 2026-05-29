---
name: update-api-docs
description: Cascadeur 公式 Python API ドキュメント(https://cascadeur.com/python-api/)の更新を検知し、変化があればダンプ・md再生成・差分記録を行い、その差分を起点に docs/ を整理する。「APIドキュメントを更新」「Cascadeur APIの差分」「公式ドキュメントが変わったか確認」などのときに使う。
argument-hint: "[check | update | apply]"
---

# Cascadeur API ドキュメント更新

`tools/api_docs/` のツールチェイン（check → dump → convert → diff）を使って、
公式 API サイトの変更を取り込み、`docs/` を最新化する。スクリプトは Python 標準
ライブラリのみ・Cascadeur 不要。重い処理はスクリプトに任せ、ここでは判断と
ドキュメント反映を行う。

## 引数（`$ARGUMENTS`）

- `check`（既定 / 引数なし）: 変更があるかだけ高速確認（約1秒・1リクエスト）。
- `update`: 変更があればダンプ＋md再生成＋差分記録まで実行（docs本文の整理はしない）。
- `apply`: `update` に加えて、差分（CHANGELOG最新エントリ）を起点に docs を整理する。

## 手順

### 1. まず変更検知（必ず最初に。軽い）

```bash
python tools/api_docs/check.py --inventory
```

- 終了コード `0` = 変更なし、`10` = 変更あり、`2` = ベースライン無し。
- 出力の `baseline index` と `live index` の etag/lm、`inventory: +N/-N pages` を読む。
- **変更が無ければここで終了**。ユーザーに「変更なし（サイトのビルド時刻が前回ダンプと同じ）」と簡潔に報告する。
- 引数が `check` のときは、結果を報告して終了。

### 2. 変更があり、引数が `update` または `apply` のとき: フル更新

```bash
python tools/api_docs/check.py --run-dump
```

これは内部で `dump.py --refresh-list --snapshot` → `convert.py` → `diff.py --json last-diff.json`
を実行し、次を更新する:
- `docs/api-reference/raw-html/`（最新の生HTML + manifest.json）
- `docs/api-reference/<module>/*.md`（再生成）
- `tools/api_docs/CHANGELOG.md`（差分を日付付きで追記。末尾に TODO(AI) 行）
- `tools/api_docs/last-diff.json`（機械可読の差分）
- `docs/api-reference/raw-html/objects.inv`（次回比較用キャッシュ）

完了後、`CHANGELOG.md` の最新エントリと `last-diff.json` を読んで、何が
追加/削除/変更されたかをユーザーに要約する。

### 3. 引数が `apply` のとき: docs への反映

`last-diff.json`（added / removed / changed_members）を見て、**変わった分だけ**反映する:

- **公式クローン版** `docs/api-reference/` は手順2で自動再生成済み。内容を確認するだけ。
- **手書き版** `docs/api/<module>.md`: 追加クラス/メソッドの追記、削除分の除去、シグネチャ変更の修正。
- **ガイド/クックブック** `docs/guides/*.md`, `docs/cookbook.md`: 新APIに関連する箇所があれば導線・例を追加。
- 反映後、`docs` 全体の相対リンクが壊れていないか確認（必要なら簡易チェック）。
- 大きな変更は要点をユーザーに提示し、判断が要るものは確認する。

## 注意

- `check.py` は **index.html 1ページの ETag/Last-Modified** でサイト全体の再ビルドを判定する
  （サイトは一括ビルドなので全ページの Last-Modified が同一）。209ページを個別に叩かない。
- ページの増減は `objects.inv`（Sphinxインベントリ）の差分で検出する。
- `tools/api_docs/snapshots/` と `last-diff.json` は `.gitignore` 済み。
- 詳細は `tools/api_docs/README.md` を参照。
