---
title: "アニメーションタイル(タイルマップ)"
weight: 5
draft: false
ghcommentid: 27
---

この記事はGodot3からGodot4へ書き換え中です。

## 課題

タイルマップでアニメーションタイルを使用したい。

## 解決策

この問題に対処する最も直接的な方法は、`AnimatedTexture`リソースを使用することです。

### アニメーションテクスチャの作成方法

以下の水タイルを使用して説明します。

![alt](/godot_recipes/3.x/img/anim_tiles.png)

これらの画像をダウンロードしてください。[water.zip](/godot_recipes/4.x/ja/files/water_tiles.zip)

画像ファイルをプロジェクトフォルダに解凍してください。
インスペクタで「新しいリソースを作成」ボタンをクリックします。

![alt](/godot_recipes/3.x/img/create_new_resource.png)

「AnimatedTexture」を選択し、［フレーム］プロパティを「5」に設定します。各フレームごとに、対応する画像を［テクスチャ］プロパティにドラッグしてください。

![alt](/godot_recipes/3.x/img/anim_texture_add.png)

アニメーション全体の速度は_Fps_プロパティで、各フレームごとの遅延時間は_Delay Sec_で個別に調整できます。

「保存」ボタンをクリックしてリソースを保存します。`water_anim.tres`のような名前を付けてください。

### TileMapでのAnimatedTextureの使用について

アニメーション付きテクスチャが保存されたので、これで`TileSet`で使用できるようになります。新規または既存の{{< gd-icon TileMap >}}`TileMap`を開き、その _Tile Set_ プロパティを選択します。新しいテクスチャを`TileSet`に追加するには、ボタンをクリックしてください。

![alt](/godot_recipes/3.x/img/anim_tile_add.png)

追加された新規テクスチャを選択し、「単一タイルとして新規作成」をクリックします。テクスチャを囲むようにボックスを描きます（「スナップ機能を有効にする」を設定すると作業が楽になります）。

![alt](/godot_recipes/3.x/img/anim_tile_select.png)

これで`TileMap`内のタイルを選択して、他の通常のタイルと同じように描画できるようになります。

![alt](/godot_recipes/3.x/img/anim_tile_draw.gif)

<translation></translation>

## 関連するレシピ

- [タイルマップ：オートタイルの活用](/godot_recipes/4.x/ja/autotile_intro)