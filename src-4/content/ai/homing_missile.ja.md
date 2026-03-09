---
title: "Homing missile"
weight: 4
draft: false
---

## 問題文

You need a "homing missile" - a projectile that will seek a moving target.

## 解決策

```
この例では、プロジェクトイルとして {{< gd-icon Area2D >}}`Area2D` ノードを使用します。エリアは通常、衝突検出が必要な弾丸に適しています。もし跳ね返る/反射するタイプの弾丸も必要であれば、`PhysicsBody` 型のノードの方が適しているかもしれません。

The node setup and behavior of the missile is the same you would use for a "dumb" bullet. If you're creating many bullet types, you can use inheritance to base all your projectiles on the same core setup.

使用するノード：

```
{{< gd-icon Area2D >}} Area2D: Missile
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
    {{< gd-icon Timer >}} Timer: Lifetime
```

テクスチャについては、お好きな画像を自由に使用できます。一例をご紹介します：

<img src=\ alt=\>

Set up the nodes and configure the sprite's texture and the collision shape. Make sure to rotate the {{< gd-icon Sprite2D >}}`Sprite2D` node by `90°` so that it's pointing to the right, ensuring it matches the parent's "forward" direction.

スクリプトを追加し、{{< gd-icon Area2d >}}`Area2D`の`body_entered`シグナルと{{< gd-icon Timer >}}`Timer`の`timeout`シグナルを接続してください。

以下に開始スクリプトを示します：

```gdscript
extends Area2D

export var speed = 350

var velocity = Vector2.ZERO
var acceleration = Vector2.ZERO

func start(_transform):
    global_transform = _transform
    velocity = transform.x * speed

func _physics_process(delta):
    velocity += acceleration * delta
    velocity = velocity.clamped(speed)
    rotation = velocity.angle()
    position += velocity * delta

func _on_Missile_body_entered(body):
    queue_free()

func _on_Lifetime_timeout():
    queue_free()
```

This creates a "dumb" rocket that travels in a straight line when fired. To use this projectile, instance it and call its `start()` method with the desired `Transform2D` to set its position and direction.

詳細については以下の［関連するレシピ］セクション（#関連レシピ）をご覧ください。

To change the behavior to seek a target, we'll use the `acceleration`. However,
we don't want the missile to "turn on a dime", so we'll add a variable to control its "steering" force. This will give the missile a turning radius that can be adjusted for different behavior. We also need a `target` variable so that the missile knows what to chase. We'll set that in `start()` as well:

```gdscript
export var steer_force = 50.0

var target = null

func start(_transform, _target):
    target = _target
    ...
```

To change the missile's direction to move toward the target, it needs to accelerate in that direction (acceleration is change in velocity). The missile "wants" to move straight towards the target, but its current velocity is pointing in a different direction. Using a little vector math, we can find that difference:

```text
![alt](/godot_recipes/4.x/img/steering_diagram.png)

The green arrow represents the needed change in velocity (i.e. `acceleration`). However, if we turn instantly, that will look unnatural, so the "steering" vector's length needs to be limited. This is the purpose of the `steer_force` variable.

これはその加速度を計算する関数です。注：目標が設定されていない場合、操舵は行われないため、ミサイルはそのまま直線軌道を維持します。

```gdscript
func seek():
    var steer = Vector2.ZERO
    if target:
        var desired = (target.position - position).normalized() * speed
        steer = (desired - velocity).normalized() * steer_force
    return steer
```

最後に、計算されたステアリング力は`_physics_process()`内で適用する必要があります：

```gdscript
func _physics_process(delta):
    acceleration += seek()
    velocity += acceleration * delta
    velocity = velocity.clamped(speed)
    rotation = velocity.angle()
    position += velocity * delta
```

以下はその結果の一例です。粒子エフェクトや爆発効果などの視覚的演出を少し追加しています：

<video controls src='/godot_recipes/4.x/img/homing_missiles.webm'></video>

以下に完全なスクリプトを示します。上記のエフェクトも含まれています。詳細は[関連レシピ](#related-recipes)をご覧ください。

```gdscript
extends Area2D

export var speed = 350
export var steer_force = 50.0

var velocity = Vector2.ZERO
var acceleration = Vector2.ZERO
var target = null

func start(_transform, _target):
    global_transform = _transform
    rotation += rand_range(-0.09, 0.09)
    velocity = transform.x * speed
    target = _target

func seek():
    var steer = Vector2.ZERO
    if target:
        var desired = (target.position - position).normalized() * speed
        steer = (desired - velocity).normalized() * steer_force
    return steer

func _physics_process(delta):
    acceleration += seek()
    velocity += acceleration * delta
    velocity = velocity.clamped(speed)
    rotation = velocity.angle()
    position += velocity * delta

func _on_Missile_body_entered(body):
    explode()

func _on_Lifetime_timeout():
    explode()

func explode():
    $Particles2D.emitting = false
    set_physics_process(false)
    $AnimationPlayer.play("explode")
    await $AnimationPlayer.animation_finished
    queue_free()
```


## 関連レシピ

```markdown
- [スプライトシートアニメーション](/godot_recipes/4.x/animation/spritesheet_animation/)
- [トップダウン型キャラクター操作](/godot_recipes/4.x/2d/topdown_movement/#option-2-rotate-and-move)
- [トランスフォーム操作](/godot_recipes/4.x/math/transforms)
