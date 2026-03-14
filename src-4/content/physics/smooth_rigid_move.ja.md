---
title: "RigidBody2D：目標位置へ移動"
weight: 3
draft: false
---

## 課題

rigidbodyを目標位置へ移動させたい。

## 解決策

{{< gd-icon RigidBody2D >}}`RigidBody2D` の操作は少し複雑です。Godot の物理エンジンで制御されるため、直接移動させるのではなく、力を加える必要があります。剛性ボディを扱う前に、[RigidBody2D API ドキュメント](https://docs.godotengine.org/ja/stable/classes/class_rigidbody2d.html) を読むことを強くお勧めします。

物体を移動させるには、特定の方向に力を加える必要があります - これが「*力*」です。物体が動き始めたら、最終位置に近づくにつれてこの力は徐々に小さくなるようにします。

この場合、まさに`Vector2.distance_to()`関数を使用するのに最適な状況です。この関数を使えばターゲットまでの距離を正確に測定でき、その値を基に適切な力を加えることができます。


```gdscript
# Smoothly move to target
extends RigidBody2D

var linear_force = 5
var target = position


func _physics_process(delta):
    var dist = position.distance_to(target)
    constant_force = dir * linear_force * dist
```

{{% notice style="note" title="線形ダンピングを使用" %}}
デフォルト設定の {{< gd-icon RigidBody2D >}}`RigidBody2D` でこの操作を試みると、物体が目標を通り過ぎてしまうことがわかります。これはオブジェクトの**Linear/Damp** プロパティによるものです（デフォルト値は `1` のプロジェクト設定にあります）。この値は「摩擦」を表しており、力を加えない場合に可動式剛体がどのくらいの速さで停止するかを制御します。この値を大きくすると、物体が目標地点でスムーズに減速するようになります。この値と `linear_force` がどのように相互作用するかを調整することで、まさに求めている動きを実現できます。
{{% /notice %}}

## 関連レシピ

- [RigidBody2D：ターゲットを注視する](/godot_recipes/4.x/ja/physics/smooth_rigid_rotate/)
