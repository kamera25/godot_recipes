---
title: "リングコマンド"
weight: 13
draft: false
---

## 課題

オプションを選択するため、「リングコマンド」を実装したい。

## 解決策

放射型メニューは様々なゲームで使用されており、複数のボタンを選択するためのインターフェースとして機能します。例えば、ゲーム内のNPCをクリックすると、会話・調査・攻撃など、取るべき行動を選択できるようになります。

メニューの具体的なデザインは、ゲーム全体の美的感覚と調和させる必要があります。このデモでは、主にメニュー機能の実装に焦点を当て、スタイリングについてはユーザー側で自由に選択できるようにしましょう。

以下にノードの設定を示します。

![alt](/godot_recipes/4.x/img/ui_radial_menu_01_4.png)



ルートノードとして `{{< gd-icon TextureButton >}}TextureButton` を使用しています。これがメニューの開閉に使用するボタンです。

`Buttons` {{< gd-icon Control >}}`Control`ノードは、必要に応じて任意の数のアイテムを配置できるコンテナとして機能します。このコントロールの**マウス/フィルター**プロパティを "Ignore" に設定することを忘れないでください。これによりマウスクリックが誤って捕捉されるのを防ぎます。

本例では、[クールタイムボタンレシピ](/godot_recipes/4.x/ja/ui/cooldown_button/) から9つのボタンを使用しています。

それでは、ボタンのスクリプトを見てみましょう。

```gdscript
extends TextureButton
class_name RadialMenuButton

@export var radius = 120
@export var speed = 0.25

var num
var active = false
```

以下が変数の定義です。`radius`はメニューの「大きさ」を表します - 円の直径です。`speed`はアニメーション用で、数値が小さいほど動作が速くなります。

`num` はボタンの総数を追跡し、`active` はメニューが開いているか閉じているかを示すフラグとして機能します。

```gdscript
func _ready():
    $Buttons.hide()
    num = $Buttons.get_child_count()
    for b in $Buttons.get_children():
        b.position = position
```

`_ready()`では、メニューボタンをデフォルトで非表示にし、その位置をメインボタンに設定することから始めます。

メインボタンの`pressed`シグナルを接続します。

```gdscript
func _on_pressed():
    disabled = true
    if active:
        hide_menu()
    else:
        show_menu()
```

このボタンをクリックするとメニューの表示／非表示が切り替わります。また、このボタンを一時的に無効化してください。そうしないと、Tween実行中にもう一度クリックすると、Tweenが最初から再生され直してしまいます。

```gdscript
func _on_tween_finished():
    disabled = false
    if not active:
        $Buttons.hide()
```

Tweenアニメーションが完了したら、アクティブ状態を切り替え、ボタンを再有効化します。

以下の`show_menu()`関数を見てみましょう。

```gdscript
func show_menu():
    $Buttons.show()
    var spacing = TAU / num
    active = true
    var tw = create_tween().set_parallel()
    tw.finished.connect(_on_tween_finished)
    for b in $Buttons.get_children():
        # Subtract PI/2 to align the first button  to the top
        var a = spacing * b.get_position_in_parent() - PI / 2
        var dest = Vector2(radius, 0).rotated(a)
        tw.tween_property(b, "position", dest, speed).from(Vector2.ZERO).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
        tw.tween_property(b, "scale", Vector2.ONE, speed).from(Vector2(0.5, 0.5)).set_trans(Tween.TRANS_LINEAR)
```

この関数では、各アイテム間に必要な角度（`spacing`）を計算します。その後、ボタンごとにループし、この角度と選択した`radius`に基づいて目的地座標（`dest`）を求めます。それぞれのボタンに対して、2つのプロパティである`position`と`scale`をTween処理することで、希望する効果を実現します。

`hide_menu()` はその正反対の機能を果たします。

```gdscript
func hide_menu():
    active = false
    var tw = create_tween().set_parallel()
    tw.finished.connect(_on_tween_finished)
    for b in $Buttons.get_children():
        tw.tween_property(b, "position", Vector2.ZERO, speed).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_IN)
        tw.tween_property(b, "scale", Vector2(0.5, 0.5), speed).set_trans(Tween.TRANS_LINEAR)
```

結果、こうなりました。

![alt](/godot_recipes/4.x/img/ui_radial_menu_02.gif)

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらでダウンロードできます。[https://github.com/godotrecipes/ui_radial_menu](https://github.com/godotrecipes/ui_radial_menu)

## 関連レシピ

* [UI：クールタイムボタン](/godot_recipes/4.x/ja/ui/cooldown_button/)