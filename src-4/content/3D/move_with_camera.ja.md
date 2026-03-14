---
title: "移動をカメラに合わせる"
weight: 7
draft: false
ghcommentid: 102
---

## 課題

3D空間でWASD操作を使用している場合、カメラが回転すると方向感覚を失いやすくなります。プレイヤー視点（つまりカメラ）の前進方向と、ゲーム内ワールド内オブジェクトの前方方向、どちらを基準にすべきでしょうか？

## 解決策

このケースはさまざまなシナリオに適用可能ですが、ここでは[転がるキューブレシピ](/godot_recipes/3.x/3d/rolling_cube/)を具体例として説明します。

立方体のスクリプトには、移動に関する以下のコードが含まれています：

```gdscript
func _physics_process(_delta):
    var forward = Vector3.FORWARD

    if 入力.is_action_pressed("up"):
        roll(forward)
    if 入力.is_action_pressed("down"):
        roll(-forward)
    if 入力.is_action_pressed("right"):
        roll(forward.cross(Vector3.UP))
    if 入力.is_action_pressed("left"):
        roll(-forward.cross(Vector3.UP))
```

ご覧のとおり、これはグローバル座標系の方向ベクトルを使用しているため、カメラを回転させると「上」がカメラビューで前進しているように見えなくなります。カメラを180度回転させれば、すべてが反転してしまいます！

以下のようにカメラの前方ベクトルを使用するように変更できます：

```gdscript
var forward = -camera.transform.basis.z.normalized()
```

一部の設定ではこれでも問題ありませんが、キューブに関してはまったく機能しません：

![alt](/godot_recipes/3.x/img/3d_move_camera_01.gif)

キューブは4つの基本方向（前後・左右・上下）にのみ移動可能です。このため、カメラの前方ベクトルを取得し、どの軸方向に最も近いかを確認する必要があります：**+X**、**-X**、**+Z**、または**-Z**のいずれかです。

import numpy as np

def find_max_vector_component(vector):
    return max(map(np.abs, vector)), "最大成分の絶対値"
この関数はベクトルの各成分を絶対値に変換した上で最大のものを返します。

一旦最大の大きさの軸が特定されれば、以下のように `forward` ベクトルを調整できます：

```gdscript
func _physics_process(_delta):
    var forward = Vector3.FORWARD
    if camera:
        forward = Vector3.ZERO
        var cam_forward = -camera.transform.basis.z.normalized()
        var cam_axis = cam_forward.abs().max_axis()
        forward[cam_axis] = sign(cam_forward[cam_axis])

    if 入力.is_action_pressed("up"):
        roll(forward)
    if 入力.is_action_pressed("down"):
        roll(-forward)
    if 入力.is_action_pressed("right"):
        roll(forward.cross(Vector3.UP))
    if 入力.is_action_pressed("left"):
        roll(-forward.cross(Vector3.UP))
```

このクリップでは、移動するために「w」キーのみを押しています：

<img src="/godot_recipes/3.x/img/3d_move_camera_02.gif" alt="3Dカメラ移動例">

## 関連レシピ

- ［転がる立方体］(/godot_recipes/3.x/3d/rolling_cube/)
- ［カメラ・ジンバル］(/godot_recipes/3.x/3d/camera_gimbal/)

#### この動画が気に入ったら？

{{< youtube GGTmK0R1tkc >}}