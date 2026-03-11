---
title: "Entering/Exiting the screen"
weight: 1
draft: false
ghcommentid: 15
---

## 課題

オブジェクトが画面内に入ったり出たりするタイミングを検知したい場合。

## 解決策

エンジンにはこの目的のためのノードが用意されています：{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D`。このノードをオブジェクトに添付すれば、`screen_entered`シグナルと`screen_exited`シグナルを利用可能になります。
*
#### 使用例 1

発射後に直線軌道で移動する投射物を考えてみましょう。継続的に射撃を続けると、画面上から外れた物体であってもエンジンが追跡すべき対象が大量に発生し、結果的にラグの原因となる可能性があります。

以下に発射体の移動コードを示します：

```gdscript
extends Area2D

var velocity = Vector2(500, 0)

func _process(delta):
    position += velocity * delta
```

プロジェクトイルが画面外に移動した際に自動的に削除されるようにするには、{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D`を追加し、その`screen_exited`シグナルを接続してください。

```gdscript
func _on_VisibleOnScreenNotifier2D_screen_exited():
    queue_free()
```

#### 使用例2

We have an enemy that performs some actions, such as moving along a path or playing an animation. On a large map with many enemies, only a few of them will be onscreen at the same time. We can disable the enemy's actions while it's offscreen using {{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D`.

コードの一部：

```gdscript
var active = false

func _process(delta):
    if active:
        play_animation()
        move()

func _on_VisibleOnScreenNotifier2D_screen_entered():
    active = true

func _on_VisibleOnScreenNotifier2D_screen_exited():
    active = false
```
