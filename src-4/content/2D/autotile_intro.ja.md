---
title: "タイルマップ：自動タイルを使用"
weight: 4
draft: false
ghcommentid: 23
---

## 今回のお題

{{< gd-icon TileMapLayer >}}`TileMapLayer`のTerrains（地形）機能を使い、隣接セルに応じて正しいタイルを自動配置してレベル作成を効率化したいです。

## 作り方

本デモでは、以下のタイルセットを使用します。

![Godot 4: タイルマップ：自動タイルを使用 (autotile tileset)](/godot_recipes/4.x/img/autotile_tileset.png)

{{% notice note %}}
これらのタイルはKenney氏の『Topdown Shooter』アートパックに含まれており、こちらから入手できます。[https://kenney.nl/assets/top-down-shooter](https://kenney.nl/assets/top-down-shooter)
{{% /notice %}}

これらのタイルから地図を作成する場合、1枚ずつ手動で配置していくと非常に手間がかかります。角や交差点、終点部分を合わせるために、常に異なるタイルを切り替えながら作業することになるからです。

Godot 4では旧版のAutoTileの代わりに、TileSetの**Terrains**機能を使います。壁を任意の方向に描画すると、Terrainsが周囲のセルに合うタイルを選択して、境界をシームレスに配置します。

以下に具体例を示します。

![Godot 4: タイルマップ：自動タイルを使用 (autotile demo)](/godot_recipes/4.x/img/autotile_demo.gif)

### 自動タイリングの仕組みについて

使用しているタイルは `3×3（最小）` のタイリング用に設計されています。単一のタイルを3×3グリッドに分割した場合を考えてみます。

![Godot 4: タイルマップ：自動タイルを使用 (autotile bitmask tile)](/godot_recipes/4.x/img/autotile_bitmask_tile.png)

タイルの「アクティブ」部分（つまり壁ではない箇所）に目印を付けることができます。

![Godot 4: タイルマップ：自動タイルを使用 (autotile bitmask tile2)](/godot_recipes/4.x/img/autotile_bitmask_tile2.png)

これを各タイルごとに実行すれば、コンピュータはどのタイルを隣接させても確実に互換性が確保されるようにできます。

3×3のグリッド上には、512通りの組み合わせパターンが存在します（2^9）。これらのほとんどは連続した壁を作る上で実用的ではないため、除外して構いません。実際に適切な形で壁面を覆うためには、48枚のタイルが必要であることが分かりました。これはタイルセットに用意されているものです。以下の7枚のタイルは無視することにします。右下隅に位置する白い背景のタイルです。

### タイルセットの作成方法

{{< gd-icon TileMapLayer >}}`TileMapLayer`を追加し、インスペクターの **Tile Set** から新しい `TileSet` リソースを作成します。TileSetエディターの **Setup** タブでタイルセット画像をアトラスソースとして追加し、タイルサイズと余白を設定してください。

次に **Terrains** タブでTerrain Setを1つ作成し、接続方式に **Match Corners and Sides** を選びます。各タイルを選択して、壁・通路として隣接可能な辺と角に同じTerrain Set／Terrain IDを割り当てます。ここでの割り当てが、旧版のビットマスクに相当します。

{{% notice tip %}}
画像に境界用のタイルが欠けていると、Terrainsは正しい接続先を選べません。直線、内外の角、T字路、端点を含むタイルを用意してから割り当てると、描画時の警告を避けられます。
{{% /notice %}}

TileMapLayerを選択してペイントモードを **Terrains** に切り替え、作成したTerrain Setを選びます。ドラッグして描画すると、隣接セルに合わせてタイルが自動的に置き換えられます。衝突判定やナビゲーションはTileSetエディターで各タイルに設定します。

### 完全タイルセット

また、自動タイルセットに衝突判定、移動経路、または遮蔽効果を追加することもできます。以下のサンプルプロジェクトをダウンロードすると、すべてのタイル上にポリゴンが定義された完全なタイルセットを入手できます。

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。 [autotile_intro.zip](/godot_recipes/4.x/ja/files/autotile_intro.zip)
{{% /notice %}} -->
