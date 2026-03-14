---
title: "弾道銃弾"
weight: 12
draft: false
ghcommentid: 30
---

## 課題

ご希望の2D弾は弧を描くように移動したり、弾道曲線を描いたりする仕様でしょうか？

## 解決策

この問題に対する解決策の一つとして、`RigidBody2D` コンポーネントを使用することが考えられます。組み込みの物理演算システムにより、発射後も重力によって自動的に地球へ引き戻されるよう設定できます。

ただし、[2Dシューティングゲームのレシピ](/godot_recipes/3.x/2d/2d_shooting/)で解説されているように、{{< gd-icon Area2D >}}`Area2D`は単純な弾丸やその他の投射物に非常に適しています。衝突判定やバウンド、その他の物理挙動を必要としない場合には特に便利です。弾道計算自体は難しくないため、物理エンジンの助けを借りるほどでもありません。

### 弾丸の設定

```markdown
- Bullet (Area2D)
    - Sprite
    - CollisionShape2D
```

以下の方法で利用できます：{{< gd-icon Area2D >}}`Area2D` の `gravity` プロパティを設定します。初期テストでは値を `150` に設定します。

```gdscript
extends Area2D

var velocity = Vector2(350, 0)


func _process(delta):
    velocity.y += gravity * delta
    position += velocity * delta
    rotation = velocity.angle()


func _on_BallisticBullet_body_entered(body):
    queue_free()
```

ここで必要なのは[運動方程式](https://www.khanacademy.org/science/physics/one-dimensional-motion/kinematic-formulas/a/what-are-the-kinematic-formulas)を適用するだけです。`velocity` の初期値は単なるテスト用です。ブレットシーンを実行してください。

![alt](/godot_recipes/3.x/img/2d_ballistic_01.gif)

現在の射撃オブジェクトでは、弾丸インスタンスを作成し、初期プロパティを設定できます。以下のいずれかの射撃処理関数／入力ハンドラに実装してください。

```gdscript
export var muzzle_velocity = 350
export var gravity = 250

func shoot():
    var b = Bullet.instance()
    owner.add_child(b)
    b.transform = $Barrel/Position2D.global_transform
    b.velocity = b.transform.x * muzzle_velocity
    b.gravity = gravity
```

以下に実際の使用例をご紹介します：

![alt](/godot_recipes/3.x/img/2d_ballistic_02.gif)

## 関連レシピ

- [2Dシューティングゲームの作成レシピ](/godot_recipes/3.x/2d/2d_shooting/)
  - [2D：軌跡を描画する方法](/godot_recipes/3.x/2d/2d_draw_trajectory/)
