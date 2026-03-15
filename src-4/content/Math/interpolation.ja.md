---
title: "補間"
weight: 1
draft: false
ghcommentid: 64
---

**線形補間**（リニア・インターポレーション）、あるいはその略称である**lerp**は、ゲーム開発の現場で頻繁に用いられる概念です。初めて耳にする方には難解で技術的に聞こえてしまうかもしれませんが、このチュートリアルを通じてご覧いただけるように、実際には理解しやすいシンプルな原理でありながら、ゲームプログラミングにおいて幅広く応用可能な強力なツールなのです。

## 数値補間処理

線形補間の基本式は以下のようになります。

```gdscript
func lerp(a, b, t):
    return (1 - t) * a + t * b
```

この数式において、`a` と `b` は2つの値を表し、`t` は補間量を示します。通常、`0`（結果は`a`）から`1`（結果は`b`）までの範囲で指定します。この関数は、指定された比率に基づいて2つの値の間に適切な中間値を求めます。具体例を挙げると以下となります。

```gdscript
x = lerp(0, 1, 0.75)  # x is 0.75
x = lerp(0, 100, 0.5)  # x is 50
x = lerp(10, 75, 0.3)  # x is 29.5
x = lerp(30, 2, 0.75)  # x is 9
```

この手法が「線形補間」と呼ばれる理由は、2点間の経路が直線であるためです。

ノードのプロパティを`lerp()`でアニメーション化することができます。例えば、経過時間を希望する持続時間で割ると、0から1の間の値が得られ、これを使ってプロパティを滑らかに変化させることができます。このスクリプトでは、スプライトを開始サイズの5倍まで拡大しつつ、2秒間かけて徐々にフェードアウトさせます（`modulate.a`を使用して)。

```gdscript
extends Sprite2D

var time = 0
var duration = 2  # length of the effect

func _process(delta):
    if time < duration:
        time += delta
        modulate.a = lerp(1, 0, time / duration)
        scale = Vector2.ONE * lerp(1, 5, time / duration)
```

## ベクトル補間処理

また、ベクトル間での補間もできます。`Vector2` および `Vector3` はどちらも `linear_interpolate()` メソッドを提供しています。

例えば、`Spatial`ノードの「前方方向ベクトル」と「左方向ベクトル」の中間に位置するベクトルを取得するには、以下のようにします。

```gdscript
var forward = -transform.basis.z
var left = transform.basis.x
var forward_left = forward.linear_interpolate(left, 0.5)
```

以下の例では、スプライトノードをマウスクリック位置に移動させています。各フレームごとにノードは目標位置まで10%ずつ近づきます。これにより、オブジェクトが近づくにつれて速度が徐々に減速する「接近」効果が得られます。

```gdscript
extends Sprite2D

var target

func _input(event):
    if event is 入力EventMouseButton and event.pressed:
        target = event.position

func _process(delta):
    if target:
        position = position.linear_interpolate(target, 0.1)
```
<!-- !LINK -->
補間のより高度な応用については、`Tween` を参照してください。