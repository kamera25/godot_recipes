---
title: "シェーダーとの連携"
weight: 2
draft: false
ghcommentid: 77
---

## 課題

GDScriptからGodotシェーダーと連携したい。

## 解決策

GDScriptから uniform の値にアクセスするには、オブジェクトの`material`プロパティに対して`set_shader_param()`メソッドを使用できます。もしアタッチされているマテリアルが`ShaderMaterial`の場合、以下のようにアクセス可能です。

```gdscript
node.material.set_shader_param("param_name", value)
```

以下の方法で値を取得することもできます。`get_shader_param()`。

例については、[ブラーシェーダー](/godot_recipes/4.x/ja/shaders/blur/)のレシピを参照してください。

## 関連するレシピ

- [シェーダー入門](/godot_recipes/3.x/shaders/intro/)