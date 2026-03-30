---
title: "動く円"
weight: 7
draft: false
pre: "07. "
---

## バグ修正について

まず最初に取り組むべきは、メニューシステムの不具合修正です。「スタート」ボタンを押すと新しいゲームが開始されますが、画面が切り替わる途中で再びボタンを押せる状態になってしまいます。試しに「連打」してみてください。大変なことになりますよ！

この問題は、画面遷移中にボタンを無効化することで解決できます。すべてのボタンが「buttons」グループに属しているため、`call_group()` 関数を使えば簡単に実装できます。

以下に更新済みの `BaseScreen.gd` を示します。

```gdscript
extends CanvasLayer

@onready var tween = $Tween

func appear():
    get_tree().call_group("buttons", "set_disabled", false)
    tween.interpolate_property(self, "offset:x", 500, 0,
                        0.5, Tween.TRANS_BACK, Tween.EASE_IN_OUT)
    tween.start()

func disappear():
    get_tree().call_group("buttons", "set_disabled", true)
    tween.interpolate_property(self, "offset:x", 0, 500,
                        0.5, Tween.TRANS_BACK, Tween.EASE_IN_OUT)
    tween.start()
```

## スコアとレベルについて

スコアが上がるにつれ、ゲームの難易度も適切に上昇させる必要があります。つまり、得点を獲得した際には一定の閾値（`circles_per_level`）に達したかどうかを確認する必要が生じます。また、ジャンプで円に乗る以外にも、得点を獲得する手段が存在するかもしれません。これを管理しやすくするため、メインスクリプト内でスコア変数に`setget`メソッドを定義します。

```gdscript
var score = 0 setget set_score
var level = 0
```

また、`new_game()`関数でそのメソッドを使用するよう更新してください。

```gdscript
func new_game():
    self.score = 0
    level = 1
```

同じように`_on_Jumper_captured()`内のスコア変更処理も修正し、HUD更新ロジックを新規メソッド`set_score()`に移動させます：

```gdscript
func _on_Jumper_captured(object):
    $Camera2D.position = object.position
    object.capture(player)
    call_deferred("spawn_circle")
    self.score += 1

func set_score(value):
    score = value
    $HUD.update_score(score)
    if score > 0 and score % settings.circles_per_level == 0:
        level += 1
        $HUD.show_message("Level %s" % str(level))
```

このゲームを試してみると、5ポイントに達した時点で画面に「レベル2」のメッセージが表示されるはずです。

## 移動する円

レベルアップに伴う難易度上昇の仕組みとして、サークルの動きを変化させる方法を採用します。既に静的タイプと限定的移動可能なタイプという複数のサークル種類が存在していますが、これらはいずれも動的な動きを可能にするべき機能を備えているため、新たなタイプを追加するわけではありません。むしろ、これは任意のサークルに付与できるプロパティとして実装されます。

シーン「Circle」を開き、「Tween」ノードを「MoveTween」という名前で追加してください。これをサークルスクリプトの先頭に追加します。

```gdscript
@onready var move_tween = $MoveTween

var move_range = 100  # Distance the circle moves.
var move_speed = 1.0  # The circle's movement speed.
```

「move_range」が 0 の場合、動かない円が表示されます。ここでデフォルト値を 100 に設定しておくと、動作確認が簡単に行えます。

移動処理を管理するために、`MoveTween`を開始します。処理が完了したら、`tween_completed`シグナルを利用して逆方向に再始動させます。

これは移動を開始するコードです。`tween_completed`シグナルをこの関数に接続してください。

```gdscript
func set_tween(object=null, key=null):
    if move_range == 0:
        return
    move_range *= -1
    move_tween.interpolate_property(self, "position:x",
                position.x, position.x + move_range,
                move_speed, Tween.TRANS_QUAD, Tween.EASE_IN_OUT)
    move_tween.start()
```

最後に、`init()` 関数の末尾に `set_tween()` を追加し、実際に動作を確認してみます。

<video controls src="/godot_recipes/img/cj_07_01.webm"></video>

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube 8SOw_IvB2gE >}}
