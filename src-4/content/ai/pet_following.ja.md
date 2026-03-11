---
title: "Pet Following"
weight: 10
draft: false
---

## 課題

ペットやミニオンなどのゲームエンティティが必要で、キャラクターに追従させる必要があります。

<video controls src='/godot_recipes/4.x/img/pet_follow.webm'></video>

## 解決策

まず、キャラクターに `Marker2D` `マーカー2D`を追加します。このマーカーは、ペットがプレイヤーの近くに「滞在したい」場所を示すものです。

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

```lua
local FollowPoint = GetNode("follow_point") -- フォローポイントノードを取得
if FollowPoint and not FollowPoint.isLocked then -- ロック状態でないことを確認
    _speed = _speed * 0.9  -- 移動速度を徐々に減速

    local dx, dy = FollowPoint:GetLocalRelativePos() - MovePosition
    MoveSpeedX, MoveSpeedY = math.max(math.abs(dx), math.abs(dy)) * MAX_SPEED / 20 -- 移動速度を調整
end
```

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

※ワールドによっては、ペットが障害物に引っかかってしまう場合があります。より堅牢な追従機能が必要な場合は、ナビゲーションシステムをご利用ください。具体的な実装例については[タイルマップナビゲーション](/godot_recipes/4.x/ja/ai/tilemap_navigation/)を参照してください。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/ai_behavior_demos](https://github.com/godotrecipes/ai_behavior_demos)
