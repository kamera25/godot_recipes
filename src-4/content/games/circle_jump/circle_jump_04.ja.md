---
title: "メニュー"
weight: 4
draft: false
pre: "04. "
---

基本ゲームプレイが完成したので、次はUIの実装に取り掛かります。タイトル画面、設定画面、そしてゲームオーバー時用のメニュー画面が必要になります。

## メニュー画面

3つの画面は共通のレイアウトと一部機能を共有するため、まずは全てがこのシーンを継承できる基本シーンから始めましょう。新しいシーンでは、まず `CanvasLayer` を作成し、名前を `BaseScreen` とします。作成したこのシーンは「UI」フォルダに保存してください。

* `CanvasLayer` ("BaseScreen"レイヤー)
  * `MarginContainer`
    * `VBoxContainer`
      * `Label`
      * `HBoxContainer` ("ボタン領域")
  * `Tween`コンポーネント

The `MarginContainer` will ensure that none of our UI elements get too close to the edge of the screen. Set all four of its _Custom Constants_ properties to `20`.

Next is a `VBoxContainer` to organize the main elements. Set its _Custom Constants/Separation_ to `150`.

The `Label` node displays the screen's title. Put "Title" in its _Text_ field and load the same font resource we used for the circles.

Finally, add an `HBoxContainer` named "Buttons" which will hold the buttons we add to the screens. Set its _Separation_ to `75`. Then duplicate the node so that we have another row of buttons.

The screen should start offscreen, so set the _Offset_ on the root node to `(500, 0)`. Then add a script to the scene:

```gdscript
extends CanvasLayer

onready var tween = $Tween

func appear():
    tween.interpolate_property(self, "offset:x", 500, 0,
                    0.5, Tween.TRANS_BACK, Tween.EASE_IN_OUT)
    tween.start()

func disappear():
    tween.interpolate_property(self, "offset:x", 0, 500,
                    0.4, Tween.TRANS_BACK, Tween.EASE_IN_OUT)
    tween.start()
```

このスクリプトでは、画面の表示／非表示を切り替えるためのアニメーション設定を行います。

Now we can make our three inherited scenes. For each, name the root node, change the Label text, and add `TextureButton`s to the "Buttons" containers. Use the images from the assets folder for each button's _Normal_ texture. Name each button for its function ("Play", "Settings", etc.) and add it to the group "buttons".

以下は、指定されたボタン名を使用した3つのシーンの外観例です：

![alt](/godot_recipes/3.x/img/cj_04_01.png)

さらに「スクリーン」という名前のルートノードを持つシーンを1つ作成し、その中に3つの画面インスタンスを追加してください。以下のスクリプトを追加すると、シーン遷移と状態管理を処理できます。

```gdscript
extends Node

signal start_game

var current_screen = null

func _ready():
    register_buttons()
    change_screen($TitleScreen)

func register_buttons():
    var buttons = get_tree().get_nodes_in_group("buttons")
    for button in buttons:
        button.connect("pressed", self, "_on_button_pressed", [button.name])

func _on_button_pressed(name):
    match name:
        "Home":
            change_screen($TitleScreen)
        "Play":
            change_screen(null)
            yield(get_tree().create_timer(0.5), "timeout")
            emit_signal("start_game")
        "Settings":
            change_screen($SettingsScreen)

func change_screen(new_screen):
    if current_screen:
        current_screen.disappear()
        yield(current_screen.tween, "tween_completed")
    current_screen = new_screen
    if new_screen:
        current_screen.appear()
        yield(current_screen.tween, "tween_completed")

func game_over():
    change_screen($GameOverScreen)
```

このスクリプトでは、すべてのボタンを接続するために、`pressed`シグナルを結び付け、ボタンの名前をパラメータとして渡します。これにより、`_on_button_press()`メソッドがそれぞれのボタンに適切な動作を決定できるようになります。

`change_screen()`メソッドは、選択した画面への遷移を処理します。これには、画面に何も表示したくない場合の`null`オプションも含まれます。

以下のコマンドを実行して画面遷移をテストしてください。

![alt](/godot_recipes/3.x/img/cj_04_02.gif)

このシーンをメインシーンでインスタンス化し、`start_game`シグナルをメインスクリプト内の`new_game()`関数に接続してください。また、`new_game()`を`_ready()`から削除するのを忘れないでください。ゲームを実行してみると、正しく開始できるはずです。最後に行うべきことは、ゲームオーバー条件を設定することです。

ジャンパー設定で、`died` というシグナルを追加し、その可視性通知メソッド内でそのシグナルを発火させます。

以下のコードを `new_game()` 関数に追加してください。

```gdscript
player.connect("died", self, "_on_Jumper_died")
```

その後、この新しい機能を追加してください。これにより、プレイヤーが死亡した時にすべての円が除去されるようになります。

```gdscript
func _on_Jumper_died():
    get_tree().call_group("circles", "implode")
    $Screens.game_over()
```

メニュー画面はシンプルで装飾を省いたものになっていますが、機能的には問題ありません。次回は、スコアカウンターやゲーム内表示などのUI制作をさらに進めていきます。

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube tWWncIkfCWs >}}