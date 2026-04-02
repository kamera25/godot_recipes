---
title: "限定サークル"
weight: 3
draft: false
pre: "03. "
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

最初の2部で基本ゲームプレイは完成しました。ここからは、サークルに様々なモードを追加していきます。

## サークルモードについて

最終的には様々なモードを実装する予定ですが、まずは「制限モード」から始めてください。このモードでは、円は特定回数の周回後に消滅します。まず、残りの周回数を表示する `Label` ノードを追加してください。テキストフィールドに数値（例：`1`）を入力して、表示方法を確認してみてください。

[カスタムフォント] セクションで、新しい `DynamicFont` を追加し、アセットフォルダから _フォントデータ_ を読み込み、 _サイズ_ を `64` に設定します。ラベルの位置を中央配置するには、「レイアウト」メニューから「中央揃え」を選択します。

以下の新しい変数を `Circle.gd` ファイルの先頭に追加してください。

```gdscript
enum MODES {STATIC, LIMITED}

var mode = MODES.STATIC
var num_orbits = 3  # Number of orbits until the circle disappears
var current_orbits = 0  # Number of orbits the jumper has completed
var orbit_start = null  # Where the orbits started
```

次に、モードを設定する方法が必要です。

```gdscript
func set_mode(_mode):
    mode = _mode
    match mode:
        MODES.STATIC:
            $Label.hide()
        MODES.LIMITED:
            current_orbits = num_orbits
            $Label.text = str(orbits_left)
            $Label.show()
```

現在はこれら2つのモードが定義されていますが、後でさらに追加される予定です。

さらに、`init()` メソッドにモードを引数として渡す方法も追加してください。デフォルト値は `STATIC` のままにしますが、今回はテスト用に `LIMITED` を使用することにします。これにより、以下のことが可能になります。

```gdscript
func init(_position, _radius=radius, _mode=MODES.LIMITED):
    set_mode(_mode)
```

The jumper is setting the rotation position when it's captured. Remove the line from `Jumper.gd` and put it in the circle's `capture()` method:

```gdscript
func capture(target):
    jumper = target
    $AnimationPlayer.play("capture")
    $Pivot.rotation = (jumper.position - position).angle()
    orbit_start = $Pivot.rotation
```

注意：現在はジャンパーへの参照を渡しているため、スクリプトの先頭に`var jumper = null`を追加し、`Main.gd`スクリプト内の呼び出しを`object.capture(player)`に変更してください。

現在位置が一周したか確認し、もしそうであれば`current_orbits`を1減算します。

```gdscript
func _process(delta):
    $Pivot.rotation += rotation_speed * delta
    if mode == MODES.LIMITED and jumper:
        check_orbits()

func check_orbits():
    # Check if the jumper completed a full circle
    if abs($Pivot.rotation - orbit_start) > 2 * PI:
        current_orbits -= 1
        $Label.text = str(current_orbits)
        if orbits_left <= 0:
            jumper.die()
            jumper = null
            implode()
        orbit_start = $Pivot.rotation
```

この機能を動作させるには、ジャンパークラスに`die()`メソッドを追加が必要です。

```gdscript
func die():
    target = null
    queue_free()

func _on_VisibilityNotifier2D_screen_exited():
    if !target:
        die()
```

さらに、ジャンパの `VisibilityNotifier2D` シグナルも接続しました。これにより、プレイヤーが画面外に出た際にプレイヤーオブジェクトを削除できるようになっています。

試しに動かしてみると、今のところ問題なく動作しています。

![alt](/godot_recipes/3.x/img/cj_03_01.gif)

### サークル効果

このセクションの最後の作業として、軌道が尽きつつあることを示すために円に「塗り」効果を追加します。まず、[公式ドキュメント](https://docs.godotengine.org/ja/latest/tutorials/2d/custom_drawing_in_2d.html#arc-polygon-function)にある描画コードを使用します。


```gdscript
func draw_circle_arc_poly(center, radius, angle_from, angle_to, color):
    var nb_points = 32
    var points_arc = PoolVector2Array()
    points_arc.push_back(center)
    var colors = PoolColorArray([color])

    for i in range(nb_points + 1):
        var angle_point = angle_from + i * (angle_to - angle_from) / nb_points - PI/2
        points_arc.push_back(center + Vector2(cos(angle_point), sin(angle_point)) * radius)
    draw_polygon(points_arc, colors)
```

以下の関数は _draw() 内で呼び出されます。

```gdscript
func _draw():
    if jumper:
        var r = ((radius - 50) / num_orbits) * (1 + num_orbits - current_orbits)
        draw_circle_arc_poly(Vector2.ZERO, r, orbit_start + PI/2,
                            $Pivot.rotation + PI/2, Color(1, 0, 0))
```

最後に、`_physics_process` に `update()` を追加し、`check_orbits()` が呼び出されるたびに実行されるようにしてください。

![alt](/godot_recipes/3.x/img/cj_03_02.gif)

次のパートでは、UI要素を追加していきます。

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube I1noxf5LV4I >}}