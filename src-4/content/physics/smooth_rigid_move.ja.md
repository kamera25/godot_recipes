---
title: "RigidBody2D: Move to Target"
weight: 3
draft: false
---

## 問題文

rigidbodyを目標位置へ移動させたい。

## 解決策

{{< gd-icon RigidBody2D >}}`RigidBody2D` の操作は少し複雑です。Godot の物理エンジンで制御されるため、直接移動させるのではなく、力を加える必要があります。剛性ボディを扱う前に、[RigidBody2D API ドキュメント](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html) を読むことを強くお勧めします。

物体を移動させるには、特定の方向に力を加える必要があります - これが「*力*」です。物体が動き始めたら、最終位置に近づくにつれてこの力は徐々に小さくなるようにします。

```python
# ベクトル間の距離計算関数を使用します
dist = Vector2.distance_to(target_vector, player_velocity)
print(\, dist)
```


```gdscript
# Smoothly move to target
extends RigidBody2D

var linear_force = 5
var target = position


func _physics_process(delta):
    var dist = position.distance_to(target)
    constant_force = dir * linear_force * dist
```

{{% notice style="note" title="Use linear damp" %}}
If you try this using the default {{< gd-icon RigidBody2D >}}`RigidBody2D` settings, you will notice that the body shoots right past the target. This is due to the body's **Linear/Damp** property, which has a default setting (found in the *Project Settings* of `1`). This value represents "friction" and controls how quickly a moving rigid body will come to a stop when no force is applied. Increasing this value will ensure that your body coasts to a stop at the target. Experiment with how this value and the `linear_force` interact to get the exactly the movement you're looking for.
{{% /notice %}}

## 関連レシピ

- [RigidBody2D：ターゲットを注視する](/godot_recipes/4.x/physics/smooth_rigid_rotate/)
