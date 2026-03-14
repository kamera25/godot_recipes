---
title: "産卵サークル"
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

    カメラの設定も行いましょう。オフセットを `(0, -200)` に設定してください - これにより、前方の世界をより広く確認できるようになります。また、カレントモードは「オン」に設定してください。

## メインシーンのスクリプト化

手動で作成したジャンパーと円のインスタンスを削除します。今後はコード内で追加するようにします。

以下を`Jumper.gd`に追加してください。

```gdscript
signal captured
```

ジャンパーが円に接触した時に、このシグナルを発生させます：

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

需要が発生した際にインスタンス化できるよう、両方のオブジェクトに対する参照が必要です。

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

function new_game() {
  // ゲームを初期化: プレイヤーとサークルを開始位置に生成し、カメラを設定する
}


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


※注意点：翻訳文では技術的な専門用語をそのまま使用していますが、より平易な表現にする場合は以下のようになります。

「カメラが次の円に移動する際に『瞬間移動』するように見える点が気になります。この問題は、カメラの［スムージング］機能を有効にすることで改善できます。［スムージング/速度］コントロールでは、カメラが新しい位置に補間されるスピードを調整します。`5`～`10`程度の間で設定してみてください。」

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

* `ノード` ("軌跡"):
     * `直線2次元` ("点"):

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

新しいアニメーション「implode」を追加してください。長さを 0.4 に設定し、ルートノードである Area2D の 2 つのプロパティにキーフレームを設定してください。スケールは (1, 1) に、モジュレートはデフォルト値 (1, 1, 1, 1) に。その後、スクラブバーを最後まで移動させ、値として (0.1, 0.1) と (1, 1, 1, 0) を設定します（これは色のアルファ値です）。

<img src="/godot_recipes/3.x/img/cj_02_02.png" alt="">

### アニメーションのキャプチャ

キャプチャアニメーションはもう少し複雑です。スプライトを複製して「SpriteEffect」という名前に変更してください。その［表示］プロパティはオフに設定します。この二つ目のリングがメインサークルに向かってズームインするアニメーションを作成します。

![alt](/godot_recipes/3.x/img/cj_02_03.png)
![alt](/godot_recipes/3.x/img/cj_02_04.gif)

以下の機能をサークルスクリプトに追加する必要があります：

```gdscript
func capture():
    $アニメーションPlayer.play("capture")

func implode():
    if !$アニメーションPlayer.is_playing():
        $アニメーションPlayer.play("implode")
    yield($アニメーションPlayer, "animation_finished")
    queue_free()
```

function Jump()
    if IsGrounded() then
        velocity = Vector3(0, 0, 0) -- ジャンプアニメーションの初期化
    else
        velocity = Vector3(jumpForce * Time.deltaTime, 0, 0) -- 重力を考慮した移動速度計算
    end
    isJumping = true
end


```gdscript
func jump():
    target.implode()
    target = null
    velocity = transform.x * jump_speed
```

メイン画面では、「キャプチャ」メソッドが実際のキャプチャ処理を実行します：

```gdscript
func _on_Jumper_captured(object):
    $Camera2D.position = object.position
    object.capture()
    call_deferred("spawn_circle")
```

**GIF**

----------

#### このプロジェクトをGitHubでフォローしよう：

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube ahsFSeDbG84 >}}