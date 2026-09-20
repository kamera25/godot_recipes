---
title: "アニメーションタイル(タイルマップ)"
weight: 5
draft: false
ghcommentid: 27
---

## 今回のお題

タイルマップでアニメーションタイルを使用したい。

## 作り方

この問題に対処する最も直接的な方法は、`AnimatedTexture`リソースを使用することです。

### アニメーションテクスチャの作成方法

以下の水タイルを使用して説明します。

![Godot 4: アニメーションタイル(タイルマップ) (anim tiles)](/godot_recipes/4.x/img/anim_tiles.png)

これらの画像をダウンロードします。[water.zip](/godot_recipes/4.x/ja/files/water_tiles.zip)

画像ファイルをプロジェクトフォルダに解凍します。
インスペクタで「新しいリソースを作成」ボタンをクリックします。

![Godot 4: アニメーションタイル(タイルマップ) (create new resource)](/godot_recipes/4.x/img/create_new_resource.png)

`AnimatedTexture`を選択し、［フレーム］プロパティを`5`に設定します。各フレームごとに、対応する画像を［テクスチャ］プロパティにドラッグします。

![Godot 4: アニメーションタイル(タイルマップ) (anim texture add)](/godot_recipes/4.x/img/anim_texture_add.png)

アニメーション全体の速度は _Fps_ プロパティで、各フレームごとの遅延時間は _Delay Sec_ で個別に調整できます。

「保存」ボタンをクリックしてリソースを保存します。`water_anim.tres`のような名前を付けてください。

### TileMapLayerでのAnimatedTextureの使用について

`AnimatedTexture` が保存されたので、これで`TileSet`で使用できるようになります。新規または既存の{{< gd-icon TileMapLayer >}}`TileMapLayer`を開き、その _Tile Set_ プロパティを選択します。Godot 4.3以降はレイヤーごとに`TileMapLayer`を使用します。新しいテクスチャを`TileSet`に追加するには、ボタンをクリックします。

![Godot 4: アニメーションタイル(タイルマップ) (anim tile add)](/godot_recipes/4.x/img/anim_tile_add.png)

追加された新規テクスチャを選択し、「単一タイルとして新規作成」をクリックします。テクスチャを囲むようにボックスを描きます（「スナップ機能を有効にする」を設定すると作業が楽になります）。

![Godot 4: アニメーションタイル(タイルマップ) (anim tile select)](/godot_recipes/4.x/img/anim_tile_select.png)

これで`TileMapLayer`内のタイルを選択して、他の通常のタイルと同じように描画できるようになります。

![Godot 4: アニメーションタイル(タイルマップ) (anim tile draw)](/godot_recipes/4.x/img/anim_tile_draw.gif)

<translation></translation>

## 関連するレシピ

- [タイルマップ：オートタイルの活用](/godot_recipes/4.x/ja/autotile_intro)
