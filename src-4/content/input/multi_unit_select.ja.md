---
title: "マウスドラッグでユニットを選択"
weight: 7
draft: false
---

## 課題

RTS(リアルタイムストラテジー)のように、複数ユニットを選択するためにクリック＆ドラッグしたい。

## 解決策

リアルタイムストラテジー（RTS）ゲームでは、複数ユニットに同時に命令する事があります。一般的な操作手法として、対象ユニットをマウスでクリックしてドラッグすることで選択範囲を決定。またユニットを選択したら、マップ上をクリックすることで移動コマンドを実行させる事が多いです。

以下に目指すべき例を示します。

![alt](/godot_recipes/4.x/img/multi_unit_01.gif)

### ユニット設定

この機能を実際に試すには、基本的なRTSスタイルのユニットが必要です。これらのユニットはターゲットに向かって移動し、互いに衝突しないように設計されています。チュートリアルではこの点について詳しく説明しません。カスタムRTSユニット作成のベースとして使いたい場合は、ユニットスクリプトにコメントが付いています。プロジェクトをダウンロードするためのリンクは以下の通りです。

### ワールドのセットアップ

ユニット選択の処理はワールド内で行います。まず「World」という名前の{{< gd-icon Node2D >}}`Node2D`オブジェクトを作成し、その中に`Unit`インスタンスをいくつか追加します。Worldノードにスクリプトをアタッチし、以下の変数を設定してください。

```gdscript
extends Node2D

var dragging = false  # Are we currently dragging?
var selected = []  # Array of selected units.
var drag_start = Vector2.ZERO  # Location where drag began.
var select_rect = RectangleShape2D.new()  # Collision shape for drag box.
```

※ボックスを描画した後は、その内部にどのユニットが位置しているかを確認する方法が必要となります。 {{< gd-icon RectangleShape2D >}}`RectangleShape2D`を使用すると物理エンジンに問い合わせて、衝突した対象を確認できます。

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

### ユニットの選択方法

選択ボックスが作成できたら、その内部に位置するユニットを特定する必要があります。ボタンを放してドラッグ操作が終了した際には、物理空間クエリを実行して対象のユニットを検索する必要があります。なお、対象となるユニットは{{< gd-icon CharacterBody2D >}}`CharacterBody2D`ですが、{{< gd-icon Area2D >}}`Area2D`やその他のボディタイプでも問題ありません。

`物理DirectSpaceState2D.intersect_shape()`を使用してユニットを検出します。これには形状（ここでは矩形）と変換行列（位置）が必要となります。詳細は[Godotドキュメント](https://docs.godotengine.org/ja/4.x/classes/class_physicsdirectspacestate2d.html)を参照してください。

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

これで物理状態への参照を取得し、`物理ShapeQueryParameters2D`を使用して形状クエリを設定できます。ここでは対象の形状を指定するとともに、ドラッグ操作中のエリアの中心座標を基準にしてクエリの変換行列を定義します。`intersect_shape()`を呼び出した後の結果は、Dictonary 配列として返され、以下のような形式になります。

```
[{ "rid": RID(4093103833089), "collider_id": 32145147326, "collider": Unit2:<CharacterBody2D#32145147326>, "shape": 0 },
{ "rid": RID(4123168604162), "collider_id": 32229033411, "collider": Unit3:<CharacterBody2D#32229033411>, "shape": 0 }]
```

各`collider`項目はそれぞれユニットへの参照であるため、これを使用すれば選択通知を行い、アウトラインシェーダーを有効にできます。

```gdscript
    for item in selected:
        item.collider.selected = true
```

![alt](/godot_recipes/4.x/img/multi_unit_03.gif)

### 部隊指揮について

最終的に、画面上の任意の位置をクリックすることで、選択したユニットに移動コマンドを発行できます。

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

ここでの `else` 条件は、`selected` が 0 より大きいときにマウスをクリックした場合にトリガーされます。各項目の `target` を設定した後、ユニットを選択解除することで、再度最初から開始できるようにしています。

## まとめ

このテクニックはリアルタイムストラテジーゲーム（RTS）やその他のジャンルのゲームに応用できます。以下から完全版プロジェクトをダウンロードして、ゲームを作る際に活用してください。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます。 [https://github.com/godotrecipes/multi_unit_support](https://github.com/godotrecipes/multi_unit_support)


## 関連レシピ

- [マウス入力](/godot_recipes/4.x/ja/input/mouse_input/)
