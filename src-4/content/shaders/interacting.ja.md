---
title: "シェーダーとの連携"
weight: 2
draft: false
ghcommentid: 77
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

GDScriptからGodotシェーダーと連携したい。

## 解決策

GDScriptから uniform の値にアクセスするには、オブジェクトの`material`プロパティに対して`set_shader_param()`メソッドを使用できます。もしアタッチされているマテリアルが ShaderMaterial の場合、以下のようにアクセス可能です。

```gdscript
node.material.set_shader_param("param_name", value)
```

以下の方法で値を取得することもできます。`get_shader_param()`。

例については、[ブラーシェーダー](/godot_recipes/4.x/ja/shaders/blur/)のレシピを参照してください。

## 関連するレシピ

- [シェーダー入門](/godot_recipes/4.x/ja/shaders/intro/)