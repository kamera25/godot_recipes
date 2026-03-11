---
title: "Grid-based movement"
weight: 2
draft: false
ghcommentid: 21
---

## 課題

グリッド状に移動する2Dキャラクターが必要です。

## 解決策

グリッド制またはタイルベースの移動方式では、キャラクターの位置が制限されます。特定のタイル上にのみ立つことができ、2枚のタイルの間に立ち続けることはできません。

### キャラクター設定

以下がプレイヤーで使用するノードです：

- `Area2D` ("プレイヤー"): `Area2D` を使用することで、オブジェクトのピックアップや敵との衝突判定が可能になります。
  - `Sprite2D`: ここではスプライトシートを使用できます（アニメーション設定は後述します）。
  - `CollisionShape2D`: ヒットボックスが大きすぎないように注意してください。プレイヤーがタイルの中心に立つため、オーバーラップ判定も中央から行われます。
  - `RayCast2D`: 指定された方向への移動が可能かどうかを確認する際に使われます。
  - `AnimationPlayer`: キャラクターの歩行アニメーションを再生するために使用します。

入力マップにいくつかの操作を追加しましょう。この例では「上」「下」「左」「右」を使用します。

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

入力Dictonaryは入力アクション名と方向ベクトルを対応付けます。ここでの名前と入力マップでの表記が完全一致していることを確認してくください（大文字小文字の区別に注意！）。

```gdscript
func _ready():
    position = position.snapped(Vector2.ONE * tile_size)
    position += Vector2.ONE * tile_size/2
```

```bash
`snapped()` 関数は位置をタイルの増分に最も近い値に「丸め」ます。さらに、半タイル量を追加することで、プレイヤーが必ずタイル中心に配置されるようになります。

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

while tween_running:
    # トゥイーン実行中は入力を無視し、直接的な位置変更を削除して
    # トゥイーンが適切に処理できるようにする。
    pass

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

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらよりダウンロード可能です：[https://github.com/godotrecipes/2d_grid_movement/](https://github.com/godotrecipes/2d_grid_movement/)

<!-- ## 関連するレシピ

- [Input Actions](/godot_recipes/3.x/input/input_actions/)
- [Interpolation](/godot_recipes/3.x/math/interpolation/) -->