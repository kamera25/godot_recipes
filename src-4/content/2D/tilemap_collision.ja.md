---
title: "タイルマップ：タイルを検出する"
weight: 1
draft: false
ghcommentid: 19
---

## 今回のお題

{{< gd-icon CharacterBody2D >}}`CharacterBody2D`キャラクターが{{< gd-icon TileMap >}}`TileMap`と衝突しており、どのタイルに衝突したのかを確認したい場合。

## 作り方

{{< gd-icon `CharacterBody2D` >}} オブジェクト同士が衝突した場合、衝突データは `KinematicCollision2D` オブジェクトとして取得されます。 {{< gd-icon TileMap >}}`TileMap` は単一のコリダーとして機能するため、`collider` プロパティを参照すると実際にはこの {{< gd-icon TileMap >}}`TileMap` ノードが返される点にご注意ください。

その後、衝突位置にある{{< gd-icon TileMap >}}`TileMap`のタイルを特定が必要です。

以下の状況を想定します。変数 `collision` に `KinematicCollision2D` オブジェクトが格納されている場合：

```gdscript
# 衝突したボディがTileMapであることを確認
if collision.collider is TileMap:
    # タイル座標におけるキャラクターの位置を取得
    var tile_pos = collision.collider.world_to_map(position)
    # 衝突したタイルの位置を取得
    tile_pos -= collision.normal
    # タイルIDを取得
    var tile_id = collision.collider.get_cellv(tile_pos)
```

`tile_id`を取得した後、`TileSet`リソースからタイルのプロパティを取得できます。これは{{< gd-icon TileMap >}}`TileMap`オブジェクトの`tile_set`プロパティで参照できます。例えば、特定のタイル名を取得するには以下のようにします。

```gdscript
    var tile_name = collision.collider.tile_set.tile_get_name(tile_id)
```

また、新しい`id`を設定することでタイルを変更することもできます。

```gdscript
    collision.collider.set_cellv(tile_pos, new_id)
```

## 関連レシピ

- [タイルマップ: オートタイルを使う](/godot_recipes/4.x/ja/2d/autotile_intro/)
- [タイルマップ: アニメーションタイル](/godot_recipes/4.x/ja/2d/tilemap_animation/)

#### この動画が気に入ったら？

{{< youtube OzgK__VowVs >}}