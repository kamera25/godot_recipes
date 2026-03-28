---
title: "2Dジョイントを使う"
weight: 7
draft: false
ghcommentid: 70
---

## 課題

Godotの`Joint2D`ノードについて理解したい。

## 解決策

ジョイントは、接続された物理オブジェクトの動きを制限するために使用されます。任意のジョイントノードには、`物理Object2D` から拡張される2つのボディを結合が必要です。

#### プロパティ

これらのプロパティはすべての関節ノードに共通です：

- _Node A_ and _Node B_: The assigned physics bodies.
- _Bias_: The rate at which the joint pulls the two bodies back together if they move apart. Defaults to `0`.
- _Disable Collisions_: Allows the connected bodies to ignore collisions between them. Defaults to `true`.

以下の3種類の {{< gd-icon Joint2D >}} `Joint2D` が存在します。すべての例で、1つの {{< gd-icon RigidBody2D >}} `RigidBody2D` がジョイントを介して {{< gd-icon StaticBody2D >}} `StaticBody2D` に接続されています。画面画像では「可視衝突形状」が有効化されているため、ジョイントの表現を確認できます。

### {{< gd-icon PinJoint2D >}} PinJoint2D

「ピン接合」は、2つの部材を1点で接続し、自由に回転できるようにします。

![alt](/godot_recipes/3.x/img/pinjoint_example.gif)

The pin joint's _Softness_ property gives some "springiness" to the connection. The value can range from `0` (the default) which allows no movement, to `16`.

![alt](/godot_recipes/3.x/img/pinjoint_example2.gif)

### {{< gd-icon DampedSpringJoint2D >}} 減衰スプリングジョイント（2D）

この継手はスプリング状の力によって2つの部材を連結します。

![alt](/godot_recipes/3.x/img/springjoint_example.gif)

以下のプロパティでスプリングの挙動を調整できます。

- _Length_: The joint's maximum length.
- _Rest Length_:The joint's length when no forces or movement are applied.
- _Stiffness_: The spring's "stretchiness", i.e. how much it resists forces pulling against it.
- _Damping_: How quickly the spring stops "bouncing".

### {{< gd-icon GrooveJoint2D >}} GrooveJoint2D

この関節は、接続された物体が直線的に移動するように制約します。

![alt](/godot_recipes/3.x/img/groovejoint_example.gif)

デフォルトでは溝は垂直方向に配置されますが、溝ノードを回転させることでこれを変更できます。

以下のプロパティは溝の動作を制御します。

- _Length_: The groove's length. The attached bodies can't move past this maximum distance.
- _Initial Offset_: Starting "position" along the groove.

<!-- You can download an example project to play with these joints here: [physics_joints.zip](/godot_recipes/3.x/files/physics_joints.zip) -->

![alt](/godot_recipes/3.x/img/joints_demo.png)

## 関連するレシピ
