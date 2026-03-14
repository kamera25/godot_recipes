---
title: "グレースケール（モノクロ）シェーダー"
weight: 3
draft: false
ghcommentid: 78
---

## 課題

画像のグレースケール変換に使用するシェーダーが必要です。

## 解決策

まずは `canvas_item`（2D）用シェーダーから始めましょう。グレースケールに変換しつつピクセルのコントラストを維持するには、画素値を**平均化**する必要があります。カラーチャンネルをすべて加算し、3で割ることで実現できます：

```glsl
shader_type canvas_item;

void fragment() {
    COLOR = texture(TEXTURE, UV);
    float avg = (COLOR.r + COLOR.g + COLOR.b) / 3.0;
    COLOR.rgb = vec3(avg);
}
```

<img src="/godot_recipes/3.x/img/shader_greyscale01.png" alt="">

この機能を画面全体に適用するには、{{< gd-icon ColorRect >}} `ColorRect` コンポーネント（カメラの動きを無視するため {{< gd-icon CanvasLayer >}} `CanvasLayer` 内に配置）を追加し、画面全体を覆うようにスケールを調整してください。

変更：`texture()` 関数を修正し、オブジェクトのピクセルではなく画面を直接サンプリングするようにします：

```glsl
COLOR = texture(SCREEN_TEXTURE, SCREEN_UV);
```

![alt](/godot_recipes/3.x/img/shader_greyscale02.png)

## 関連するレシピ

- [シェーダー入門](/godot_recipes/3.x/shaders/intro/)