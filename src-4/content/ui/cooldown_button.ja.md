---
title: "Cooldown Button"
weight: 5
draft: false
---

## 問題文

RPG風のスキルボタンを作成したい。クールダウン効果も組み込みたい。

![alt](/godot_recipes/4.x/img/cooldown_01.gif)

## 解決策

ボタン用のアイコンが必要な場合、[Game-icons.net](https://game-icons.net/)では多種多様なデザイン性の高いボタン素材を提供しています。このレシピでもその一部を使用しています。

### ノード設定

能力ボタン用のシーンには以下のノードが必要です：

```
AbilityButton: {{< gd-icon TextureButton >}} TextureButton
   Sweep: {{< gd-icon TextureProgressBar >}} TextureProgress
   {{< gd-icon Timer >}} Timer
   Counter: {{< gd-icon MarginContainer >}} MarginContainer
      Value: {{< gd-icon Label >}} Label
```

選択したアイコンを `AbilityButton` の **Textures/Normal** プロパティにドロップしてください。

On the `Sweep` node, choose "Full Rect" from the **Presets** menu. Set the **Fill Mode** to "Counter Clockwise".

We also want our cooldown "radial wipe" to darken the button, so set the **Modulate** property to a dark gray with some transparency:

![alt](/godot_recipes/4.x/img/cooldown_02.png)

The {{< gd-icon Timer >}}`Timer` node should be set to "One Shot".

`Counter` is a container to hold and align the text. Set its layout to "Bottom Wide", and in its **Theme Overrides/Constants**, both **Margin Right** and **Margin Left** to `5`.

Finally, on the `Value` label, set **Horizontal Alignment** to "Right" and **Clip Text** to "On". Add a font to the **Theme Overrides/Font**. Put a value like `0.0` in the **Text** field to check how it works. Since our icon is black and white, it also helps to add a **Theme Overrides/Constants/Outline Size**_ of `1`.

### スクリプト

以下のスクリプトを `AbilityButton` に追加してください：
- `Timer` の `timeout` シグナルと `AbilityButton` の `pressed` シグナルを接続します。

```gdscript
extends TextureButton
class_name AbilityButton

@onready var time_label = $Counter/Value

@export var cooldown = 1.0


func _ready():
    time_label.hide()
    $Sweep.value = 0
    $Sweep.texture_progress = texture_normal
    $Timer.wait_time = cooldown
    set_process(false)
```

まず、能力のクールダウン時間を格納する`cooldown`変数をエクスポートします。次に、`_ready()`メソッド内でこの値を使用して`Timer`を設定できます。最後に、カウントダウン中のみ表示させたいため、ラベルは非表示にしておきます。

次に、`TextureProgress` 表示に割り当てるテクスチャが必要です。この例では、ボタンのテクスチャをコピーしていますが、お好みで別のテクスチャを使用しても構いません。

最後に、スイープ値を 0 に設定し、ノードの処理フラグを false にします。アニメーションは _process() 内で処理するため、クールダウンモードではない時に実行される必要がないようにします。

```gdscript
func _process(delta):
    time_label.text = "%3.1f" % $Timer.time_left
    $Sweep.value = int(($Timer.time_left / cooldown) * 100)
```

```_process()``` メソッドでは、タイマーの `time_left` 値を使用してラベルの `text` とスイープの `value` を設定します。

```gdscript
func _on_AbilityButton_pressed():
    disabled = true
    set_process(true)
    $Timer.start()
    time_label.show()
```

ボタンをクリックするとすべてが始まります。

```gdscript
func _on_Timer_timeout():
    print("ability ready")
    $Sweep.value = 0
    disabled = false
    time_label.hide()
    set_process(false)
```

タイマーが切れるとすべての設定は初期化されます。複数のボタンを `{{< gd-icon HBoxContainer >}}HBoxContainer` に配置するだけで、アクションバーが完成します：

<img src=\ alt=\>

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトのサンプルコードはこちらからダウンロードできます: [https://github.com/godotrecipes/ui_cooldown_button](https://github.com/godotrecipes/ui_cooldown_button)

<!-- ## 関連レシピ

- [UI: Labels](/godot_recipes/3.x/ui/labels/)
- [UI: Object Healthbars](/godot_recipes/3.x/ui/unit_healthbar/) -->
