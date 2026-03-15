---
title: "カーソルのカスタマイズ"
weight: 5
draft: false
ghcommentid: 50
---

## 課題

ゲーム中のマウスカーソルをカスタマイズしたい。

## 解決策

マウスカーソルの設定は `入力.set_custom_mouse_cursor()` メソッドを使用して行います。必要なのは使用するテクスチャだけです。なお、このテクスチャのサイズは最大で `256x256` ピクセル以内にしてください。

例えば、以下の画像を使用するには：

![alt](/godot_recipes/3.x/img/crosshair137.png)

そして、ホットスポットを中央位置に設定します。

```gdscript
extends Node2D

func _ready():
    Input.set_custom_mouse_cursor(cursor_image,
            Input.CURSOR_ARROW,
            Vector2(64, 64))
```

第2パラメータはどのシステムカーソルを置き換えるかを指定します。完全なリストについては[入力ドキュメント](https://docs.godotengine.org/en/latest/classes/class_input.html#enum-input-cursorshape)を参照してください。
