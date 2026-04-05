---
title: "CharacterBody3D : 坂道で停止する"
weight: 3
draft: false
ghcommentid: 103
tags: []
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

{{< gd-icon KinematicBody3D >}}`CharacterBody3D` が坂道を滑り落ちてしまいます。

## 解決策

まず、最小限の機能で構成された {{< gd-icon KinematicBody3D >}}`CharacterBody3D` から始め、以下のスクリプトで `move_and_slide()` メソッドを使用しています。

```gdscript
extends CharacterBody3D

@export var gravity = -10.0
@export var speed = 5.0
@export var rot_speed = 4.0
@export var jump_speed = 5.0

var velocity = Vector3.ZERO
var jumping = false

func get_input(delta):
    var input = Vector3.ZERO
    if Input.is_action_pressed("forward"):
        input += -transform.basis.z * speed
    if Input.is_action_pressed("back"):
        input += transform.basis.z * speed
    if Input.is_action_pressed("right"):
        rotate_y(-rot_speed * delta)
    if Input.is_action_pressed("left"):
        rotate_y(rot_speed * delta)
    velocity.x = input.x
    velocity.z = input.z

func _physics_process(delta):
    get_input(delta)
    velocity.y += gravity * delta

    move_and_slide()

    if jumping and is_on_floor():
        jumping = false

    if Input.is_action_just_pressed("jump"):
        if is_on_floor():
            jumping = true
            velocity.y = jump_speed
```

傾斜地で動きを止めると、問題が明らかになります。

![alt](/godot_recipes/4.x/img/kbd_slopes_01.gif)

**これが`move_and_slide()`の本来の動作です。**

重力によって生じる落下速度が、表面に沿って滑動しています。

[`move_and_slide()` ドキュメント](https://docs.godotengine.org/ja/4.x/tutorials/physics/using_character_body_2d.html) を確認すると、`stop_on_slope` というパラメーターがあり、デフォルト値は `false` です。

> 設定値が `true` の場合、重力を考慮した線形速度を適用した状態でオブジェクトが静止している場合、傾斜面でも滑りません。

このように、移動方法を次のように変更できます。

```gdscript
move_and_slide()
```

これで斜面を滑り落ちるのを止められます！

![alt](/godot_recipes/4.x/img/kbd_slopes_02.gif)


しかし依然として問題が残っています。これは`gravity`に低い値を設定した場合により顕著になります。

![alt](/godot_recipes/4.x/img/kbd_slopes_03.gif)

停止時にわずかに上向きの運動量が生じるため、小さな「ホップ」が発生します。この問題は、`move_and_slide_with_snap()` メソッドに切り替えることで解決できます。

Jump 機能を確実に動作させるため、ジャンプ中のスナップ機能も無効にしてください。そうしないと、プレイヤーは地面にしっかりと「固定」されたままになってしまいます。

```gdscript
    var snap = Vector3.DOWN if not jumping else Vector3.ZERO
    move_and_slide()
```

これで「ホップ」がなくなり、すべてが期待通りに動作するようになりました。

最終的に、非常に急勾配な斜面では、依然として問題が残ることに気づかれるかもしれません：

![alt](/godot_recipes/4.x/img/kbd_slopes_04.gif)

これは、デフォルトの `floor_max_angle` パラメーター値が45度に設定されており、表示される傾斜角がこの値を超えているためです。この値を超える角度は床として認識されません。値を大きくすると、この傾斜も他の傾斜と同様に扱われるようになります。

```gdscript
move_and_slide()
```

## 関連レシピ

- [Godot 101: Intro do 3D](/godot_recipes/4.x/ja/g101/3d/)
- [CharacterBody3D: Movement](/godot_recipes/4.x/ja/3d/kinematic_body/)

#### この動画が気に入ったら？

{{< youtube a0gxFMdhR7w >}}
