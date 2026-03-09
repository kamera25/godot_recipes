---
title: "Displaying debug data"
weight: 10
draft: true
ghcommentid: 59
---

## 問題文

デバッグデータを画面上に表示するための簡単な方法が必要です。

## 解決策

任意のノードがプロパティを登録でき、その値が適切な形式で表示されるオーバーレイを作成します。

以下に目指すべき例を示します：

<img src=\ alt=\>

まず最初に、名前を `DebugStats` とする `MarginContainer` を追加し、その中に `VBoxContainer` の子要素を配置します。マージンは適切な値に設定してください（私は通常 `20` を使用しています）。

コードを見てみましょう：

```gdscript
extends MarginContainer

class Property:
    var num_format = "%4.2f"
    var object  # The object being tracked.
    var property  # The property to display (NodePath).
    var label_ref  # A reference to the Label.
    var mode  # Display option (rounded, etc.)

    func _init(_object, _property, _label, _mode):
        object = _object
        property = _property
        label_ref = _label
        mode = _mode

    func update_label():
        # Sets the label's text.
        var s = object.name + "/" + property + " : "
        var p = object.get_indexed(property)
        match mode:
            "":
                s += str(p)
            "length":
                s += num_format % p.length()
            "round":
                match typeof(p):
                    TYPE_INT, TYPE_FLOAT:
                        s += num_format % p
                    TYPE_VECTOR2, TYPE_VECTOR3:
                        s += str(p.round())
        label_ref.text = s

var props = []  # An array of the tracked properties.

func _process(_delta):
    if not visible:
        return
    for prop in props:
        prop.update_label()
```

まず、追跡対象オブジェクトとプロパティのデータをカプセル化するカスタムクラスから始めましょう。このクラスのプロパティを分解します：

* `object` - This is a reference to the object we're tracking.
* `property` - This is in the form of a `NodePath`, meaning we can track something like `"position"`, but also `"position:x"`.
* `label_ref` - Each property is linked to a {{< gd-icon Label >}}`Label` node, this is a reference to the label so that we can set its `text`.
* `mode` - This is an optional setting to configure how the value should be displayed (see below).

```python
def update_label(self):
    # ラベルの text プロパティに表示する文字列を構築
    label_content = f\
    if self.mode == 'edit':
        label_content += \
    elif self.mode == 'view':
        label_content += \

    # 構築したコンテンツをラベルの text プロパティに設定
    self.widget.text = label_content
```

本例では、`mode` オプションの設定例として以下の2つのケースを示します：

* `"length"` - if the `property` is a vector, we'll display its length.
* `"round"` - if the property is a numeric type, we'll round its values.

Loading plamo-2-translate ⠙
Loading plamo-2-translate ⠹
Loading plamo-2-translate ⠸
Loading plamo-2-translate ⠼
Loading plamo-2-translate ⠴
Loading plamo-2-translate ⠦
Loading plamo-2-translate ⠧
Loading plamo-2-translate ⠇
Loading plamo-2-translate ⠏
Loading plamo-2-translate ⠋
Loading plamo-2-translate ⠙
Loading plamo-2-translate ⠹
Loading plamo-2-translate ⠸
Loading plamo-2-translate ⠼
Loading plamo-2-translate ⠴

```gdscript
func add_property(object, property, mode):
    var label = load("res://debug_overlay/debug_label.tscn").instantiate()
    $VBoxContainer.add_child(label)
    properties.append(Property.new(object, property, label, mode))

func remove_property(object, property):
    for prop in properties:
        if prop.object == object and prop.property == property:
            prop.label.queue_free()
            properties.erase(prop)
```

`add_property()` は任意のノードから呼び出すことができます（デバッグ表示機能はシングルトンとしてロードする必要があります - 後述参照）。

Note we're loading and instantiating a "debug_label" scene. This allows you to customize how you want the individual labels to appear - font, size, color, etc. Make a separate scene with a {{< gd-icon Label >}}`Label` node and configure it to your liking.

### ゲームへの追加について

To use it in game, you'll want the debug display to be rendered on top of your game, whether in 2D or 3D. Create one more scene called "DebugOverlay" and make its root node a {{< gd-icon CanvasLayer >}}`CanvasLayer`. Add the `DebugStats` scene as a child.

簡単に参照できるように、私はこれを `DebugOverlay` スクリプトに追加しています：

```gdscript
@onready var stats = $DebugStats
```

次に、［プロジェクト設定＞自動ロード］で `DebugOverlay` を追加してください。

現在では、ゲーム中の任意のノードで以下のようにプロパティを登録・削除できます：

```gdscript
DebugOverlay.stats.add_property(self, "velocity", "length")
DebugOverlay.stats.add_property(self, "transform:origin", "round")
```

このサイトの各種サンプルプロジェクトで、デバッグオーバーレイの動作を実際に確認できます。デバッグ描画レイヤーを追加する関連レシピもぜひご覧ください。

<!-- ## 関連レシピ

- [Drawing Vectors in 3D](/godot_recipes/3.x/3d/debug_overlay) -->