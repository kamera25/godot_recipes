---
title: "ゲームの開始と終了方法"
weight: 10
draft: false
pre: "10. "
---

最後のステップとして、ゲームにスタートボタンと「ゲームオーバー」状態を追加します。

## ゲーム開始方法

現在ゲームを実行するとすぐに開始されますが、起動用のボタンを追加しましょう。

`Main`を`CanvasLayer`の子要素として追加し、そこに{{< gd-icon CenterContainer >}}`CenterContainer`を追加し、そのレイアウトを**フル矩形**に設定します。次に、{{< gd-icon TextureButton >}}`TextureButton`をその子要素として追加します。このボタンに「Start」という名前を付け、その**通常状態**のテクスチャとして`START (48 x 8).png`画像を設定します。

スクリプトの上部に参照を追加：

```gdscript
@onready var start_button = $CanvasLayer/CenterContainer/Start
```

このボタンの`pressed`テクスチャを`Main`に接続し、このコードを追加してください。

```gdscript
func _on_start_pressed():
    start_button.hide()
    new_game()
```

`new_game()`関数はゲームの開始処理を担当するため、`_ready()`を変更し、敵を生成しないようにしつつ、ボタンが表示されるようにするだけです。

```gdscript
func _ready():
    start_button.show()
#	spawn_enemies()
```

次に、`new_game()`関数を追加します。

```gdscript
func new_game():
    score = 0
    $CanvasLayer/UI.update_score(score)
    $Player.start()
    spawn_enemies()
```

現在は、シーンを実行するとボタンが表示され、クリックするとゲームが開始されるはずです。

## ゲーム終了方法

 `CenterContainer`の子として `{{< gd-icon TextureRect >}}`TextureRect` を追加し、ノード名を `GameOver` に設定します。画像には `GAME_OVER (72 x 8).png` を使用します。この画像はスタートボタンと重なりますが、問題ありません。ゲームでは一度に表示するのは一つだけだからです。

スクリプトの上部に別の参照を追加：

```gdscript
@onready var game_over = $CanvasLayer/CenterContainer/GameOver
```

また、`_ready()` に `game_over.hide()` を追加してください。

メインモジュールでプレイヤーの `died` シグナルを接続してください。

```gdscript
func _on_player_died():
    get_tree().call_group("enemies", "queue_free")
    game_over.show()
    await get_tree().create_timer(2).timeout
    game_over.hide()
    start_button.show()
```

この操作で2秒間「ゲームオーバー」画面が表示され、その後スタートボタンに戻るので、再度プレイできます。ぜひお試しいただき、何ゲームか続けて遊んでみてください。

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_09/" icon="fas fa-arrow-left" %}} 前へ{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_end/" icon="fas fa-arrow-right" icon-position="right" %}} 次へ{{% /button %}} |
|------|------:|
