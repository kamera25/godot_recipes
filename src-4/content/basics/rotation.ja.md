---
title: "円運動"
weight: 6
draft: false
ghcommentid: 14
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

オブジェクトを別のオブジェクトの周りで「周回」（円軌道を描くように移動）させたい。

## 解決策

これは初心者がよく抱く疑問で、三角関数をあれこれ試した後によく出てきます。答えは実はとてもシンプルです。

![alt](/godot_recipes/4.x/img/circle_motion_01.png)

軌道周回させるスプライトをメインスプライトの子ノードに配置します（ここでは「ピボット」と呼びます）。オフセット値を適用し、`Pivot`で回転させます。

```gdscript
extends Node2D

@export var rotation_speed = PI


func _process(delta):
    $Sprite/Pivot.rotation += rotation_speed * delta
```

![alt](/godot_recipes/4.x/img/circle_motion_02.gif)

この手法は3D空間でも同じように機能します。

```gdscript
extends Node3D

@export var rotation_speed = PI


func _process(delta):
    $MeshInstance/Pivot.rotate_y(rotation_speed * delta)

```

![alt](/godot_recipes/4.x/img/circle_motion_03.gif)