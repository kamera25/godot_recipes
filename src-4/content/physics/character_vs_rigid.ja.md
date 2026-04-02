---
title: "CharacterとRigidBodyの相互作用"
weight: 5
draft: false
---

## 課題

キャラクターのボディをリジッドボディと相互作用させたい場合に使用します。

## 解決策

{{% notice note %}}
このレシピは2Dノードと3Dノードの両方に同様に適用できます。{{% /notice %}}

デフォルトでは、 `move_and_slide()` または `move_and_collide()` で移動させた `CharacterBody2D` は、衝突する任意の `RigidBody2D` を押しません。リジッドボディは全く反応せず、単なる `StaticBody2D` と同じように振る舞います。

![alt](/godot_recipes/4.x/img/char_push_default.gif)

場合によってはこれで十分なこともあります。ただし、ボディーを押し出したい場合は、変更がいくつか必要です。

この例では、[プラットフォーマー用キャラクター](/godot_recipes/4.x/ja/2d/platform_character/) レシピで解説されている2Dキャラクターを使用します。この例ではキャラクター移動の最も一般的な方法である `move_and_slide()` を採用しています。もし代わりに `move_and_collide()` を使用している場合は、以下の実装を適切に変更してください。

リジッドボディとのインタラクション方法を決定する際には、以下の2つの選択肢があります。

1. 物理を無視して直接押すこともできます。Godot 3.x に慣れている方なら、これは"infinite inertia(無限慣性)"オプションと同等の機能です。
1. キャラクターの想定する「質量」と「速度」に基づいて押力を発揮させることもできます。これにより「リアルな」結果が得られます - 重い物体は少し、軽い物体は大きく押し出されるようになります。

以下の両方のオプションを試してみます。

### 無限の慣性力

この設定には長所と短所があります。最大の利点は、追加コードが不要であることです。必要なのはオブジェクトの衝突レイヤー/マスクを正しく設定することだけです。本事例では、以下の3つの物理レイヤを定義しています。

![alt](/godot_recipes/4.x/img/2d_physics_layers_01.png)

硬体オブジェクトについては、「アイテム」レイヤー（レイヤー3）に配置し、マスクはデフォルト設定のまま全レイヤーを覆う状態にしています。

![alt](/godot_recipes/4.x/img/physics_layers_box.png)

次に、プレイヤーを「プレイヤー」レイヤー（レイヤー2）に配置し、マスクを設定して「アイテム」を無視するように構成しました。

![alt](/godot_recipes/4.x/img/physics_layers_player.png)

ゲームを実行してみると、ボックスを自由に移動できることがわかります。なお、箱の質量は関係ありません。すべて同じように押されます。

![alt](/godot_recipes/4.x/img/char_push_inf.gif)

このオプションの欠点もここに現れています。箱の物理演算が無視されているため、壁を貫通したり、上に乗ることすらできません。

一部のゲームではこれで問題ありませんが、オブジェクトのめり込み（クリッピング）を防ぎたい場合は次の方法を試してみてください。

### インパルスの適用方法

衝突する物体に「押し」を与えるには、インパルスを適用が必要です。インパルスとは「瞬間的な衝撃的の力」のことで、野球でバットがボールを打つようなイメージです。これは、物体に対して連続的に力を加えるのとは異なります。

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

衝突時の法線ベクトルはリジッドボディの外側を指しているため、これを反転させてキャラクターから離れる方向に調整し、`push_force` 係数を適用します。これで再び押す動作が可能になります。なお、壁越しにリジッドボディを移動させることはできません。

![alt](/godot_recipes/4.x/img/char_push_impulse.gif)

リジッドボディの質量と関連させて `push_force` を調整が必要です。力が大きすぎると衝突が発生してしまいますし、小さすぎると全く押し込めなくなります。

実験を通じて、特定のゲームに最適な設定を見つけます。

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/character_vs_rigid](https://github.org/godotrecipes/character_vs_rigid)

## 関連レシピ

- [プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)

## <i class="fas fa-video"></i> 動画を観る
{{< youtube SJuScDavstM >}}
