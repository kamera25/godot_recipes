---
title: "シェーダーとの連携"
weight: 2
draft: false
ghcommentid: 77
---

## 課題

您希望从 GDScript 编程方式与神经网格着色器进行交互。

## 解決策

To access the uniform's value from GDScript, you can use `set_shader_param()` on the object's `material` property. If the attached material is a ShaderMaterial, then you can access it like so:

```gdscript
node.material.set_shader_param("param_name", value)
```

以下の方法で値を取得することもできます：`get_shader_param()`。

例については、[ブラーシェーダー](/godot_recipes/3.x/shaders/blur/)のレシピを参照してください。

## 関連するレシピ

- [シェーダー入門](/godot_recipes/3.x/shaders/intro/)