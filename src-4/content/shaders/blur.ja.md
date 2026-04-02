---
title: "ブラーシェーダー"
weight: 4
draft: false
ghcommentid: 79
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

オブジェクトや画面をぼかすシェーダーが欲しい。

## 解決策

```glsl
shader_type canvas_item;

uniform float blur_amount : hint_range(0, 5);

void fragment() {
	COLOR = textureLod(SCREEN_TEXTURE, SCREEN_UV, blur_amount);
}
```

例えば、シーン切り替え効果のために画面全体を徐々にぼかすには。

![alt](/godot_recipes/3.x/img/blur_shader1.png)
![alt](/godot_recipes/3.x/img/blur_shader2.png)

ぼかし効果もアニメーション化できます。

```gdscript
extends Node

# Add a ColorRect or other Control set to fill the screen
# Place it lower in the tree and/or place in CanvasLayer
# so it's on top of the rest of the scene.
@onready var blur = $Blur
var blur_amount = 0

func _process(delta):
    blur_amount = wrapf(blur_amount + 0.05, 0.0, 5.0)
    blur.material.set_shader_param("blur_amount", blur_amount)
```

<video controls src='/godot_recipes/3.x/img/blur_shader3.webm'></video>

## 関連するレシピ

- [シェーダー入門](/godot_recipes/4.x/ja/shaders/intro/)
- [シェーダーとの連携](/godot_recipes/4.x/ja/shaders/interacting/)