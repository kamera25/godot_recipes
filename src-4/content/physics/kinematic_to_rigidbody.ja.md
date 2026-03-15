---
title: "運動学から剛体相互作用へ"
weight: 5
draft: false
---

## 課題

您希望动态角色与刚体进行交互。

## 解決策

このレシピは2Dノードと3Dノードの両方に同様に適用できます。

デフォルトでは、`move_and_slide()` または `move_and_collide()` で移動させた運動体は、衝突した剛体すべてに影響を及ぼします。この相互作用は、運動体移動関数の `infinite_inertia`（無限慣性）パラメータのため、剛体の物理特性を考慮しません。

![alt](/godot_recipes/3.x/img/inf_inertia1.gif)

※場合によってはこれだけで十分なこともあります。ただし、キャラクターが重なって見えたり、トンネル現象が発生したりするなど、現実離れした挙動を防ぎたい場合は、相互作用に関するコードを追加する必要があります。

本例では、[プラットフォームキャラクターレシピ](http://kidscancode.org/godot_recipes/ai/platform_character) で説明されている2Dキャラクターを使用します。

最も一般的に使用されている動的ボディの移動方法は `move_and_slide()` です。サンプルコードでは、この処理は以下の行で行われています。

```gdscript
velocity = move_and_slide(velocity, Vector2.UP)
```

# 追加パラメータの説明：
# - friction: 摩擦係数（デフォルトは0.9）
# - bounciness: 跳ね返り強度（デフォルトは1.0）
# - jump_height: ジャンプ時の高さ制限（デフォルトは0.25）

```text
move_and_slide ( Vector2 linear_velocity,
    Vector2 floor_normal=Vector2( 0, 0 ),
    bool stop_on_slope=false, int max_slides=4,
    float floor_max_angle=0.785398,
    bool infinite_inertia=true )
```

最後の引数を変更する必要があります。GDScriptには名前付きパラメータがないため、すべての引数を渡す必要がありますが、デフォルト値をそのまま保持できます：

```gdscript
    velocity = move_and_slide(velocity, Vector2.UP,
                    false, 4, PI/4, false)
```

现在，如果尝试移动，你会看到机械体在碰撞时完全停止。它根本不能推动刚体。

![alt](/godot_recipes/3.x/img/inf_inertia2.gif)

衝突する物体に「押し」を与えるには、インパルスを適用する必要があります。インパルスとは瞬間的な「衝撃」のことで、野球でバットがボールを打つようなイメージです。これは、物体に対して連続的に力を加えるフォースとは異なります。

```gdscript
# This represents the player's inertia.
export (int, 0, 200) var push = 100

func _physics_process(delta):

    # after calling move_and_slide()
    for index in get_slide_count():
        var collision = get_slide_collision(index)
        if collision.collider.is_in_group("bodies"):
            collision.collider.apply_central_impulse(-collision.normal * push)
```

衝突法線ベクトルは剛体の外側を向いているため、これを反転させてキャラクターから離れる方向に向け直し、`push`係数を適用します。これで再び押し出し機能が有効になりますが、壁を通過させるほどの強い力にはなりません：

![alt](/godot_recipes/3.x/img/inf_inertia3.gif)

また、衝撃力の大きさをキャラクターの速度に応じて調整することもできます。

```gdscript
collision.collider.apply_central_impulse(-collision.normal * velocity.length() * push_factor)
# Depending on your character's movement speed, adjust push_factor to
# something between 0 and 1.
```

実験を通じて、特定のゲームに最適な設定を見つけましょう。

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます [kinematic_vs_rigid.zip](/godot_recipes/3.x/files/kinematic_vs_rigid.zip)
{{% /notice %}} -->

## 関連レシピ

- [プラットフォームキャラクタ実装](http://kidscancode.org/godot_recipes/ai/platform_character)

#### この動画が気に入ったら？

{{< youtube C-Sn55e5wnk >}}
