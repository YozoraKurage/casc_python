# csc.math

3D 数学の型と関数。トランスフォーム計算（位置・回転・行列）の中心です。値の多くは `numpy.ndarray[float32]`（ベクトルは `(3,)`、行列は `(3,3)` / `(4,4)`）です。

### 型
- [Rotation](#rotation) / [Quaternion](#quaternion) / [AngleAxis](#angleaxis) / [Affine](#affine)
- [OrthogonalTransform](#orthogonaltransform) / [ScaledTransform](#scaledtransform)
- [Plane](#plane) / [ParametrizedLine](#parametrizedline) / [Sphere](#sphere) / [Circle](#circle) / [Triangle](#triangle)
- [SizesInterval](#sizesinterval)

### 関数
- [変換](#変換関数) / [幾何](#幾何関数) / [変換ユーティリティ](#変換ユーティリティ関数)

---

## Rotation

オイラー角ベースの回転。Cascadeur のローカル/グローバル回転はこの型で扱われることが多い。

| 静的メソッド | 説明 |
|---|---|
| `from_euler(x, y, z)` | オイラー角から生成 |
| `from_angle_axis(angle, axis)` | 角度+軸から生成 |
| `from_quaternion(w, x, y, z)` | クォータニオン成分から生成 |
| `from_rotation_matrix(m3x3)` | 回転行列から生成 |

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `to_euler_angles_x_y_z()` | Vector3 | オイラー角へ |
| `to_angle_axis()` | `AngleAxis` | 角度+軸へ |
| `to_quaternion()` | `Quaternion` | クォータニオンへ |
| `to_rotation_matrix()` | 3x3行列 | 回転行列へ |

```python
import csc, numpy as np
r = csc.math.Rotation.from_euler(90, 45, 30)
q = r.to_quaternion()
m = r.to_rotation_matrix()
r2 = csc.math.Rotation.from_angle_axis(np.radians(90), np.array([0, 1, 0]))
```

---

## Quaternion

回転計算のためのクォータニオン。

| プロパティ | 型 | 説明 |
|---|---|---|
| `w`, `x`, `y`, `z` | `float` | 各成分 |

| メソッド / 静的 | 戻り値 | 説明 |
|---|---|---|
| `static from_two_vectors(v1, v2)` | `Quaternion` | 2ベクトル間の回転 |
| `static identity()` | `Quaternion` | 単位クォータニオン |
| `inverse()` | `Quaternion` | 逆 |

```python
q = csc.math.Quaternion.from_two_vectors(np.array([1,0,0]), np.array([0,1,0]))
qi = q.inverse()
```

---

## AngleAxis

回転を角度と軸で表す。

| プロパティ | 型 | 説明 |
|---|---|---|
| `angle` | `float` | 角度 |
| `axis` | Vector3 | 軸 |

---

## Affine

`AngleAxis` で定義されるアフィン変換。

| プロパティ | 型 | 説明 |
|---|---|---|
| `linear` | 3x3行列 | 線形部分 |

---

## OrthogonalTransform

位置 + 回転による直交変換。トランスフォーム計算の主役。

| プロパティ | 型 | 説明 |
|---|---|---|
| `position` | Vector3 | 位置 |
| `rotation` | `Rotation` | 回転 |

```python
ot = csc.math.OrthogonalTransform()
ot.position = obj_position
ot.rotation = obj_rotation.to_quaternion()
world = csc.math.transform_point(ot, [0.0, 50.0, 0.0])
```

> コンストラクタは `OrthogonalTransform(position, quaternion)` の形でも生成可能（リギング例で `csc.math.OrthogonalTransform(pos, rot.to_quaternion())`）。

---

## ScaledTransform

スケールを含む変換。

| メンバー | 型 | 説明 |
|---|---|---|
| `position` | Vector3 | 位置 |
| `rotation` | `Rotation` | 回転 |
| `scale` | Vector3 | スケール |

---

## Plane

法線と点で定義される平面。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `projection(point)` | Vector3 | 点を平面へ投影 |

コンストラクタ: `Plane(normal, point)`（例: `csc.math.Plane([1,0,0], [0,0,0])`）。

---

## ParametrizedLine

直線（パラメータ化）。

| メソッド | 戻り値 | 説明 |
|---|---|---|
| `projection(point)` | Vector3 | 点を直線へ投影 |

---

## Sphere

| プロパティ | 型 | 説明 |
|---|---|---|
| `center` | Vector3 | 中心 |
| `radius` | `float` | 半径 |

---

## Circle

球と法線で定義される円。

| プロパティ | 型 | 説明 |
|---|---|---|
| `sphere` | `Sphere` | 定義球 |
| `normal` | Vector3 | 法線 |

---

## Triangle

3点で定義される三角形。

| メンバー | 型 |
|---|---|
| `point1`, `point2`, `point3` | Vector3 |

---

## SizesInterval

整数区間。

| メソッド / 静的 | 戻り値 | 説明 |
|---|---|---|
| `static construct_in_right_order(first, second)` | `SizesInterval` | 正しい順序で構築 |
| `contains(i)` | `bool` | 含むか |
| `inside_interval_inclusive(n)` | `bool` | 包含（両端含む） |
| `empty()` | `bool` | 空か |
| `start()` / `end()` | `int` | 開始/終了 |
| `static intersect_intervals(a, b)` | `SizesInterval` | 交差 |
| `static union_overlaping_intervals(a, b)` | `SizesInterval` | 重なり結合 |

---

## 変換関数

| 関数 | 戻り値 | 説明 |
|---|---|---|
| `transform_point(transform, point)` | Vector3 | 点を変換（`OrthogonalTransform` または 4x4 行列） |
| `inverse_transform_point(transform, point)` | Vector3 | 逆変換で点を変換 |
| `transforms_difference(a, b)` | `OrthogonalTransform` | 2変換の差分（親子相対の算出に多用） |
| `modify_position_by_matrix(m3x3, position)` | Vector3 | 3x3行列で位置を変換 |
| `decompose_matrix(m4x4)` | `ScaledTransform` | 4x4行列を分解 |
| `basic_transform_from_triangle(triangle)` | `OrthogonalTransform` | 三角形から基準変換 |

```python
# ローカル→ワールド
world = csc.math.transform_point(ot, [0.0, 50.0, 0.0])
world = csc.math.transform_point(obj_matrix4x4, [0.0, 50.0, 0.0])
# ワールド→ローカル
local = csc.math.inverse_transform_point(ot, [0.0, 50.0, 0.0])
# 親子相対
diff = csc.math.transforms_difference(parent_tpose, child_tpose)
```

---

## 幾何関数

| 関数 | 戻り値 | 説明 |
|---|---|---|
| `line_on_intersection_planes(p1, p2)` | `Optional[ParametrizedLine]` | 2平面の交線 |
| `point_on_intersection_planes(p1, p2)` | `Optional[Vector3]` | 2平面の交点 |
| `project_point_on_basic_line(line_dir, point)` | Vector3 | 点を直線へ投影 |
| `spheres_intersection(s1, s2)` | `Optional[Circle]` | 2球の交差円 |
| `spheres_intersection_extended(s1, s2)` | `Optional[Circle]` | 拡張交差 |
| `ik_spline(start, points, quats, weights)` | `Tuple[List[Vector3], List[Quaternion]]` | IK スプライン |

---

## 変換ユーティリティ関数

| 関数 | 戻り値 | 説明 |
|---|---|---|
| `euler_angles_to_quaternion_x_y_z(euler)` | `Quaternion` | オイラー→クォータニオン |
| `quaternion_to_euler_angles_x_y_z(q)` | Vector3 | クォータニオン→オイラー |
| `euler_flip(e1, e2)` | `Rotation` | オイラー角のフリップ |
| `get_m3f_diag(m3x3)` | Vector3 | 3x3行列の対角成分 |
| `step_linear_func(start, end, pos)` | `float` | 線形ステップ関数 |

> このほか、リギング例では `csc.math.combine_transforms(a, b)`、`csc.math.untwist(a_matr, b_matr, weight, roll, axis, negate)` も使われています（[`commands/go_to_default_pose.py`](../cookbook.md)）。実環境の `dir(csc.math)` で最新の関数一覧を確認してください。

---

[← API 目次](README.md)
