---
title: "Grid-based movement"
weight: 2
draft: false
ghcommentid: 21
---

## 問題文

グリッド状に移動する2Dキャラクターが必要です。

## 解決策

グリッド制またはタイルベースの移動方式では、キャラクターの位置が制限されます。特定のタイル上にのみ立つことができ、2枚のタイルの間に立ち続けることはできません。

### キャラクター設定

以下がプレイヤーで使用するノードです：

- {{< gd-icon Area2D >}}`Area2D` ("Player"): Using an {{< gd-icon Area2D >}}`Area2D` means we can detect overlap (for picking up objects or colliding with enemies).
  - {{< gd-icon Sprite2D >}}`Sprite2D`: You can use a sprite sheet here (we'll set up the animation below).
  - {{< gd-icon CollisionShape2D >}}`CollisionShape2D`: Don't make the hitbox too big. Since the player will be standing on the center of a tile, overlaps will be from the center.
  - {{< gd-icon RayCast2D >}}`RayCast2D`: For checking if movement is possible in the given direction.
  - {{< gd-icon AnimationPlayer >}}`AnimationPlayer`: For playing the character's walk animation(s).

Add some input actions to the Input Map. We'll use "up", "down", "left", and "right" for this example.

### 基本的な動き

まず、アニメーションや補間なしで、タイル単位の移動設定から始めましょう。

```gdscript
extends Area2D

var tile_size = 64
var inputs = {"right": Vector2.RIGHT,
            "left": Vector2.LEFT,
            "up": Vector2.UP,
            "down": Vector2.DOWN}
```

```tile_size``` にはタイルのサイズに合わせて適切な値を設定してください。大規模なプロジェクトでは、メインシーンからプレイヤーインスタンスを生成する際にこの設定を行います。以下の例では 64×64ピクセルのタイルを使用しています。

入力辞書は入力アクション名と方向ベクトルを対応付けます。ここでの名前と入力マップでの表記が完全一致していることを確認してくください（大文字小文字の区別に注意！）。

```gdscript
func _ready():
    position = position.snapped(Vector2.ONE * tile_size)
    position += Vector2.ONE * tile_size/2
```

`snapped()` allows us to "round" the position to the nearest tile increment, and adding a half-tile amount makes sure the player is centered on the tile.

```gdscript
func _unhandled_input(event):
    for dir in inputs.keys():
        if event.is_action_pressed(dir):
            move(dir)

func move(dir):
    position += inputs[dir] * tile_size
```

以下が実際の移動処理コードです。入力イベントが発生すると、4方向をチェックし、該当する方向を特定した後に`move()`関数に渡して位置を変更します。

![alt](/godot_recipes/4.x/img/grid_example1.gif)

### 衝突事故

以下の例のように、障害物を追加する方法はいくつかあります。手動で障害物を追加したい場合は{{< gd-icon StaticBody2D >}}`StaticBody2D`オブジェクトを使用するか（グリッドに正確に配置できるようスナップ機能を有効にしてください）、衝突判定が定義されたTileMapを利用することもできます。

```
移動先タイルへの進入が許可されているかどうかを判定するために、`RayCast2D` 機能を使用します。

```gdscript
onready var ray = $RayCast2D

func move(dir):
    ray.target_position = inputs[dir] * tile_size
    ray.force_raycast_update()
    if !ray.is_colliding():
        position += inputs[dir] * tile_size
```

レイキャストの `target_position` プロパティを変更する場合、物理エンジンは次の物理フレームまで衝突を再計算しません。`force_raycast_update()` を使用すると、即座にレイの状態を更新できます。もし衝突が発生していなければ、移動は許可されます。

![alt](/godot_recipes/4.x/img/grid_example2.gif)

{{% notice note %}}
もう一つの一般的な方法として、各方向に一つずつ計4つのレイキャストを使用する手法があります。
{{% /notice %}}

### 動きのアニメーション化

最後にタイル間の位置補間を行い、滑らかな移動感を実現します。アニメーションには`Tween`ノードを使用して`position`プロパティを制御します。

```gdscript

var animation_speed = 3
var moving = false
```

ノード `Tween` に参照を追加し、移動速度を設定する変数を作成します。

```gdscript
func _unhandled_input(event):
    if moving:
        return
    for dir in inputs.keys():
        if event.is_action_pressed(dir):
            move(dir)
```

```python
while tween_running:
    # トゥイーン実行中は入力を無視し、直接的な位置変更を削除して
    # トゥイーンが適切に処理できるようにする。
    pass
```

```gdscript
func move(dir):
    ray.target_position = inputs[dir] * tile_size
    ray.force_raycast_update()
    if !ray.is_colliding():
        #position += inputs[dir] * tile_size
        var tween = create_tween()
        tween.tween_property(self, "position",
            position + inputs[dir] *    tile_size, 1.0/animation_speed).set_trans(Tween.TRANS_SINE)
        moving = true
        await tween.finished
        moving = false
```




![alt](/godot_recipes/4.x/img/grid_example3.gif)

異なるトランジション効果を試してみましょう：

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらよりダウンロード可能です：[https://github.com/godotrecipes/2d_grid_movement/](https://github.com/godotrecipes/2d_grid_movement/)

<!-- ## 関連するレシピ

- [Input Actions](/godot_recipes/3.x/input/input_actions/)
- [Interpolation](/godot_recipes/3.x/math/interpolation/) -->