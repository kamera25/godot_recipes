---
title: "回転立方体"
weight: 6
draft: false
ghcommentid: 101
---

## 課題

3Dで回転する立方体を作成したいのですね。

<video width="500" controls src="/godot_recipes/4.x/img/rolling_cube.webm"></video>

## 解決策

立方体を回転させるのは見た目より難しいです。単に中心軸を中心に回すだけではうまくいきません：

![alt](/godot_recipes/4.x/img/cube_001.gif)

その代わり、立方体はその底面のエッジを中心に回転させる必要があります。

![alt](/godot_recipes/4.x/img/cube_002.gif)

ここが重要なポイントです：どの底面の縁でしょうか？ それは、立方体がどの方向に転がっているかによって異なります。

このレシピを作成するにあたり、私はいくつかの異なる解決策を試しました：

・純粋数学 - 回転変換の計算と適用
・アニメーションPlayer - アニメーションを使用して回転値とオフセットをキー設定
・補助ノード - 空間オブジェクトを回転ヘルパーとして使用

すべて正常に動作しましたが、最後のオプションが最も柔軟で設定しやすいと感じたので、ここではその方法を採用します。

### ノード設定

```
Cube: {{< gd-icon CharacterBody3D >}} CharacterBody3D
    Pivot: {{< gd-icon Node3D >}} Node3D
        Mesh: {{< gd-icon MeshInstance3D >}} MeshInstance3D
    Collision: {{< gd-icon CollisionShape3D >}} CollisionShape3D
```

「CharacterBody3D」、または {{< gd-icon Area3D >}} 「Area3D」を衝突ノードとして使用できます。ただし、移動制御の方法には若干の違いが生じます。どのノードを選択するかは、ゲームで他にどのような挙動を必要とするかによって決めるべきです。このレシピでは、単に動きに焦点を当てています。


デフォルトでは、すべてが座標 `(0, 0, 0)` を中心に配置されています。まず最初に行うことは、立方体の*底面中央*が {{< gd-icon CharacterBody3D >}}`CharacterBody3D` の位置と一致するように全体をオフセットすることです。

デフォルトのサイズが `(1, 1, 1)` の場合、以下のように設定します。メッシュノードと衝突判定ノードを両方とも `(0, 0.5, 0)` に移動し、その他は元のままにします。これでルートノードを選択すると、その位置がキューブの *底面* に対応します。

![alt](/godot_recipes/4.x/img/cube_003.png)

Now when you want to roll the cube, you'll need to move the `Pivot` `0.5` in the direction you want to move. Since the mesh is attached, you need to move it the opposite amount. For example, to roll to the right (**+X**), you'll end up with this:

!

現在、ピボットノードは正しいエッジ上に配置されており、これを回転させるとメッシュ全体が一緒に回転します。

### 移動スクリプト

この動作は3つのステップに分かれています：

#### ステップ1

以下のように、先に示した2つのオフセットを適用します。「ピボット」を移動方向にシフトし、「メッシュ」はその反対方向にシフトします。

#### ステップ2

このステップでは、回転アニメーションを実装します。方向ベクトルと下方ベクトルの**外積**を用いて、回転軸を計算します。その後、{{< gd-icon Tween >}}`Tween` を使用してピボット要素の `transform` プロパティをアニメーションさせ、滑らかな回転効果を実現します。

#### ステップ3

最終的にアニメーションが終了したら、すべてを初期状態にリセットして、次回の動作に備えておく必要があります。最終的には、立方体が選択方向に1単位移動し（サイズ1の立方体の場合）、かつピボットとメッシュが元の位置に戻るようにしたいということです。

```gdscript
extends CharacterBody3D

@onready var pivot = $Pivot
@onready var mesh = $Pivot/MeshInstance3D

var cube_size = 1.0
var speed = 4.0
var rolling = false

func _physics_process(delta):
    var forward = Vector3.FORWARD
    if 入力.is_action_pressed("ui_up"):
        roll(forward)
    if 入力.is_action_pressed("ui_down"):
        roll(-forward)
    if 入力.is_action_pressed("ui_right"):
        roll(forward.cross(Vector3.UP))
    if 入力.is_action_pressed("ui_left"):
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

Mesh の回転を保持するために 2 行追加します。

```gdscript
    # Step 3: Finalize the movement and reset the offset.
	transform.origin += dir * cube_size
	var b = mesh.global_transform.basis  # Save the mesh rotation.
	pivot.transform = Transform3D.IDENTITY
	mesh.position = Vector3(0, cube_size / 2, 0)
	mesh.global_transform.basis = b  # Restore the mesh rotation.
```

### 衝突チェック中

ゲームに障害物を導入する場合、移動前に衝突判定を行うことができます（他のグリッドベース移動方式と同様）。移動処理の**ステップ1**の前に、レイキャストによる衝突チェックを追加してください。

```gdscript
# Cast a ray before moving to check for obstacles
var space = get_world_3d().direct_space_state
var ray = 物理RayQueryParameters3D.create(mesh.global_position,
        mesh.global_position + dir * cube_size, collision_mask, [self])
var collision = space.intersect_ray(ray)
if collision:
    return
```

{{% notice note %}}
以下の方法も使用可能です：{{< gd-icon RayCast3D >}}`RayCast3D`ノードを使用する場合。ただし、チェックを実行する前に必ず`force_raycast_update()`を呼び出すようにしてください。
{{% /notice %}}

### トランジションで遊んでみよう

public void setMoveSpeedFactor(double factor) {
    this.moveSpeedFactor = factor;
}

移行タイプを変更するだけで、全く異なる印象を得られます。例えば：

```gdscript
var tween = create_tween().set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_IN)
```

<!-- gif -->

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます：[https://github.com/godotrecipes/rolling_cube](https://github.com/godotrecipes/rolling_cube)

## 関連レシピ

- [変換処理](/godot_recipes/4.x/ja/math/transforms/)
