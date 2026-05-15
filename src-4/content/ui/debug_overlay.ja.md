---
title: "デバッグデータを表示しています"
weight: 10
draft: true
ghcommentid: 59
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 今回のお題

デバッグデータを画面上に表示するための簡単な方法が必要となります。

## 作り方

任意のノードがプロパティを登録でき、その値が適切な形式で表示されるオーバーレイを作成します。

以下に目指すべき例を示します。

![alt](/godot_recipes/4.x/img/debug_stats_01.png)

まず最初に、名前を `DebugStats` とする {{< gd-icon MarginContainer >}}`MarginContainer` を追加し、その中に {{< gd-icon VBoxContainer >}}`VBoxContainer` の子要素を配置します。マージンは適切な値に設定しましょう（ここでは `20` を使用しています）。

コードを見てみてください。

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

まず、追跡対象オブジェクトとプロパティのデータをカプセル化するカスタムクラスから始めてください。このクラスのプロパティを分解します。

*  `object` - 追跡対象オブジェクトへの参照です。
　・ `property` - `NodePath`形式で指定し、例えば `"position"` だけでなく `"position:x"` のようなプロパティも追跡できます。
　・ `label_ref` - 各プロパティは対応する {{< gd-icon Label >}}`Label`ノードと紐付けられており、この参照によりラベルの `text`属性を設定できます。
　・ `mode` - 表示方法を指定するオプション設定です（詳細は後述）。

In the `update_label()` method we build up a string to display in the label's `text` property. We include the object's name and which property we're showing, plus the value modified by the `mode` option.

本例では、`mode` オプションの設定例として以下の2つのケースを示します。

* `"length"` - `property`がベクトルの場合、その長さを表示します。
* `"round"` - プロパティが数値型の場合、値を四捨五入します。

We then need functions to add/remove properties from the display:

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

`add_property()` は任意のノードから呼び出すことができます（デバッグ表示機能はシングルトンとしてロードが必要となります。後述参照）。

注意：現在「debug_label」シーンのロードとインスタンス化を行っています。これにより、個別のラベルの表示方法（フォント、サイズ、色など）を自由にカスタマイズできます。別途、{{< gd-icon Label >}}`Label`ノードを含むシーンを作成し、お好みの設定に調整します。

### ゲームへの追加について

ゲーム内でこの機能を使用するには、2D/3Dを問わず、デバッグ表示がゲーム画面の上に重ねて表示されるようが必要です。「DebugOverlay」というシーンをさらに1つ作成し、そのルートノードに{{< gd-icon CanvasLayer >}}`CanvasLayer`を設定します。次に、このScene内に`DebugStats`シーンを子要素として追加します。

簡単に参照できるように、これを `DebugOverlay` スクリプトに追加しています。

```gdscript
@onready var stats = $DebugStats
```

次に、［プロジェクト設定＞自動ロード］で `DebugOverlay` を追加します。

現在では、ゲーム中の任意のノードで以下のようにプロパティを登録・削除できます。

```gdscript
DebugOverlay.stats.add_property(self, "velocity", "length")
DebugOverlay.stats.add_property(self, "transform:origin", "round")
```

このサイトの各種サンプルプロジェクトで、デバッグオーバーレイの動作を実際に確認できます。デバッグ描画レイヤーを追加する関連レシピもぜひご覧ください。

## 関連レシピ

- [3D空間でのベクトル描画](/godot_recipes/4.x/ja/3d/debug_overlay) -->