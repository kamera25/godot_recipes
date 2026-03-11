---
title: "Homing missile"
weight: 4
draft: false
---

## 問題文

必要になるのが「ホーミングミサイル」です。これは移動する標的を自動で追尾する砲弾です。

## 解決策

この例では、プロジェクトイルとして {{< gd-icon Area2D >}}`Area2D` ノードを使用します。エリアは通常、衝突検出が必要な弾丸に適しています。もし跳ね返る/反射するタイプの弾丸も必要であれば、`PhysicsBody` 型のノードの方が適しているかもしれません。

ノードの設定とミサイルの挙動は、従来の「単純な」弾丸と同様の仕組みを採用しています。複数種類の弾丸を作成する場合、継承機能を活用してすべてのプロジェクトイルを共通の基本設定に基づいて構築することが可能です。

使用するノード：

```
{{< gd-icon Area2D >}} Area2D: Missile
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
    {{< gd-icon Timer >}} Timer: Lifetime
```

テクスチャについては、お好きな画像を自由に使用できます。一例をご紹介します：

<img src="/godot_recipes/4.x/img/missile.png" alt="ミサイル">

```
ノードの設定を行い、スプライトのテクスチャと衝突形状を構成します。{{< gd-icon Sprite2D >}}`Sprite2D`ノードは必ず `90°` 回転させ、右向きになるように調整してください。これにより、親オブジェクトの「前方」方向と一致するようになります。

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

この設定により、発射時に直線軌道で移動する「単純な」ロケットが作成されます。この投射物を使用するためには、インスタンス化した後、`start()` メソッドを呼び出し、目的の位置と方向を設定するために適切な `Transform2D` を指定する必要があります。

詳細については以下の［関連するレシピ］セクション（#関連レシピ）をご覧ください。

ターゲット捜索動作を変更するため、`acceleration`（加速度）を利用します。ただし、ミサイルが「一瞬で方向転換する」のは避けたいので、制御する「ステアリング力」を調整する変数を追加します。この設定により、異なる挙動に対応した旋回半径を調整できるようになります。また、ミサイルが追跡対象を把握するための`target`変数も必要です。これも`start()`関数内で適切に初期化します：

```gdscript
export var steer_force = 50.0

var target = null

func start(_transform, _target):
    target = _target
    ...
```

ミサイルを目標に向かって移動させるには、方向転換して加速する必要があります（加速度とは速度の変化のことです）。ミサイルは本来、まっすぐ目標方向へ進みたいところですが、現在の速度ベクトルは別の方向に向いた状態です。簡単なベクトル計算によって、このずれ量を求めることができます：

```text
![alt](/godot_recipes/4.x/img/steering_diagram.png)

緑の矢印は必要な速度変化（すなわち「加速度」）を示しています。ただし、瞬時に方向転換すると不自然に見えるため、この「操舵」ベクトルの長さには制限を設ける必要があります。これを実現するための変数が`steer_force`です。

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
- [スプライトシートアニメーション](/godot_recipes/4.x/ja/animation/spritesheet_animation/)
- [トップダウン型キャラクター操作](/godot_recipes/4.x/ja/2d/topdown_movement/#option-2-rotate-and-move)
- [トランスフォーム操作](/godot_recipes/4.x/ja/math/transforms)
