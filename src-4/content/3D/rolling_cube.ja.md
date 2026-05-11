---
title: "転がるキューブ"
weight: 6
draft: false
ghcommentid: 101
---

## 課題

3Dで回転するキューブを作成したい。

<video width="500" controls src="/godot_recipes/4.x/img/rolling_cube.webm"></video>

## 解決策

キューブを転がすのは見た目より難しいです。単に中心軸を中心に回すだけではうまくいきません：

![alt](/godot_recipes/4.x/img/cube_001.gif)

代わりに、キューブを底面のエッジを中心に回転させます。

![alt](/godot_recipes/4.x/img/cube_002.gif)

ここが重要なポイントです。どの底面の縁でしょうか？ それは、キューブがどの方向に転がっているかによって異なります。

このレシピを作成するにあたり、異なる解決策を試しました。

* 純粋数学 - 回転変換の計算と適用
* AnimationPlayer - アニメーションを用いた回転およびオフセット制御
* ヘルパーノード - RotationHelperとしてNode3Dを利用

すべて正常に動作しましたが、最後のオプションが最も柔軟で設定しやすいと感じたので、ここではその方法を採用します。

### ノード設定

```
Cube: {{< gd-icon CharacterBody3D >}} CharacterBody3D
    Pivot: {{< gd-icon Node3D >}} Node3D
        Mesh: {{< gd-icon MeshInstance3D >}} MeshInstance3D
    Collision: {{< gd-icon CollisionShape3D >}} CollisionShape3D
```

{{< gd-icon `RigidBody3D` >}}{{% notice tip %}}
「{{< gd-icon `CharacterBody3D` >}}`CharacterBody3D`」、または {{< gd-icon Area3D >}} 「Area3D」を衝突ノードとして使用できます。ただし、移動制御の方法には若干の違いが生じます。どのノードを選択するかは、ゲームで他にどのような挙動を必要とするかによって決めるべきです。このレシピでは、単に動きに焦点を当てています。
{{% /notice %}}

デフォルトでは、すべてが座標 `(0, 0, 0)` を中心に配置されています。まず最初に行うことは、キューブの*底面中央*が {{< gd-icon CharacterBody3D >}}`CharacterBody3D` の位置と一致するように全体をオフセットすることです。

{{< gd-icon `BoxMesh3D` >}}デフォルトのサイズが `(1, 1, 1)` の場合、以下のように設定します。メッシュノードと衝突判定ノードを両方とも `(0, 0.5, 0)` に移動し、その他は元のままにします。これでルートノードを選択すると、その位置がキューブの *底面* に対応します。

![alt](/godot_recipes/4.x/img/cube_003.png)

これでキューブを転がしたい場合、`Pivot`を「移動させたい方向」に`0.5`ユニット動かす必要があります。メッシュはオブジェクトに取り付けられているため、反対方向に同じ量だけ動かさなければなりません。例えば、右方向へ転がす場合（**+X**軸方向）、最終的に以下のコードになります。

![alt](/godot_recipes/4.x/img/cube_004.gif)

現在、ピボットノードは正しいエッジ上に配置されており、これを回転させるとメッシュ全体が一緒に回転します。

### 移動スクリプト

この動作は3つのステップに分かれています。

#### ステップ1

以下のように、先に示した2つのオフセットを適用します。`Pivot`を移動方向にシフトし、`Mesh`をその反対方向にシフトします。

#### ステップ2

このステップでは、回転アニメーションを実装します。方向ベクトルと下方ベクトルの**外積**を用いて、回転軸を計算します。その後、{{< gd-icon Tween >}}`Tween` を使用してピボット要素の `transform` プロパティをアニメーションさせ、滑らかな回転効果を実現します。

#### ステップ3

アニメーションが終了したら、初期状態にリセットして次回の動作に備えます。キューブが選択方向に1単位移動し（サイズ1のキューブの場合）、かつピボットとメッシュが元の位置に戻るようにしたいということです。

```gdscript
extends CharacterBody3D

@onready var pivot = $Pivot
@onready var mesh = $Pivot/MeshInstance3D

var cube_size = 1.0
var speed = 4.0
var rolling = false

func _physics_process(delta):
    var forward = Vector3.FORWARD
    if Input.is_action_pressed("ui_up"):
        roll(forward)
    if Input.is_action_pressed("ui_down"):
        roll(-forward)
    if Input.is_action_pressed("ui_right"):
        roll(forward.cross(Vector3.UP))
    if Input.is_action_pressed("ui_left"):
        roll(-forward.cross(Vector3.UP))

func roll(dir):
    # Do nothing if we're currently rolling.
    if rolling:
        return
    rolling = true

    # Step 1: Offset the pivot.
    pivot.translate(dir * cube_size / 2)
    mesh.global_translate(-dir * cube_size / 2)

    # Step 2: Animate the rotation.
    var axis = dir.cross(Vector3.DOWN)
    var tween = create_tween()
    tween.tween_property(pivot, "transform",
            pivot.transform.rotated_local(axis, PI/2), 1 / speed)
    await tween.finished

    # Step 3: Finalize the movement and reset the offset.
    transform.origin += dir * cube_size
    var b = mesh.global_transform.basis
    pivot.transform = Transform3D.IDENTITY
    mesh.position = Vector3(0, cube_size / 2, 0)
    mesh.global_transform.basis = b
    rolling = false
```

キューブのテクスチャが非対称の場合、転がすたびにリセットされることに気付くかもしれません。メッシュの回転を保持するには、以下を追加してください。

ステップ1では：

翻訳を修正してください: `mesh.translate(-dir)` を `mesh.global_translate(-dir)` に変更してください。

ステップ3では：

Mesh の回転を保持するために 2 行追加してください。

```gdscript
    # Step 3: Finalize the movement and reset the offset.
	transform.origin += dir * cube_size
	var b = mesh.global_transform.basis  # Save the mesh rotation.
	pivot.transform = Transform3D.IDENTITY
	mesh.position = Vector3(0, cube_size / 2, 0)
	mesh.global_transform.basis = b  # Restore the mesh rotation.
```

### 衝突のチェック

ゲームに障害物を導入する場合、移動前に衝突判定を行えます（他のグリッドベース移動方式と同様）。移動処理の**ステップ1**の前に、レイキャストによる衝突チェックを追加してください。

```gdscript
# Cast a ray before moving to check for obstacles
var space = get_world_3d().direct_space_state
var ray = PhysicsRayQueryParameters3D.create(mesh.global_position,
        mesh.global_position + dir * cube_size, collision_mask, [self])
var collision = space.intersect_ray(ray)
if collision:
    return
```

{{% notice note %}}
以下の方法も使用できます。{{< gd-icon RayCast3D >}}`RayCast3D`ノードを使用する場合。ただし、チェックを実行する前に必ず`force_raycast_update()`を呼び出すようにしてください。
{{% /notice %}}

### トランジションで遊んでみよう

使用する`TransitionType`を変更することで、キューブの転がり動作に様々な個性を持たせることができます。デフォルトは`Tween.TRANS_LINEAR`で、これにより移動全体を通じて一定速度が得られます。

移行タイプを変更するだけで、全く異なる印象を得られます。例えば。

```gdscript
var tween = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN)
```

<!-- gif -->

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらからダウンロードできます。[https://github.com/godotrecipes/rolling_cube](https://github.com/godotrecipes/rolling_cube)

## 関連レシピ

- [トランスフォーム](/godot_recipes/4.x/ja/math/transforms/)
