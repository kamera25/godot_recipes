---
title: "見下ろし型での移動"
weight: 1
draft: false
ghcommentid: 20
---

## 課題

2D見下ろし方式のゲームを開発しており、キャラクターの動きを制御が必要です。

## 解決策

このソリューションでは、以下の入力アクションが定義されているとします。

   アクション | キー
--------|------
`"up"` | W,↑
`"down"` | S,↓
`"right"` | D,→
`"left"` | A,←
`"click"` | マウスボタン1

また、以下のノードを使用していると想定します。{{< gd-icon \ CharacterBody2D >}} `\ CharacterBody2D` ノード。

この問題は、求める行動の種類に応じてさまざまな方法で解決できます。

### その1：8方向移動方式

このシナリオでは、プレイヤーは4方向キー（斜め移動含む）を使って操作します。

```gdscript
extends CharacterBody2D

var speed = 400  # speed in pixels/sec

func _physics_process(delta):
    var direction = Input.get_vector("left", "right", "up", "down")
    velocity = direction * speed

    move_and_slide()
```

### その2: 回転と移動を組み合わせる場合

この操作方法では、左右でキャラクターを回転させ、上下で向いている方向に前進・後退します。これは「アステロイド風」と呼ばれる伝統的な操作方式です。

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

### その3：マウスで照準を合わせる方法

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

### その4：クリックして移動

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

ターゲット位置に近づくと移動を停止します。これを行わないと、キャラクターは「ぐらぐら」動きながら、少しずつ目標を越えては戻り、再び越えて…という動作を繰り返します。オプションとして、`look_at()` を使って移動中の方向を向くようにすることもできます。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードをダウンロードするにはこちら：[https://github.com/godotrecipes/topdown_movement](https://github.com/godotrecipes/topdown_movement)
