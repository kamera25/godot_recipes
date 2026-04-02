---
title: "2Dジョイントを使う"
weight: 7
draft: false
ghcommentid: 70
---

## 課題

Godotの`Joint2D`ノードについて理解したい。

## 解決策

ジョイントは、接続された物理オブジェクトの動きを制限するために使います。任意のジョイントノードには、`PhysicsObject2D` から拡張される2つのボディを結合が必要です。

#### プロパティ

これらのプロパティはすべての関節ノードに共通です。

*  _Node A_ and _Node B_：割り当てられた物理ボディ
*  _Bias_：両オブジェクトが離れる方向に関節が引き寄せる速度。デフォルト値は 0 です
*  _Disable Collisions_：接続されたオブジェクト間の衝突を考慮しないようにできます。デフォルトは true（有効）です

以下の3種類の {{< gd-icon Joint2D >}} `Joint2D` があります。すべての例で、1つの {{< gd-icon RigidBody2D >}} `RigidBody2D` がジョイントを介して {{< gd-icon StaticBody2D >}} `StaticBody2D` に接続されています。画面画像では「可視衝突形状」が有効化されているため、ジョイントの表現を確認できます。

### {{< gd-icon PinJoint2D >}} PinJoint2D

「ピン接合」は、2つの部材を1点で接続し、自由に回転できるようにします。

![alt](/godot_recipes/3.x/img/pinjoint_example.gif)

ピン接合部の［柔軟性］プロパティにより、接続にある程度の「弾力」が与えられます。この値はデフォルト値の `0`（移動不可）から最大値 `16` まで設定できます。

![alt](/godot_recipes/3.x/img/pinjoint_example2.gif)

### {{< gd-icon DampedSpringJoint2D >}} 減衰スプリングジョイント（2D）

この継手はスプリング状の力によって2つの部材を連結します。

![alt](/godot_recipes/3.x/img/springjoint_example.gif)

以下のプロパティでスプリングの挙動を調整できます。

*  _Length_ : 関節の最大許容長値
*  _Rest Length_ : 外力や運動が作用していない状態における関節の長さ
*  _Stiffness_ : ばねの「伸びにくさ」、すなわち外力に対する抵抗強度を表す指標
*  _Damping_ : ばねが「反発動作」を停止する速度特性を示すパラメータ

### {{< gd-icon GrooveJoint2D >}} GrooveJoint2D

この関節は、接続された物体が直線的に移動するように制約します。

![alt](/godot_recipes/3.x/img/groovejoint_example.gif)

デフォルトでは溝は垂直方向に配置されますが、溝ノードを回転させることでこれを変更できます。

以下のプロパティは溝の動作を制御します。

- _Length_：溝の全長。この最大距離を超える位置まで付属パーツは移動できません。
- _Initial Offset_：溝に沿った起点となる「位置」です。

<!-- You can download an example project to play with these joints here: [physics_joints.zip](/godot_recipes/4.x/ja/files/physics_joints.zip) -->

![alt](/godot_recipes/3.x/img/joints_demo.png)

## 関連するレシピ
