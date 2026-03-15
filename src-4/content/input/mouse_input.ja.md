---
title: "マウス入力"
weight: 2
draft: false
ghcommentid: 47
---

## 課題

マウス入力を検出したい。

## 解決策

`入力EventMouse` はマウスイベントの基本クラスです。これには `position` および `global_position` プロパティが含まれています。このクラスを継承するサブクラスとして、`入力EventMouseButton` と `入力EventMouseMotion` の2つが存在します。

{{% notice note %}}
インプットマップでマウスボタンイベントを割り当てられるので、`is_action_pressed()` 関数を使用してこれらを利用することができます。
{{% /notice %}}

### `入力EventMouseButton`

`@GlobalScope.ButtonList` には、各可能なボタンに対応する定数リスト（例：BUTTON_*）が格納されており、これらの値はイベントのbutton_indexプロパティで報告されます。なお、スクロールホイールも1つのボタンとしてカウントされます - 正確には2つのボタンがあり、それぞれ`BUTTON_WHEEL_UP`と`BUTTON_WHEEL_DOWN`という別々のイベントとして扱われます。

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

### `入力EventMouseMotion`

これらのイベントはマウスが移動するたびに発生します。移動距離（画面座標単位）は「`relative`」プロパティで取得できます。

以下に、マウス操作による3Dキャラクターの回転動作を実装した具体例を紹介します。

```gdscript
# Converts mouse movement (pixels) to rotation (radians).
var mouse_sensitivity = 0.002

func _unhandled_input(event):
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
```