---
title: "画面ループ"
weight: 1
draft: false
ghcommentid: 17
---

## 課題

クラシックな2Dゲーム（『パックマン』タイプの作品など）でよく使われる、プレイヤーキャラクターが画面端から反対側に移動する機能を実装したいです。

## 解決策

1. スクリーンサイズ（ビューポート）を取得します。

    ```gdscript
    @onready var screen_size = get_viewport_rect().size
    ```

    `get_viewport_rect()` は `CanvasItem` 派生ノードであればどのノードからも利用できます。

1. プレイヤーの座標を比較します。

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

    注意：この処理ではノードの`position`を使用しています。これは通常、スプライトまたはボディの中心座標を指します。

1. `wrapf()` を使用して、シンプルに実装します。

    上記のコードは、GDScriptの`wrapf()`関数を使用することで簡略化できます。この関数は指定された範囲内で値を「ループ」させます。

    ```gdscript
    position.x = wrapf(position.x, 0, screen_size.x)
    position.y = wrapf(position.y, 0, screen_size.y)
    ```
