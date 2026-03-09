---
title: "Coding the Player"
weight: 3
draft: false
pre: "03. "
---

最後のセクションでは、プロジェクトを設定し、ゲームアートをダウンロードしました。これでコーディングを開始する準備が整いました。まずはプレイヤー操作可能な宇宙船から着手しましょう。

## スクリプトの追加方法

```
スクリプトを記述してノードやその他のオブジェクトにアタッチすることは、ゲームの動作やメカニクスを構築する基本的な方法です。現在の`Player`シーンでは宇宙船を表示し、その衝突判定ボックスなどを定義していますが、実際には移動できず、仮に他のものと衝突しても何の反応も生じません。この機能を追加するため、これからコードを実装していきます。

選択してください：

[alt](/godot_recipes/4.x/img/2d_101_13.png)

**ノードスクリプトの添付** ウィンドウでオプションを変更する必要はありませんので、単に **作成** ボタンをクリックすると、スクリプトエディタに移動します。

スクリプトの最初の行を見てみましょう。これは自動的に追加されたものです。

```gdscript
extends Area2D
```

この行はこのスクリプトをアタッチすべきオブジェクトのタイプを指定しています。つまり、スクリプトは `{{< gd-icon Area2D >}}Area2D` が提供するすべての機能にアクセスできるようになります。

您的 `extends` 行应始终与脚本附加到的节点类型匹配。

{{% notice style="info" title="Accessing scripts" %}}
A script on its own doesn't do much of anything. Scripts *define* additional functionality for whatever object they're attached to. You will never be accessing a variable in some script, you'll be accessing a property of an *object*, which is *defined* by that script. This is a very important distinction.
{{% /notice %}}

## 移動

まず、船を画面上で移動させる機能から作成しましょう。以下の動作を行うコードから始めてみましょう：

* プレイヤーが押している入力を検知する
* その入力方向に宇宙船を移動させる

```gdscript
@export var speed = 150

func _process(delta):
    var input = Input.get_vector("left", "right", "up", "down")
    position += input * speed * delta
```

これを行ごとに分解してみましょう：

* 変数名の前に `@export` を付けると、**インスペクター** でその値を調整できるようになります。

![alt](/godot_recipes/4.x/img/2d_101_14.png)

```
※ `_process()` 関数はエンジンによって1フレームごとに呼び出されます。この関数内に書いたコードはすべて毎フレーム実行されます。
※ `Input.get_vector()` は、指定された4つの入力状態をチェックし、それらの方向に向くベクトルを生成します。
※ 最後に、与えられた入力ベクトルを移動量として船の `position` に加算します。この時、速度値に合わせてベクトルの大きさを調整し、さらに `delta` でスケール処理を行います。

{{% expand "Links to more information" %}}
* Understanding vectors: [Vector Math](https://docs.godotengine.org/en/latest/tutorials/math/vector_math.html)
* What is `delta`? [Understanding delta](/godot_recipes/4.x/basics/understanding_delta/)
{{% /expand %}}

シーンを実行するには**［現在のシーンを実行］**ボタンをクリックしてください。その後、自由に移動してみてください。

![alt](/godot_recipes/4.x/img/2d_101_15.png)

### 画面表示を維持する機能

一つの問題点として、プレイヤーが動き続けると画面外へと移動してしまう点が挙げられます。この問題を解決するには、スクリプト上部でプレイヤーの `position` プロパティを画面矩形内に制限する必要があります。以下のように追加してください：

```gdscript
@onready var screensize = get_viewport_rect().size
```

The `@onready` here tells Godot not to set the value of the `screensize` variable until the `Player` node has entered the scene tree. Effectively, it means "wait until the game starts", because there's no window to get the size of until the game is running.

次のステップは、位置をその `screensize` 矩形の範囲内で固定することです。`position` が使用する `Vector2` には、`clamp()` メソッドがあります。`position` 設定直後に、この行を追加してください：

```gdscript
func _process(delta):
    var input = Input.get_vector("left", "right", "up", "down")
    position += input * speed * delta
    position = position.clamp(Vector2.ZERO, screensize)
```

もう一度シーンを実行して、画面の端から移動してみてください。船の半分が画面からはみ出していることに気付くはずです。これは、船の `position` 値が `Sprite2D` オブジェクトの中心位置に設定されているためです。私たちの船のサイズは `16x16` ピクセルであることがわかっているため、`clamp()` 関数に追加で8ピクセル分を包含するように変更できます：

```gdscript
position = position.clamp(Vector2(8, 8), screensize - Vector2(8, 8))
```

### 方向に合わせたアニメーションの適用方法

Now that the ship is moving, we can choose the "tilted" ship images when moving left or right, as well as the matching "Booster" animation.

移動方向を判断するには、`input`ベクトルの`x`値を確認します。値が正であれば右方向へ、負なら左方向へ、0であれば停止中と判定し、それぞれ対応する`frame`値を持つ`Sprite2D`と、適切な`animation`を選択します。

```gdscript
func _process(delta):
    var input = Input.get_vector("left", "right", "up", "down")
    if input.x > 0:
        $Ship.frame = 2
        $Ship/Boosters.animation = "right"
    elif input.x < 0:
        $Ship.frame = 0
        $Ship/Boosters.animation = "left"
    else:
        $Ship.frame = 1
        $Ship/Boosters.animation = "forward"
    position += input * speed * delta
    position = position.clamp(Vector2(8, 8), screensize-Vector2(8, 8))
```

もう一度シーンを再生し、左右へ移動した際に画像が正しく切り替わることを確認してください。次のステップに進む前に、すべてが意図通りに動作することを必ず検証してください。

次のステップでは、「弾丸」シーンを作成し、プレイヤーが射撃できるようにします。

| {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_02/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_04/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
