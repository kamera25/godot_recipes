---
title: "Yソートを使う"
weight: 4
draft: false
---

## 課題

多くの2Dゲームでは「3/4視点」と呼ばれるアングルが採用されており、カメラが少し斜め上から見下ろしているような構図になっています。これを実現するためには、より「奥」にあるオブジェクトを先に描画し、手前のオブジェクトの後ろに配置が必要です。実際には、これは「y軸ソート」（描画順序をオブジェクトの`y座標`に紐付けること）を意味します。画面上の高い位置にあるものほど遠くに位置するため、レンダリング順序もそれに応じて低く設定されることになります。

以下のような問題が発生します。

![alt](/godot_recipes/4.x/img/ysort_01.png)

以下のオブジェクトはデフォルトのレンダリング順序（ツリー順）で描画されています。シーンツリー上での配置は以下の通りです。

![alt](/godot_recipes/4.x/img/ysort_06.png)

## 解決策

Godotにはレンダリング順序を変更する組み込みオプションが用意されています。任意の{{< gd-icon CanvasItem >}}`CanvasItem`ノード（{{< gd-icon Node2D >}}`Node2D`または{{< gd-icon Control >}}`Control`）に対して、**Y軸ソート有効化** プロパティを有効にできます。この機能が有効になると、すべての子ノードがY軸に沿って並べ替えられます。

上記の例では、{{< gd-icon TileMap >}}`TileMap`ノード上でプロパティを有効にできます。ただし、まだ解決すべき問題が残っています。

![alt](/godot_recipes/4.x/img/ysort_01.png)

ドロー順序は各オブジェクトの `y` 座標に基づいています。デフォルトではこれはオブジェクトの中心位置となります。

![alt](/godot_recipes/4.x/img/ysort_04.png)

オブジェクトが「地面」の上に配置されているように見せたい場合、オブジェクトの `position` プロパティがスプライトの最下部位置と一致するようにオフセットすることで解決できます。

![alt](/godot_recipes/4.x/img/ysort_05.png)

だいぶ良くなりました。

![alt](/godot_recipes/4.x/img/ysort_02.gif)

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコード: [https://github.com/godotrecipes/using_ysort](https://github.com/godotrecipes/using_ysort)