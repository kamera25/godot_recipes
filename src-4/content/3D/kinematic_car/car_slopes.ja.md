---
title: "3Dで自動車を作ろう：傾斜面＆スロープ"
weight: 4
draft: false
ghcommentid: 44
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

[キネマティックカー](/godot_recipes/4.x/ja/3d/kinematic_car/car_base/) は斜面を登れるようになりましたが、見た目が少し不自然です。

![alt](/godot_recipes/4.x/img/3d_car_10.png)

## 解決策

運動体は衝突時に自動で回転しません。画像のように車輪が地面に接触していない場合、手動で車を整列させる必要があります。

まず、車輪が地面に接触していない状況を検出する必要があります。車に2つの {{< gd-icon RayCast3D >}}`RayCast` ノードを追加し、以下のように前輪と後輪にそれぞれ配置します。

![alt](/godot_recipes/4.x/img/3d_car_11.png)

両方の場合、［キャスト先］を（0、-0.25、0）に設定し、「有効」ボックスのチェックを忘れずに行ってください。

### 3Dオブジェクトの整列方法

[CharacterBody3D: 表面に合わせる]レシピのコードを再利用します。これを`car_base.gd`に追加してください：

```gdscript
func align_with_y(xform, new_y):
    xform.basis.y = new_y
    xform.basis.x = -xform.basis.z.cross(new_y)
    xform.basis = xform.basis.orthonormalized()
    return xform
```

`_physics_process()` 関数内で `move_and_slide_with_snap()` を呼び出した直後に、車両を整列させる必要があるかどうかをチェックします。

```gdscript
# If either wheel is in the air, align to slope.
if $FrontRay.is_colliding() or $RearRay.is_colliding():
    # If one wheel is in air, move it down
    var nf = $FrontRay.get_collision_normal() if $FrontRay.is_colliding() else Vector3.UP
    var nr = $RearRay.get_collision_normal() if $RearRay.is_colliding() else Vector3.UP
    var n = ((nr + nf) / 2.0).normalized()
    var xform = align_with_y(global_transform, n)
    global_transform = global_transform.interpolate_with(xform, 0.1)
```

### 使用方法

どちらの車輪も地面に接していない場合、車はまったく回転しません。

それ以外の場合は、前面および背面レイの結果を平均化して使用します。衝突が発生している場合、衝突オブジェクトの表面法線が考慮されます。この方法により、例えばカーブした坂道のように2つの車輪が異なる斜面に接している状況でも、両方の車輪を可能な限り表面に接触させようとする処理が行われます。

![alt](/godot_recipes/4.x/img/3d_car_12.png)

この画像では、車がどちらの面にも平行ではなく、中間位置に配置されていることがわかります。

レイが何も検出しない場合は、水平な面と仮定します。これにより、一方のホイールが接触している場合にもう一方の車輪が下がります。

## 関連レシピ

- [運動力学カー：ベースモデル](/godot_recipes/4.x/ja/3d/kinematic_car/car_base/)
- [CharacterBody3D：地面に沿う](/godot_recipes/4.x/ja/3d/3d_align_surface/)

#### この動画が気に入ったら？

