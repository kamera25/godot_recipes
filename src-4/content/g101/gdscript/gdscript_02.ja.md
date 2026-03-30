---
title: "スプライトを移動中"
weight: 1
draft: true
ghcommentid: 90
pre: "02. "
---

前の手順では、`Sprite2D`コンポーネントにスクリプトを追加し、そのスクリプトを使って位置を設定しました。

以下が現時点でのスクリプトです。

```gdscript
extends Sprite2D

func _ready():
    position = Vector2(100, 150)
```

## スプライトの移動

このスプライトを画面上で移動させたいと思います。Godotはデフォルトで*60 fps*（フレーム/秒）で動作しており、各フレームごとに少しずつ動かしたいです。このコードをスクリプトに追加して実行すると、どのような動きになるか確認できます。

```gdscript
func _process(delta):
    position.x += 100 * delta
```

見えた？ 右方向に移動するスプライトについて分析してみよう。

ノードが初めて起動したとき（「再生」ボタンを押した時）に`_ready()`関数が呼び出されるのと同様に、`_process()`は毎フレーム呼び出されます。つまり、この関数内に記述したコードは、1秒間に60分の1秒ごとに実行されることになります。ここで`delta`が示すのは、このフレームの長さを秒で表したものです。

ここでは、Godotに毎フレーム何をさせるべきか？スプライトの `x`座標を取得し、その値に `100 * 1/60` を加える必要があります。

その結果、スプライトが毎秒 100 ピクセルの速さで右方向に移動するようになりました。

{{% expand title="詳細情報" %}}
`delta`について、またゲーム開発においてこれを使用する理由について詳しく知りたい方は、[デルタの理解](/godot_recipes/4.x/ja/basics/understanding_delta/)をご覧ください。
{{% /expand %}}

## ベクトルの使用法

What if we want to move the sprite diagonally? That means we need to change the `x` and `y` coordinates at the same time. `position` is a **vector** - it contains both coordinates in one quantity. Vectors can be added, so let's change the code をこれに：

```gdscript
func _process(delta):
    position += Vector2(100, 50) * delta
```

コードを実行すると、スプライトが下方向に移動していくのが確認できるはずです。

これをより扱いやすくするために、**変数**を使ってみます。

```gdscript
extends Sprite2D

var velocity = Vector2(100, 50)

func _ready():
    position = Vector2(100, 150)

func _process(delta):
    position += velocity * delta
```

この数量を変数として定義しました。変数は、キーワード `var` を使用して宣言し、名前を付けた後、`=` 演算子で値を代入することで作成します。

変数は見つけやすい最上位で宣言する方が多くの場合便利です。スプライトの複数インスタンスを作成するようになると、この方が後々さらに便利に感じられるでしょう。

## 移動のランダム化について

これをシャッフルして、スプライトの移動方向をランダムに選んでみます。

```gdscript
func _ready():
    position = Vector2(100, 150)
    velocity = Vector2.RIGHT.rotated(randf_range(0, TAU))
    velocity = velocity * randf_range(100, 400)
```

かなり多いですね。それでは、項目ごとに分解してみます。

1. First, we're setting `velocity` to point to the right. `Vector2.RIGHT` is a built-in *constant* that represents the vector `(1, 0)`.

* 次に、`Vector2`の`rotated()`メソッドを使ってベクトルを回転させます。`rotated()`メソッドの括弧内には角度を指定する必要があります。

* ランダムな角度で回転させたいので、`randf_range()`を使って`0`から`TAU`までの乱数を取得します。

    {{% expand title="About angles" %}}
角度を扱う際、GDScript（ほとんどのプログラミング言語と同様）では度数法ではなくラジアンを使用します。ラジアンでは、1回転が正確に `2 * PI` に相当します（または `TAU` - これは約 `360` 度と同等です）。
    {{% /expand %}}

1. 最後に、`velocity`にもう1つの乱数を乗算し、ランダムな速さを与えます。

シーンを何度か実行してみると、スプライトが様々な方向に移動するのが確認できるはずです。





```gdscript
func _process(delta):
    position += velocity * delta
    position.x = wrapf(position.x, -64, screensize.x+64)
    position.y = wrapf(position.y, -64, screensize.y+64)
```