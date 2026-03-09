---
title: "Input Actions"
weight: 2
draft: false
ghcommentid: 46
---

## 問題文

You want to understand Godot's "input action" system.

## 解決策

Let's say you're making a top-down character and you write code using `InputActionKey` that uses the arrow keys for movement. You'll quickly find that many players prefer to use "WASD" style controls. You can go back into your code and add the additional key checks, but this would result in duplicated/redundant code.

入力アクションを活用することで、コードの設定可能性を高めることができます。特定のキーをハードコーディングする代わりに、コードを変更することなく動的に調整・カスタマイズできるようになります。

### 入力の作成方法

You define input actions in the "Project Settings" under the "Input Map" tab. Here, you can create new actions and/or assign inputs to them.

You'll see when you click on the tab there are already some default actions configured. They are all named "ui_*" to indicate that they are the default interface actions. "Tab" for next UI element, for example.

一般的に、既存のアクションを使用するよりも、自分のゲーム用に独自のアクションを作成する方がよいでしょう。

この例では、プレイヤーがキーボードまたはマウスでゲームを操作できるようにしたいとしましょう。プレイヤーは左クリックボタンを押すか、スペースバーを押すことで、射撃ができるようにしなければなりません。

Create the new action "shoot" by typing the name in the "Action" field at the top and clicking "Add" (or pressing enter). Scroll to the bottom and you'll see the new action has been added to the list.

Now you can assign inputs to this action by clicking the "+" sign to the right. Inputs can be keys, mouse buttons, or joy/gamepad inputs. Choose "Key" and you can press the key on the keyboard you want to assign - let's press the spacebar - and click "OK".

Click "+" to add another input, and this time choose "Mouse Button". The default of "Device 0" and "Left Button" is fine, but you can select others if you like.

### 入力アクションの使用について

以下の方法でアクションをチェックできます：
・各フレームごとに単一インスタンス `Input` をポーリングする方法：

```gdscript
func _process(delta):
    if Input.is_action_pressed("shoot"):
        # This will execute every frame as long as the input is held.
```

これは、継続的な動作――例えば移動など、常時確認が必要な状況に最適です。

```python
def on_event(event):
    print(\, event)

def handle_keyboard_event(key):
    if key == 'KEY_LEFT':
        move_left()
    elif key == 'KEY_RIGHT':
        move_right()

input_callback = on_event  # メインループ内でのコールバック
unhandled_input_callback = handle_keyboard_event  # 未処理入力時のハンドラ

```gdscript
func _unhandled_input(event):
    if event.is_action_pressed("shoot"):
       # This will run once on the frame when the action is first pressed
```

入力状態を確認するために使える機能はいくつかあります：

- `is_action_pressed()`: この関数は現在アクションが「押された」状態にある場合に`true`を返します。

```bash
- `is_action_released()`: この関数は、アクションが `pressed` 状態にない場合に `true` を返します。

```python
- is_action_just_pressed() / is_action_like_released(): これらのメソッドは上記と同様の機能を持ちますが、イベント発生後の1フレーム目にのみ`true`を返す点が異なります。射撃やジャンプなど、ユーザーがキーを放した後に再度押して動作を繰り返す必要がある非反復アクションに特に有用です。

## 関連するレシピ

- [入力システム入門](/godot_recipes/3.x/input/input_intro/)