---
title: "分割画面マルチプレイヤー"
weight: 1
draft: false
ghcommentid: 18
---
## 解決策

このデモでは、ローカルマルチプレイヤーゲーム――見下ろし型の迷路ゲームを例に挙げます。このゲームでは2人のプレイヤーが参加し、一方は矢印キー、もう一方はWASDキーで操作します。これは問題ありませんが、もしゲーム世界全体が1画面に収められる程度の大きさであれば、特に問題はありません。しかし、マップが非常に広い場合、両プレイヤーを個別に表示する「分割画面」ビューが必要になるでしょう。

![alt](/godot_recipes/3.x/img/splitscreen2.gif)

また、ミニマップ表示をすばやく設定する方法についても解説します。

### ゲーム設定

We won't spend a lot of time on the setup of the game world. The two players
are {{< gd-icon CharacterBody2D >}}`CharacterBody2D` objects using no-frills 8-way movement.

{{% notice note %}}
このパーツのセットアップでお困りの場合は、公式Godotドキュメントの以下のセクションをご覧ください: [2D移動概要](http://docs.godotengine.org/ja/stable/tutorials/2d/2d_movement.html)。
{{% /notice %}}

各操作は、プロジェクト設定の[インプットマップ]セクションで個別に設定されています。「right_1」は右矢印キー、「right_2」はDキーなどです。このように命名することで、コード内で以下の構文を使用でき、開発効率を大幅に向上させられます。

{{< highlight gdscript>}}
@export var id = 0

func get_input():
    velocity = Vector2()
    if Input.is_action_pressed('right_%s' % id):
        velocity.x += 1
    # etc.
{{< /highlight >}}

この方法であれば、キャラクターが同じ移動スクリプトを使用できます。各プレイヤーに適切な値を `id` として割り当てるだけです。

以下の手順に従って、2つのプレイヤーを `TileMap` を含む「ワールド」シーンに追加します。

![alt](/godot_recipes/3.x/img/splitscreen_map.png)

ご希望であれば、ワールドが既に設定済みの開始プロジェクトをこちらからダウンロードできます。

<!-- !LINK -->
[splitscreen_start.zip](/blog/img/splitscreen_start.zip)

このマップはゲーム画面よりもはるかに大きいことに注意してください。ただ、それ以外の点ではすべて正常に動作します。このようにゲームの「世界」を個別に設定することで、ビューポートの設定が格段に容易になり、より柔軟に扱えるようになります。

### ビューポート、カメラ、およびワールドについて

まず、2つのビューポートを含む新しいシーンを作成します。
ルートノードとして使用するノードを作成します。私は通常、`Node`を使用します。このノードには独自のプロパティが何もないため（単にシーンの他の要素を保持するためのものです）、使い勝手が良いからです。

By themselves, {{< gd-icon Viewport >}}`Viewport` nodes don't have position information (they don't
inherit from {{< gd-icon Node3D >}}`Node3D` or {{< gd-icon Node2D >}}`Node2D`). We're going to use {{< gd-icon SubViewportContainer >}}`ViewportContainer`,
a {{< gd-icon Control >}}`Control` node, to hold each viewport. To keep them arranged side-by-side, we'll
use an {{< gd-icon HBoxContainer >}}`HBoxContainer`.

{{< gd-icon HBoxContainer >}}`HBoxContainer`の配置を「中央」に設定し、2つのビューポート間に小さな隙間を設けるには、_カスタム定数/間隔_に `5` を設定してください。「レイアウト」メニューでは「フル矩形」を選択します。

次に、2つの{{< gd-icon SubViewportContainer >}}`ViewportContainer`を子要素として追加し、それぞれに`2`と`1`という名前を付けます（これらは表示するプレイヤーに対応するためです）。両方のコンテナについて_サイズフラグ_を「画面いっぱいに拡張」に設定してください。これにより、各コンテナが画面の半分を埋めるように拡大されます。さらに、_伸縮指定_プロパティもチェックすることで、{{< gd-icon Viewport >}}`Viewport`が自動的にコンテナのサイズに合わせて調整されるようになります。

各コンテナ内に、{{< gd-icon Viewport >}}`Viewport` 要素を追加してください。なお、ビューポートの
_サイズ_ プロパティを設定した場合、その値はコンテナによってリセットされますのでご注意ください。

{{< gd-icon Viewport >}}`ビューポート`に何らかのコンテンツを表示するには、{{< gd-icon Camera2D >}}`Camera2D`が必要です。このカメラは{{< gd-icon Viewport >}}`ビューポート`上にレンダリングを行います。各ビューポートに1つずつ追加してください。また、カメラを有効にするには_現在のプロパティを必ずチェックしてください_。さらに、各カメラのズーム値を`(0.75, 0.75)`に設定することで、プレイヤー周辺のエリアをより詳細に表示できるようになります。

ノードを以下のようにします。

```markdown
 ┖╴Main (Node)
    ┖╴Viewports (HBoxContainer)
       ┠╴ViewportContainer2
       ┃  ┖╴Viewport2
       ┃    ┖╴Camera2D
       ┖╴ViewportContainer1
          ┖╴Viewport1
            ┖╴Camera2D
```

{{% notice note %}}
注意点：`ViewportContainer1`を{{< gd-icon HBoxContainer >}}`HBoxContainer`内で2番目に配置しました。この設定により、プレイヤー1が矢印キーを使用するため、コンテナは右側に表示されます。
{{% /notice %}}

#### 空間（World）の追加

シーンを実行すると、ビューポートには何も表示されません。これはビューポートがレンダリングする「世界」を持っていないためです。3Dの場合は`world`プロパティ、2Dの場合は`world_2d`プロパティが、ビューポートの環境設定を表し、カメラによって何が表示されるかを決定します。ワールドはコード内で設定可能ですが、2Dの場合、追加した子ノードも自動的に表示される点に注意が必要です。

以下のように、「World」シーンを「Viewport1」の子としてインスタンス化します。これでシーンを実行すると、左ビューポート内に世界が表示されます。

また、「ビューポート2」に世界を追加が必要ですが、同じ世界を使用させたい場合はどうすればよいでしょうか。
これはコードで処理できます。メインオブジェクトにスクリプトをアタッチし、以下を追加してください。

{{< highlight gdscript>}}
extends Node

@onready var viewport1 = $Viewports/ViewportContainer1/Viewport1
@onready var viewport2 = $Viewports/ViewportContainer2/Viewport2
@onready var camera1 = $Viewports/ViewportContainer1/Viewport1/Camera2D
@onready var camera2 = $Viewports/ViewportContainer2/Viewport2/Camera2D
@onready var world = $Viewports/ViewportContainer1/Viewport1/World

func _ready():
    viewport2.world_2d = viewport1.world_2d
{{< /highlight >}}

The `onready` node references are for convenience - we'll be using them as we progress forward. Remember that when you type "`$`", Godot will automatically suggest node paths so you don't need to type them. You can also drag a node directly from the scene tree into the script editor, and you'll get the node's path.

現在シーンを実行すると、両方のビューポートでレンダリングされた世界が表示されます。ただし、どちらのカメラも移動していないため、表示されるのは世界のごく一部に過ぎません。

#### カメラのセットアップ方法

以下のスクリプトを各カメラに適用してください。

{{< highlight gdscript>}}
extends Camera2D

var target = null

func _physics_process(delta):
    if target:
        position = target.position
{{< /highlight >}}

現在、各カメラにターゲットを割り当て、そのノードの位置に従うように設定できます。
以下の「Main」スクリプトで実装します。

{{< highlight gdscript>}}
func _ready():
    viewport2.world_2d = viewport1.world_2d
    camera1.target = world.get_node("Player_1")
    camera2.target = world.get_node("Player_2")
{{< /highlight >}}

現在シーンを実行すると、各プレイヤーは自分のビューポートの中央に配置され、分割画面の設定が正しく機能しています！

{{% notice tip %}}
カメラの［ドラッグ余白］プロパティを無効にすると、見た目が一番良くなると思います。
{{% /notice %}}

### カメラの制限

次に、プレイヤーカメラがマップの表示範囲外にスクロールしないように制限を追加してください。この関数をメインスクリプトに追加し、`_ready()` で呼び出してください。

{{< highlight gdscript>}}
func set_camera_limits():
    var map_limits = world.get_used_rect()
    var map_cellsize = world.cell_size
    for cam in [camera1, camera2]:
        cam.limit_left = map_limits.position.x * map_cellsize.x
        cam.limit_right = map_limits.end.x * map_cellsize.x
        cam.limit_top = map_limits.position.y * map_cellsize.y
        cam.limit_bottom = map_limits.end.y * map_cellsize.y
{{< /highlight >}}

## ミニマップ

もう一つ便利な機能を追加してください。マップ全体を見渡せるミニマップです。プレイヤーが現在地を把握しやすくなります。

{
  "steps": [
    {
      "description": "新たに `ViewportContainer` 要素を作成が必要ですが、今回は `Main` の子要素として追加します。今回のケースでは**Stretchモードは使用しません**。以下の手順に従ってください。\
- {{< gd-icon Viewport >}}`Viewport`要素を追加し、_Size_プロパティを `(340, 200)` に設定します\
- 次に {{< gd-icon Camera2D >}}`Camera2D`要素を追加します。画面中央に配置するため、{{< gd-icon Viewport >}}`Camera2D`の _Position_ プロパティを `(512, 300)` に設定します\
- ズームアウトするには、_Zoom_プロパティを `(9, 9)` に設定してください。忘れずにこのカメラでも**Currentモードを選択**することをお忘れなく"
    }
  ]
}

`_ready()`関数内では、ミニマップが他の2つのビューポートと同じワールドを使用するように設定します。

{{< highlight gdscript>}}
$Minimap/Viewport.world_2d = viewport1.world_2d
{{< /highlight >}}

「レイアウト」メニューを使用してMinimapコンテナを「中央下部」に配置してください。実際に見てみてください。

![alt](/godot_recipes/3.x/img/splitscreen_minimap1.png?width=400)

エッジ周りのグレーゾーンを解消が必要です。正確なズームレベルを特定して希望のミニマップサイズに合わせることもできますが、代わりに{{< gd-icon Viewport >}}`Viewport`設定の_透過背景(Bg_をチェックします。これで非地図領域が見えなくなり、ミニマップがメインビューポートの上に直接浮かんで表示されるようになります。

![alt](/godot_recipes/3.x/img/splitscreen_minimap2.png?width=400)

### まとめ

ビューポートは非常に強力な機能ですが、同時に混乱を招く可能性もあります。効果的な管理方法として、ゲームロジックから完全に切り離し、表示専用として使用する方法が有効です。

