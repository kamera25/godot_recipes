---
title: "ユーザーインターフェースとスコア"
weight: 9
draft: false
pre: "09. "
---

ゲームの最後の主要コンポーネントは *ユーザーインターフェース* (UI) です。プレイヤーにスコアやその他の情報を表示する方法が必要になります。これを実現するために、Godotが提供する各種 {{< gd-icon Control >}}`Control` ノードを使用します。これらはUI構築用に設計された専用ノードです。

## ユーザインタフェースシーン

シーンの開始には {{< gd-icon MarginContainer >}}`MarginContainer` を使用し、名前は `UI` としてください。

*コンテナノード* は{{< gd-icon Control >}}`Control`ノードの一種で、子要素のサイズや位置を制御するように設計されています。これを使用することで、手動で調整する手間をかけずにコントロールノードを簡単に配置・移動できます。{{< gd-icon MarginContainer >}}`MarginContainer`を使用すると、その子要素が端に近づきすぎるのを防ぐことができます。

**インスペクター**の**テーマオーバーライド/定数**セクションで、4つの**マージン**値をすべて `10` に設定します。その後、ビューポート上部のメニューバーで、アンカーを**トップワイド**プリセットに設定してください。

![alt](/godot_recipes/4.x/img/2d_101_21.png)

次に、{{< gd-icon HBoxContainer >}}`HBoxContainer` を追加します。このコンテナは子要素を水平方向に配置します。その上に、船のシールドレベルを表示する{{< gd-icon TextureProgressBar >}}`TextureProgressBar` を追加し、「`ShieldBar`」と名前を付けます。

申し訳ありませんが、進捗バーとして使用できる適切な画像がアートパックにありません（1つ存在はしますが、使い勝手の良いフォーマットではありません）。代わりに以下の2つの画像を使用します。1つは緑色のプログレスバー、もう1つは白い枠線です。これらをプロジェクトフォルダに保存してください。

![alt](/godot_recipes/4.x/img/bar_foreground.png?width=100)
![alt](/godot_recipes/4.x/img/bar_background.png?width=100)

テクスチャ設定セクションで、背景画像のドラッグ先を「Progress」に、前景画像のドロップ先を「Under」に指定します。まず気づくのは、デフォルトサイズが非常に小さいことです。最初にレイアウト設定で「カスタム最小サイズ」を `(80, 16)` に設定してください。オレンジ色の選択枠は大きくなりますが、画像は変わりません。これは単に画像を延ばすと見た目が悪くなるためです。代わりに、「ナインパッチストレッチ」チェックボックスを有効にし、4つの「伸縮マージン値」をすべて `3` に設定します。

これで長くて塗りつぶされていないバーが表示されているはずです。塗りつぶされた状態でどのように見えるかを確認するには、「Range」セクションの「Value」プロパティを `0` から `100` の間の任意の値に変更してください。

![alt](/godot_recipes/4.x/img/2d_101_22.png)

右側にはスコアを表示したいです。単に{{< gd-icon Label >}}`Label`ノードを使ってフォントを追加するだけでもできますが、それでは面白みがありません。アートパックには、代わりに使用できる美しいピクセル数字セットが含まれています。適切に表示するためには、少しコーディングして数値を切り出す必要があります。

## スコアカウンター

新しいシーンを開始し、{{< gd-icon HBoxContainer >}}`HBoxContainer`を追加します。「スコアカウンター」と名前を付け、**レイアウト設定**を**ワイド・トップ配置**に設定し、**整列方法**を「末尾」に設定してください。さらに、**テーマのオーバーライド/定数/分離幅**を `0` に設定します（プロパティ名の横にあるチェックボックスを必ず有効化してください）。

このコンテナでは、各数字を表示する {{< gd-icon TextureRect >}}`TextureRect`ノードの文字列を配置します。まずは1つ追加し、それを複製する方法から始めてください。

{{< gd-icon TextureRect >}}`TextureRect` `Digit0`という名前を付けます。**テクスチャ**セクションで「新規AtlasTexture」を選択し、ボックスをクリックして開きます。`Number_font (8 x 8).png`ファイルを**アトラス**プロパティにドラッグし、**領域**を `(32, 8, 8, 8)` に設定します。**伸縮モード**は「アスペクト比を維持（中心固定）」に設定してください。

「Digit0」ノードを選択し、「Ctrl + D」を7回押してノードの複製を作成します。この手順完了後に表示されるべき画面例を以下に示します。

![alt](/godot_recipes/4.x/img/2d_101_23.png)

問題が発生しました。{{< gd-icon TextureRect >}}`TextureRect` を8つの個別コピーに複製したにもかかわらず、すべてのインスタンスが同じ `AtlasTexture` を**テクスチャ**プロパティで共有しています。つまり、**領域**を変更して別の数字を表示しようとすると、すべての数字が同時に変わってしまうのです。

これはなぜかというと、`Resource`オブジェクト（例えば`Texture`）はメモリにロードされてから共有されるからです。実際には単一のテクスチャしか存在しないため、このアプローチは非常に効率的です - 同じ画像を何度も読み込んでメモリを浪費するのを防げます。ただし、特定のノードをユニークにする場合は明示的に指定します。

各ノードについて、`AtlasTexture` の隣にある下向き矢印をクリックし、「ユニーク化」を選択します。

![alt](/godot_recipes/4.x/img/make_unique.png)

これから、`ScoreCounter` にスクリプトを追加します。このスクリプトは、表示する必要のある数字に応じて適切な **リージョン** 値を選択します。

```gdscript
extends HBoxContainer

var digit_coords = {
    1: Vector2(0, 0),
    2: Vector2(8, 0),
    3: Vector2(16, 0),
    4: Vector2(24, 0),
    5: Vector2(32, 0),
    6: Vector2(0, 8),
    7: Vector2(8, 8),
    8: Vector2(16, 8),
    9: Vector2(24, 8),
    0: Vector2(32, 8)
}

func display_digits(n):
    var s = "%08d" % n
    for i in 8:
        get_child(i).texture.region = Rect2(digit_coords[int(s[i])],
                Vector2(8, 8))
```

まず、画像内で各数字が検出された座標をリスト化します。次に、`display_digits()`関数で数値を8桁形式に整形します（例：`258` は `"00000258"` に変換）。その後、配列から対応する座標を取得し、各数字の表示位置に適用します。

## ユーザーインターフェースのスクリプト化

「`UI`」シーンに戻り、「`ScoreCounter`」を{{< gd-icon HBoxContainer >}}`HBoxContainer`に追加し、その後「`UI`」にスクリプトを追加してください。

```gdscript
extends MarginContainer

@onready var shield_bar = $HBoxContainer/ShieldBar
@onready var score_counter = $HBoxContainer/ScoreCounter

func update_score(value):
    score_counter.display_digits(value)


func update_shield(max_value, value):
    shield_bar.max_value = max_value
    shield_bar.value = value
```

これらの関数はスコアやシールドを更新する必要がある場合に、`Main`モジュールから呼び出されるようにします。

## メイン画面にUIを追加

次に「Main」シーンに  ノードを追加し、その子要素として `UI` インスタンスを配置します。{{< gd-icon CanvasLayer >}}`CanvasLayer` ノードは新しい描画レイヤーを生成するため、UI はゲームの他のコンテンツの上に重なって表示されます。

メインスクリプト `main.gd` 内のこの関数を変更します。

```gdscript
func _on_enemy_died(value):
    score += value
    $CanvasLayer/UI.update_score(score)
```

ゲームを実行し、敵を撃つとスコアが上がることを確認してください。


## プレイヤーシールド

また、シールドをプレイヤースクリプトに追加することもできます。`player.gd`ファイルの先頭にこれらの新しい行を追加してください。

```gdscript
signal died
signal shield_changed

@export var max_shield = 10
var shield = max_shield:
    set = set_shield
```

この `set =` 構文は、Godotに対して、`shield` 変数の値が変更されるたびに `set_shield()` 関数を呼び出すよう指示するものです。

```gdscript
func set_shield(value):
    shield = min(max_shield, value)
    shield_changed.emit(max_shield, shield)
    if shield <= 0:
        hide()
        died.emit()
```

また、艦船の`area_entered`シグナルも接続することで、敵が艦船に命中したことを検出できます。

```gdscript
func _on_area_entered(area):
    if area.is_in_group("enemies"):
        area.explode()
        shield -= max_shield / 2
```

敵の攻撃弾については、命中時にシールドに追加ダメージを与えるようにしてください。

```gdscript
func _on_area_entered(area):
    if area.name == "Player":
        queue_free()
        area.shield -= 1
```

最後に、プレイヤーノードの `shield_changed` シグナルをシールドバー表示用UI関数に接続が必要です。メインシーン内の `Player` ノードを選択してインスペクターから実行できます。［ノード］タブで `shield_change`dシグナルをダブルクリックすると、「シグナル接続」ウィンドウが開きます。この画面で、対象となる `UI` ノードを選択し、**受信メソッド** 欄に `update_shield` と入力してください。

![alt](/godot_recipes/4.x/img/2d_101_24.png)

ゲームを再度実行し、弾丸や敵の攻撃を受けた際にシールドが減少することを確認してください。

## 次のステップ

基本機能はほぼ完成しました。あとはゲームの開始と終了方法を追加するだけです。

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_08/" icon="fas fa-arrow-left" %}}戻る{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_10/" icon="fas fa-arrow-right" icon-position="right" %}}次へ{{% /button %}} |
|------|------:|

