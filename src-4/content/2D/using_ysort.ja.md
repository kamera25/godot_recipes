---
title: "Using Y-Sort"
weight: 4
draft: false
---

## 問題文

Many 2D games use a "3/4 view" perspective, giving the impression that the camera is looking at the world at an angle. To make this work, objects that are "farther" away need to be rendered behind "nearer" objects. In practice, that means we want to "y-sort" - making the drawing order tied to the object's `y` coordinate. The higher on the screen, the farther away and therefore lower the render order.

以下に問題の具体例を示します：

<img alt=\ src=\>

以下のオブジェクトはデフォルトのレンダリング順序（ツリー順）で描画されています。シーンツリー上での配置は以下の通りです：

[alt](/godot_recipes/4.x/img/ysort_06.png)

## 解決策

Godotにはレンダリング順序を変更する組み込みオプションが用意されています。任意の{{< gd-icon CanvasItem >}}`CanvasItem`ノード（{{< gd-icon Node2D >}}`Node2D`または{{< gd-icon Control >}}`Control`）に対して、**Y軸ソート有効化** プロパティを有効にすることができます。この機能が有効になると、すべての子ノードがY軸に沿って並べ替えられます。

上記の例では、{{< gd-icon TileMap >}}`TileMap`ノード上でプロパティを有効にできます。ただし、まだ解決すべき問題が残っています：

<img alt=\ src=\>

ドロー順序は各オブジェクトの y 座標に基づいています。デフォルトではこれはオブジェクトの中心位置となります：

![alt](/godot_recipes/4.x/img/ysort_04.png)

Since we want to give the impression that the objects are on the "ground", we can solve this by offsetting each object's sprite so that the object's `position` is aligned with the *bottom* of the sprite:

<img src=\ alt=\>

これで状況はずいぶん改善されました：

<img src=\ alt=\>

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/using_ysort](https://github.com/godotrecipes/using_ysort)