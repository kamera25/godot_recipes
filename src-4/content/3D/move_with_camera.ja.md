---
title: "移動をカメラに合わせる"
weight: 7
draft: false
ghcommentid: 102
---

## 課題

3D空間でWASD操作を使用している場合、カメラが回転すると方向感覚を失いやすくなります。プレイヤー視点（つまりカメラ）の前進方向と、ゲーム内ワールド内オブジェクトの前方方向、どちらを基準にすべきでしょうか？

## 解決策

このケースはさまざまなシナリオに適用できますが、ここでは[転がるキューブレシピ](/godot_recipes/4.x/ja/3d/rolling_cube/)を具体例として説明します。

キューブのスクリプトには、移動に関する以下のコードが含まれています。

```gdscript
func _physics_process(_delta):
    var forward = Vector3.FORWARD

    if Input.is_action_pressed("up"):
        roll(forward)
    if Input.is_action_pressed("down"):
        roll(-forward)
    if Input.is_action_pressed("right"):
        roll(forward.cross(Vector3.UP))
    if Input.is_action_pressed("left"):
        roll(-forward.cross(Vector3.UP))
```

ご覧のとおり、これはグローバル座標系の方向ベクトルを使用しているため、カメラを回転させると「上」がカメラビューで前進しているように見えなくなります。カメラを180度回転させれば、すべてが反転してしまいます！

以下のようにカメラの前方ベクトルを使用するように変更できます。

```gdscript
var forward = -camera.transform.basis.z.normalized()
```

一部の設定ではこれでも問題ありませんが、キューブに関してはまったく機能しません：

![alt](/godot_recipes/3.x/img/3d_move_camera_01.gif)

キューブは4つの基本方向（前後・左右・上下）にのみ移動できます。このため、カメラの前方ベクトルを取得し、どの軸方向に最も近いかを確認する必要があります。**+X**、**-X**、**+Z**、または **-Z** のいずれかです。

これは、`Vector3.max_axis()`関数を使用してみます。この関数は、ベクトルの成分のうち最も大きい値を返します。値は正または負になる可能性があるため、まず`abs()`を適用して絶対値に変換します。

一旦最大の大きさの軸が特定されれば、以下のように `forward` ベクトルを調整できます。

```gdscript
func _physics_process(_delta):
    var forward = Vector3.FORWARD
    if camera:
        forward = Vector3.ZERO
        var cam_forward = -camera.transform.basis.z.normalized()
        var cam_axis = cam_forward.abs().max_axis()
        forward[cam_axis] = sign(cam_forward[cam_axis])

    if Input.is_action_pressed("up"):
        roll(forward)
    if Input.is_action_pressed("down"):
        roll(-forward)
    if Input.is_action_pressed("right"):
        roll(forward.cross(Vector3.UP))
    if Input.is_action_pressed("left"):
        roll(-forward.cross(Vector3.UP))
```

このクリップでは、移動するために「w」キーのみを押しています。

![alt](/godot_recipes/3.x/img/3d_move_camera_02.gif)

## 関連レシピ

- [転がるキューブ](/godot_recipes/4.x/ja/3d/rolling_cube/)
- [カメラ・ジンバル](/godot_recipes/4.x/ja/3d/camera_gimbal/)

#### この動画が気に入ったら？

{{< youtube GGTmK0R1tkc >}}