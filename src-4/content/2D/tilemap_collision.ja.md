---
title: "タイルマップ：タイルを検出する"
weight: 1
draft: false
ghcommentid: 19
---

## 今回のお題

{{< gd-icon CharacterBody2D >}}`CharacterBody2D`キャラクターが{{< gd-icon TileMapLayer >}}`TileMapLayer`と衝突しており、どのタイルに衝突したのかを確認したい場合。

## 作り方

{{< gd-icon `CharacterBody2D` >}} オブジェクト同士が衝突した場合、衝突データは `KinematicCollision2D` オブジェクトとして取得されます。Godot 4.3以降では各レイヤーを {{< gd-icon TileMapLayer >}}`TileMapLayer` ノードとして扱います。`get_collider()` は衝突したレイヤーノードを返します。

その後、衝突位置にある{{< gd-icon TileMapLayer >}}`TileMapLayer`のタイルを特定します。

以下の状況を想定します。変数 `collision` に `KinematicCollision2D` オブジェクトが格納されている場合：

```gdscript
if collision.get_collider() is TileMapLayer:
    var tile_map: TileMapLayer = collision.get_collider()
    # 衝突面の少し内側をセル座標へ変換する
    var collision_point = collision.get_position() - collision.get_normal()
    var tile_pos = tile_map.local_to_map(tile_map.to_local(collision_point))
    var source_id = tile_map.get_cell_source_id(tile_pos)
    var atlas_coords = tile_map.get_cell_atlas_coords(tile_pos)
```

Godot 4では単一のタイルIDではなく、ソースIDとアトラス座標でセルを識別します。タイル固有のゲーム情報は `TileData` のカスタムデータレイヤーに保存すると扱いやすくなります。

```gdscript
    var tile_data = tile_map.get_cell_tile_data(tile_pos)
    if tile_data:
        var tile_name = tile_data.get_custom_data("name")
```

セルを変更する場合は、ソースID・アトラス座標・代替タイルIDを指定します。

```gdscript
    tile_map.set_cell(tile_pos, source_id, new_atlas_coords, alternative_tile)
```

## 関連レシピ

- [タイルマップ: オートタイルを使う](/godot_recipes/4.x/ja/2d/autotile_intro/)
- [タイルマップ: アニメーションタイル](/godot_recipes/4.x/ja/2d/tilemap_animation/)

#### この動画が気に入ったら？

{{< youtube OzgK__VowVs >}}
