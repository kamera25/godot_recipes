---
title: "クリックして移動"
weight: 12
draft: false
ghcommentid: 38
---

## 課題

クリックして指定した位置に3Dオブジェクトを移動させたい。

## 解決策

まず、私たちの世界として平面から始めましょう。俳優はこの平面上を移動します。

![alt](/godot_recipes/4.x/img/3d_click_01.png)

このデモで使用するアクターは三角柱メッシュです：

!

以下に移動動作のコードを示します。目標地点を指定すると、オブジェクトは向きを変えてその方向へ移動します。

```gdscript
extends CharacterBody3D

@export var speed = 5
@export var gravity = -5

var target = Vector3.ZERO

func _physics_process(delta):
    velocity.y += gravity * delta
    if target:
        look_at(target, Vector3.UP)
        rotation.x = 0
        velocity = -transform.basis.z * speed
        if transform.origin.distance_to(target) < .5:
            target = Vector3.ZERO
            velocity = Vector3.ZERO
    move_and_slide()
```

また、シーンに「マーカー」という名前の `{{< icon MeshInstance3D >}}MeshInstance3D` を追加しました。このオブジェクトは、クリックされた位置を示すために移動します。

![alt](/godot_recipes/4.x/img/3d_click_03.png)

### マウス→3D

現在、マウスの位置を3D空間にマッピングする手段が必要です。スクリーンを3D世界の窓と見立てると、マウスは画面ガラス上に固定されています。3D空間で何かを選択するには、カメラ（視点）から出発し、マウスの位置を通って現実世界へと伸びる光線を投影しなければなりません。

While this can be done manually using the {{< gd-icon Camera3D >}}`Camera3D`'s `project_ray` methods, we can take advantage of the fact that {{< gd-icon CollisionObject3D >}}`CollisionObject3D` nodes do this automatically. All we need to do is connect our {{< gd-icon StaticBody3D >}}`StaticBody3D` ground's `input_event` signal:

```gdscript
func _on_StaticBody_input_event(camera, event, click_position, click_normal, shape_idx):
    if event is 入力EventMouseButton and event.pressed:
        $Marker.transform.origin = click_position
        $Player.target = click_position
```

我們將標識的位置和玩家目標設置為所點擊的位置：

![alt](/godot_recipes/4.x/img/3d_click_04.gif)

## まとめ

この手法を使えば、3Dワールド内の任意のオブジェクトに対するクリックを検出できます。

<!-- ## 関連レシピ -->

<!-- - [UI: ラベル](/godot_recipes/3.x/ui/labels/)
- [UI: ユニットヘルスバー](/godot_recipes/3.x/ui/unit_healthbar/) -->

<!-- #### この動画が気に入ったら？ -->

