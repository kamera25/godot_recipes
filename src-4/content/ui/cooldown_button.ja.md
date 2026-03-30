---
title: "クールタイムボタン"
weight: 5
draft: false
---

## 課題

RPG風のスキルボタンを作成したい。クールタイム効果も組み込みたい。

![alt](/godot_recipes/4.x/img/cooldown_01.gif)

## 解決策

ボタン用のアイコンが必要な場合、[Game-icons.net](https://game-icons.net/)では多種多様なデザイン性の高いボタン素材を提供しています。このレシピでもその一部を使用しています。

### ノード設定

能力ボタン用のシーンには以下のノードが必要となります：

```
AbilityButton: {{< gd-icon TextureButton >}} TextureButton
   Sweep: {{< gd-icon TextureProgressBar >}} TextureProgress
   {{< gd-icon Timer >}} Timer
   Counter: {{< gd-icon MarginContainer >}} MarginContainer
      Value: {{< gd-icon Label >}} Label
```

選択したアイコンを `AbilityButton` の **Textures/Normal** プロパティにドロップしてください。

「掃引」ノードでは、**プリセット**メニューから「完全矩形」を選択します。**塗りつぶしモード**を「反時計回り」に設定してください。

また、クールタイム時の「時計ワイプ」でボタンを暗く表示させたいため、**[変調]** プロパティに透明度のある濃いグレーを設定してください。

![alt](/godot_recipes/4.x/img/cooldown_02.png)

`Timer`ノードの設定は「ワンショット」に設定してください。

`Counter`はテキストを保持・配置するためのコンテナです。レイアウトを"Bottom Wide"に設定し、**Theme Overrides/Constants** セクションでは両方の **Margin Right** と **Margin Left**  を `5` に指定してください。

最後に、［値］ラベルで［水平整列］を「右揃え」に設定し、［テキストクリッピング］を「有効」にしてください。**テーマオーバーライド／フォント**にフォントを追加します。動作確認のため、**テキスト**欄には `0.0` のような値を入力してください。アイコンが白黒の場合は、**テーマオーバーライド／定数／アウトラインサイズ**として `1` を設定すると効果的です。

### スクリプト

以下のスクリプトを `AbilityButton` に追加してください。
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

まず、能力のクールタイム時間を格納する`cooldown`変数をエクスポートします。次に、`_ready()`メソッド内でこの値を使用して`Timer`を設定できます。最後に、カウントダウン中のみ表示させたいため、ラベルは非表示にしておきます。

次に、`TextureProgress` 表示に割り当てるテクスチャが必要となります。この例では、ボタンのテクスチャをコピーしていますが、お好みで別のテクスチャを使用しても構いません。

最後に、スイープ値を `0` に設定し、ノードの処理フラグを `false` にします。アニメーションは `_process()` 内で処理するため、クールタイムモードではない時に実行される必要がないようにします。

```gdscript
func _process(delta):
    time_label.text = "%3.1f" % $Timer.time_left
    $Sweep.value = int(($Timer.time_left / cooldown) * 100)
```

を設定します。

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

タイマーが切れるとすべての設定は初期化されます。複数のボタンを {{< gd-icon HBoxContainer >}}`HBoxContainer` に配置するだけで、アクションバーが完成します。

![alt](/godot_recipes/4.x/img/cooldown_03.gif)

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます。 [https://github.com/godotrecipes/ui_cooldown_button](https://github.com/godotrecipes/ui_cooldown_button)

## 関連レシピ

- [UI: ラベル](/godot_recipes/4.x/ja/ui/labels/)
   - [UI: ユニットHPバー](/godot_recipes/4.x/ja/ui/unit_healthbar/) -->
