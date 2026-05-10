---
title: "敵の射撃"
weight: 8
draft: false
pre: "08. "
---

敵が攻撃できるようになったので、今度は彼らが撃つ対象を与えます。

## 敵弾シーン

以前プレイヤー用の弾丸を作成したときと同じように、新しい`EnemyBullet`シーンを作成してください。ここでは詳細な手順は割愛しますが、行き詰まった場合はその部分を参照してください。唯一の違いは、代わりに`Enemy_projectile (16 x 16).png`画像を使用できる点です。

スクリプトは少し異なります。

```gdscript
extends Area2D

@export var speed = 150

func start(pos):
    position = pos

func _process(delta):
    position.y += speed * delta
```

{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D`と{{< gd-icon Area2D >}}`Area2D`の `screen_exited` シグナルと `area_entered` シグナルをそれぞれ接続してください。

```gdscript
func _on_visible_on_screen_notifier_2d_screen_exited():
    queue_free()

func _on_area_entered(area):
    if area.name == "Player":
        queue_free()
```

※プレイヤーへのヒットは検出していますが、現時点では何も処理していません。ダメージを与える仕組みを追加した時点で、この問題に対処します。

## 敵への射撃を追加

敵のスクリプト上部で新しい弾丸をロードします。

```gdscript
var bullet_scene = preload("res://enemy_bullet.tscn")
```

次に射撃関数を書き換えます。

```gdscript
func _on_shoot_timer_timeout():
    var b = bullet_scene.instantiate()
    get_tree().root.add_child(b)
    b.start(position)
    $ShootTimer.wait_time = randf_range(4, 20)
    $ShootTimer.start()
```

`Main` シーンを再生し直すと、ランダムな敵の弾丸が出現するはずです。

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_07/" icon="fas fa-arrow-left" %}}戻る{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_09/" icon="fas fa-arrow-right" icon-position="right" %}}次へ{{% /button %}} |
|------|------:|
