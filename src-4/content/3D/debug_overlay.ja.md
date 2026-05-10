---
title: "3Dにおけるベクトル描画"
weight: 10
draft: false
ghcommentid: 37
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

3Dゲームで視覚的なデバッグ情報が欲しい。例えば、速度や位置などを表すベクトルを可視化する方法があれば嬉しい。

## 解決策

2Dでの描画デバッグは非常に便利です。{{< gd-icon CanvasItem2D >}}`CanvasItem`は`_draw()`コールバック内で使用できる多彩なプリミティブ描画メソッドを提供します。3Dの場合、状況はそれほど単純ではありません。一つの解決策として`ImmediateGeometry`を使って手動でメッシュを作成する方法がありますが、これは非常に手間がかかり、迅速なデバッグには不便です。

適切な解決策としては、引き続き`CanvasItem`の描画メソッドを使用することです。そのためにはまず、3D空間内の位置を2Dビューポートに投影する必要があります。幸い、{{< gd-icon Camera3D >}}`Camera`オブジェクトは、その`unproject_position()`メソッドを使ってこれを処理してくれます。

### セットアップ方法

表示レイヤーについては、3Dシーンに{{< gd-icon CanvasLayer >}}`CanvasLayer`コンポーネントを追加し、その中に`Control`を配置してください。さらに、この{{< gd-icon Control >}}`Control`にスクリプトを割り当てる必要があります。

![alt](/godot_recipes/4.x/img/3d_debug_03.png)

例：描画制御ノードがプレイヤーノードを参照しており、その`velocity(速度)`ベクトルを描画したいとします。また、{{< gd-icon Camera3D >}}`Camera`も参照しています。これらの参照方法については後ほど詳しく説明します。

```gdscript
var player
var camera

func _draw():
    var color = Color(0, 1, 0)
    var start = camera.unproject_position(player.global_transform.origin)
    var end = camera.unproject_position(player.global_transform.origin + player.velocity)
    node.draw_line(start, end, color, width)
    node.draw_triangle(end, start.direction_to(end), width*2, color)

func draw_triangle(pos, dir, size, color):
    var a = pos + dir * size
    var b = pos + dir.rotated(2*PI/3) * size
    var c = pos + dir.rotated(4*PI/3) * size
    var points = PoolVector2Array([a, b, c])
    draw_polygon(points, PoolColorArray([color]))
```

ベクトルの始点と終点を求めるために`unproject_position()`を使用します。`draw_triangle()`は、見栄えの良い尖った矢印形状を表示するために用意されています。

![alt](/godot_recipes/4.x/img/3d_debug_01.png)

![alt](/godot_recipes/4.x/img/3d_debug_02.png)

### ゲームオブジェクトからの簡単なアクセス方法

さて、これをより実用的な機能に改良します。ゲームにはデバッグ用ベクトルを描画したいオブジェクトが多数存在するはずです。敵の向き、加速度ベクトル、目的地など、様々な要素が考えられます。どんなオブジェクトでも簡単にデバッグ描画レイヤーに追加できる仕組みが必要となります。

以下の手順で`DebugOverlay`を自動読み込みとして追加し、シングルトンとして設定してください。これにより、どのノードからでもアクセス可能になります。このスクリプトに以下の内容を追加してください。

```gdscript
extends CanvasLayer

@onready var draw = $DebugDraw3D

func _ready():
    if not InputMap.has_action("toggle_debug"):
        InputMap.add_action("toggle_debug")
        var ev = InputEventKey.new()
        ev.scancode = KEY_BACKSLASH
        InputMap.action_add_event("toggle_debug", ev)

func _input(event):
    if event.is_action_pressed("toggle_debug"):
        for n in get_children():
            n.visible = not n.visible
```

視認性を切り替える入力アクションを追加するコードを含めておきました。これにより、任意のプロジェクトに簡単に組み込むことができ、インプットマップを変更する必要がありません。これで、`DebugOverlay.draw` を使って描画レイヤーを参照できるようになりました。

{{% notice note %}}
ここには他のデバッグレイヤーも追加できます。例えば、プロパティをテキスト形式で表示するようなものです。
{{% /notice %}}

まず、表示したいデバッグ値に関する情報をすべて保持するためのカスタムオブジェクトを定義します。

```gdscript
extends Control

class Vector:
    var object  # The node to follow
    var property  # The property to draw
    var scale  # Scale factor
    var width  # Line width
    var color  # Draw color

    func _init(_object, _property, _scale, _width, _color):
        object = _object
        value = _property
        scale = _scale
        width = _width
        color = _color

    func draw(node, camera):
        var start = camera.unproject_position(object.global_transform.origin)
        var end = camera.unproject_position(object.global_transform.origin + object.get(property) * scale)
        node.draw_line(start, end, color, width)
        node.draw_triangle(end, start.direction_to(end), width*2, color)

var vectors = []  # Array to hold all registered values.
```

このオブジェクトには、表示したい各ベクトルの機能がすべてカプセル化されており、前述した描画コードも含まれています。`_process()` メソッド内では、これらのベクトルを描画することができ、その際には必ず現在アクティブなカメラを取得する必要があります。

```gdscript
func _process(delta):
    if not visible:
        return
    update()

func _draw():
    var camera = get_viewport().get_camera()
    for vector in vectors:
        vector.draw(self, camera)
```

最後に、新しいフォロー対象ベクトルを登録する関数を追加できます。

```gdscript
func add_vector(object, property, scale, width, color):
    vectors.append(Vector.new(object, property, scale, width, color))
```

これでゲーム内の任意のオブジェクトから、以下の方法でデバッグ用ベクトルを追加できるようになりました。

```gdscript
DebugOverlay.draw.add_vector(self, "velocity", 1, 4, Color(0,1,0, 0.5))
```

以下に、レイキャストと操舵方向を表示するAI制御車両の実例をご紹介します。

![alt](/godot_recipes/4.x/img/3d_debug_04.gif)

## 関連レシピ

- [UI：デバッグデータの表示](/godot_recipes/4.x/ja/ui/debug_overlay)