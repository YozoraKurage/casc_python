# csc（トップレベル）

`csc` 直下に定義される共通型です。ID・バージョン・方向などの基本的な値型が中心です。

- [Direction](#direction)
- [DirectionValue](#directionvalue)
- [Guid](#guid)
- [SystemVariables](#systemvariables)
- [Version](#version)

> サブモジュール（`csc.app`, `csc.model` など）は [API 目次](README.md) から各ページへ。

---

## Direction

方向を扱うクラス。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `inverse()` | `csc.DirectionValue` | 反対方向を返す |
| `value()` | `csc.DirectionValue` | 現在の方向値を返す |
| `to_string()` | `str` | 文字列表現 |

```python
import csc
d = csc.Direction(csc.DirectionValue.In)
print(d.value())
```

---

## DirectionValue

方向を表す列挙型（enum）。

| メンバー | 値 |
|---|---|
| `In` | 0 |
| `Out` | 1 |
| `Unknown` | 2 |

プロパティ: `name`（名前）、`value`（整数値）。

```python
print(csc.DirectionValue.In)         # DirectionValue.In
print(csc.DirectionValue.In.value)   # 0
```

---

## Guid

シーン内のオブジェクト・ビヘイビア・アセットなどを一意に識別する GUID。`csc` 全体で多用されます（ビヘイビア ID は `Guid`）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `is_null()` | `bool` | null GUID か判定 |
| `static null()` | `csc.Guid` | null GUID を返す |
| `to_string()` | `str` | 文字列表現 |

```python
null_guid = csc.Guid.null()
if null_guid.is_null():
    print("null GUID")

new_guid = csc.Guid()                # 新規 GUID 生成
print(new_guid.to_string())
```

> 新規生成 `csc.Guid()` はユニークな ID を作るため、オブジェクト名の自動生成などにも使われます（例: `name = csc.Guid().to_string()`）。

---

## SystemVariables

Cascadeur のビルド情報（git）を取得する静的メソッド群。

| 静的メソッド | 戻り値 | 説明 |
|---|---|---|
| `git_count()` | `str` | コミット数 |
| `git_date()` | `str` | 日付 |
| `git_sha()` | `str` | SHA ハッシュ |
| `git_version()` | `str` | バージョン |

```python
print(csc.SystemVariables.git_sha())
print(csc.SystemVariables.git_version())
```

---

## Version

バージョン情報（メジャー・マイナー・パッチ）を扱う。

| プロパティ | 型 |
|---|---|
| `major` | `int` |
| `minor` | `int` |
| `patch` | `int` |

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `to_string()` | `str` | `"4.2.1"` 形式へ |
| `static from_string(s)` | `csc.Version` | 文字列から生成 |

```python
v = csc.Version.from_string("4.2.1")
print(v.major, v.minor, v.patch)   # 4 2 1
print(v.to_string())               # 4.2.1
```

---

[← API 目次](README.md)
