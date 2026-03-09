---
title: "Screen wrap"
weight: 1
draft: false
ghcommentid: 17
---

## 問題文

プレイヤーキャラクターが画面を「巻き戻して」反対側に移動できるようにする機能ですね。これは特にクラシックな2Dゲーム（『パックマン』タイプの作品など）でよく使われる定番機能です。

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

    上記のコードは、GDScriptの`wrapf()`関数を使用することで簡略化できます。この関数は指定された範囲内で値を「ループ」させます。

    ```gdscript
    position.x = wrapf(position.x, 0, screen_size.x)
    position.y = wrapf(position.y, 0, screen_size.y)
    ```
