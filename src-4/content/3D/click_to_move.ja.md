---
title: "クリックして移動"
weight: 12
draft: false
ghcommentid: 38
---

## 今回のお題

クリックして指定した位置に3Dオブジェクトを移動させたい。

## 作り方

まず、世界として平面から始めてください。オブジェクトはこの平面上を移動します。

![Godot 4: クリックして移動 (3d click 01)](/godot_recipes/4.x/img/3d_click_01.png)

このデモで使用するアクターは三角柱メッシュです。

![Godot 4: クリックして移動 (3d click 02)](/godot_recipes/4.x/img/3d_click_02.png)

以下に移動動作のコードを示します。目標地点を指定すると、オブジェクトは向きを変えてその方向へ移動します。

```gdscript
extends CharacterBody3D

@export var speed = 5
@export var gravity = 5

var target = Vector3.ZERO

func _physics_process(delta):
    velocity.y -= gravity * delta
    if target:
        look_at(target, Vector3.UP)
        rotation.x = 0
        velocity = -transform.basis.z * speed
        if global_position.distance_to(target) < .5:
            target = Vector3.ZERO
            velocity = Vector3.ZERO
    move_and_slide()
```

また、シーンに「マーカー」という名前の {{< icon MeshInstance3D >}}{{< gd-icon MeshInstance3D >}}`MeshInstance3D` を追加しました。このオブジェクトは、クリックされた位置を示すために移動します。

![Godot 4: クリックして移動 (3d click 03)](/godot_recipes/4.x/img/3d_click_03.png)

### マウス→3D

現在、マウスの位置を3D空間にマッピングする手段が必要となります。スクリーンを3D世界の窓と見立てると、マウスは画面ガラス上に固定されています。3D空間で何かを選択するには、カメラ（視点）から出発し、マウスの位置を通って現実世界へと伸びるレイを投影しなければなりません。

これは手動で{{< gd-icon Camera3D >}}`Camera3D`の`project_ray`メソッドを使用して行うことも可能ですが、以下のように、{{< gd-icon CollisionObject3D >}}`CollisionObject3D`ノードがこの処理を自動的に行う特性を活用することもできます。必要なのは、{{< gd-icon StaticBody3D >}}`StaticBody3D`グラウンドの`input_event`シグナルに接続することだけです。

```gdscript
func _on_StaticBody_input_event(camera, event, click_position, click_normal, shape_idx):
    if event is InputEventMouseButton and event.pressed:
        $Marker.global_position = click_position
        $Player.target = click_position
```

マーカーとプレイヤーのターゲットの位置をクリックされた位置に設定します。

![Godot 4: クリックして移動 (3d click 04)](/godot_recipes/4.x/img/3d_click_04.gif)

## まとめ

この手法を使えば、3Dワールド内の任意のオブジェクトに対するクリックを検出できます。

<!-- ## 関連レシピ -->

<!-- - [UI: ラベル](/godot_recipes/4.x/ja/ui/labels/)
- [UI: ユニットHPバー](/godot_recipes/4.x/ja/ui/unit_healthbar/) -->

<!-- #### この動画が気に入ったら？ -->
