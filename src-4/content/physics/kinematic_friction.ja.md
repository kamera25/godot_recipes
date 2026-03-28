---
title: "動摩擦"
weight: 3
draft: false
---

## 課題

運動キャラクターに摩擦と加速度を加え、より自然な動きを実現したい。

## 解決策

多くのゲームにおいて、必ずしも完全な物理シミュレーションを求めているわけではありません。重要なのはアクション性、反応の良さ、そしてアーケードならではの爽快感です。だからこそ、RigidBodyではなくKinematicBodyを選択するのです - これによって物体の動きを直接制御できるようになります。ただし、ある程度の物理的な挙動は必要です。これはつまり、オブジェクトが突然方向を変えたり停止したりしないようにするためです。

以下に、シンプルな運動力学に基づくプラットフォーマーキャラクター用のコードを示します。

```gdscript
extends CharacterBody2D

var speed = 1200
var jump_speed = -1800
var gravity = 4000

var velocity = Vector2.ZERO

func get_input():
    velocity.x = 0
    if Input.is_action_pressed("ui_right"):
        velocity.x += speed
    if Input.is_action_pressed("ui_left"):
        velocity.x -= speed

func _physics_process(delta):
    get_input()
    velocity.y += gravity * delta
    velocity = move_and_slide(velocity, Vector2.UP)
    if Input.is_action_just_pressed("ui_select"):
        if is_on_floor():
            velocity.y = jump_speed
```

このコードを実行すると、キャラクターの**x**方向速度が瞬時に変化してしまうことに気づくでしょう。これを修正するために、`lerp()`関数を使用して速度を徐々に増減させるようにします。

#### 「lerp」の使用例

```gdscript
lerp(start_value, end_value, amount)
```

`lerp()`（線形補間）は、2つの数値間で「ブレンドされた」値を求める関数です。詳細は[補間処理](/godot_recipes/3.x/math/interpolation/)を参照してください。

以下のコードでは、`friction(摩擦係数)`はキャラクターが停止する速度を、`acceleration(加速力)`は最大加速するまでの速度を決定する要素です。どちらも値が`0.0`から`1.0`の範囲内で設定されます。

「get_input()」のコードを以下に置き換えます。

```gdscript
var friction = 0.1
var acceleration = 0.5

func get_input():
    var input_dir = 0
    if Input.is_action_pressed("ui_right"):
        input_dir += 1
    if Input.is_action_pressed("ui_left"):
        input_dir -= 1
    if dir != 0:
        # accelerate when there's input
        velocity.x = lerp(velocity.x, dir * speed, acceleration)
    else:
        # slow down when there's no input
        velocity.x = lerp(velocity.x, 0, friction)
```

### 解説

摩擦係数と加速度をブレンド量として使用します。加速時には、現在速度から最大速度までの適切な値を求めます。減速時には、現在速度を徐々に0へ減衰させます。

{{% notice tip %}}
値に `1.0` を使用すると、当初の「瞬間的な」移動状態が復活します。
{{% /notice %}}

![alt](/godot_recipes/3.x/img/friction_platformer.gif)

## 関連するレシピ

- [プラットフォームキャラクター](/godot_recipes/3.x/2d/platform_character/)