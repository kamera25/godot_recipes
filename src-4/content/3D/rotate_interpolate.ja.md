---
title: "Smooth rotation"
weight: 12
draft: false
ghcommentid: 39
---

## 問題文

3Dオブジェクトをスムーズに回転させ、新しい方向に向けさせたい場合。

## 解決策

When you first encounter this problem, you may find yourself thinking in terms of *Euler angles* - the three values representing the angles to the **x/y/z** axes. While Godot will allow you to see the object's Euler angles in the `rotation` property, it is not recommended to use them to work in 3D. There are a number of reasons why this the case, such as a problem called "gimbal lock", where you lose one degree of freedom when one of your rotations reaches 90 degrees.

{{% notice info %}}
オイラー角の背景や、ジンバルロックといった関連する問題についてさらに詳しく知りたい方には、[こちらの解説動画](https://www.youtube.com/watch?v=zc8b2Jo7mno)がおすすめです
{{% /notice %}}

Godotではオブジェクトの`transform`プロパティを利用することで、3Dオイラー角を使用する必要を回避できます。このプロパティはオブジェクトの空間内における位置と向きを同時に表現します。これは数学的なマトリックス構造によって実現されていますが、実際に使用する際にはその背後にある数学的原理を理解する必要はありません。

### look_at()

以下の例では、ミサイルや矢のような3Dオブジェクトを目標方向に向ける方法を示します。これは`Node3D`クラスの`look_at()`メソッドを使用することで実現できます：

```gdscript
func _process(delta):
    var target_position = $Target.transform.origin
    $Arrow.look_at(target_position, Vector3.UP)
```

このコードでは、ノード（`$Arrow`）がターゲットの位置を常に向くようになります。ターゲットがどのように移動しても関係ありません。

* 回転軸の選択
  * Z軸に設定
  * 垂直方向の動きのみ許可
  * 水平方向には移動させない

![alt](/godot_recipes/4.x/img/3d_rotate_01.gif)

Note that `look_at()` requires 2 parameters: the target position, and an "up vector". Imagine an airplane pointing its nose towards a target - there are an infinite number of ways it could be oriented, because the plane could roll about its axis. This second parameter is how you define what you want the final orientation to be.

### スムーズな回転制御

The above code works, but it snaps the rotation instantly to the target. This might be fine if you have a very slow-moving target, but looks unnatural. It would look better if we move smoothly, or "interpolated", the rotation smoothly between the starting orientation and the ending.

Godotはこの問題も適切に解決しています。`look_at()`の代わりに、`Transform`オブジェクトの`looking_at()`メソッドを使用できます。このメソッドはノード自体を回転させることなく、ターゲットを見るための変換行列を返すだけです。さらに、`interpolate_with()`メソッドと組み合わせることで、現在の向きから目標の向きへと滑らかに遷移させることができます。

```gdscript
var speed = 5

func _process(delta):
    var target_position = $Target.transform.origin
    var new_transform = $Arrow.transform.looking_at(target_position, Vector3.UP)
    $Arrow.transform  = $Arrow.transform.interpolate_with(new_transform, speed * delta)
```

!

```markdown
注：`interpolate_with()` は `transform` を操作するため、回転と位置の両方に対して補間を行うことができます。

## まとめ

これで完了です！この便利な方法を使って3Dオブジェクトを回転させ、角度の計算に煩わされることなく作業を進めましょう！


## 関連レシピ


