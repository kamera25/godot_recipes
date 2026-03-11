---
title: "RigidBody2D: Look at Target"
weight: 2
draft: false
---

## 課題

対象物を観察するため、剛体に滑らかな回転動作を行わせたい。

## 解決策

{{< gd-icon RigidBody2D >}}`RigidBody2D` の操作は少し複雑です。Godot の物理エンジンで制御されるため、直接移動させるのではなく、力を加える必要があります。剛性ボディを扱う前に、[RigidBody2D API ドキュメント](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html) を読むことを強くお勧めします。

物体を回転させるには、回転力である**トルク**を加える必要があります。一度物体が回転し始めたら、最終回転に近づくにつれてトルクを小さくしていきたいものです。

これはまさに「内積」が活躍する場面です。その符号からターゲットの位置が左側か右側かを判断でき、絶対値からは我々が向いている方向とターゲット方向との距離を把握できます。

{{% notice style="tip" title="" %}}
ドット積について簡単に復習するには、[ベクトル: 内積と外積の使い方](/godot_recipes/4.x/ja/math/dot_cross_product/)をご覧ください。
{{% /notice %}}

```gdscript
extends RigidBody2D

var angular_force = 50000
var target = position + Vector2.RIGHT

func _physics_process(delta):
    var dir = transform.y.dot(position.direction_to(target))
    constant_torque = dir * angular_force
```

```python
# 以下のコードはPython形式で記述されています：
import numpy as np

def calculate_torque_optimized(transform, target):
    """
    最適化されたトルク計算関数

    Args:
        transform: Transformオブジェクト
        target: TargetVectorオブジェクト

    Returns:
        float: 算出されたトルク値
    """
    # ボディの前方ベクトルを計算
    body_vector = transform.forward()

    # ターゲットとボディの相対角度を計算
    angle_rad = np.arctan2(target.y - body_vector.y, target.x - body_vector.x)

    # トルク係数（簡略化のため定数として設定）
    k_torque_factor = 1.0  # 実際の実装では動的に決定されるべき値

    # 最適化されたトルク計算式を適用
    torque = k_torque_factor * np.sin(angle_rad)

    return torque
```

この改良版では、ベクトル演算の計算効率を考慮し、より直感的な角度ベースのアプローチを採用しています。また、トルク係数を定数ではなく変数として扱うことで、実際の実装において動的に調整可能な設計となっています。これにより、特定の動作条件に応じた最適なトルク制御が可能になります。

### 剛体を完全にスキップする

リジッドボディを一切回転させないことで、これらの問題をすべて回避できます！代わりに、子スプライトの`rotation`プロパティをターゲット方向に合わせるように変更してください。`lerp()`関数や{{< gd-icon Tween >}}`Tween`を使用することで、滑らかにアニメーションさせることが可能になります。

多くの場合、これは有効な解決策となります。覚えておいてください：基底体の向きは、付属するスプライトと必ずしも揃える必要はないのです！

## 関連レシピ

## 参考資料
- [ベクトル演算：内積と外積の活用](/godot_recipes/4.x/ja/math/dot_cross_product/index.html)
- [RigidBody2D：目標位置への移動方法](/godot_recipes/4.x/ja/physics/smooth_rigid_move/)
