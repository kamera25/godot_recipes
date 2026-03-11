---
title: "Mouse Input"
weight: 2
draft: false
ghcommentid: 47
---

## 課題

マウス入力を検出したいようです。

## 解決策

`InputEventMouse` はマウスイベントの基本クラスです。これには `position` および `global_position` プロパティが含まれています。このクラスを継承するサブクラスとして、`InputEventMouseButton` と `InputEventMouseMotion` の2つが存在します。

{{% notice note %}}
入力マップでマウスボタンイベントを割り当てられるので、`is_action_pressed()` 関数を使用してこれらを利用することができます。
{{% /notice %}}

### `InputEventMouseButton`

```python
'@GlobalScope.ButtonList' には、各ボタンタイプに対応する定数 'BUTTON_*' のリストが含まれており、これらはイベントの 'button_index' プロパティで報告されます。なお、スクロールホイールも1つのボタンとしてカウントされますのでご注意ください。正確には、`BUTTON_WHEEL_UP` と `BUTTON_WHEEL_DOWN` はそれぞれ別個のイベントとして扱われます。

```
{{% notice tip %}}
通常のボタンとは異なり、マウスホイールクリックでは「押された」イベントのみが発生します。マウスホイールクリックが「離された」という概念は存在しません。
{{% /notice %}}

```gdscript
func _unhandled_input(event):
    if event is InputEventMouseButton:
        if event.button_index == BUTTON_LEFT:
            if event.pressed:
                print("Left button was clicked at ", event.position)
            else:
                print("Left button was released")
        if event.button_index == BUTTON_WHEEL_DOWN:
            print("Wheel down")
```

### `InputEventMouseMotion`

これらのイベントはマウスが移動するたびに発生します。移動距離（画面座標単位）は「`relative`」プロパティで取得できます。

以下に、マウス操作による3Dキャラクターの回転動作を実装した具体例を紹介します：

```gdscript
# Converts mouse movement (pixels) to rotation (radians).
var mouse_sensitivity = 0.002

func _unhandled_input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
```