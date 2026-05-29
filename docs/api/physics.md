# csc.physics

物理計算で使われる小さなデータ構造です。

---

## PosMass

質量と位置を持つ構造体。重心計算などで利用されます。

| メンバー | 型 | 説明 |
|---|---|---|
| `mass` | `float` | 質量 |
| `position` | Vector3f | 位置 |

```python
import csc
pm = csc.physics.PosMass()
pm.mass = 1.0
pm.position = [0.0, 0.0, 0.0]
```

> 重心関連の実処理は `commands/center_of_mass/`、`rig_gen2/center_of_mass/` も参照（[クックブック](../cookbook.md) / [リギング](../guides/rigging.md)）。

---

[← API 目次](README.md)
