---
title: "タイルマップ：タイルを検出中"
weight: 1
draft: false
ghcommentid: 19
---

## Problem

You have a {{< gd-icon CharacterBody2D >}}`CharacterBody2D` character colliding with a {{< gd-icon TileMap >}}`TileMap`, and you want to know which tile it collided with.

## Solution

When a {{< gd-icon CharacterBody2D >}}`CharacterBody2D` collides, the collision data is returned in a `KinematicCollision2D` object. The {{< gd-icon TileMap >}}`TileMap` acts as a single collider, so if you reference the `collider` property, it will be the {{< gd-icon TileMap >}}`TileMap` node.

その後、衝突位置にある{{< gd-icon TileMap >}}`TileMap`のタイルを特定が必要です。

以下の状況を想定してください。変数 `collision` に `KinematicCollision2D` オブジェクトが格納されている場合：

```gdscript
# Confirm the colliding body is a TileMap
if collision.collider is TileMap:
    # Find the character's position in tile coordinates
    var tile_pos = collision.collider.world_to_map(position)
    # Find the colliding tile position
    tile_pos -= collision.normal
    # Get the tile id
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

## Related recipes

- [タイルマップ: オートタイルを利用する](/godot_recipes/4.x/ja/2d/autotile_intro/)
- [タイルマップ: アニメーションタイル](/godot_recipes/4.x/ja/2d/tilemap_animation/)

#### この動画が気に入ったら？

{{< youtube OzgK__VowVs >}}