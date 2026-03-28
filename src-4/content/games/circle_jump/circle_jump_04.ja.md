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

{
  "title": "マージンコンテナの設定",
  "content": "「マージンコンテナ」を使用すると、UI要素が画面端に近づきすぎるのを防止できます。4つのカスタム定数プロパティをすべて'20'に設定してください。"
}

次に使用するのはメイン要素を整理するための`VBoxContainer`です。このコンテナの［カスタム定数／間隔］設定を`150`に設定してください。

「ラベル」ノードは画面のタイトルを表示します。［テキスト］フィールドに「タイトル」と入力し、円と同じフォントリソースを読み込みます。

最後に、「ボタン」という名前の `HBoxContainer` を追加します。このコンテナには、後でスクリーンに追加するボタンが格納されます。その _間隔_ を `75` に設定します。次にノードを複製して、もう1列分のボタンを作成します。

スクリーンは画面外に表示開始されるので、ルートノードの _オフセット値_ を `(500, 0)` に設定してください。その後、シーンにスクリプトを追加します。

```gdscript
extends CanvasLayer

@onready var tween = $Tween

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

これで3つの継承されたシーンを作成できます。それぞれについて：ルートノードに名前を付け、ラベルテキストを変更し、「Buttons」コンテナーに「TextureButton」を追加してください。各ボタンのノーマルテクスチャには、アセットフォルダ内の画像を使用してください。各ボタンにはその機能に応じた名前を付けてください（例：「再生」「設定」など）。そしてこれらをすべてグループ「buttons」に追加します。

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