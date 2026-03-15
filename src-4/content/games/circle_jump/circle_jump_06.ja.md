---
title: "サウンドとカラー設定"
weight: 6
draft: false
pre: "06. "
---

## 設定シングルトン

まず、スクリプトタブで［ファイル］→［新規スクリプト］を選択して新しいスクリプトを追加します。スクリプト名は `settings.gd` とします。

このスクリプトでは、ゲームの設定パラメータを配置します。

```gdscript
var enable_sound = true
var enable_music = true

var circles_per_level = 5
```

スクリプトを自動読み込みに登録するには、「プロジェクト設定」を開き、「自動読み込み」タブを選択してください。ロードしたいスクリプトのフォルダをクリックし、その後「追加」をクリックします。

![alt](/godot_recipes/3.x/img/cj_06_01.png)

## サウンドの追加方法

サウンドを再生するために、複数の`音声StreamPlayer`ノードを異なるシーンに追加します。

- 1. まず「メイン」シーンに「音楽」という名前を追加します。［ストリーム］プロパティには `res://assets/audio/Music_Light-Puzzles.ogg` を使用してください。

- 「スクリーン」シーンに新たに「クリック」という画面を追加します。ボタンをタップした際にこの画面が表示されるようにします。アセットフォルダから「menu_click.wav」を使用します。

* 「Circle」シーンに、名前を『Beep』としたオーディオプレイヤーを追加し、`89.ogg`サウンドファイルを使用します。

- 最後にジャンパー部では、「ジャンプ」と「キャプチャー」の2種類の効果音が必要です。それぞれ`70.ogg`と`88.ogg`を使用してください。

サウンドを再生するには、それぞれの `play()` メソッドを呼び出すだけです。`Main.new_game()` にこれを追加しましょう。

```gdscript
if settings.enable_music:
    $Music.play()
```

 および `Main._on_Jumper_died()` 関数：

 ```gdscript
 if settings.enable_music:
    $Music.stop()
 ```

'Screens.gd' ファイルの `_on_button_pressed()` 関数に以下を追加してください。

```gdscript
if settings.enable_sound:
    $Click.play()
```

円軌道において、限定された円（制限軌道）が1周完了した際に「ビープ音」を再生したいです。これは`check_orbits()`関数内で実装します。

```gdscript
current_orbits -= 1
if settings.enable_sound:
    $Beep.play()
```

そして `Jumper.gd` に、次のようにサウンドを追加します。-- Jumper.gd ファイル内でサウンドを追加します:

```gdscript
func jump():
    target.implode()
    target = null
    velocity = transform.x * jump_speed
    if settings.enable_sound:
        $Jump.play()

func _on_Jumper_area_entered(area):
    target = area
    velocity = Vector2.ZERO
    emit_signal("captured", area)
    if settings.enable_sound:
        $Capture.play()
```

ゲームを起動し、すべての音が期待通りに聞こえるか確認してください。

## 音声設定

音声機能が正常に動作するようになったので、「設定」画面で音と音楽を切り替えられるボタンも接続できるようになりました。

ボタンの表示を、プロパティの現在のオン／オフ状態に合わせる必要があります。まずはテクスチャを読み込んでから、必要に応じて割り当てられるようにします。

```gdscript
var sound_buttons = {true: preload("res://assets/images/buttons/audioOn.png"),
                    false: preload("res://assets/images/buttons/audioOff.png")}
var music_buttons = {true: preload("res://assets/images/buttons/musicOn.png"),
                    false: preload("res://assets/images/buttons/musicOff.png")}
```

// Current issue: We are currently passing only the button name,
// which prevents us from changing its texture.
// We're refactoring register_buttons() to accept a direct reference to the button object instead:

```gdscript
button.connect("pressed", self, "_on_button_pressed", [button])
```

その後で `_on_button_pressed()` を以下のように更新できます。

```gdscript
func _on_button_pressed(button):
    if settings.enable_sound:
        $Click.play()
    match button.name:
        "Home":
            change_screen($TitleScreen)
        "Play":
            change_screen(null)
            yield(get_tree().create_timer(0.5), "timeout")
            emit_signal("start_game")
        "Settings":
            change_screen($SettingsScreen)
        "Sound":
            settings.enable_sound = !settings.enable_sound
            button.texture_normal = sound_buttons[settings.enable_sound]
        "Music":
            settings.enable_music = !settings.enable_music
            button.texture_normal = music_buttons[settings.enable_music]
```

## カラーテーマ設定

さらに、色テーマをカスタマイズできる機能も追加予定です。これらは以下のような方法で変更できます。設定項目として選択するか、プレイヤーがより高いレベルに到達するにつれて段階的に変化させる、といった方法が考えられます。

カラースキームデータを辞書形式で保存します。キーは各配色の「名称」となります。各配色自体も辞書形式とし、キーはその配色を使用するゲームコンポーネントを示します。

以下を `settings.gd` に追加してください。

```gdscript
var color_schemes = {
    "NEON1": {
        'background': Color8(0, 0, 0),
        'player_body': Color8(203, 255, 0),
        'player_trail': Color8(204, 0, 255),
        'circle_fill': Color8(255, 0, 110),
        'circle_static': Color8(0, 255, 102),
        'circle_limited': Color8(204, 0, 255)
    },
    "NEON2": {
        'background': Color8(0, 0, 0),
        'player_body': Color8(246, 255, 0),
        'player_trail': Color8(255, 255, 255),
        'circle_fill': Color8(255, 0, 110),
        'circle_static': Color8(151, 255, 48),
        'circle_limited': Color8(127, 0, 255)
    },
    "NEON3": {
        'background': Color8(0, 0, 0),
        'player_body': Color8(255, 0, 187),
        'player_trail': Color8(255, 148, 0),
        'circle_fill': Color8(255, 148, 0),
        'circle_static': Color8(170, 255, 0),
        'circle_limited': Color8(204, 0, 255)
    }
}

var theme = color_schemes["NEON1"]
```

現在各オブジェクトに対して、設定プロパティに基づいて色を設定が必要です。

円形の場合、シェーダーマテリアルリソースを使用して色を設定しています。共有リソースを使用しているため、1つの円の色を変更するとすべての円に影響が及びます。これを回避するため、各サークルのマテリアルを個別にしてみましょう。

```gdscript
$Sprite.material = $Sprite.material.duplicate()
$SpriteEffect.material = $Sprite.material
```

円形の色はそのモードによって決定されるため、実際の選択処理は `set_mode()` 関数内で行います。

```gdscript
func set_mode(_mode):
    mode = _mode
    var color
    match mode:
        MODES.STATIC:
            $Label.hide()
            color = settings.theme["circle_static"]
        MODES.LIMITED:
            current_orbits = num_orbits
            $Label.text = str(current_orbits)
            $Label.show()
            color = settings.theme["circle_limited"]
    $Sprite.material.set_shader_param("color", color)
```

Then in the `_draw()` function where we're filling in the limited circle, replace the red color with `settings.theme["circle_fill"]`.

プレイヤーの設定では、`_ready()` 内で色を指定します。

```gdscript
func _ready():
    $Sprite.material.set_shader_param("color", settings.theme["player_body"])
    $Trail/Points.default_color = settings.theme["player_trail"]
```

次のパートでは、円に動きを追加します。

----------

#### このプロジェクトをGitHubでフォローしよう：

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube 8yvVej_fLMs >}}