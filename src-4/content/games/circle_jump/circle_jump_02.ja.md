---
title: "サークルをスポーンさせる"
weight: 2
draft: false
pre: "02. "
---

前回のパートでは、ゲームの中核をなす`ジャンパー`オブジェクトと`サークル`オブジェクトを作成しました。次に、プレイヤーがミスするまで連続して出現するサークルの進行システムを追加する必要があります。

## メインシーンの拡張

メイン・ノードにさらにノードを追加しましょう。

- **Marker2D ("StartPosition")**

    このゲームの開始位置をマークします。画面中央下部付近に置いてください。

- **カメラ 2D**

    カメラはプレイヤーの動きに合わせて追従します。

    カメラの設定も行いましょう。 _オフセット_ を `(0, -200)` に設定してください。これにより、前方の世界をより広く確認できるようになります。また、カレントモードは「オン」に設定してください。

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
    player = Jumper.instantiate()
    player.position = $StartPosition.position
    add_child(player)
    player.connect("captured", self, "_on_Jumper_captured")
    spawn_circle($StartPosition.position)
```

「new_game()」関数は、プレイヤーと円を開始位置にスポーンさせ、カメラを設定することでゲームを初期化します。

```gdscript
func spawn_circle(_position=null):
    var c = Circle.instantiate()
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

カメラが次のサークルに移動するときに「瞬間移動」してしまうのは不自然です。これは、カメラの「Smoothing」を有効にすることで改善できます。「Smoothing/Speed」は、新しい位置への補間の速さを制御します。`5`から`10`の間で試してみてください。

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

## トレイルコース

これらのノードをジャンパに追加してください。

* `Node` ("Trail")
  * `Line2D` ("Points")

We're going to use this to make a trail that streams out behind the player. Later we'll make it more visually appealing, but for now, let's stick with a simple gradient. In the _Fill_ add a new Gradient, and go from transparent to a color of your choosing:

![alt](/godot_recipes/3.x/img/cj_02_01.png?width=200)

ジャンパのスクリプトに、以下を追加しましょう。

```gdscript
@onready var trail = $Trail/Points

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

新しいアニメーション「implode」を追加してください。長さを 0.4 に設定し、ルートノードである Area2D の 2 つのプロパティにキーフレームを設定してください。スケールは (1, 1) に、モジュレートはデフォルト値 (1, 1, 1, 1) に。その後、スクラブバーを最後まで移動させ、値として (0.1, 0.1) と (1, 1, 1, 0) を設定します（これは色のアルファ値です）。

![alt](/godot_recipes/3.x/img/cj_02_02.png)

### アニメーションのキャプチャ

キャプチャアニメーションはもう少し複雑です。スプライトを複製して「SpriteEffect」という名前に変更してください。その［表示］プロパティはオフに設定します。この二つ目のリングがメインサークルに向かってズームインするアニメーションを作成します。

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