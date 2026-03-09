---
title: "Minimap/radar"
weight: 12
draft: false
---

## 問題文

プレイヤーの視界外にあるオブジェクトの位置を表示するためのミニマップまたはレーダー風UI要素が欲しいとのことですね。

## 解決策

Here's an example of what we are going for:
<video controls src="/godot_recipes/4.x/img/minimap_01.webm"></video>

### プロジェクト設定

この機能を説明するため、まずは[オートタイルレシピ](/godot_recipes/4.x/2d/autotile_intro/)を使用した簡素なトップダウンゲームと[トップダウンキャラクター操作レシピ](godot_recipes/2d/topdown_movement/#option-2-rotate-and-move)に基づくプレイヤーから始めましょう。各コンポーネントの動作詳細については、リンク先のレシピを参照してください。

{{% notice note %}}
本プロジェクトのアートワークは[kenney.nl](https://kenney.nl)提供のものを使用しています。以下からダウンロード可能です：[Minimap アセット](/godot_recipes/4.x/files/minimap_assets.zip).
{{% /notice %}}

私たちのメインシーン設定は以下のように構成されています：

![alt](/godot_recipes/4.x/img/minimap_01.png)

```
`CanvasLayer` ノードは、ミニマップ／レーダーなどのUIコンポーネントを保持するために使用されます。このレシピで作成するこれらの要素を収容するためのものです。

### ユーザーインターフェース配置

まず最初に、ミニマップのレイアウトを作成する必要があります。ゲーム内に存在する他のUI要素と連携させるためには、スムーズなリサイズが可能で、コンテナベースのレイアウトに適切に統合できるものでなければなりません。

Add a {{< gd-icon MarginContainer >}}`MarginContainer` first. Set its **Theme Overrides/Constants** all to `5`. This control will hold the rest of the nodes and ensure it doesn't bleed over into any other elements. Name it "Minimap" and save the scene.

次に、このプロジェクトに {{< gd-icon NinePatchRect >}}`NinePatchRect`ノードを追加します。このノードは `TextureRect`と似ていますが、角や端を引き伸ばさずにリサイズする点が異なります。アセットフォルダから **[テクスチャ]** プロパティに `panel_woodDetail_blank.png` 画像をドラッグ＆ドロップしてください。この画像は `128x128`ピクセルのもので、ルート {{< gd-icon MarginContainer >}}`MarginContainer`ノードを拡大すると、画像が伸びすぎて見栄えが悪くなります：

![alt](/godot_recipes/4.x/img/minimap_02.gif)

Using the {{< gd-icon NinePatchRect >}}`NinePatchRects`'s properties, we can ensure that the frame remains the same size when stretched. You can define these properties graphically in the "TextureRegion" panel, but it's sometimes easier to enter the values directly. Set all four properties in the **Patch Margin** section to `64` and change the node's name to "Frame".

サイズを変更するとどうなるか、次に見てみましょう：

![alt](/godot_recipes/4.x/img/minimap_03.gif)

次に、フレームの内側部分をグリッドパターン「pattern_blueprintPaper.png」で埋めたいと思います：

<img src=\ alt=\
>

ただし、フレームのサイズがどうあれ自動でタイル表示されるようにする必要があります。また、グリッドエリアはミニマップマーカーが表示される場所なので、枠線を超えて拡張しないようにしなければなりません。

As a child of the `MiniMap` (and a sibling of the `Frame`), add another {{< gd-icon MarginContainer >}}`MarginContainer`. Set all four margin properties in **Theme Overrides/Constants** to `20`. As a child of this node, add a {{< gd-icon TextureRect >}}`TextureRect` and assign its **Texture** to the above image. Set its **Stretch Mode** to "Tile". Name this node "Grid".

ルートノードのサイズを変更して効果を確認してください：

![alt](/godot_recipes/4.x/img/minimap_04.gif)

```
まずはミニマップのサイズを `(200, 200)` のままにしておきましょう。ルートノードの **[Size]** プロパティは [レイアウト] セクションで確認できます。

この時点までに、シーンツリーは以下のようになっているはずです：

!

### マップマーカー

As a child of `Grid`, add a {{< gd-icon Sprite2D >}}`Sprite2D` node named "PlayerMarker" and give it the `minimapIcon_arrowA.png` texture. Note the sprite's **Transform/Position** property: `(0, 0)`, which places it exactly in the top-left corner of the `Grid`:

![alt](/godot_recipes/4.x/img/minimap_05.png)

```
もし現在のグリッドサイズが (150, 150) であれば（これは［サイズ］プロパティで確認できます）、中心座標は (75, 75) になります。ここにプレイヤーマーカーの位置を設定して：

!

心配しないでください。後で自動化します。

Add two more {{< gd-icon Sprite2D >}}`Sprite2D` nodes: "MobMarker" and "AlertMarker", using the `minimapIcon_jewelRed.png` and `minimapIcon_exclamationYellow.png` textures.

![alt](/godot_recipes/4.x/img/minimap_08.png)

These will represent two different types of objects in the game world. Click the "Toggle Visibility" button next to each so that they won't appear by default.

### マップマーカーのスクリプト設定

ここでいくつかの重要な判断が求められます。ミニマップに世界オブジェクトを配置する方法は、ゲームの設計方針に大きく依存します。このプロジェクトは非常に簡素なデモ版のため、プロセスはシンプルに保ちましょう。より大規模なゲームでは、より堅牢なアプローチが必要になる場合があります。

本デモで使用するゲームオブジェクトは2種類です：ランダムにマップを徘徊する「モブ」と、プレイヤーが持ち上げ可能な「木箱」です。これらのオブジェクトの多くがメインシーン内に散らばっています。それぞれを適切に表示するために、先ほど作成したマップマーカーのいずれかを使用する必要があります。

Add each item that you want to appear on the minimap to a group named "minimap_objects". In each object's script, assign it a `minimap_icon` property:

```gdscript
# In the mob's script:
var minimap_icon = "mob"

# In the crate's script:
var minimap_icon = "alert"
```

Now we can begin adding a script to the `Minimap`. First, a `player` reference that can be assigned in the Inspector when the minimap is added to the main scene and a `zoom` property to calibrate the scale - how far the minimap can "see". We also have some `@onready` variables to make it more convenient to access the nodes we need.

```gdscript
extends MarginContainer
class_name Minimap

@export var player: Player
@export var zoom = 1.5

@onready var grid = $MarginContainer/Grid
@onready var player_marker = $MarginContainer/Grid/PlayerMarker
@onready var mob_marker = $MarginContainer/Grid/MobMarker
@onready var alert_marker = $MarginContainer/Grid/AlertMarker
```

次は、辞書を使ってユニットに割り当てた 'minimap_icon' タグを対応するマーカーにマッピングします：

```gdscript
@onready var icons = {
    "mob": mob_marker,
    "alert": alert_marker
}
```

次に、マップサイズとワールドサイズの比率を計算して保持する変数が必要です。各オブジェクトにアクティブマーカーを割り当てるため、別の辞書を使用します。キーは対象オブジェクト（例：`Mob` または `Crate` インスタンス）、値は割り当てられたマーカーになります。

```gdscript
var grid_scale
var markers = {}
```

```python
def _ready():
    # グリッドの中央にプレイヤーマーカーを中央配置し、スケール係数を計算する
    pass  # (注：動的サイズUIの場合は、'resized'シグナルに接続し、この処理をすべてコールバック内で実装する必要があります)
```

```gdscript
func _ready():
    await get_tree().process_frame
    player_marker.position = grid.size / 2
    grid_scale = grid.size / (get_viewport_rect().size * zoom)
```

{{% notice style="warning" title="Nodes in Containers" %}}
Due to the way that {{< gd-icon Container >}}`Container` nodes handle their children, at `_ready()` time you won't get the correct value for the child's size. For this reason, we need to wait until the next frame to get the Grid's size.
{{% /notice %}}

We'll also create markers for every game object (using the "minimap_objects" group) by duplicating the matching marker node and tying the marker to the object via the `markers` dictionary:

```gdscript
    var map_objects = get_tree().get_nodes_in_group("minimap_objects")
    for item in map_objects:
        var new_marker = icons[item.minimap_icon].duplicate()
        grid.add_child(new_marker)
        new_marker.show()
        markers[item] = new_marker
```

マーカーを作成し、それぞれのオブジェクトにリンクさせた今、`_process()` 内でその位置を更新できます。もしどの `player` も割り当てられていない場合は、何も行いません：

```gdscript
func _process(delta):
    if !player:
        return
```

如果存在玩家，首先我们会根据玩家的方向旋转玩家标记。由于我们的 PlayerMarker 图灵向上方而不是沿 x 轴指向，因此需要增加 90 度：

```gdscript
player_marker.rotation = player.rotation + PI/2
```

次に、各オブジェクトの位置をプレイヤー座標系で計算し、それを基にマーカーの位置を求めます（制御原点が左上にあるため、オフセットとして `grid.size / 2` を考慮することを忘れないようにしてください）。

```gdscript
for item in markers:
    var obj_pos = (item.position - player.position) * grid_scale + grid.size / 2
    markers[item].position = obj_pos
```

この問題は、マーカーがグリッドの外側にも配置できてしまう点にあります：

<img src=\ alt=\>

この問題を解決するには、`obj_pos` を計算した後、マーカーの位置を設定する前に、その値をグリッドの矩形範囲にクリップしてください：

```gdscript
obj_pos = obj_pos.clamp(Vector2.ZERO, grid.size)
```

![alt](/godot_recipes/4.x/img/minimap_11.png)

We can also decide what to do about markers that are "off-screen" - when they would be outside the grid's rectangle. Choose one of the following options (do this also before using `clamp()`). The first option is to hide them:

```gdscript
if grid.get_rect().has_point(obj_pos + grid.position):
    markers[item].show()
else:
    markers[item].hide()
```

二点目は、視覚的な表現を変更する方法です。この場合、サイズを小さくすることで被写体がより遠くにあることを示唆します：

```gdscript
if grid.get_rect().has_point(obj_pos + grid.position):
    markers[item].scale = Vector2(1, 1)
else:
    markers[item].scale = Vector2(0.75, 0.75)
```

<img src=\ alt=\>

### オブジェクトの削除方法

モブが倒されたり、木箱が拾われたりすると、マーカー参照が有効でなくなるためゲームがクラッシュしてしまいます。オブジェクトと一緒にマーカーも確実に削除されるようにする必要があります。以下に、簡易的なデモ環境でこれを実装する簡単な方法を紹介します：

Add `signal removed` to any object that you've put in the "minimap_objects" group. Emit this signal when the object is destroyed (or collected), along with a reference to itself so the map can identify it:

```gdscript
removed.emit(self)
```

メインスクリプトの`_ready()`関数内で、以下のシグナルをミニマップに接続してください：

```gdscript
func _ready():
    for object in get_tree().get_nodes_in_group("minimap_objects"):
        object.removed.connect(minimap._on_object_removed)
```

現在の処理：minimapスクリプトに受信機能を追加し、マーカーを解放して参照を削除します：

```gdscript
func _on_object_removed(object):
    if object in markers:
        markers[object].queue_free()
        markers.erase(object)
```

### ズームの調整方法

ここまでお読みいただいた方には、最後にもう一つの機能を追加します。この「調整可能なズームレベル」を使えば、地図の上にマウスカーソルを置いた状態でホイールを回すことで、表示の拡大・縮小が可能になります。

まず、`zoom`プロパティにセッターを追加します：

```gdscript
@export var zoom = 1.5:
    set = set_zoom

func set_zoom(value):
    zoom = clamp(value, 0.5, 5)
    grid_scale = grid.size / (get_viewport_rect().size * zoom)
```

ノード「MiniMap」で、インスペクター内の信号 `_gui_input` を接続して、スクロールホイールイベントを処理できるようにします：

```gdscript
func _on_gui_input(event):
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_WHEEL_UP:
            zoom += 0.1
        if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
            zoom -= 0.1
```

これで完了です。スクロールインとアウトの効果を確認してみましょう：

<img src=\ alt=\>

## まとめ

このレシピはかなり規模が大きいですが、現在取り組んでいるプロジェクトにも柔軟に組み込めるよう配慮しています。

追加すると役立つかもしれない項目：

* 各種ゲームオブジェクトに対応したより多様なマーカータイプを追加
* ユニットが生成されるタイミングで新規ユニットを追加する機能（ヒント：ユニット削除時と同様にシグナルを使用）
* マーカーをクリックするとその詳細情報が表示されるように改良
* グリッドの代わりにマップ画像をそのままミニマップ背景として使用可能に

## <i class="fas fa-code-branch"></i> Download This Project

以下からプロジェクトのサンプルコードをダウンロードできます：[https://github.com/godotrecipes/minimap](https://github.com/godotrecipes/minimap)

## 関連レシピ

- [トップダウン方式キャラクター移動](/godot_recipes/4.x/2d/topdown_movement/)

<!-- #### この動画が気に入ったら？

{{< youtube -R1rasEyuqY >}} -->