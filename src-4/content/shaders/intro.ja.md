---
title: "シェーダー入門編"
weight: 1
draft: false
ghcommentid: 76
---

## 課題

シェーダーのコーディングをやってみたい。

## 解決策

シェーダーとは、コンピュータのGPU（グラフィックスカード）上で動作する専用プログラムのことです。GPUは特定種類の演算処理を極めて効率的に実行できるよう最適化されています。このシェーダーコードをオブジェクトに適用することで、画面上でのレンダリング方法に影響を与えることができます。

シェーダープログラムの出力結果は、オブジェクトを構成するピクセル群の色情報です。シェーダーは2D環境（`canvas_item` 用シェーダー）および3D環境（`spatial` シェーダー）で利用できます。

The most difficult part for newcomers to understand about shaders is that they run in _parallel_. A shader runs simultaneously on *all* pixels. This allows for great speed, but also limits what information you have access to in the shader.

To add a shader to an object, find its _Material_ property and select "New ShaderMaterial". Click the new material to open it, and select "New Shader". Click that, and you'll see a shader editor open at the bottom of the screen.

シェーダーの最初の行にはそのタイプを指定が必要です。接続されているノードが2Dノードの場合は：

```glsl
shader_type canvas_item;
```

もしくは3Dノードの場合：

```glsl
shader_type spatial;
```

これらの初期例では2Dに限定して進めましょう。まず`Sprite`ノードを追加し、上記の手順に従ってシェーダーを適用してください。テクスチャにはGodotのデフォルトアイコンを使用することもできます。

There are two basic types of shader we'll discuss here: _vertex_ and _fragment_.

### フラグメントシェーダー

フラグメントシェーダーはピクセルの色を計算します。具体例を見てみましょう。

```glsl
void fragment() {
    COLOR = vec4(1.0, 0.0, 0.0, 1.0);
}
```

![alt](/godot_recipes/3.x/img/shader_intro_01.png)

全てのピクセルが赤色になります。`COLOR`はフラグメントシェーダーの出力値であり、これをすべてのピクセルに同時に適用します。しかし、何らかのバリエーションを持たせたい場合はどうしましょうか？

#### UV座標

シェーダーでは、ピクセル座標は **UV** 表記で指定されます。これらは正規化された値で、範囲は `(0, 0)`（左上）から `(1, 1)`（右下）までです。

{{% notice note %}}
シェーダーではベクトル型 (`vec4`) を使用してRGBAカラーを表現します。個々の成分には `color.r` のようにアクセスできます。色をベクトルとして扱うことで、ベクトル演算に基づく様々な興味深いエフェクトを実現できます。
{{% /notice %}}

```glsl
void fragment() {
    COLOR = vec4(UV.x, 0.0, 0.0, 1.0);
}
```

![alt](/godot_recipes/3.x/img/shader_intro_02.png)

現在の赤色チャンネルは、左側から右側にかけて「0」から「1.0」まで変化し、これは**UV座標**とともに変動します。

別の例：

```glsl
void fragment() {
    COLOR = vec4(UV.x, 1.0 - UV.y, 0.5, 1.0);
```

![alt](/godot_recipes/3.x/img/shader_intro_02a.png)

### 次のステップ

ピクセルカラーを直接設定するため、Godotアイコンのデータは破棄されています。テクスチャデータには`TEXTURE`入力と`texture()`関数を使用してアクセスできます。

```glsl
void fragment() {
    COLOR = texture(TEXTURE, UV);
}
```

これで元の画像に戻りました。各ピクセルの色は、それぞれの**UV**座標に対応するテクスチャの色値に設定されています。

また、`COLOR`出力の特定のチャンネルのみを変更することもできます。

```glsl
void fragment() {
    COLOR = texture(TEXTURE, UV);
    COLOR.a = 1.0 - UV.x;
}
```

![alt](/godot_recipes/3.x/img/shader_intro_03.png)

この操作によりアルファチャンネルの値が低下し、フェードアウト効果が得られます。

#### 時間で変動させる

もう一つの便利な組み込みシェーダープロパティは`TIME`で、現在の経過時間を表す増加し続ける値を提供します。さらに、範囲が`-1`から`1`である`sin()`関数も使用すると、以下のような効果が得られます。

```glsl
void fragment() {
    COLOR = texture(TEXTURE, UV);
    COLOR.a = abs(sin(TIME * 0.5));
}
```

![alt](/godot_recipes/3.x/img/shader_intro_04.gif)

またはこちら：

```glsl
void fragment() {
    COLOR = texture(TEXTURE, UV);
    COLOR.a = max(0.0, UV.x - abs(sin(TIME)));
}
```
![alt](/godot_recipes/3.x/img/shader_intro_05.gif)

### 頂点シェーダー

Vertex shaders alter the vertices of the object, allowing for deformations and scaling. Just as fragment shaders run on every pixel, vertex shaders run on every _vertex_ of an object. In a `canvas_item` shader, this typically means the four corners of the texture. In a `spatial` shader, it's each vertex of the mesh.

例えば、以下の例でどうなるか観察してみましょう。

```glsl
void vertex() {
    VERTEX.x += UV.x * 10.0;
}
```

![alt](/godot_recipes/3.x/img/shader_intro_06.png)

このシェーダーでは、左側の2つの頂点 `(0, 0)` と `(0, 1)` は変更されず、右側の頂点がそれぞれ `(10, 0)` と `/` 10, 1) に変わります。

頂点位置を時間経過に応じて変化させることで、さまざまな興味深い効果を生み出せます。

```glsl
void vertex() {
    VERTEX.y += sin(UV.x * TIME) * 10.0;
}
```

![alt](/godot_recipes/3.x/img/shader_intro_07.gif)

## ユニフォーム

To pass a value to the shader, you need a variable declared with the _uniform_ keyword. Once you do this, the variable appears in the Inspector in much the same way an `export` variable. However, a uniform's value *can not* be changed in the shader!

均一値（uniforms）はシェーダー全体でグローバルに使用可能であり、任意の関数からアクセスできます。

### ヒント

インスペクターで値を設定する際に補助として使用できるオプションの *ヒント* も利用できます。

```glsl
uniform float radius : hint_range(0, 1);
```

各種データ型に対応するヒントが用意されています。完全なリストについては [シェーダー言語リファレンス](https://docs.godotengine.org/ja/latest/tutorials/shading/shading_reference/shading_language.html#uniforms) を参照してください。

### まとめ

これはシェーダーで実現できる機能のほんの一例に過ぎません。このセクションの他のレシピも参照して、プロジェクトで使えるテクニックを増やしていきましょう。

## 関連するレシピ
