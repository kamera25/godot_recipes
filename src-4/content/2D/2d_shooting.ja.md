---
title: "Shooting projectiles"
weight: 2
draft: false
ghcommentid: 26
---

## 問題文

プレイヤー／モブなどから投射物を発射させたいのですね。

## 解決策

### 弾丸の設定

First, we'll set up a "bullet" object that we can instance. Here are the nodes we'll use:

```
{{< gd-icon Area2D >}} Area2D: Bullet
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
```

```html

![alt](/godot_recipes/4.x/img/laserRed01.png)

ノードの設定とスプライトおよび衝突判定形状を構成します。テクスチャが上向きに配置されている場合（上記例のように）は、{{< gd-icon Sprite2D >}}`Sprite` ノードを `90°` 回転させて右方向に向け、親オブジェクトの「前方」方向に一致するように調整してください。

スクリプトを追加し、{{< gd-icon Area2D >}}`Area2D`の`body_entered`シグナルに接続してください。

```gdscript
extends Area2D

var speed = 750

func _physics_process(delta):
    position += transform.x * speed * delta

func _on_Bullet_body_entered(body):
    if body.is_in_group("mobs"):
        body.queue_free()
    queue_free()
```

For this example, we'll remove the bullet if it hits anything at all. We'll also delete anything tagged in the "mobs" group that it hits.

### 撮影について

We need to set up a spawn location for the bullets. Add a {{< gd-icon Marker2D >}}`Marker2D` and place it where you want the bullets to spawn. Here's an example, placed at the barrel of the gun. I've named it "Muzzle".

![alt](/godot_recipes/4.x/img/2d_shoot_01.gif)

```python
notice = True
while notice:
    if player.rotated:
        print(\)
        break
    else:
        print(\)

# 弾丸をスポーンする際、この機能が非常に役立ちます。変換座標を使用することで、適切な位置と向きを簡単に取得できます
new_bullet.transform = muzzle_transform
```

{{% notice tip %}}
This will work for any character type, not just the "rotate-and-move" style shown here. Just attach the {{< gd-icon Marker2D >}}`Marker2D` where you want the bullets to spawn.
{{% /notice %}}

キャラクタースクリプト内で、インスタンス化用の弾丸シーンを保持する変数を追加します：

```gdscript
@export var Bullet : PackedScene
```

入力アクションが定義されているか確認してください：

```gdscript
    if Input.is_action_just_pressed("shoot"):
        shoot()
```

```python
def shoot():
    bullet = Bullet()
    scene.root_node.add_child(bullet)
```

## よくある間違い：プレイヤーを親ノードにしてしまうこと
```python
# これはNG！
player = Player()
scene.root_node.add_child(player)  # プレイヤーがツリーのルートになってしまう

```gdscript
func shoot():
    var b = Bullet.instantiate()
    add_child(b)
    b.transform = $Muzzle.transform
```

問題は、弾丸がプレイヤーの子オブジェクトであるため、プレイヤーが移動または回転した際に影響を受ける点です。

<img src=\ alt=\>

この問題を解決するには、弾丸をワールドに追加する必要があります。ここではプレイヤーのシーンルートノードを参照する `owner` 変数を使います。ただし、銃口の **グローバル** 変換行列も適用する必要がある点に注意してください。これを行わないと、弾丸が想定した位置に表示されない可能性があります。

```gdscript
func shoot():
    var b = Bullet.instantiate()
    owner.add_child(b)
    b.transform = $Muzzle.global_transform
```

![alt](/godot_recipes/4.x/img/2d_shoot_03.gif)

## 関連レシピ

<!-- - [Top-down character](/godot_recipes/3.x/2d/topdown_movement/) -->
- [ゲーム開発数学：トランスフォーム操作](/godot_recipes/4.x/math/transforms/)
<!-- - [AI: Homing missiles](/godot_recipes/3.x/ai/homing_missile/) -->

<!-- #### この動画が気に入ったら？

{{< youtube 7axJJYont6Y >}} -->

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらからダウンロードできます：[https://github.com/godotrecipes/2d_shooting](https://github.com/godotrecipes/2d_shooting)
