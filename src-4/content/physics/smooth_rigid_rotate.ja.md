---
title: "RigidBody2D：対象物を見る"
weight: 2
draft: false
---

## 課題

対象物を観察するため、剛体に滑らかな回転動作を行わせたい。

## 解決策

{{< gd-icon RigidBody2D >}}`RigidBody2D` の操作は少し複雑です。Godot の物理エンジンで制御されるため、直接移動させるのではなく、力を加える必要があります。剛性ボディを扱う前に、[RigidBody2D API ドキュメント](https://docs.godotengine.org/ja/stable/classes/class_rigidbody2d.html) を読むことを強くお勧めします。

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

ここで`transform.y`を使用している理由について疑問に思われるかもしれません。というのも、`transform.x`はボディの前方ベクトルを表すからです。もし`transform.x`を使用していれば、ドット積が最大となるのはボディが完全にターゲット方向を向いている時になりますが、その時点でトルク値をゼロにしたいと考えています。一方、`transform.y`を使用することで、ターゲット方向に完全に揃っていない状態ほどトルク値が増加するようになります。

### 剛体を完全にスキップする

リジッドボディを一切回転させないことで、これらの問題をすべて回避できます！代わりに、子スプライトの`rotation`プロパティをターゲット方向に合わせるように変更してください。`lerp()`関数や{{< gd-icon Tween >}}`Tween`を使用することで、滑らかにアニメーションさせることが可能になります。

多くの場合、これは有効な解決策となります。覚えておいてください。基底体の向きは、付属するスプライトと必ずしも揃える必要はないのです！

## 関連レシピ

## 参考資料
- [ベクトル演算：内積と外積の活用](/godot_recipes/4.x/ja/math/dot_cross_product/index.html)
- [RigidBody2D：目標位置への移動方法](/godot_recipes/4.x/ja/physics/smooth_rigid_move/)
