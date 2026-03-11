---
title: "Mouse: Drag-select multiple units"
weight: 7
draft: false
---

## 課題

複数ユニットを選択するためにクリック＆ドラッグしたいんですね、RTSスタイルのように。

## 解決策

リアルタイムストラテジー（RTS）ゲームでは、複数ユニットに同時に命令を出す必要がある場合が多い。一般的な操作手法として、対象ユニットをマウスでクリックしてドラッグすることで選択範囲を指定する方法がある。ユニットを選択したら、マップ上をクリックすることで移動コマンドを実行できる。

以下に目指すべき例を示します：

![alt](/godot_recipes/4.x/img/multi_unit_01.gif)

### ユニット設定

この機能を実際に試すには、基本的なRTSスタイルのユニットが必要です。これらのユニットはターゲットに向かって移動し、互いに衝突しないように設計されています。チュートリアルではこの点について詳しく説明しません。カスタムRTSユニット作成のベースとして使いたい場合は、ユニットスクリプトにコメントが付いています。プロジェクトをダウンロードするためのリンクは以下の通りです：

### 世界設定

ユニット選択の処理はワールド内で行います。まず「World」という名前の{{< gd-icon Node2D >}}`Node2D`オブジェクトを作成し、その中にいくつかの`Unit`インスタンスを追加します。ワールドノードにスクリプトをアタッチし、以下の変数を設定してください：

```gdscript
extends Node2D

var dragging = false  # Are we currently dragging?
var selected = []  # Array of selected units.
var drag_start = Vector2.ZERO  # Location where drag began.
var select_rect = RectangleShape2D.new()  # Collision shape for drag box.
```

※ボックスを描画した後は、その内部にどのユニットが位置しているかを確認する方法が必要です。 `{{< gd-icon RectangleShape2D >}}`RectangleShape2D`を使用すると物理エンジンに問い合わせて、衝突した対象を確認できます。

### ボックスの描画方法

この操作にはマウスの左ボタンを使用します。クリックすることでドラッグが開始され、指を離すと終了します。この作業中に、視認性のために長方形を描いていきます。

```gdscript
func _unhandled_input(event):
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            # If the mouse was clicked and nothing is selected, start dragging
            if selected.size() == 0:
                dragging = true
                drag_start = event.position
        # If the mouse is released and is dragging, stop dragging
        elif dragging:
            dragging = false
            queue_redraw()
    if event is InputEventMouseMotion and dragging:
        queue_redraw()

func _draw():
    if dragging:
        draw_rect(Rect2(drag_start, get_global_mouse_position() - drag_start),
                Color.YELLOW, false, 2.0)
```

### 単位の選択方法

# 選択ボックス内に包含されるユニットを特定します
selection_box.get_units()

```cpp
// Define the rectangle shape and location transform
PhysicsBodyRectShape rect_shape;
Transform loc_transform;

// Initialize with appropriate values
rect_shape.set_origin(Vector2(0.5, 0.5));
loc_transform = Transform::identity();

// Perform intersection test
bool is_intersected = physics_space_state->intersect_shape(&rect_shape, &loc_transform);
```

この例では、`PhysicsDirectSpaceState2D` を使用して長方形形状と位置変換を定義し、交差判定を行っています。[Godot公式ドキュメント](https://docs.godotengine.org/ja/stable/classes/class_physicsdirectspacestate2d.html#class-physicsdirectspacestate2d-method-intersect-shape) に詳細な解説がありますので、必要に応じて参照してください。

```gdscript
elif dragging:
    dragging = false
    queue_redraw()
    var drag_end = event.position
    select_rect.extents = abs(drag_end - drag_start) / 2
```

まず、ボタンを離した瞬間の位置座標を取得し、この値を使って{{< gd-icon RectangleShape2D >}}`RectangleShape2D`の `extents` を設定します（注意点：`extents`は矩形の*中心*から計測されるため、実際の幅・高さの半分となります）。

```gdscript
    var space = get_world_2d().direct_space_state
    var query = PhysicsShapeQueryParameters2D.new()
    query.shape = select_rect
    query.collision_mask = 2  # Units are on collision layer 2
    query.transform = Transform2D(0, (drag_end + drag_start) / 2)
    selected = space.intersect_shape(query)
```

# Create physics state and set it up using PhysicsShapeQueryParameters2D
physics_state = Box2DWorld.create_physics_state()
shape_query_params = PhysicsShapeQueryParameters2D()
shape_query_params.set_body_shapes([car_shape])

# Set origin of the query transformation to the center of the dragged area
origin_point = pymunk.Vec2d(self.dragged_area.center())
query_transform = TransformedPhysicsBodyFilter(physics_state, origin_point)
shape_query_params.set_filter(query_transform)

# Perform intersection test and get results
intersection_results = physics_state.intersect_shapes2D(shape_query_params)

```
[{ "rid": RID(4093103833089), "collider_id": 32145147326, "collider": Unit2:<CharacterBody2D#32145147326>, "shape": 0 },
{ "rid": RID(4123168604162), "collider_id": 32229033411, "collider": Unit3:<CharacterBody2D#32229033411>, "shape": 0 }]
```

各「コリダー」項目はそれぞれユニットへの参照であるため、これを使用すれば選択通知を行い、アウトラインシェーダーを有効にできます：

```gdscript
    for item in selected:
        item.collider.selected = true
```

<img src="/godot_recipes/4.x/img/multi_unit_03.gif" alt="Multi Unit 03">

### 部隊指揮について

最終的に、画面上の任意の位置をクリックすることで、選択したユニットに移動コマンドを発行できます：

```gdscript
func _unhandled_input(event):
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            # If the mouse was clicked and nothing is selected, start dragging
            if selected.size() == 0:
                dragging = true
                drag_start = event.position
            # Otherwise a click tells the selected units to move
            else:
                for item in selected:
                    item.collider.target = event.position
                    item.collider.selected = false
                selected = []
```

```
ここでの `else` 条件は、`selected` が 0 より大きいときにマウスをクリックした場合にトリガーされます。各項目の `target` を設定した後、ユニットを選択解除することで、再度最初から開始できるようにしています。

## まとめ

この技術は様々なリアルタイムストラテジーゲーム（RTS）やその他のジャンルのゲームに応用可能です。以下から完全版プロジェクトをダウンロードして、自分の作品を作る際のベースとして活用してください。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます: [https://github.com/godotrecipes/multi_unit_support](https://github.com/godotrecipes/multi_unit_support)


## 関連レシピ

- [マウス入力](/godot_recipes/4.x/ja/input/mouse_input/)
