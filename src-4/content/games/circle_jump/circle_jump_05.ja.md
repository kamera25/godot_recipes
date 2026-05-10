---
title: "スコアとHUD"
weight: 5
draft: false
pre: "05. "
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

最終部分では、ゲームの開始と設定するためのメニュー形式のUIを実装しました。また、スコアなどのゲーム内情報を表示するためのUIも必要です。

## HUDシーン

HUDとして使用する`CanvasLayer`をルートとする新しいシーンを追加してください。以下の2つの子要素を持たせます。「ScoreBox」という名前の`MarginContainer`と、「メッセージ」という名前の`Label`です。

Scene treeは以下のようになっている必要があります。

![alt](/godot_recipes/4.x/img/cj_05_01.png)

以下の設定を行ってください。
- `ScoreBox` のレイアウトを「下部ワイド」に設定
- すべてのカスタム定数値を`20`に設定
- `HBoxContainer` 子要素を追加し、その下に2つの `Label`ノードを配置
- 2番目のラベルに「スコア」という名前を付け、 _Text_ プロパティに `100` を入力
- `HBoxContainer` の _Alignment_ を「End」に設定

同じ`DynamicFont`リソースを両方のラベルに追加しますが、最初のラベルでは「ユニークにする」を選択し、そのサイズを `32` に設定します。_Text_プロパティには「スコア」と入力してください。その _Size Flags/Vertical_ で「塗りつぶし」を設定します。レイアウトは以下のようになります。

![alt](/godot_recipes/4.x/img/cj_05_02.png)

次に、`Message`ノードの処理に移ります。まずフォントを読み込み、 _Text_ プロパティに「メッセージ」を設定します。こうすることで表示内容が確認できるようになります。さらに、フォントリソースで「ユニーク化」（Make Unique）を選択してください（この理由は次のセクションで説明します）。 _Align_ と _Valign_ は「中央」に設定し、 _Clip Text_ は「オン」にしてください。レイアウトに関しては「ワイド・センタリング」を選択します。また、_Grow Direction/Vertical_を「両方」に設定します。

## メッセージアニメーション

このゲーム中に表示されるメッセージです（レベルアップ時の通知やボーナス表示など）。アニメーション付きで表示させ、フェードアウト効果を加えたいと思います。シーンに `AnimationPlayer` を追加してください。

以下の2つのアニメーションを作成します。初期値を設定するものと、メッセージ表示をアニメーションさせるものです。まず最初のアニメーション「init」を追加し、「ページ読み込み時に自動再生」ボタンをクリックします。持続時間は`0.1`に設定してください。

時刻 `0` に _フォント/サイズ_ (`64`) のキーフレームを追加し、_表示_ を「オフ」に設定するキーフレームも追加してください。

2番目のアニメーション「show_message」を追加してください。長さを `0.75` に、キーフレームの透明度設定を『オン』に設定してください。

次に、時刻`0`と`200`におけるフォントサイズを`64`からキーフレーム化します。トラックの更新モードを「連続」に設定してください。

また、オブジェクトが成長するにつれて徐々に透明度が低下するようにしたいので、キーフレームを使用してアルファ値を`255`から`0`まで変化させます。

以下にアニメーション設定の例を示します。

![alt](/godot_recipes/4.x/img/cj_05_03.png)

アニメーション再生時の挙動：

![alt](/godot_recipes/4.x/img/cj_05_04.gif)

## HUDスクリプト

次に、ディスプレイを更新するためのメソッドを含むスクリプトをシーンに追加してください。

```gdscript
extends CanvasLayer

func show_message(text):
    $Message.text = text
    $AnimationPlayer.play("show_message")

func hide_score():
    $ScoreBox.hide()

func show_score():
    $ScoreBox.show()

func update_score(value):
    $ScoreBox/HBoxContainer/Score.text = str(value)
```

メインシーンにHUDインスタンスを作成し、`_ready()`関数と`_on_Jumper_died()`関数内に`$HUD.hide_score()`を追加してください。`new_game()`関数では、HUDを表示してメッセージを表示します。以下のように実装します。

```gdscript
$HUD.show_score()
$HUD.show_message("Go!")
```

スコアを追加するには、`new_game()` 関数内で `score` 変数を作成し、初期値として `0` を設定してください。`_on_Jumper_captured()` 関数内では、この変数の値を 1 ずつ加算します。それぞれの処理後に `$HUD.update_score(score)` を呼び出すことを忘れないでください。

次のパートでは、ゲームにサウンドと色を追加していきます！

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画で見る

{{< youtube Fz2ltnvI4MQ >}}
