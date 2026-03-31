---
title: "画面への入力／出口"
weight: 1
draft: false
ghcommentid: 15
---

## Problem

オブジェクトが画面内に入ったり出たりするタイミングを検知したい場合。

## Solution

この目的のためのノードが用意されています。{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D`。このノードをオブジェクトにアタッチすれば、`screen_entered`シグナルと`screen_exited`シグナルを利用可能になります。
#### 例 1

発射後に直線軌道で移動する投射物を考えてみます。継続的に射撃を続けると、画面上から外れた物体であってもエンジンが追跡すべき対象が大量に発生し、結果的にラグの原因となる可能性があります。

以下に発射体の移動コードを示します。

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

#### 例2

敵キャラクターがいて、経路に沿って移動したりアニメーションを再生したりするなどの動作を行います。大規模なマップで多数の敵が存在する場合、同時に画面上に表示されるのはそのうちのわずか数人だけです。{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D` を使用することで、オフスクリーン状態の間だけ敵の動作を無効化できます。

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
