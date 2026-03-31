---
title: "マウスのキャプチャ"
weight: 3
draft: false
ghcommentid: 49
---

## 課題

マウスカーソルを隠し、ゲームウィンドウからマウス。これは多くの3Dゲーム（および一部の2Dゲーム）で一般的な機能です。

## 解決策

マウスの状態を設定したい場合は、`Input.mouse_mode`を使用できます。利用可能なマウスモードは以下の4種類です。

- **MOUSE_MODE_VISIBLE**: マウスが視認可能で、ウィンドウ内外を自由に移動できます。これがデフォルト状態です。

- **MOUSE_MODE_HIDDEN**：マウスカーソルは表示されませんが、マウス操作でウィンドウ外に移動できます。

- **MOUSE_MODE_CAPTURED**：マウスカーソルが非表示になり、ゲームウィンドウの外側にマウスを移動させることができなくなります。

- **MOUSE_MODE_CONFINED** ：マウスは表示されていますが、ゲームウィンドウの外には移動できません。

「キャプチャ」は最も一般的に使用されるオプションです。実行時にマウスモードを設定するには、以下のコマンドを使用できます。

```gdscript
func _ready():
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
```

マウスが捕捉されている状態でも、通常どおりマウス入力イベントは伝達されます。ただし、問題が生じることに注意してください。ゲームを終了したり他のウィンドウに切り替えたい場合、それが不可能になります。このため、「マウス解放」機能も実装しておくと便利です。例えば、プレイヤーがEscキーを押したときにマウスを解放するには：

```gdscript
func _input(event):
    if event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
```

他のウィンドウに表示されている時にマウス操作がゲームに反映されないようにするには、キャラクターコントローラ内で以下を使用してキャプチャ状態を判定できます。

```gdscript
if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
```

マウスボタンを離すと、再びクリック操作を開始するために再キャプチャが必要になります。インプットマップにマウスクリック用のイベントが設定されている場合、以下のように対処できます。

```gdscript
    if event.is_action_pressed("click"):
        if Input.mouse_mode == Input.MOUSE_MODE_VISIBLE:
            Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
```

マウスクリックで射撃や別のアクションを実行する場合もあるため、イベント伝播を停止させるのは有効な方法です。マウスモード設定後に以下を追加してください。

```gdscript
get_tree().set_input_as_handled()
```
