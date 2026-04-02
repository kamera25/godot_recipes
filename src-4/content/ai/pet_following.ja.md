---
title: "追いかけるペット"
weight: 10
draft: false
---

## 課題

ゲーム要素としてペットやミニオンを追加します。なので、キャラクターに追従させる必要があります。

<video controls src='/godot_recipes/4.x/img/pet_follow.webm'></video>

## 解決策

まず、キャラクターに {{< gd-icon Marker2D >}}`Marker2D` を追加します。このマーカーは、ペットがプレイヤーの近くに「滞在したい」場所を示すものです。

![alt](/godot_recipes/4.x/img/pet_follow_01.png)

この例では、{{< gd-icon Sprite2D >}}`Sprite2D`の子要素として設定しています。これはキャラクターのコード内で `$Sprite2D.scale.x = -1` を使用して左移動時に水平方向を反転させているためです。マーカーはスプライトの子要素であるため、同様に反転表示されます。

### ペット用スクリプト

以下はペット用の台本です。

```gdscript
extends CharacterBody2D

@export var parent : CharacterBody2D

var speed = 25

@onready var follow_point = parent.get_node("Sprite2D/FollowPoint")
```

`parent`変数には、ペットが追従すべきキャラクターへの参照情報が格納されています。その後、そのノードから`FollowPoint`を取得し、`_physics_process()`関数内でその位置情報を取得します。

```gdscript
func _physics_process(delta):
    var target = follow_point.global_position
    velocity = Vector2.ZERO
    if position.distance_to(target) > 5:
        velocity = position.direction_to(target) * speed

    if velocity.x != 0:
        $Sprite2D.scale.x = sign(velocity.x)

    if velocity.length() > 0:
        $AnimationPlayer.play("run")
    else:
        $AnimationPlayer.play("idle")

    move_and_slide()
```

目標地点に近い場合は、ペットの移動を停止します。

### 障害物の回避方法

ワールドによっては、ペットが障害物に引っかかってしまう場合があります。より堅牢な追従機能が必要な場合は、ナビゲーションシステムをご利用ください。具体的な実装例については[タイルマップナビゲーション](/godot_recipes/4.x/ja/ai/tilemap_navigation/)を参照してください。

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/ai_behavior_demos](https://github.com/godotrecipes/ai_behavior_demos)
