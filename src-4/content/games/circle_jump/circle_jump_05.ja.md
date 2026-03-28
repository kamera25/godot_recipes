---
title: "スコアとHUD"
weight: 5
draft: false
pre: "05. "
---

最終部分では、ゲームの開始と設定を行うためのメニュー形式のUIを実装しました。また、スコアなどのゲーム内情報を表示するためのUIも必要です。

## HUDシーン

HUDとして使用する`CanvasLayer`をルートとする新しいシーンを追加します。以下の2つの子要素を持たせます。「スコアボックス」という名前の`MarginContainer`と、「メッセージ」という名前の`Label`です。

Scene treeは以下のようになっている必要があります。

![alt](/godot_recipes/3.x/img/cj_05_01.png)

Set the layout of the `ScoreBox` to "Bottom Wide" and the _Custom Constants_ all to `20`. Add an `HBoxContainer` child and under that two `Label` nodes. Name the second label "Score" and put `100` in its _Text_ property. Set the `HBoxContainer`'s _Alignment_ to "End".

Add the same `DynamicFont` resource to both labels, but choose "Make Unique" on the first label and set its size to `32`. Set its _Text_ property to "Score". In its _Size Flags/Vertical, set "Fill". Your layout should look like this:

![alt](/godot_recipes/3.x/img/cj_05_02.png)

Now for the `Message` node load the font and set _Text_ to "Message" so we'll have something to see. Also choose "Make Unique" on the font resource (you'll see why in the next section). Set _Align_ and _Valign_ to "Center" and _Clip Text_ to "On". For layout, choose "Center Wide". Also, set _Grow Direction/Vertical_ to "Both".

## メッセージアニメーション

このゲーム中に表示されるメッセージです（レベルアップ時の通知やボーナス表示など）。アニメーション付きで表示させ、フェードアウト効果を加えたいと思います。シーンに `アニメーションPlayer` を追加してください。

以下の2つのアニメーションを作成します。初期値を設定するものと、メッセージ表示をアニメーションさせるものです。まず最初のアニメーション「init」を追加し、「ページ読み込み時に自動再生」ボタンをクリックします。持続時間は`0.1`に設定してください。

Add a keyframe at time `0` for the _Font/Size_ (`64`), and one for the _Visible_
set to "Off".

Add the second animation, "show_message". Set its length to `0.75` and keyframe _Visibility_ to "On".

Next, we'll keyframe the _Font/Size_ from `64` at time `0` and `200` at the end. Set the track's _Update Mode_ to "Continuous".

We also want it to fade out as it grows, so keyframe the _Modulate_ alpha value from `255` to `0`.

以下にアニメーション設定の例を示します。

![alt](/godot_recipes/3.x/img/cj_05_03.png)

アニメーション再生時の挙動：

![alt](/godot_recipes/3.x/img/cj_05_04.gif)

## HUDスクリプト

次に、ディスプレイを更新するためのメソッドを含むスクリプトをシーンに追加しましょう。

```gdscript
extends CanvasLayer

func show_message(text):
    $Message.text = text
    $AnimationPlayer.play("show_message")

func hide():
    $ScoreBox.hide()

func show():
    $ScoreBox.show()

func update_score(value):
    $ScoreBox/HBoxContainer/Score.text = str(value)
```

メインシーンにHUDインスタンスを作成し、`_ready()`関数と`_on_Jumper_died()`関数内に`$HUD.hide()`を追加します。`new_game()`関数では、HUDを表示してメッセージを表示します。以下のように実装します。

```gdscript
$HUD.show()
$HUD.show_message("Go!")
```

スコアを追加するには、`new_game()` 関数内で `score` 変数を作成し、初期値として 0 を設定してください。`_on_Jumper_captured()` 関数内では、この変数の値を 1 ずつ加算します。それぞれの処理後に `$HUD.update_score(score)` を呼び出すことを忘れないでください。

次のパートでは、ゲームにサウンドと色を追加していきます！

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube Fz2ltnvI4MQ >}}
