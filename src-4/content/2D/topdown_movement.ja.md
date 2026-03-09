---
title: "Top-down movement"
weight: 1
draft: false
ghcommentid: 20
---

## 問題文

2Dトップダウン方式のゲームを開発しており、キャラクターの動きを制御する必要があります。

## 解決策

このソリューションでは、以下の入力アクションが定義されていると仮定します：

   Action Name | Key(s)
--------|------
`"up"` | W,↑
`"down"` | S,↓
`"right"` | D,→
`"left"` | A,←
`"click"` | Mouse button 1

また、以下のノードを使用していると想定します：{{< gd-icon CharacterBody2D >}} `CharacterBody2D` ノード。

この問題は、求める行動の種類に応じてさまざまな方法で解決可能です。

### オプション1：8方向移動方式

このシナリオでは、プレイヤーは4方向キー（斜め移動含む）を使って操作します。

```gdscript
extends CharacterBody2D

var speed = 400  # speed in pixels/sec

func _physics_process(delta):
    var direction = Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed

    move_and_slide()
```

### オプション2: 回転と移動を組み合わせる場合

In this scenario, the left/right actions rotate the character and up/down move the character forward and back in whatever direction it's facing. This is sometimes referred to as "Asteroids-style" movement.

```gdscript
extends CharacterBody2D

var speed = 400  # move speed in pixels/sec
var rotation_speed = 1.5  # turning speed in radians/sec

func _physics_process(delta):
    var move_input = Input.get_axis("down", "up")
    var rotation_direction = Input.get_axis("left", "right")
    velocity = transform.x * move_input * speed
    rotation += rotation_direction * rotation_speed * delta
    move_and_slide()
```

{{% notice note %}}
Godotでは角度0度を「x」軸に沿っていることを意味します。これは、ノードの前方方向（`transform.x`）が右向きであることを示しています。キャラクタースプライトも同様に、右側に向かって描画されるように設定してください。
{{% /notice %}}

### オプション3：マウスで照準を合わせる方法

オプション2と同様ですが、今回はキャラクターの向きをマウスで操作できます（常にマウス方向へ向いています）。前後移動はこれまで通りキーボードキーで行います。

```gdscript
extends CharacterBody2D

var speed = 400  # move speed in pixels/sec

func _physics_process(delta):
    look_at(get_global_mouse_position())
    var move_input = Input.get_axis("down", "up")
    velocity = transform.x * move_input * speed
    move_and_slide()
```

### オプション4：クリックして移動

このオプションでは、キャラクターがクリックした位置に移動します。

```gdscript
extends CharacterBody2D

var speed = 400  # move speed in pixels/sec
var target = null

func _input(event):
    if event.is_action_pressed("click"):
        target = get_global_mouse_position()

func _physics_process(delta):
    if target:
        # look_at(target)
        velocity = position.direction_to(target) * speed
        if position.distance_to(target) < 10:
            velocity = Vector2.ZERO
    move_and_slide()
```

Note that we stop moving if we get close to the target position. If you don't do this, the character will "jiggle" back and forth as it moves a little bit past the target, moves back, goes a little past it, and so on. Optionally, you can use `look_at()` to face in the direction of movement.

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードをダウンロードするにはこちら：[https://github.com/godotrecipes/topdown_movement](https://github.com/godotrecipes/topdown_movement)
