---
title: "グレースケール（モノクロ）シェーダー"
weight: 3
draft: false
ghcommentid: 78
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

画像のグレースケール変換に使用するシェーダーが必要です。

## 解決策

まずは `canvas_item`（2D）用シェーダーから始めてください。グレースケールに変換しつつピクセルのコントラストを維持するには、画素値を**平均化**が必要です。カラーチャンネルをすべて加算し、3で割ることで実現できます。

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

`texture()` 関数を修正し、オブジェクトのピクセルではなく画面を直接サンプリングするようにしてください。

```glsl
COLOR = texture(SCREEN_TEXTURE, SCREEN_UV);
```

![alt](/godot_recipes/3.x/img/shader_greyscale02.png)

## 関連するレシピ

- [シェーダー入門](/godot_recipes/4.x/ja/shaders/intro/)