---
title: "RayCast2D"
draft: false
ghcommentid: 87
---

## {{< gd-icon RayCast2D >}}RayCast2D

*レイキャスティング* はゲーム開発で広く用いられる手法です。「レイを飛ばす(キャストする)」とは、ある点から直線を伸ばし、それが何かに衝突するか限界に達するまで移動させる操作を指します。

### ノードのプロパティ

{{< gd-icon RayCast2D >}}`RayCast2D` ノードを追加して、インスペクターを確認します。

![alt](/godot_recipes/4.x/img/kyn_raycast2d_01_4.png)

以下に主要な特性をご説明します。

* **Enabled**

この機能を無効にするとレイキャスト操作が無効化されます。

* **Exclude Parent**

このプロパティにより、レイは親オブジェクトとの衝突を無視するようになります。デフォルトで有効になっています。

* **Target Position**

これはレイの到達点です。※注：この座標系はローカル座標です。

また、「衝突対象」セクションにも注意してください。初期設定ではレイはオブジェクトのみを検出するため、領域も検知したい場合や代わりに使用したい場合は、ここで設定する必要があります。

### 便利な機能

ノードの機能一覧は[APIドキュメント](https://docs.godotengine.org/ja/stable/classes/class_raycast2d.html)で確認できます。特に便利な主要機能をいくつかご紹介します。

* `is_colliding()`

ブール型関数。レイが何らかの物体と衝突しているかどうかを判定します。

*  `get_collision_point()`

光線が衝突している場合、この関数は衝突位置をグローバル座標系で返します。

* `get_collider()`

衝突が発生している場合、この関数は衝突中のオブジェクトへの参照を返します。

* `get_collision_normal()`

別の有用な情報として、衝突点における衝突オブジェクトの法線ベクトルを示します。

### 使用例

レイキャストには多様な用途があります。可視判定（AはBを確認できるか、その間に障害物はないか）、近接検出（壁や地面、障害物の近くにいるか）などです。以下に実用的な使用例をいくつかご紹介します。

#### 1. 撮影プロセス

高速で移動する発射物には、障害物を「すり抜けてしまう」という問題がよく発生します。これは、衝突判定が1フレーム内で検出できないほど物体の移動速度が速いためです。代替案として、経路（あるいはレーザーなど）を表現するには {{< gd-icon RayCast2D >}}`Raycast2D` を使用する方法があります。

ここに、銃の先端にレイキャストが取り付けられたプレイヤースプライトがあります。`target_position`は`(250, 0)`に設定されています。

![alt](/godot_recipes/4.x/img/kyn_raycast2d_02.png)

プレイヤーが射撃した際、光線が何かに衝突しているかどうかを判定します。

```gdscript
func _input(event):
    if event.is_action_pressed("shoot"):
        if $RayCast2D.is_colliding():
            print($RayCast2D.get_collider().name)
```

#### 2. エッジ検出処理

以下の方法でmobに下向きレイキャストを2つ追加してください。

![alt](/godot_recipes/4.x/img/kyn_raycast2d_03.png)

モブキャラクターのスクリプト内で、レイが衝突を*停止*したときを確認します。その時点までに境界線に到達したことを意味するので、向きを変える必要があります。

```gdscript
func _physics_process(delta):
    velocity.y += gravity * delta
    if not $RayRight.is_colliding():
        dir = -1
    if not $RayLeft.is_colliding():
        dir = 1
    velocity.x = dir * speed
    $AnimatedSprite.flip_h = velocity.x > 0
    velocity = move_and_slide(velocity, Vector2.UP)
```

動作中の様子をご覧ください。

![alt](/godot_recipes/4.x/img/kyn_raycast2d_04.gif)

## 関連レシピ

- [Interpolated Camera](/godot_recipes/3.x/3d/interpolated_camera/)
- [Inputs: Introduction](/godot_recipes/3.x/input/input_intro/)
- [CharacterBody3D: Movement](/godot_recipes/3.x/3d/kinematic_body/) -->

<!-- #### Videoが気に入ったら？ -->

{{< youtube Lx2d5cgMj5U >}} -->