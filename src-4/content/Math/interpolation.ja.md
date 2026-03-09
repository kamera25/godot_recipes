---
title: "Interpolation"
weight: 1
draft: false
ghcommentid: 64
---

**線形補間**（リニア・インターポレーション）、あるいはその略称である**lerp**は、ゲーム開発の現場で頻繁に用いられる概念です。初めて耳にする方には難解で技術的に聞こえてしまうかもしれませんが、このチュートリアルを通じてご覧いただけるように、実際には理解しやすいシンプルな原理でありながら、ゲームプログラミングにおいて幅広く応用可能な強力なツールなのです。

## 数値補間処理

線形補間の基本式は以下のようになります：

```gdscript
func lerp(a, b, t):
    return (1 - t) * a + t * b
```

この数式において、`a` と `b` は2つの値を表し、`t` は補間量を示します。通常、`0`（結果は`a`）から`1`（結果は`b`）までの範囲で指定します。この関数は、指定された比率に基づいて2つの値の間に適切な中間値を求めます。具体例を挙げると：

```gdscript
x = lerp(0, 1, 0.75)  # x is 0.75
x = lerp(0, 100, 0.5)  # x is 50
x = lerp(10, 75, 0.3)  # x is 29.5
x = lerp(30, 2, 0.75)  # x is 9
```

この手法が「線形内挿」と呼ばれる理由は、2点間の経路が直線であるためです。

```javascript
const elapsedTime = Time.deltaTime;
const duration = 0.5; // 2秒のアニメーション期間

function lerpScaleAndFade(node, startSize, endSize) {
    let scaleFactor = Mathf.Lerp(startSize, endSize, elapsedTime / duration);
    node.scale = Vector3.one * scaleFactor;

    // 2秒間かけて徐々に透明化（不透明度0〜1）
    const fadeDuration = 0.2; // 1秒のフェード期間
    const currentFadeValue = Mathf.Lerp(0, 1, elapsedTime / fadeDuration);
    node.modulate.a = Mathf.LerpAmplitude(currentFadeValue, startSize, endSize);
}

// 2秒間かけてスプライトを5倍に拡大しながら徐々に透明化
lerpScaleAndFade("MySprite", 1.0, 5.0);
```

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

また、ベクトル間での補間も可能です。`Vector2` および `Vector3` はどちらも `linear_interpolate()` メソッドを提供しています。

例如，要找到一个向量位于空间节点的前方向和左方向之间的中点：

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
    if event is InputEventMouseButton and event.pressed:
        target = event.position

func _process(delta):
    if target:
        position = position.linear_interpolate(target, 0.1)
```
<!-- !LINK -->
インターポレーションのより高度な応用については、`Tween` を参照してください。