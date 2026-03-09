---
title: "Using Y-Sort"
weight: 4
draft: false
---

## 問題文

多くの2Dゲームでは「3/4視点」と呼ばれるアングルが採用されており、カメラが少し斜め上から見下ろしているような構図になっています。これを実現するためには、より「奥」にあるオブジェクトを先に描画し、手前のオブジェクトの後ろに配置する必要があります。実際には、これは「y軸ソート」（描画順序をオブジェクトの`y座標`に紐付けること）を意味します。画面上の高い位置にあるものほど遠くに位置するため、レンダリング順序もそれに応じて低く設定されることになります。

以下に問題の具体例を示します：

<img alt="YSort の設定例" src="/godot_recipes/4.x/img/ysort_01.png">

以下のオブジェクトはデフォルトのレンダリング順序（ツリー順）で描画されています。シーンツリー上での配置は以下の通りです：

[alt](/godot_recipes/4.x/img/ysort_06.png)

## 解決策

Godotにはレンダリング順序を変更する組み込みオプションが用意されています。任意の{{< gd-icon CanvasItem >}}`CanvasItem`ノード（{{< gd-icon Node2D >}}`Node2D`または{{< gd-icon Control >}}`Control`）に対して、**Y軸ソート有効化** プロパティを有効にすることができます。この機能が有効になると、すべての子ノードがY軸に沿って並べ替えられます。

上記の例では、{{< gd-icon TileMap >}}`TileMap`ノード上でプロパティを有効にできます。ただし、まだ解決すべき問題が残っています：

<img alt="YSort の設定例" src="/godot_recipes/4.x/img/ysort_01.png">

ドロー順序は各オブジェクトの y 座標に基づいています。デフォルトではこれはオブジェクトの中心位置となります：

![alt](/godot_recipes/4.x/img/ysort_04.png)

```markdown
オブジェクトが「地面」の上に配置されているように見せたい場合、各オブジェクトのスプライトをオフセットすることで解決できます。具体的には、オブジェクトの `position` プロパティがスプライトの最下部位置と一致するようにします。：

<img src="/godot_recipes/4.x/img/ysort_05.png" alt="">

これで状況はずいぶん改善されました：

<img src="/godot_recipes/4.x/img/ysort_02.gif" alt="YSortの操作例">

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/using_ysort](https://github.com/godotrecipes/using_ysort)