---
title: "アニメーションタイル(タイルマップ)"
weight: 5
draft: false
ghcommentid: 27
---

## 課題

タイルマップでアニメーションタイルを使用したい。

## 解決策

この問題に対処する最も直接的な方法は、`AnimatedTexture`リソースを使用することです。

### アニメーションテクスチャの作成方法

以下の水タイルを使用して説明します。

![alt](/godot_recipes/3.x/img/anim_tiles.png)

これらの画像をダウンロードしてください。[water.zip](/godot_recipes/3.x/files/water_tiles.zip)

画像ファイルをプロジェクトフォルダに解凍してください。
インスペクタで「新しいリソースを作成」ボタンをクリックします。

![alt](/godot_recipes/3.x/img/create_new_resource.png)

Choose `AnimatedTexture` and set the _Frames_ property to `5`. For each frame, drag the corresponding image to its _Texture_ property.

![alt](/godot_recipes/3.x/img/anim_texture_add.png)

You can adjust the overall animation's speed with the _Fps_ property, as well as each individual frame's _Delay Sec_.

「保存」ボタンをクリックしてリソースを保存します。`water_anim.tres`のような名前を付けてください。

### タイルマップでのAnimatedTextureの使用について

Now that the `AnimatedTexture` is saved, it can be used in a `TileSet`. Open a new or existing {{< gd-icon TileMap >}}`TileMap` and select its _Tile Set_ property. Click the button to add a new texture to the `TileSet`:

![alt](/godot_recipes/3.x/img/anim_tile_add.png)

追加された新規テクスチャを選択し、「単一タイルとして新規作成」をクリックします。テクスチャを囲むようにボックスを描きます（「スナップ機能を有効にする」を設定すると作業が楽になります）。

![alt](/godot_recipes/3.x/img/anim_tile_select.png)

これで`TileMap`内のタイルを選択して、他の通常のタイルと同じように描画できるようになります。

![alt](/godot_recipes/3.x/img/anim_tile_draw.gif)

<translation></translation>

## 関連するレシピ

- [タイルマップ：オートタイルの活用](http://kidscancode.org/godot_recipes/autotile_intro)