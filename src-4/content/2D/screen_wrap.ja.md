---
title: "Screen wrap"
weight: 1
draft: false
ghcommentid: 17
---

## 問題文

You want to allow the player to "wrap around" the screen, teleporting from one side of the screen to the other. This is a common feature, especially in old-school 2D games (think Pac-man).

## 解決策

1. スクリーンサイズ（ビューポート）を取得

    ```gdscript
    @onready var screen_size = get_viewport_rect().size
    ```

    `get_viewport_rect()` は `CanvasItem` 派生ノードであればどのノードからも利用可能です。

1. プレイヤーのポジションを比較する

    ```gdscript
    if position.x > screen_size.x:
        position.x = 0
    if position.x < 0:
        position.x = screen_size.x
    if position.y > screen_size.y:
        position.y = 0
    if position.y < 0:
        position.y = screen_size.y
    ```

    注意：これはノードの「position」属性を使用しています。これは通常、スプライトまたはボディの中心位置を指します。

1. `wrapf()` を使用した簡略化処理

    The above code can be simplified using GDScript's `wrapf()` function, which "loops" a value between the given limits.

    ```gdscript
    position.x = wrapf(position.x, 0, screen_size.x)
    position.y = wrapf(position.y, 0, screen_size.y)
    ```
