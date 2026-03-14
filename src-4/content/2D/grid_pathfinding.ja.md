---
title: "2Dグリッド上での経路探索"
weight: 5
draft: false
---

## 課題

グリッドベースの環境があり、ナビゲーションを可能にする経路探索システムを構築したいと考えています。

## 解決策

Godot は経路探索のための複数の手法を提供しています。今回のレシピでは「A*(エースター)」アルゴリズムを取り上げます。

{{% notice style="info" title="A*について" %}}
A*アルゴリズムは、2点間の最短経路を求めるために広く利用されている手法です。グリッドに限らず、あらゆるグラフ構造データに適用可能です。
{{% /notice %}}

`AStarGrid2D` はGodotの汎用クラス `AStar2D` をグリッド環境用に最適化した専用バージョンです。グリッドベースで設計されているため、個々のセルや接続関係を手動で追加する必要がなく、より高速かつ簡単にセットアップできます。

### グリッドの設定

最も重要な設定決定事項は、セルのサイズとグリッド自体のサイズです。ここでは例として `(64, 64)` を使用しますが、ウィンドウサイズは画面上に収まるセル数を決定するために使用します。ただし、セルサイズが異なっても基本的な動作原理は同じです。

このコードを `Node2D` の `{{<  gd-icon Node2D >}}`に追加してください。

```gdscript
extends Node2D

@export var cell_size = Vector2i(64, 64)

var astar_grid = AStarGrid2D.new()
var grid_size

func _ready():
    initialize_grid()

func initialize_grid():
    grid_size = Vector2i(get_viewport_rect().size) / cell_size
    astar_grid.size = grid_size
    astar_grid.cell_size = cell_size
    astar_grid.offset = cell_size / 2
    astar_grid.update()
```

このコードでは、画面サイズを「セルサイズ」で割ることでグリッド全体の寸法を計算しています。これにより、`AStarGrid2D` オブジェクトの `size` プロパティを適切に設定できます。

The `offset` property will come into play when we ask for a path between two points. Using `cell_size / 2` means the path will be calculated from the center of each cell rather than the corners.

最後に、`AStarGrid2D`のプロパティを設定または変更した後は必ず`update()`メソッドを呼び出す必要があります。

### グリッド線の描画

本デモでは、グリッドの描画をプログラムコードで実装します。実際のゲームアプリケーションでは、通常 `TileMap` クラスやその他の視覚的表現を用いて世界を表現することになります。

以下は、グリッドを描画するためのコード例です：

```gdscript
func _draw():
    draw_grid()

func draw_grid():
    for x in grid_size.x + 1:
        draw_line(Vector2(x * cell_size.x, 0),
            Vector2(x * cell_size.x, grid_size.y * cell_size.y),
            Color.DARK_GRAY, 2.0)
    for y in grid_size.y + 1:
        draw_line(Vector2(0, y * cell_size.y),
            Vector2(grid_size.x * cell_size.x, y * cell_size.y),
            Color.DARK_GRAY, 2.0)
```

これによりグリッドが視覚的に明確に表示されます：

![alt](/godot_recipes/4.x/img/astar_grid_01.png)

### 経路の描画方法

パスを見つけるには、開始点と終了点が必要です。スクリプトの上部にこれらの変数を追加しましょう。

```gdscript
var start = Vector2i.ZERO
var end = Vector2i(5, 5)
```

そして以下の行を _draw() 関数に追加して表示させます：

```gdscript
    draw_rect(Rect2(start * cell_size, cell_size), Color.GREEN_YELLOW)
    draw_rect(Rect2(end * cell_size, cell_size), Color.ORANGE_RED)
```

2点間の経路は`get_point_path()`メソッドを使用して取得できますが、これを可視化する必要もあります。ここでは{{< gd-icon Line2D >}}`Line2D`を使用できるので、シーンに追加します。

以下の方法でパスを取得し、得られた点を `{{< gd-icon Line2D >}}`Line2D` に追加する方法をご紹介します。

```gdscript
func update_path():
    $Line2D.points = PackedVector2Array(astar_grid.get_point_path(start, end))
```

以下が結果です：

![alt](/godot_recipes/4.x/img/astar_grid_02.png)

注：2点間に斜線が引かれています。これはデフォルト設定では経路に斜め移動が含まれるためです。この設定は`diagonal_mode`を変更することで変更可能です：

* `DIAGONAL_MODE_ALWAYS` - デフォルト値。対角移動を使用可能。
* `DIAGOAL_MODE_NEVER` - すべての移動は直行移動のみ。
* `DIAGONAL_MODE_AT_LEAST_ONE_WALKABLE` - この設定では対角移動が可能ですが、斜め配置された障害物の「間」を経路が通過するのを防ぎます。
* `DIAGONAL_MODE_ONLY_IF_NO_OBSTACLES` - この場合、障害物のないオープンエリアでのみ対角移動が可能です。障害物付近ではこのモードは適用されません。

プロパティを変更すると結果が大きく変わる可能性があるため、環境に合わせた調整が重要です。`initialize_grid()` 関数にこれを追加しましょう。

```gdscript
astar_grid.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
```

現在可能な動きは直交移動のみです：

![alt](/godot_recipes/4.x/img/astar_grid_03.png)

### 障害物の追加

グリッドに障害物を追加することも可能です。セルを「固体」としてマークすると、そのセルを通過する経路は除外されます。`set_point_solid()` 関数を使用すると、セルの状態（固体／非固体）を切り替えることができます。

壁を描画するコードを追加しましょう（存在する場合）。固体セルを探し出して色付けします。

```gdscript
func fill_walls():
    for x in grid_size.x:
        for y in grid_size.y:
            if astar_grid.is_point_solid(Vector2i(x, y)):
                draw_rect(Rect2(x * cell_size.x, y * cell_size.y, cell_size.x, cell_size.y), Color.DARK_GRAY)
```

`_draw()` 内でこの関数を呼び出してください。

その後、マウスを使ってセルをクリックし、その状態を切り替えることができます：

```gdscript
func _input(event):
    if event is 入力EventMouseButton:
        # Add/remove wall
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            var pos = Vector2i(event.position) / cell_size
            if astar_grid.is_in_boundsv(pos):
                astar_grid.set_point_solid(pos, not astar_grid.is_point_solid(pos))
            update_path()
            queue_redraw()
```

注意：まず `is_in_boundsv()` をチェックしています。これにより、グリッド領域外にマウスをクリックした場合のエラー発生を防ぐことができます。

現在では、障害物が経路に及ぼす影響を確認できます：

![alt](/godot_recipes/4.x/img/astar_grid_04.png)

### ヒューリスティック選択について

結果となる経路に大きく影響する重要な要素は、使用する「ヒューリスティック手法」です。「ヒューリスティック」という用語は「最適な推測」を意味し、経路探索の文脈においては具体的に：目標地点へ向かう際に、まずどの方向を試すべきかを決定する方法を指します。

例えば、ユークリッド距離はピタゴラスの定理を用いて経路を推定します。

![alt](/godot_recipes/4.x/img/astar_grid_03.png)

マンハッタン距離は南北または東西方向の距離のみを考慮しますが、以下の点に注意が必要です：

![alt](/godot_recipes/4.x/img/astar_grid_manhattan.png)

オクトイルヒューリスティックを適用すると、以下のような経路が得られます：

![alt](/godot_recipes/4.x/img/astar_grid_octile.png)

このプロパティを使用してヒューリスティックを選択できます：

```gdscript
astar_grid.default_estimate_heuristic = AStarGrid2D.HEURISTIC_OCTILE
```

どの方法が最も効果的か（最も見栄えの良い経路が得られるか）は、環境の特性によって異なります。広いオープンスペースが中心で、周囲に障害物が点在しているような状況でしょうか？ それとも、複雑に絡み合った通路が入り組んだ迷路のような空間でしょうか？ 必ずご自身の具体的なプロジェクトで試行錯誤してみてください。

以下のサンプルプロジェクトをダウンロードして、この設定を実際に試してみましょう。壁を配置するだけでなく、右クリック／中クリックでエンドポイントとスタート地点を移動させることができます。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/grid_pathfinding](https://github.com/godotrecipes/grid_pathfinding)