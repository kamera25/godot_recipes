---
title: "ミニマップ／レーダー"
weight: 12
draft: false
---

## Problem

プレイヤーの視界外にあるオブジェクトの位置を表示するためのミニマップまたはレーダー風UI要素が欲しいとの。

## Solution

以下に、目指している実装例をご紹介します。
<video controls src="/godot_recipes/4.x/img/minimap_01.webm"></video>

### プロジェクト設定

この機能を説明するため、まずは[オートタイルレシピ](/godot_recipes/4.x/ja/2d/autotile_intro/)を使用した簡素な見下ろし型ゲームと[見下ろしキャラクター操作レシピ](godot_recipes/2d/topdown_movement/#option-2-rotate-and-move)に基づくプレイヤーから始めてください。各コンポーネントの動作詳細については、リンク先のレシピを参照してください。

{{% notice note %}}
本プロジェクトのアートワークは[kenney.nl](https://kenney.nl)提供のものを使用しています。以下からダウンロードできます。[Minimap アセット](/godot_recipes/4.x/ja/files/minimap_assets.zip).
{{% /notice %}}

メインシーン設定は以下のように構成されています。

![alt](/godot_recipes/4.x/img/minimap_01.png)

`CanvasLayer` ノードは、ミニマップ／レーダーなどのUIコンポーネントを保持するために使います。このレシピで作成するこれらの要素を収容するためのものです。

### ユーザーインターフェース配置

まず最初に、ミニマップのレイアウトを作成してください。ゲーム内に存在する他のUI要素と連携させるためには、スムーズなリサイズが可能で、コンテナベースのレイアウトに適切に統合できるものでなければなりません。

まず、{{< gd-icon MarginContainer >}}`MarginContainer`を追加します。次に、その［テーマ設定/定数］をすべて`5`に設定します。このコントロールは残りのノードを保持し、他の要素に影響を与えないようにする役割を果たします。名前は「ミニマップ」とし、シーンを保存してください。

次に、このプロジェクトに {{< gd-icon NinePatchRect >}}`NinePatchRect`ノードを追加します。このノードは `TextureRect`と似ていますが、角や端を引き伸ばさずにリサイズする点が異なります。アセットフォルダから **[テクスチャ]** プロパティに `panel_woodDetail_blank.png` 画像をドラッグ＆ドロップしてください。この画像は `128x128`ピクセルのもので、ルート {{< gd-icon MarginContainer >}}`MarginContainer`ノードを拡大すると、画像が伸びすぎて見栄えが悪くなります。

![alt](/godot_recipes/4.x/img/minimap_02.gif)

{{< gd-icon NinePatchRect >}}`NinePatchRects`のプロパティを使用することで、引き伸ばした場合もフレームサイズが一定に保たれます。これらのプロパティは「テクスチャ領域」パネルでグラフィカルに定義できますが、直接数値を入力する方が簡単な場合もあります。**パッチ余白** セクションにある4つのプロパティをすべて `64` に設定し、ノード名を "Frame" に変更してください。

サイズを変更するとどうなるか、次に見てみてください。

![alt](/godot_recipes/4.x/img/minimap_03.gif)

次に、フレームの内側部分をグリッドパターン「pattern_blueprintPaper.png」で埋めたいと思います。

![alt](/godot_recipes/4.x/img/pattern_blueprintPaper.png)

ただし、フレームのサイズがどうあれ自動でタイル表示されるようにする必要があります。また、グリッドエリアはミニマップマーカーが表示される場所なので、枠線を超えて拡張しないようにしなければなりません。

「MiniMap」の子要素（かつ「Frame」の兄弟要素）として、新たに {{< gd-icon MarginContainer >}}`MarginContainer` を追加します。**テーマオーバーライド/定数** で4つのマージンプロパティをすべて `20` に設定します。このノードの子要素として {{< gd-icon TextureRect >}}`TextureRect` を追加し、**テクスチャ** を上記の画像に割り当てます。**伸縮モード** は「タイル」に設定してください。このノードには「Grid」という名前を付けます。

ルートノードのサイズを変更して効果を確認してください。

![alt](/godot_recipes/4.x/img/minimap_04.gif)

まずはミニマップのサイズを `(200, 200)` のままにしておきます。ルートノードの **[Size]** プロパティは [レイアウト] セクションで確認できます。

この時点までに、シーンツリーは以下のようになっているはずです。

![alt](/godot_recipes/4.x/img/minimap_06.png)

### マップマーカー

`Grid`の子要素として、名前を「PlayerMarker」とする`Sprite2D`ノードを追加します。また、minimapIcon_arrowA.pngテクスチャを適用します。スプライトのTransform/Positionプロパティに注意してください：(0, 0)となっており、これによりグリッドの左上隅に正確に配置されます。

![alt](/godot_recipes/4.x/img/minimap_05.png)

もし現在のグリッドサイズが (150, 150) であれば（これは［サイズ］プロパティで確認できます）、中心座標は (75, 75) になります。ここにプレイヤーマーカーの位置を設定して：

![alt](/godot_recipes/4.x/img/minimap_07.png)

心配しないでください。後で自動化します。

以下の 2 つの {{< gd-icon Sprite2D >}}`Sprite2D`ノードを追加してください: "MobMarker" と "AlertMarker"。テクスチャには `minimapIcon_jewelRed.png` および `minimapIcon_exclamationYellow.png` を使用してください。

![alt](/godot_recipes/4.x/img/minimap_08.png)

これらのオブジェクトはゲーム内世界の異なる2種類のアイテムを表します。デフォルトでは表示されないよう、各アイテムの横にある「表示/非表示切り替え」ボタンをクリックしてください。

### マップマーカーのスクリプト設定

ここで重要な判断がいくつか求められます。ミニマップに世界オブジェクトを配置する方法は、ゲームの設計方針に大きく依存します。このプロジェクトは非常に簡素なデモ版のため、プロセスはシンプルに保ちます。より大規模なゲームでは、より堅牢なアプローチが必要になる場合があります。

本デモで使用するゲームオブジェクトは2種類です。ランダムにマップを徘徊する「モブ」と、プレイヤーが持ち上げ可能な「木箱」です。これらのオブジェクトの多くがメインシーン内に散らばっています。それぞれを適切に表示するために、先ほど作成したマップマーカーのいずれかを使用してください。

ミニマップ上に表示させたい各アイテムを「minimap_objects」というグループに追加してください。各オブジェクトのスクリプトにおいて、`minimap_icon`プロパティを適切に設定します。

```gdscript
# In the mob's script:
var minimap_icon = "mob"

# In the crate's script:
var minimap_icon = "alert"
```

これで`Minimap`にスクリプトを追加する準備が整いました。まず、メインシーンにミニマップが追加された時にインスペクターで割り当て可能なプレイヤー参照と、スケールを調整するズームプロパティを実装します。必要なノードへのアクセスを容易にするため、`@onready`変数も用意しました。

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

次は、Dictonaryを使ってユニットに割り当てた 'minimap_icon' タグを対応するマーカーにマッピングします。

```gdscript
@onready var icons = {
    "mob": mob_marker,
    "alert": alert_marker
}
```

次に、マップサイズとワールドサイズの比率を計算して保持する変数が必要となります。各オブジェクトにアクティブマーカーを割り当てるため、別のDictonaryを使用します。キーは対象オブジェクト（例：`Mob` または `Crate` インスタンス）、値は割り当てられたマーカーになります。

```gdscript
var grid_scale
var markers = {}
```

`_ready()`では、プレイヤーのマーカーをグリッドの中心に配置し、スケールファクターを計算します。（**注：** UIのサイズが動的に変わる場合は、`resized`シグナルを接続し、これらの処理をコールバック内で行う必要があります）。

```gdscript
func _ready():
    await get_tree().process_frame
    player_marker.position = grid.size / 2
    grid_scale = grid.size / (get_viewport_rect().size * zoom)
```

{{% notice style="warning" title="コンテナ内ノードについて" %}}
{{< gd-icon Container >}}`Container` ノードが子要素をどのように処理するかの特性上、`_ready()` の時点では子要素の正確なサイズ値が取得できません。このため、グリッドのサイズを正しく取得するには次のフレームまで待つ必要があります。
{{% /notice %}}

これで`Minimap`にスクリプトを追加し始めることができます。まず第一に、メインシーンにミニマップが追加された際にインスペクターで割り当て可能な`player`リファレンスと、スケールを調整するための`zoom`プロパティが必要となります。これにより、ミニマップが「視認」できる範囲を設定できます。また、必要なノードにより簡単にアクセスできるよう、`@onready`変数もいくつか追加しています。

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

もし`player`が存在する場合、まずプレイヤーマーカーを回転させてプレイヤーの向きに合わせます。私たちの `PlayerMarker` スプライトは `x` 軸に沿ってではなく上方を向いているため、90度を追加する必要があります。

```gdscript
player_marker.rotation = player.rotation + PI/2
```

次に、各オブジェクトの位置をプレイヤー座標系で計算し、それを基にマーカーの位置を求めます（制御原点が左上にあるため、オフセットとして `grid.size / 2` を考慮することを忘れないようにしてください）。

```gdscript
for item in markers:
    var obj_pos = (item.position - player.position) * grid_scale + grid.size / 2
    markers[item].position = obj_pos
```

この問題は、マーカーがグリッドの外側にも配置できてしまう点にあります。

![alt](/godot_recipes/4.x/img/minimap_09.png)

この問題を解決するには、`obj_pos` を計算した後、マーカーの位置を設定する前に、その値をグリッドの矩形範囲にクリップしてください。

```gdscript
obj_pos = obj_pos.clamp(Vector2.ZERO, grid.size)
```

![alt](/godot_recipes/4.x/img/minimap_11.png)

以下のオプションから1つ選択できます（`clamp()`を使用する前に設定してください）。最初の選択肢はマーカーを非表示にする方法です。

```gdscript
if grid.get_rect().has_point(obj_pos + grid.position):
    markers[item].show()
else:
    markers[item].hide()
```

二点目は、視覚的な表現を変更する方法です。この場合、サイズを小さくすることで被写体がより遠くにあることを示唆します。

```gdscript
if grid.get_rect().has_point(obj_pos + grid.position):
    markers[item].scale = Vector2(1, 1)
else:
    markers[item].scale = Vector2(0.75, 0.75)
```

![alt](/godot_recipes/4.x/img/minimap_12.png)

### オブジェクトの削除方法

モブが倒されたり、木箱が拾われたりすると、マーカー参照が有効でなくなるためゲームがクラッシュしてしまいます。オブジェクトと一緒にマーカーも確実に削除されるようにする必要があります。以下に、簡易的なデモ環境でこれを実装する簡単な方法を紹介します。

「minimap_objects」グループに追加したすべてのオブジェクトに `signal removed` を追加してください。このシグナルは、オブジェクトが破棄（または回収）される際に、マップがそのオブジェクトを識別できるように参照と共に発火させます。

```gdscript
removed.emit(self)
```

メインスクリプトの`_ready()`関数内で、以下のシグナルをミニマップに接続してください。

```gdscript
func _ready():
    for object in get_tree().get_nodes_in_group("minimap_objects"):
        object.removed.connect(minimap._on_object_removed)
```

現在の処理：minimapスクリプトに受信機能を追加し、マーカーを解放して参照を削除します。

```gdscript
func _on_object_removed(object):
    if object in markers:
        markers[object].queue_free()
        markers.erase(object)
```

### ズームの調整方法

ここまでお読みいただいた方には、最後にもう一つの機能を追加します。この「調整可能なズームレベル」を使えば、地図の上にマウスカーソルを置いた状態でホイールを回すことで、表示の拡大・縮小が可能になります。

まず、`zoom`プロパティにセッターを追加します。

```gdscript
@export var zoom = 1.5:
    set = set_zoom

func set_zoom(value):
    zoom = clamp(value, 0.5, 5)
    grid_scale = grid.size / (get_viewport_rect().size * zoom)
```

ノード「MiniMap」で、インスペクター内のシグナル `_gui_input` を接続して、スクロールホイールイベントを処理できるようにします。

```gdscript
func _on_gui_input(event):
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_WHEEL_UP:
            zoom += 0.1
        if event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
            zoom -= 0.1
```

これで完了です。スクロールインとアウトの効果を確認してみます。

![alt](/godot_recipes/4.x/img/minimap_10.gif)

## Wrapping up

このレシピはかなり規模が大きいですが、現在取り組んでいるプロジェクトにも柔軟に組み込めるよう配慮しています。

追加すると役立つかもしれない項目：

* 各種ゲームオブジェクトに対応したより多様なマーカータイプを追加
* ユニットが生成されるタイミングで新規ユニットを追加する機能（ヒント：ユニット削除時と同様にシグナルを使用）
* マーカーをクリックするとその詳細情報が表示されるように改良
* グリッドの代わりにマップ画像をそのままミニマップ背景として使用可能に

## <i class="fas fa-code-branch"></i> Download This Project

以下からプロジェクトのサンプルコードをダウンロードできます。[https://github.com/godotrecipes/minimap](https://github.com/godotrecipes/minimap)

## Related recipes

- [見下ろし方式キャラクター移動](/godot_recipes/4.x/ja/2d/topdown_movement/)

<!-- #### Like video?

{{< youtube -R1rasEyuqY >}} -->