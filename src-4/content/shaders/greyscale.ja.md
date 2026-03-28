---
title: "グレースケール（モノクロ）シェーダー"
weight: 3
draft: false
ghcommentid: 78
---

## 課題

画像のグレースケール変換に使用するシェーダーが必要です。

## 解決策

Let's start with a `canvas_item` (2D) shader. To convert to greyscale but also preserve pixel contrast, we need to _average_ the pixel's color value. Add the color channels together and divide by 3:

```glsl
shader_type canvas_item;

void fragment() {
    COLOR = texture(TEXTURE, UV);
    float avg = (COLOR.r + COLOR.g + COLOR.b) / 3.0;
    COLOR.rgb = vec3(avg);
}
```

![alt](/godot_recipes/3.x/img/shader_greyscale01.png)

この機能を画面全体に適用するには、{{< gd-icon ColorRect >}} `ColorRect` コンポーネント（カメラの動きを無視するため {{< gd-icon CanvasLayer >}} `CanvasLayer` 内に配置）を追加し、画面全体を覆うようにスケールを調整してください。

`texture()` 関数を修正し、オブジェクトのピクセルではなく画面を直接サンプリングするようにしましょう。

```glsl
COLOR = texture(SCREEN_TEXTURE, SCREEN_UV);
```

![alt](/godot_recipes/3.x/img/shader_greyscale02.png)

## 関連するレシピ

- [シェーダー入門](/godot_recipes/4.x/ja/shaders/intro/)