---
title: "コンベアベルト"
weight: 9
draft: false
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

キャラクターまたはリジッドボディを移動させるコンベアベルトオブジェクトを作成したい。

## 解決策

`constant_linear_velocity` プロパティを使用することで、{{< gd-icon StaticBody2D >}}`StaticBody2D`だけでコンベアベルトオブジェクトを作成できます。

{{% notice note %}}
この問題を3D環境で解決する方法については[以下を参照](#3d)ください。
{{% /notice %}}

以下に具体例を示します。{{< gd-icon StaticBody2D >}}`StaticBody2D`と{{< gd-icon RigidBody2D >}}`RigidBody2D`を使用しています。追加コードは一切ありません。スタティックボディの*線速度一定*は `(200, 0)` に設定されています。

![alt](/godot_recipes/4.x/img/conveyor_02.gif)

### ベルトの動きをアニメーション化

コンベアベルトの「外観」を表現する方法は、使用するアートアセットによって異なります。今回のデモプロジェクトでは、以下の単一サイズ88×88ピクセルのタイルマップのみを使用しています。

![alt](/godot_recipes/4.x/img/tileGreen_03.png)

スタティックボディに {{< gd-icon Sprite2D >}}`Sprite` を追加し、 *テクスチャ* セクションで「新規AtlasTexture」を選択してください。

![alt](/godot_recipes/4.x/img/conveyor_04.png)

タイルテクスチャをプロパティの*Texture*項目に配置し、*Region*を`(0, 0, 880, 88)`に設定してください。

![alt](/godot_recipes/4.x/img/conveyor_05.png)

「880」を選択すれば、幅が正確に10タイルのコンベアベルトを作成できます。必要な幅を自由に設定できます。

![alt](/godot_recipes/4.x/img/conveyor_06.png)

{{% notice tip %}}
画像が繰り返されていない、または表示がおかしい場合、*リピート* フラグを「有効」に設定して再インポートしてください。
{{% /notice %}}

*Region* プロパティの `x` の値を調整してみてください。タイルがずれるのが確認できるはずです。これがベルトのアニメーションに必要な動きです。このアニメーションは {{< gd-icon AnimationPlayer >}}`AnimationPlayer`を使用するか、コードで実装するかです。ここでは後者の方法を実演します。

```gdscript
extends StaticBody2D

@export var speed = 100

func _ready():
    constant_linear_velocity.x = speed

func _process(delta):
    $Sprite.texture.region.position.x -= speed * delta
```

このコードは、ベルトが目標速度で動作することと、アニメーションが物理効果と同期することを保証します。注意点として、方向は反対になっています。領域の `x` 値を増やすと画像は左方向に移動します。

![alt](/godot_recipes/4.x/img/conveyor_01.gif)

これはキャラクターボディに対しても完璧に動作します。同じコンベアベルトオブジェクトの追加する場合は、[プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character)を参照してください。

![alt](/godot_recipes/4.x/img/conveyor_07.gif)

### 3D

執筆時点では、`constant_linear_velocity`は{{< gd-icon StaticBody3D >}}`StaticBody`を使用した3D環境で正しく動作しません。

ただし、プロジェクト設定で「弾丸」から「GodotPhysics」エンジンに変更すれば、この手法を使用できます。

![alt](/godot_recipes/4.x/img/conveyor_03.png)

![alt](/godot_recipes/4.x/img/conveyor_3d.gif)

## 関連レシピ

- [プラットフォームキャラクターの実装方法](/godot_recipes/4.x/ja/2d/platform_character)
- [CharacterBody2Dコンポーネントの活用法](/godot_recipes/4.x/ja/physics/godot3_kinematic2d/)
- [移動式プラットフォームの作成テクニック](/godot_recipes/4.x/ja/2d/moving_platforms/)