---
title: "サークルをスポーンさせる"
weight: 2
draft: false
pre: "02. "
---

前回のパートでは、ゲームの中核をなす`ジャンパー`オブジェクトと`サークル`オブジェクトを作成しました。次に、プレイヤーがミスするまで連続して出現するサークルの進行システムを追加する必要があります。

## メインシーンの拡張

メイン・ノードにさらにノードを追加しましょう。

- **Position2D ("StartPosition")**

    このゲームの開始位置をマークします。画面中央下部付近に置いてください。

- **カメラ 2D**

    カメラはプレイヤーの動きに合わせて追従します。

    Let's also configure the camera. Set its _Offset_ to `(0, -200)` - this will ensure we can see more of the world ahead of us. Also set _Current_ to "On".

## メインシーンのスクリプト化

手動で作成したジャンパーと円のインスタンスを削除します。今後はコード内で追加するようにします。

以下を`Jumper.gd`に追加してください。

```gdscript
signal captured
```

ジャンパーが円に接触した時に、このシグナルを発生させます。

```gdscript
func _on_Jumper_area_entered(area):
    target = area
    velocity = Vector2.ZERO
    emit_signal("captured", area)
```

また、円の `init()` 関数を修正して、位置も受け取れるようにしましょう。

```gdscript
func init(_position, _radius=radius):
    position = _position
```

それでは、「メイン」シーンにスクリプトを追加しましょう。

```gdscript
extends Node

var Circle = preload("res://objects/Circle.tscn")
var Jumper = preload("res://objects/Jumper.tscn")

var player
```

We need references to both objects so that we can instance them when needed.

```gdscript
func _ready():
    randomize()
    new_game()
```

これは一時的なものです。後で新規ゲーム機能を呼び出すスタートボタンを備えたUIを実装する予定です。

```gdscript
func new_game():
    $Camera2D.position = $StartPosition.position
    player = Jumper.instance()
    player.position = $StartPosition.position
    add_child(player)
    player.connect("captured", self, "_on_Jumper_captured")
    spawn_circle($StartPosition.position)
```

「new_game()」関数は、プレイヤーと円を開始位置にスポーンさせ、カメラを設定することでゲームを初期化します。

```gdscript
func spawn_circle(_position=null):
    var c = Circle.instance()
    if !_position:
        var x = rand_range(-150, 150)
        var y = rand_range(-500, -400)
        c.position = player.target.position + Vector2(x, y)
    add_child(c)
    c.init(_position)
```

こちらが`spawn_circle()`関数です。位置を指定すればその位置にオブジェクトを配置し、指定しない場合は現在のターゲットから一定距離離れた場所にランダム配置されます。これらの数値は暫定値であり、ゲームプレイシステムが完全に実装された後に微調整を行う予定です。

```gdscript
func _on_Jumper_captured(object):
    $Camera2D.position = object.position
    call_deferred("spawn_circle")
```

最後に、ジャンパーの「captured」シグナルを処理する関数が必要です。この関数ではカメラを新しい円に移動させ、別のインスタンスを生成します。なお、この関数は物理演算処理中に呼び出されるため、シーンツリーに追加しようとするとエラーが発生します。`call_deferred()` を使うことで、エンジンが安全に実行できるタイミングが来るまでその関数の実行を遅延させることができます。

試してみてください。円から円へジャンプできるはずです。いくつ成功しましたか？

One jarring thing is that the camera "teleports" when it moves to the next circle. We can improve this by enabling _Smoothing_ on the camera. The _Smoothing/Speed_ controls how quickly the camera interpolates to the new position. Try something between `5` and `10`.

### 調整項目

また、円オブジェクトに衝突してもその場で回転が開始されない点も違和感があります。以下のコードをジャンパー用の`_on_Jumper_area_entered()`関数に追加してください。

```gdscript
target.get_node("Pivot").rotation = (position - target.position).angle()
```

Circleの`init()`メソッドにもこれを追加しておきましょう。

```gdscript
rotation_speed *= pow(-1, randi() % 2)
```

この機能はランダムに回転速度の向きを正または負に切り替えるため、常に同じ方向に周回するわけではありません。

## トレイル

これらのノードをジャンパに追加してください。

* `Node` ("Trail")
  * `Line2D` ("Points")

We're going to use this to make a trail that streams out behind the player. Later we'll make it more visually appealing, but for now, let's stick with a simple gradient. In the _Fill_ add a new Gradient, and go from transparent to a color of your choosing:

![alt](/godot_recipes/3.x/img/cj_02_01.png?width=200)

ジャンパのスクリプトに、以下を追加しましょう。

```gdscript
onready var trail = $Trail/Points

var trail_length = 25
```

そして `_physics_process()` 内では：

```gdscript
if trail.points.size() > trail_length:
    trail.remove_point(0)
trail.add_point(position)
```

**画像 / GIF**

## サークルアニメーション

最後に、円に視覚効果を追加します。まず、プレイヤーがジャンプして離れた時に円が消えるエフェクトを実装します。さらに、円に触れた際のキャプチャーエフェクトも追加します。

Circle ノードに `アニメーションPlayer` を追加します。

### 「インプロージョン」アニメーション

Add a new animation called "implode". Set the length to 0.4 and keyframe two properties of the root `Area2D` node: _Scale_ at `(1, 1)` and _Modulate_ at its default (`(1, 1, 1, 1)`). Then move the scrubber all the way to the end and key the values `(0.1, 0.1)` and `(1, 1, 1, 0)` (that's the "alpha" value of the color).

![alt](/godot_recipes/3.x/img/cj_02_02.png)

### アニメーションのキャプチャ

The capture animation is a little more complex. Duplicate the Sprite and call it `SpriteEffect`. Set its _Visible_ property off. We're going to animate this second ring zooming in on the main circle.

![alt](/godot_recipes/3.x/img/cj_02_03.png)
![alt](/godot_recipes/3.x/img/cj_02_04.gif)

以下の機能をサークルスクリプトに追加する必要があります。

```gdscript
func capture():
    $AnimationPlayer.play("capture")

func implode():
    if !$AnimationPlayer.is_playing():
        $AnimationPlayer.play("implode")
    yield($AnimationPlayer, "animation_finished")
    queue_free()
```

And then in `Jumper.gd`, our jump function becomes:

```gdscript
func jump():
    target.implode()
    target = null
    velocity = transform.x * jump_speed
```

メイン画面では、「キャプチャ」メソッドが実際のキャプチャ処理を実行します。

```gdscript
func _on_Jumper_captured(object):
    $Camera2D.position = object.position
    object.capture()
    call_deferred("spawn_circle")
```

**GIF**

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube ahsFSeDbG84 >}}