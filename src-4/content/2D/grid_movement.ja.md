---
title: "グリッドベースの移動"
weight: 2
draft: false
ghcommentid: 21
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

グリッド状に移動する2Dキャラクターが必要です。

## 解決策

グリッド制またはタイルベースの移動方式では、キャラクターの位置が制限されます。特定のタイル上にのみ立つことができ、2枚のタイルの間に立ち続けることはできません。

### キャラクター設定

以下がプレイヤーで使用するノードです。

- {{< gd-icon Area2D >}}`Area2D` ("プレイヤー"): {{< gd-icon Area2D >}}`Area2D` を使用することで、オブジェクトのピックアップや敵との衝突判定が実現できます。
  - {{< gd-icon Sprite2D >}}`Sprite2D`: ここではスプライトシートを使用できます（アニメーション設定は後述します）。
  - {{< gd-icon CollisionShape2D >}}`CollisionShape2D`: ヒットボックスが大きすぎないように注意してください。プレイヤーがタイルの中心に立つため、オーバーラップ判定も中央から行われます。
  - {{< gd-icon RayCast2D >}}`RayCast2D`: 指定された方向への移動が可能かどうかを確認する際に使われます。
  - {{< gd-icon AnimationPlayer >}}`AnimationPlayer`: キャラクターの歩行アニメーションを再生に使います。

インプットマップに操作を追加してください。この例では「上」「下」「左」「右」を使用します。

### 基本的な動き

まず、アニメーションや補間なしで、タイル単位の移動設定から始めてください。

```gdscript
extends Area2D

var tile_size = 64
var inputs = {"right": Vector2.RIGHT,
            "left": Vector2.LEFT,
            "up": Vector2.UP,
            "down": Vector2.DOWN}
```

`tile_size`にはタイルのサイズに合わせて適切な値を設定してください。大規模なプロジェクトでは、メインシーンからプレイヤーインスタンスを生成する際にこを設定します。以下の例では 64×64ピクセルのタイルを使用しています。

`inputs` Dictonaryは入力アクション名と方向ベクトルを対応付けます。ここでの名前とインプットマップでの表記が完全一致していることを確認してくください（大文字小文字の区別に注意！）。

```gdscript
func _ready():
    position = position.snapped(Vector2.ONE * tile_size)
    position += Vector2.ONE * tile_size/2
```

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

以下の例のように、障害物を追加する方法は複数あります。手動で障害物を追加したい場合は{{< gd-icon StaticBody2D >}}`StaticBody2D`オブジェクトを使用するか（グリッドに正確に配置できるようスナップ機能を有効にしてください）、衝突判定が定義されたTileMapを利用することもできます。

移動先タイルへの進入が許可されているかどうかを判定するために、{{< gd-icon RayCast2D >}}`RayCast2D` 機能を使用します。

```gdscript
@onready var ray = $RayCast2D

func move(dir):
    ray.target_position = inputs[dir] * tile_size
    ray.force_raycast_update()
    if !ray.is_colliding():
        position += inputs[dir] * tile_size
```

レイキャストの `target_position` プロパティを変更する場合、物理エンジンは次の物理フレームまで衝突を再計算しません。`force_raycast_update()` を使用すると、即座にレイの状態を更新できます。もし衝突が発生していなければ、移動できます。

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

ノード {{< gd-icon Tween >}}`Tween` に参照を追加し、移動速度を設定する変数を作成します。

```gdscript
func _unhandled_input(event):
    if moving:
        return
    for dir in inputs.keys():
        if event.is_action_pressed(dir):
            move(dir)
```

Tween が実行されている間は入力を無視し、直接的な `位置` 変更を無効とすることで、Tween自体がその処理を行えるようにします。

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

異なるトランジション効果を試してみます。

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらよりダウンロードできます。[https://github.com/godotrecipes/2d_grid_movement/](https://github.com/godotrecipes/2d_grid_movement/)

<!-- ## 関連レシピ

- [入力アクション設定](/godot_recipes/4.x/ja/input/input_actions/)
- [補間処理](/godot_recipes/4.x/ja/math/interpolation/) -->