---
title: "トランスフォーム"
date: 2019-04-09T19:49:14-07:00
weight: 3
draft: false
ghcommentid: 65
---

このチュートリアルを読み進める前に、まずベクトルの概念とゲーム開発における使用方法を理解する必要があります。もし不十分と感じている場合、Godotドキュメントの、以下の入門記事を読むことを強くオススメします。
[ベクトル演算](https://docs.godotengine.org/ja/latest/tutorials/math/vector_math.html)

## 2Dトランスフォーム

2D空間では、おなじみのX軸・Y軸座標平面を使用します。Godotでは（ほとんどのコンピュータグラフィックスアプリケーションと同様に）、**Y**軸は下向きに定義されていることに注意してください。

![alt](/godot_recipes/4.x/img/0_2d_coordinate_plane.png?width=250px)

まず、宇宙空間を漂流しているこの宇宙船について考えてみましょう。

![alt](/godot_recipes/4.x/img/0_2d_rocket1.png?width=250px)

船の進行方向は座標軸の**X軸**と同じ方向を向いています。これを前進させたい場合は、**X座標**に値を加えることで右方向へ移動させられます。

```gdscript
position += Vector2(10, 0)
```

しかし、船が回転した場合はどうなるのでしょうか？

![alt](/godot_recipes/4.x/img/0_2d_rocket2.png?width=250px)

How do we move the ship forward now? If you remember Trigonometry from school, you might be starting to think about angles, sine and cosine and doing something like `position += Vector2(10 * cos(angle), 10 * sin(angle))`. While this would work, there's a much more convenient way: the _Transform_.

もう一度回転した船を見てみましょう。今回は、その船が独自の **X** 軸と **Y** 軸を持っており、それらは世界的な座標系とは独立して移動していることを想定します。

![alt](/godot_recipes/4.x/img/0_2d_rocket3.png?width=250px)

これらの「ローカル」座標軸は、オブジェクトの `transform` プロパティに含まれています。

この特性を利用すれば、船を**X軸**に沿って移動させることで簡単に前進できます。角度計算や三角関数を気にする必要もありません。Godotでこれを実現するには、すべての[{{< gd-icon Node2D >}}`Node2D`]([https://link](https://docs.godotengine.org/ja/latest/classes/class_node2d.html))派生ノードで利用できる`transform`プロパティを使用します。

```gdscript
    position += transform.x * 10
```

This code says "Add the transform's x vector multiplied by 10." Let's break down what that means. The `transform` contains `x` and `y` properties that represent those local axes. They are _unit vectors_, which means their length is `1`. Another term for unit vector is _direction vector_. They tell us the direction the ship's **x** axis is pointing. We then multiply by `10` to scale it to a longer distance.

{{% notice tip %}}
The `transform` property of a node is _relative_ to its parent node. If you need to get the global value, it's available in `global_transform`.
{{% /notice %}}

In addition to the local axes, the transform also contains a component called the `origin`. The origin represents the _translation_, or change in position.

この画像では、青色のベクトルが `transform.origin` です。これはオブジェクトの `position` ベクトルと等しくなります。

![alt](/godot_recipes/4.x/img/0_2d_rocket4.png?width=250px)

### ローカル空間とグローバル空間での座標変換

座標変換を適用してローカル座標系からグローバル座標系への変換ができます。利便性を考慮して、`Node2D` と `Spatial` にはこの処理を支援する関数が用意されています。それが `to_local()` と `to_global()` です。

```gdscript
    var global_position = to_global(local_position)
```

2次元平面上のオブジェクトを例に取り、マウスクリック座標（グローバル空間）をオブジェクト相対座標に変換する方法を説明します。

```gdscript
extends Sprite

func _unhandled_input(event):
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == BUTTON_LEFT:
            printt(event.position, to_local(event.position))
```

利用可能なプロパティとメソッドの一覧については、[Transform2Dドキュメント](https://docs.godotengine.org/ja/latest/classes/class_transform2d.html)を参照してください。

## 3D トランスフォーム

3D空間において、変換の概念は2D空間で適用される場合と全く同様に機能します。実際、3次元で角度を扱う場合には様々な問題が生じる可能性があるため、この重要性はさらに高まります。これについては後ほど詳しく説明します。

3Dノードは基本ノード{{< gd-icon Node3D >}}`Node3D`を継承しており、変換情報を保持しています。3D空間におけるトランスフォームは、2D版に比べてより複雑な情報を必要とします。位置座標はこれまで通り`origin`プロパティで管理されますが、回転情報は新たに追加された`basis`プロパティに格納されます。このプロパティには、オブジェクトのローカル座標系における**X軸**、**Y軸**、**Z軸**を表す単位ベクトルが3つ含まれています。

エディタで3Dノードを選択すると表示されるギズモを使用すると、変換操作を行えます。

![alt](/godot_recipes/4.x/img/3d_intro_gizmo.png)

{{% notice style="note" title="ローカル空間モード" %}}
エディタ内で「ローカル空間モード」ボタンをクリックすると、オブジェクトの局所的な向きを表示・操作できます。
![alt](/godot_recipes/4.x/img/3d_intro_local_space.png)
このモードでは、「Local Space Mode」が有効になっている間、3本の色分けされた軸線がオブジェクトの局所座標系の基底軸として表示されます。
{{% /notice %}}

2Dと同様に、ローカル軸を使ってオブジェクトを前方に移動させることができます。Godotの3D座標系（ **Y軸正方向** ）では、デフォルトでボディの **-Z軸** が前進方向になります。前に進むには。

```gdscript
    position += -transform.basis.z * speed * delta
```

{{% notice tip %}}
Godotにはデフォルトのベクター値が定義されています。例えば：`Vector3.FORWARD == Vector3(0, 0, -1)`。詳細は[Vector2](https://docs.godotengine.org/ja/latest/classes/class_vector2.html)および[Vector3](https://docs.beetsaudio.com/docs/reference/vectors.html)のドキュメントを参照してください。
{{% /notice %}}

