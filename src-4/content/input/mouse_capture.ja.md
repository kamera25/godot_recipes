---
title: "Capturing the Mouse"
weight: 3
draft: false
ghcommentid: 49
---

## 問題文

マウスカーソルを隠し、ゲームウィンドウからマウスが外れるのを防ぎたい場合。これは多くの3Dゲーム（および一部の2Dゲーム）で一般的な機能です。

## 解決策

マウスの状態を設定したい場合は、`Input.mouse_mode`を使用できます。利用可能なマウスモードは以下の4種類です：

- **MOUSE_MODE_VISIBLE**: マウスが視認可能で、ウィンドウ内外を自由に移動できます。これがデフォルト状態です。

- **マウスモード非表示時**：マウスカーソルは表示されませんが、マウス操作でウィンドウ外に移動可能です。

- **マウスモード捕捉中**：マウスカーソルが非表示になり、ゲームウィンドウの外側にマウスを移動させることができなくなります。

- **MOUSE_MODE_CONFINED** ：マウスは表示されていますが、ゲームウィンドウの外には移動できません。

"Captured" is the most commonly used option. You can set the mouse mode at runtime using:

```gdscript
func _ready():
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
```

When the mouse is captured, mouse input events will still be passed as normal. However, you will find there is a problem. If you want to close the game or switch to another window, you can't. For this reason, you will want to also include a way to "release" the mouse. For example, to release when the player pressed the Escape key:

```gdscript
func _input(event):
    if event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
```

他のウィンドウに表示されている時にマウス操作がゲームに反映されないようにするには、キャラクターコントローラ内で以下を使用してキャプチャ状態を判定できます：

```gdscript
if Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
```

マウスボタンを離すと、再びクリック操作を開始するために再キャプチャが必要になります。入力マップにマウスクリック用のイベントが設定されている場合、以下のように対処できます：

```gdscript
    if event.is_action_pressed("click"):
        if Input.mouse_mode == Input.MOUSE_MODE_VISIBLE:
            Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
```

マウスクリックで射撃や別のアクションを実行する場合もあるため、イベント伝播を停止させるのは有効な方法です。マウスモード設定後に以下を追加してください：

```gdscript
get_tree().set_input_as_handled()
```
