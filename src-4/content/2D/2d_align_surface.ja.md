---
title: "CharacterBody2D: align with surface"
weight: 5
draft: true
---

## 問題文

あなたのキャラクターボディは、立っている面と平行になるように調整する必要があります。

## 解決策

まずは基本的なキネマティックプラットフォームキャラクタから始めましょう。詳細は[プラットフォームキャラクターレシピ](/godot_recipes/4.x/2d/platform_char/)を参照してください。

以下の移動コードがあります：

```gdscript
func _physics_process(delta):
    velocity.y += gravity * delta
    var dir = Input.get_axis("walk_left", "walk_right")
    velocity.x = dir * speed

    move_and_slide()
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_speed
```

<video controls src="/godot_recipes/4.x/img/2d_align_01.webm"></video>

ご覧の通り、いくつかの問題があります。第一に、キャラクターは走っている時に斜面から滑り落ちてしまいます。また、入力がない状態でも坂を滑って降りていきます。

以下の方法で部分的に解決できます：`move_and_slide()`から`move_and_slide_with_snap()`に変更する：

```gdscript
snap = Vector2.DOWN * 128 if !is_jumping else Vector2.ZERO
velocity = move_and_slide_with_snap(velocity, snap, Vector2.UP, true)
```

<video controls src="/godot_recipes/4.x/img/2d_align_02.webm"></video>

現在では、斜面を登る途中で停止した際に「上昇ジャンプ」が発生します。これは入力が途絶えたことで`x`方向の速度が`0`に設定される一方、`y`方向の速度は影響を受けないためです。

## 速度ベクトルの方向決定

この問題を解決するには、速度ベクトルを斜面に対して適切に調整すればよいでしょう。具体的に説明するため、まずキャラクターの向きを調整して斜面と平行にします。これは、床の上にいるときに床面法線を確認することで実現可能です：

```gdscript
if is_on_floor():
    rotation = get_floor_normal().angle() + PI/2
```

<video controls src="/godot_recipes/4.x/img/2d_align_03.webm"></video>

この操作はまだ移動そのものには影響を与えませんが、今後行うべき作業のイメージを掴む上で役立ちます。斜面上にいる場合、ローカル変換行列は以下のようになります：

![alt](/godot_recipes/4.x/img/2d_align_04.png)

現在の実装では、移動時に速度ベクトルをローカル座標系のx軸（赤色矢印）に、重力/ジャンプ力をy軸（緑色矢印）に合わせる必要があります。入力処理コードはそのままで、常に「velocity」がローカル座標系で計算されると仮定できます。唯一の問題は「move_and_slide()」関数が速度ベクトルをグローバル座標系で受け取ることを期待している点です。この問題を解決するため、以下のように`move_and_slide_with_snap()`を調整しましょう：

```gdscript
snap = transform.y * 128 if !is_jumping else Vector2.ZERO
velocity = move_and_slide_with_snap(velocity.rotated(rotation),
        snap, -transform.y, true)
# Convert velocity back to local space.
velocity = velocity.rotated(-rotation)
```

ここではいくつか変更点がありますので、詳しく見ていきましょう。

・`snap`ベクトルは現在ローカルの下向きベクトルとなっており、斜面に対して常に垂直方向を指し示すようになります。
・`floor_normal`パラメータもローカル上向き方向（`-transform.y`）に変更されます。
・速度変換では、まずプレイヤーの回転に合わせて座標系を調整し、その後逆操作を行って結果的な速度を再びローカル座標系に戻します。

結果：

<video controls src="/godot_recipes/4.x/img/2d_align_05.webm"></video>

## まとめ

この手法により、さまざまなプラットフォーマー風の移動システムを実現できます。例えば、以下のような楽しい機能を実装可能です：

<video controls src="/godot_recipes/4.x/img/2d_align_06.webm"></video>

以下が完全なスクリプトです：

```gdscript
func _physics_process(delta):
    get_input()
    velocity.y += gravity * delta
    snap = transform.y * 128 if !is_jumping else Vector2.ZERO
    velocity = move_and_slide_with_snap(velocity.rotated(rotation),
                    snap, -transform.y, true, 4, PI/3)
    velocity = velocity.rotated(-rotation)

    if is_on_floor():
        rotation = get_floor_normal().angle() + PI/2
        is_jumping = false
        if Input.is_action_just_pressed("ui_up"):
            is_jumping = true
            velocity.y = jump_speed
```

## 関連レシピ

[プラットフォームキャラクタの実装](/godot_recipes/4.x/2d/platform_character)
[KinematicBody2Dの活用方法](/godot_recipes/4.x/physics/godot3_kinematic2d/)

<!-- #### この動画が気に入ったら？ -->
