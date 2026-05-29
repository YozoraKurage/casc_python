# api_docs — Cascadeur API ドキュメントの定期ダンプ & 差分ツール

`https://cascadeur.com/python-api/` を定期的にミラーし、**前回との差分**を出して、
その差分を起点に `docs/` を AI に整理させるためのツールチェインです。

```
check.py    変更検知(HEADのみ・軽量) -> 変化があったページを列挙（任意で更新を自動起動）
dump.py     生HTMLをDL           -> docs/api-reference/raw-html/  (+ manifest.json)
convert.py  HTML -> Markdown      -> docs/api-reference/<module>/*.md (+ _index.md)
diff.py     前回スナップショットと比較 -> CHANGELOG.md に追記 (+ 任意でJSON)
snapshots/  各回の生HTMLを日時別保存（diff の比較基準）
```

すべて **Python 3 標準ライブラリのみ**（外部依存なし）。Cascadeur 本体は不要
（ツールはウェブサイトだけを触る。`csc` は import しません）。

> **「Cascadeurは更新を通知してくれる？」→ いいえ。** ドキュメントはアプリ機能ではなく
> ただのWebサイトなので、アプリからのプッシュ通知はありません。ただしサーバーが
> `ETag` / `Last-Modified` ヘッダを返すため、`check.py` が **HEADリクエストだけ**で
> 「変わったか?」を判定できます（全文DL不要・軽量）。これを定期実行すれば、実質的に
> 「更新があったときだけ」ダンプを走らせられます。

---

## いちばん簡単な定期運用（変更があったときだけ更新）

```bash
cd tools/api_docs
python check.py --run-dump
```

`check.py` が各ページに HEAD を投げ、前回ダンプ（`manifest.json` の ETag/Last-Modified）と
比較します。**変化が無ければ何もしません**。変化があれば自動で
`dump --snapshot → convert → diff` を実行し、差分を `CHANGELOG.md` に記録します。

これを OS のタスクスケジューラ / cron に「毎日」などで登録すれば、ほぼ放置で追従できます。
（`check.py` は変更検知時に終了コード 10 を返すので、CI で「10 のときだけダンプ」も可能。）

```powershell
# Windows タスクスケジューラ登録例（毎日 9:00）
schtasks /Create /SC DAILY /ST 09:00 /TN "CascadeurApiCheck" ^
  /TR "python \"D:\YozoLab\VSCode\_Claude\casc_python\tools\api_docs\check.py\" --run-dump"
```

---

## 手動フルワークフロー（明示的に全部回す）

```bash
cd tools/api_docs

# 0.（任意）まず変更があるか軽くチェック
python check.py

# 1. 最新を取得（ページ集合が変わっていてもいいよう一覧も更新）。取得物をスナップショット保存。
python dump.py --refresh-list --snapshot

# 2. Markdown を再生成（docs/api-reference/ を上書き）
python convert.py

# 3. 前回スナップショットとの差分を CHANGELOG.md に追記 + AI 用 JSON を出力
python diff.py --json last-diff.json
```

`diff.py` は新旧スナップショットを比較し、**追加/削除/変更されたページ**と、
変更ページ内の**追加/削除されたメソッド・プロパティ・enum メンバー**を一覧化して
`CHANGELOG.md` 先頭に日付付きで追記します。各エントリ末尾の `TODO(AI)` 行が、
ドキュメント整理の起点です。

> 初回（ベースライン）は既に作成済み: 生HTML・md・初回スナップショットが揃っています。
> 2回目以降に上記を回すと差分が出ます。

---

## AI にドキュメント整理を頼むときの定型

`diff.py` 実行後、次のように依頼すると差分ベースで更新できます。

> 「`tools/api_docs/CHANGELOG.md` の最新エントリ（と `last-diff.json`）を見て、
> 変わった分だけ `docs/api-reference/`（公式クローン）と `docs/api/`・`docs/guides/`・
> `docs/cookbook.md`（手書き）を更新して。新規ページはガイドへの導線も足して。」

差分が「無し」のときは何もする必要がありません。

---

## 各スクリプトの詳細

### check.py（変更検知・高速 ~1秒）
```bash
python check.py                 # index.html 1個のETagでサイト再ビルドを判定（約1秒）
python check.py --inventory     # objects.inv も取得し、追加/削除ページを列挙
python check.py --run-dump      # 変化があれば自動で dump→convert→diff を実行
python check.py --manifest PATH # 比較元の manifest.json を指定
```
- **1〜2リクエストで完了**。サイトは Sphinx の一括ビルドで全ページの `Last-Modified` が
  同一になるため、`index.html` の ETag/Last-Modified を見れば「どれか1ページでも変わったか」が分かる。
- ページの増減は `objects.inv`（全シンボル一覧・16KB）の差分で検出（`--inventory` または変更検知時に自動）。
- 終了コード: `0`=変化なし / `10`=変化あり（スケジューラ/CIのトリガ用）/ `2`=baseline無し。
- ⚠️ 209ページを個別に叩く実装は**遅い（数分）**ので不可。必ず index + objects.inv 方式で。

### dump.py
```bash
python dump.py                  # pages.txt のページを raw-html/ にDL
python dump.py --refresh-list   # 先に公式 genindex/csc から全ページ集合を再取得
python dump.py --snapshot       # 取得物を snapshots/<UTC日時>/raw-html/ にも保存
python dump.py --out PATH       # 出力先を変更
```
- `manifest.json`（各ページの sha256 とサイズ）を書き出し、`diff.py` が高速比較に使う。
- `pages.txt` は対象ページ一覧（1行=1ドット名）。`--refresh-list` で自動更新。

### convert.py
```bash
python convert.py               # raw-html/ -> docs/api-reference/<module>/*.md
python convert.py --only csc.app    # 一部だけ再変換
python convert.py --no-index    # _index.md を書かない
```
- Sphinx 構造（`py class`/`py method`/`py property`/`highlight`）を解析して md 化。
- enum は `## Members`（整数値付き）、メソッドは完全シグネチャ＋説明/戻り値、コード例は ```python ブロックで保持。
- 生HTMLは常に残るので、変換ロジックを改善したらいつでも再変換できる。

### diff.py
```bash
python diff.py                       # 最新スナップショット vs 現在の raw-html
python diff.py --old DIR --new DIR   # 明示比較
python diff.py --json report.json    # 機械可読の差分も出力
python diff.py --no-changelog        # CHANGELOG.md を触らない（確認だけ）
```
- ページ単位（sha256）＋メンバー単位（メソッド/プロパティ/enum 名）で差分を出す。
- pybind ボイラープレート（`__init__`/`name`/`value` 等）は除外して signal を保つ。

---

## フォルダ構成

```
tools/api_docs/
├── dump.py          生HTML取得
├── convert.py       HTML -> Markdown
├── diff.py          差分検出 + CHANGELOG追記
├── pages.txt        対象ページ一覧（209）
├── CHANGELOG.md     差分の履歴（diffが追記）
├── snapshots/       各回の生HTMLダンプ（日時別。比較基準。容量大）
└── README.md        このファイル
```

出力先（別ツリー）:
```
docs/api-reference/
├── raw-html/        最新の生HTML（manifest.json 同梱）
├── <module>/*.md    変換後Markdown（csc, app, view, model, ... の14フォルダ）
└── README.md        クローン版の索引
```

---

## 注意

- `snapshots/` は回数分の生HTMLが溜まるため容量が増えます。古いものは削除可（直近1〜2回あれば差分は取れる）。git に含めたくない場合は `.gitignore` で `tools/api_docs/snapshots/` を除外してください。
- 公式サイトのHTML構造が将来変わると `convert.py` の調整が必要になる場合があります。生HTMLは保持しているので、`convert.py` を直して再変換すれば追従できます。
- 対象バージョン基準: Cascadeur v2026.1.2（2026-05 時点の公式サイト）。
