---
title: "スプライトシートアニメーション"
weight: 1
draft: false
---

## 課題

2Dアニメーションを含むスプライトシートを使いたい。

## 解決策

スプライトシートは2Dアニメーションの一般的な配布形式です。単一の画像ファイルに全てのアニメーションフレームを集約した形式で、効率的なデータ管理ができます。

このデモでは、Elthen氏制作の優れた「冒険者」スプライトを使用します。このアセットをはじめ、多くの高品質なアート素材は以下から入手できます。[https://elthen.itch.io/](https://elthen.itch.io/)

![alt](/godot_recipes/4.x/img/adventurer_sprite_sheet_v1.1.png)

{{% notice warning %}}
Godotが自動的に画像を切り分けできるように、スプライトシート内の画像は均一なグリッド状に配置してください。不規則に配置されている場合、ここで説明する手法は使用できませんのでご注意ください。
{{% /notice %}}

### ノード設定

このアニメーション手法では、`Sprite2D`ノードを使用してテクスチャを表示し、その後`アニメーションPlayer`でフレームの切り替えをアニメーション化します。これはあらゆる2Dノードで使用できますが、ここではデモンストレーション用に`CharacterBody2D`ノードを使用しています。

以下のノードをシーンに追加してください。

```
{{< gd-icon CharacterBody2D >}}CharacterBody2D: Player
  {{< gd-icon Sprite2D >}} Sprite2D
  {{< gd-icon CollisionShape2D >}} CollisionShape2D
  {{< gd-icon AnimationPlayer >}} AnimationPlayer
```

Drag the spritesheet texture into the _Texture_ property of the {{< gd-icon Sprite2D >}}`Sprite2D`. You'll see the entire spritesheet displayed in the viewport. To slice it up into individual frames, expand the "アニメーション" section in the Inspector and set the _Hframes_ to `13` and _Vframes_ to `8`. _Hframes_ and _Vframes_ are the number of horizontal and vertical frames in your spritesheet.

![alt](/godot_recipes/4.x/img/sprite_animation_01.png)

Try changing the _Frame_ property to see the image change. This is the property we’ll be animating.

### アニメーションの追加方法

以下の手順に従ってアニメーションを設定します。

1. 「アニメーションPlayer」コンポーネントを選択します。
2. 「アニメーション」ボタンをクリックし、続いて「新規作成」を選択します。
3. 新しいアニメーションに「idle」という名前を付けます。
4. アニメーションの長さを `2` に設定します。
5. 「ループ」ボタンをクリックして、アニメーションが繰り返し再生されるようにします（詳細は以下を参照）。

With the scrubber at time `0`, select the {{< gd-icon Sprite2D >}}`Sprite2D` node. Set its _Animation/Frame_ to `0`, then click the key icon next to the value.

![alt](/godot_recipes/4.x/img/sprite_animation_02.png)

アニメーションを再生してみると、何も変化がないように見えます。これは最後のフレーム（12）が最初のフレーム（0）と全く同じ表示になっているためで、その間のフレーム（1～11）が全く反映されていないからです。これを修正するには、トラックの「更新モード」をデフォルト値の「離散」から「連続」に変更してください。このボタンはトラック右側の端に配置されています。

![alt](/godot_recipes/4.x/img/sprite_animation_03.png)

Note that this will only work for spritesheets where the frames are already in order. If they are not, you'll have to keyframe each _Frame_ seperately along the timeline.

![alt](/godot_recipes/4.x/img/sprite_animation_04.gif)

自由に他のアニメーションを追加してください。例えば「ジャンプ」アニメーションはフレーム 65～70 に設定されています。

## 関連レシピ

- [プラットフォームキャラクター](http://kidscancode.org/godot_recipes/2d/platform_character/)
 <!-- - [アニメーション状態のコントロール](http://kidscancancode.org/godot_recipes/animation/animation_state_machine/) -->