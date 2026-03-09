---
title: "Character to Rigid Body Interaction"
weight: 5
draft: false
---

## 問題文

キャラクターのボディを剛体と相互作用させたい場合に使用します。

## 解決策

このレシピは2Dノードと3Dノードの両方に同様に適用できます。

デフォルトでは、 `move_and_slide()` または `move_and_collide()` で移動させた `CharacterBody2D` は、衝突する任意の `RigidBody2D` を押しません。リジッドボディは全く反応せず、単なる `StaticBody2D` と同じように振る舞います。

<img src=\ alt=\>

場合によってはこれで十分なこともあります。ただし、ボディーを押し出したい場合は、いくつかの変更が必要です。

```
この例では、[プラットフォーマー用キャラクター](/godot_recipes/4.x/2d/platform_character/) レシピで解説されている2Dキャラクターを使用します。この例ではキャラクター移動の最も一般的な方法である `move_and_slide()` を採用しています。もし代わりに `move_and_collide()` を使用している場合は、以下の実装を適切に変更してください。

リジッドボディとのインタラクション方法を決定する際には、以下の2つの選択肢があります：

1. You can just push them, ignoring physics. If you're familiar with Godot 3.x, this is equivalent to the "infinite inertia" option.
1. You can give them a push based on the character's imagined "mass" and velocity. This will give you a "realistic" result - pushing heavy bodies a little, and lighter bodies a lot.

以下の両方のオプションを試してみましょう。

### 無限の慣性力

この設定には長所と短所があります。最大の利点は、追加コードが不要であることです。必要なのはオブジェクトの衝突レイヤー/マスクを正しく設定することだけです。本事例では、以下の3つの物理レイヤを定義しています：

![alt](/godot_recipes/4.x/img/2d_physics_layers_01.png)

For the rigid body, we've placed it on the "items" layer (layer 3), and left the mask at the default (masking all layers):

![alt](/godot_recipes/4.x/img/physics_layers_box.png)

Then, we've placed the player on the "player" layer (layer 2), and configured the mask to ignore the "items":

![alt](/godot_recipes/4.x/img/physics_layers_player.png)

ゲームを実行してみると、ボックスを自由に移動できることがわかります。なお、箱の質量は関係ありません。すべて同じように押されます。

![alt](/godot_recipes/4.x/img/char_push_inf.gif)

このオプションの欠点もここに現れています。箱の物理演算が無視されているため、壁を貫通したり、上に乗ることすらできません。

一部のゲームではこれで問題ありませんが、クリッピングを防ぎたい場合はオプション2を選択してください。

### 衝撃波の適用方法

To give the colliding body a "push" we'll need to apply an impulse. An impulse is an instantaneous "kick" - think of a bat hitting a ball. This is as opposed to a force, which is a continuous "push" on an object.

```gdscript
# This represents the player's inertia.
var push_force = 80.0

func _physics_process(delta):
    # after calling move_and_slide()
    for i in get_slide_collision_count():
        var c = get_slide_collision(i)
        if c.get_collider() is RigidBody2D:
            c.get_collider().apply_central_impulse(-c.get_normal() * push_force)
```

衝突正規ベクトルは剛体の外側を指しているため、これを反転させてキャラクターから離れる方向に調整し、`push_force` 係数を適用します。これで再び押す動作が可能になりますが、壁越しに剛体を移動させることはできません。：

![alt](/godot_recipes/4.x/img/char_push_impulse.gif)

剛性体の質量と関連させて `push_force` を調整する必要があります。力が大きすぎると衝突が発生してしまいますし、小さすぎると全く押し込めなくなります。

実験を通じて、特定のゲームに最適な設定を見つけましょう。

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/character_vs_rigid](https://github.org/godotrecipes/character_vs_rigid)

## 関連レシピ

* [プラットフォームキャラクタ](/godot_recipes/4.x/2d/platform_character/)

## <i class="fas fa-video"></i> Watch Video
{{< youtube SJuScDavstM >}}
