---
title: "Starting and Ending the Game"
weight: 10
draft: false
pre: "10. "
---

Our last step is to add a start button and a "game over" state to the game.

## ゲーム開始方法

現在ゲームを実行するとすぐに開始されますが、起動用のボタンを追加しましょう。

```
In `Main` as a child of `CanvasLayer`, add a {{< gd-icon CenterContainer >}}`CenterContainer` and set its layout to **Full Rect**. Then add a {{< gd-icon TextureButton >}}`TextureButton` child. Name this button `Start` and add the `START (48 x 8).png` image as its **Normal** texture.
```

スクリプトの上部に参照を追加：

```gdscript
@onready var start_button = $CanvasLayer/CenterContainer/Start
```

このボタンの`押された`テクスチャを`メイン`に接続し、このコードを追加してください：

```gdscript
func _on_start_pressed():
    start_button.hide()
    new_game()
```

```python
def _mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return False

            # 他のゲームロジックをここに追加...

        screen.fill(BACKGROUND_COLOR)
        button_image = create_ready_button()
        screen.blit(button_image, (BUTTON_POSITION[0], BUTTON_POSITION[1]))
        pygame.display.flip()
```

## 変更点説明:
- **`if event.type == pygame.QUIT or ...`**: QUITイベントまたはESCキー押下時にゲーム終了処理を行う。
- **`screen.fill(BACKGROUND_COLOR)`**: 背景色を再描画する。
- **`button_image = create_ready_button()`**: `create_ready_button()`関数で準備完了ボタンの画像を生成する。
- **`pygame.display.flip()`**: 画面を更新して変更を適用する。

```gdscript
func _ready():
    start_button.show()
#	spawn_enemies()
```

次に、`new_game()`関数を追加します：

```gdscript
func new_game():
    score = 0
    $CanvasLayer/UI.update_score(score)
    $Player.start()
    spawn_enemies()
```

現在は、シーンを実行するとボタンが表示され、クリックするとゲームが開始されるはずです。

## ゲーム終了方法

```

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

This will show the "game over" image for 2 seconds, then switch back to the start button so you can play again. Try it out and see if you can play a few games.

| {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_09/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_end/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
