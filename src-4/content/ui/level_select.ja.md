---
title: "Level Select Menu"
weight: 12
draft: false
---

## 問題文

Your game needs a "level select" menu, where the user can choose from a grid of options.

[画像: alt=\ /path/to/image/level_select_03.gif]


## 解決策

As shown in the example above, we'll make a scrolling grid of level "boxes" that the player can choose from. Let's start with the individual level boxes:

### 1: レベルボックス

以下にノードの設定を示します：

```
LevelBox: {{< gd-icon PanelContainer >}} PanelContainer
    {{< gd-icon Label >}} Label
    {{< gd-icon MarginContainer >}} MarginContainer
        {{< gd-icon TextureRect >}} TextureRect
```

{{< gd-icon TextureRect >}} テクスチャレクトはロックアイコンの表示用、{{< gd-icon Label >}} ラベルはレベル番号の表示用に使用されます。一方が表示されている間は、もう一方は非表示になります。

ご自由にスタイルを設定できます。例として：

!

インスペクターで `LevelBox` の**カスタム最小サイズ**を必ず設定してください。ここでは例として `(110, 110)` を使用していますが、実際のレイアウト要件に応じて調整が必要です。

次に、スクリプトを追加し、`gui_input`シグナルに接続してください。

```gdscript
@tool
extends PanelContainer

signal level_selected

@export var locked = true:
    set = set_locked
@export var level_num = 1:
    set = set_level

@onready var lock = $MarginContainer/Lock
@onready var label = $Label

func set_locked(value):
    locked = value
    if not is_inside_tree():
        await ready
    lock.visible = value
    label.visible = not value

func set_level(value):
    level_num = value
    if not is_inside_tree():
        await ready
    label.text = str(level_num)


func _on_gui_input(event):
    if locked:
        return
    if event is InputEventMouseButton and event.pressed:
        level_selected.emit(level_num)
        print("Clicked level ", level_num)
```

```
ここで `@tool` を使用しているのは、インスペクターでプロパティを変更した場合、その変更が即座に反映されるようにするためです。シーンを実行しなくても変化を確認できます。ぜひお試しください。**［ロック］** プロパティをクリックして、ロック表示が出たり消えたりするのを確認してください。

本プロジェクトでは実際のレベルを読み込む必要がないため、`print()` 文を使用してクリックが検出されているかをテストできます。

### 2: グリッド表示

```
```
ボックスシーンが完成したら、次に `{{< gd-icon GridContainer >}}`GridContainer` を使用して新規シーンを追加します。その上に任意の数の `LevelBox` インスタンスを配置し、**列数** 値を必ず設定してください。以下は6列に設定した例です：

![alt](/godot_recipes/4.x/img/level_select_02.png)

この例では、**テーマオーバーライド / 定数 / H分離幅**と**V分離幅** がどちらも`10`に設定されています。

このシーンを「LevelGrid」として保存します。メニューでは、複数のインスタンスを使用して希望するレベル数を表示します。

### 3: メニュー画面

これで最終的なメニューを作成できます。

以下が基本レイアウトの概要です：

![alt](/godot_recipes/4.x/img/level_select_04.png)

以下のノードを使用して作成します：

```
LevelMenu:{{< gd-icon MarginContainer >}} MarginContainer
    {{< gd-icon VBoxContainer >}} VBoxContainer
        Title: {{< gd-icon Label >}} Label
        {{< gd-icon HBoxContainer >}} HBoxContainer
            BackButton: {{< gd-icon TextureButton >}} TextureButton
            ClipControl: {{< gd-icon Control >}} Control
            NextButton: {{< gd-icon TextureButton >}} TextureButton
```

ノードプロパティを調整：

* {{< gd-icon MarginContainer >}}`レベルメニュー`
    * **テーマオーバーライド/定数/マージン**: `20`
* {{< gd-icon VBoxContainer >}} `VBoxコンテナ`
    * **テーマオーバーライド/定数/間隔**: `50`
* {{< gd-icon Label >}} `タイトル`
    * フォントスタイルはお好みでカスタマイズ可能
* {{< gd-icon TextureButton >}} `戻るボタン` / `次へボタン`
    * **テクスチャサイズの無視**: `有効化`
    * **伸縮モード**: `中央固定`
    * **レイアウト/コンテナサイズ指定/水平方向/拡張**: `有効化`
* {{< gd-icon Control >}} `クリップコントロール`
    * **レイアウト/内容クリッピング**: `有効化`
    * **レイアウト/カスタム最小サイズ**: `(710, 350)` (`レベルグリッド`のサイズに相当)

```
ノード「ClipControl」内にグリッドが配置されます。**コンテンツを切り取る** を有効にすると、コントロール領域を超える内容は自動的に切り取られます。これにより、水平スクロール可能なグリッドセットを作成できるようになります。「ClipControl」に{{< gd-icon HBoxContainer >}} `HBoxContainer` 要素を「GridBox」という名前で追加し、その内部にインスタンス3個以上の `LevelGrid`を配置してください。

必ず**テーマのオーバーライド／定数／区切り文字**を `0` に設定してください。

レイアウトはこの例と同様に設定してください（動作を分かりやすくするため、**コンテンツの切り取り機能**は無効にしています）：

![alt](/godot_recipes/4.x/img/level_select_05.png)

「クリップコンテンツ」を有効にすると、3つのグリッドはすべて表示されますが、`ClipControl`では1つずつしか表示されないようになっています。

さて、メニューをスクロールするには、`グリッドボックス` を左右に `710` ピクセル分シフトさせる必要があります。

```
110 (width of each LevelBox)
    * 6 (grid columns)
    + 10 (grid spacing) * 5
    == 710
```

```
{{% notice info %}}
「なぜこの場面で{{< gd-icon ScrollContainer >}} `ScrollContainer`を使わないのか」と疑問に思われるかもしれません。もちろん、使用することは可能ですが、私たちは連続スクロールを望んでいませんし、スクロールバーが表示されることも避けたいからです。
{{% /notice %}}

スクリプトを `LevelMenu` に追加し、2つのボタンの `pressed` 信号を接続してください。

```gdscript
extends MarginContainer

var num_grids = 1
var current_grid = 1
var grid_width = 710

@onready var gridbox = $VBoxContainer/HBoxContainer/ClipControl/GridBox

func _ready():
    # Number all the level boxes and unlock them
    # Replace with your game's level/unlocks/etc.
    # You can also connect the "level_selected" signals here
    num_grids = gridbox.get_child_count()
    for grid in gridbox.get_children():
        for box in grid.get_children():
            var num = box.get_position_in_parent() + 1 + 18 * grid.get_position_in_parent()
            box.level_num = num
            box.locked = false

func _on_BackButton_pressed():
    if current_grid > 1:
        current_grid -= 1
        gridbox.rect_position.x += grid_width

func _on_NextButton_pressed():
    if current_grid < num_grids:
        current_grid += 1
        gridbox.rect_position.x -= grid_width
```

When you run the scene, try clicking the "Next" and "Back" buttons and verify that it's scrolling as expected. Clicking the individual level boxes should print to the console.

ダウンロード可能なサンプルプロジェクトでは、スクロールアニメーション用のトゥイーン機能を含む完全な実装例を確認できます（トゥイーンを使えば、あらゆる動作がより洗練されたものになります）。

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらからダウンロードできます：[https://github.com/godotrecipes/ui_level_select](https://github.com/godotrecipes/ui_level_select)

<!-- ## 関連レシピ

- [Containers](/godot_recipes/3.x/ui/containers/)
- [Know Your Nodes: Label](/godot_recipes/3.x/kyn/label/) -->

<!-- #### この動画が気に入ったら？

{{< youtube C-Sn55e5wnk >}} -->