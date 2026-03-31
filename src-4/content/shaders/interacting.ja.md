---
title: "シェーダーとの連携"
weight: 2
draft: false
ghcommentid: 77
---

## Problem

GDScriptからGodotシェーダーと連携したい。

## Solution

GDScriptから uniform の値にアクセスするには、オブジェクトの`material`プロパティに対して`set_shader_param()`メソッドを使用できます。もしアタッチされているマテリアルが`ShaderMaterial`の場合、以下のようにアクセス可能です。

```gdscript
node.material.set_shader_param("param_name", value)
```

以下の方法で値を取得することもできます。`get_shader_param()`。

例については、[ブラーシェーダー](/godot_recipes/4.x/ja/shaders/blur/)のレシピを参照してください。

## Related Recipes

- [シェーダー入門](/godot_recipes/4.x/ja/shaders/intro/)