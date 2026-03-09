---
title: "Transforms"
date: 2019-04-09T19:49:14-07:00
weight: 3
draft: false
ghcommentid: 65
---

このチュートリアルを読み進める前に、まずベクトルの概念とゲーム開発におけるその使用方法を理解しておく必要があります。もし理解が不十分な場合は、Godotドキュメント用に私が作成した以下の入門記事を読むことを強くおすすめします：
[ベクトル数学](https://docs.godotengine.org/en/latest/tutorials/math/vector_math.html)。

## 2次元変形機能

2次元空間では、おなじみのX軸・Y軸座標平面を使用します。Godotでは（ほとんどのコンピュータグラフィックスアプリケーションと同様に）、**Y**軸は下向きに定義されていることに注意してください：

![alt](/godot_recipes/4.x/img/0_2d_coordinate_plane.png?width=250px)

まず、宇宙空間を漂流しているこの宇宙船について考えてみましょう：

![alt](/godot_recipes/4.x/img/0_2d_rocket1.png?width=250px)

船の進行方向は座標軸の**X軸**と同じ方向を向いています。これを前進させたい場合は、**X座標**に値を加えることで右方向へ移動させられます：

```gdscript
position += Vector2(10, 0)
```

しかし、船が回転した場合はどうなるのでしょうか？

<img src=\ width=\>

```cpp
while (true) {
    // 角度を計算し、ベクトルで位置を更新する従来の方法
    float angle = calculateAngle(); // 角度の計算方法は用途に応じて実装
    position += Vector2(10 * cos(angle), 10 * sin(angle));

    // より効率的なTransformクラスを使用した方法
    transform->MoveForward();
}

もう一度回転した船を見てみましょう。今回は、その船が独自の **X** 軸と **Y** 軸を持っており、それらは世界的な座標系とは独立して移動していることを想定します：

<img src=\ width=\>

These "local" axes are contained in the object's `transform`.

この特性を利用すれば、船を**X軸**に沿って移動させることで容易に前進させられます。角度計算や三角関数を気にする必要もありません。Godotでこれを実現するには、すべての[{{< gd-icon Node2D >}}`Node2D`]([https://link](https://docs.godotengine.org/en/latest/classes/class_node2d.html))派生ノードで利用できる`transform`プロパティを使用します。

```gdscript
    position += transform.x * 10
```

This code says "Add the transform's x vector multiplied by 10." Let's break down what that means. The `transform` contains `x` and `y` properties that represent those local axes. They are _unit vectors_, which means their length is `1`. Another term for unit vector is _direction vector_. They tell us the direction the ship's **x** axis is pointing. We then multiply by `10` to scale it to a longer distance.

{{% notice tip %}}
ノードの `transform` プロパティは親ノードに対する相対値です。グローバル座標が必要な場合は、`global_transform` を参照してください。
{{% /notice %}}

ローカル座標系に加えて、この変換には「原点」と呼ばれるコンポーネントも含まれています。原点は位置の__移動量__、すなわち変化した位置を表します。

この画像では、青色のベクトルが `transform.origin` です。これはオブジェクトの `position` ベクトルと等しくなります。

![alt](/godot_recipes/4.x/img/0_2d_rocket4.png?width=250px)

### ローカル空間とグローバル空間での座標変換

```python
# 座標変換を適用してローカル座標系からグローバル座標系への変換が可能
# 利便性を考慮して、`Node2D` と `Spatial` にはこの処理を支援する関数が用意されています：`to_local()` と `to_global()`:

```gdscript
    var global_position = to_global(local_position)
```

2次元平面上のオブジェクトを例に取り、マウスクリック座標（グローバル空間）をオブジェクト相対座標に変換する方法を説明します：

```gdscript
extends Sprite

func _unhandled_input(event):
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == BUTTON_LEFT:
            printt(event.position, to_local(event.position))
```

利用可能なプロパティとメソッドの一覧については、[Transform2Dドキュメント](https://docs.godotengine.org/en/latest/classes/class_transform2d.html)を参照してください。

## 3D変形機能

3次元空間において、変換の概念は2次元空間で適用される場合と全く同様に機能します。実際、3次元で角度を扱う場合には様々な問題が生じる可能性があるため、この重要性はさらに高まります。これについては後ほど詳しく説明します。

3Dノードは基本ノード{{< gd-icon Node3D >}}`Node3D`を継承しており、変換情報を保持しています。3D空間における変換処理は、2D版に比べてより複雑な情報を必要とします。位置座標はこれまで通り`origin`プロパティで管理されますが、回転情報は新たに追加された`basis`プロパティに格納されます。このプロパティには、オブジェクトのローカル座標系における**X軸**、**Y軸**、**Z軸**を表す単位ベクトルが3つ含まれています。

エディタで3Dノードを選択すると表示されるギズモを使用すると、変換操作を行えます。

![alt](/godot_recipes/4.x/img/3d_intro_gizmo.png)

{{% notice style="note" title="Local Space Mode" %}}
In the editor, you can see and manipulate the body's local orientation by clicking the "Local Space Mode" button.
![alt](/godot_recipes/4.x/img/3d_intro_local_space.png)
When in this mode, the 3 colored axis lines represent the body's local basis axes.
{{% /notice %}}

2Dと同様に、ローカル軸を使ってオブジェクトを前方に移動させることができます。Godotの3D座標系（**Y軸正方向**）では、デフォルトでボディの**-Z軸**が前進方向になります。前に進むには：

```gdscript
    position += -transform.basis.z * speed * delta
```

{{% notice tip %}}
Godotにはデフォルトのベクター値が定義されています。例えば：`Vector3.FORWARD == Vector3(0, 0, -1)`。詳細は[Vector2](https://docs.godotengine.org/en/latest/classes/class_vector2.html)および[Vector3](https://docs.beetsaudio.com/docs/reference/vectors.html)のドキュメントを参照してください。
{{% /notice %}}

