---
title: "Spritesheet animation"
weight: 1
draft: false
---

## 問題文

あなたは2Dアニメーションを含むスプライトシートを使用したいと考えています。

## 解決策

スプライトシートは2Dアニメーションの一般的な配布形式です。単一の画像ファイルに全てのアニメーションフレームを集約した形式で、効率的なデータ管理が可能です。

For this demo, we'll be using the excellent "Adventurer" sprite by Elthen. You can get this and lots of other great art at[https://elthen.itch.io/](https://elthen.itch.io/).

![alt](/godot_recipes/4.x/img/adventurer_sprite_sheet_v1.1.png)

{{% notice warning %}}
スプライトシート内の画像は均一なグリッド状に配置してください。これによりGodotが自動的に画像を切り分け可能になります。不規則に配置されている場合、以下の手法は使用できませんのでご注意ください。
{{% /notice %}}

### ノード設定

このアニメーション手法では、`Sprite2D`ノードを使用してテクスチャを表示し、その後`AnimationPlayer`でフレームの切り替えをアニメーション化します。これはあらゆる2Dノードで使用可能ですが、ここではデモンストレーション用に`CharacterBody2D`ノードを使用しています。

以下のノードをシーンに追加してください：

```
{{< gd-icon CharacterBody2D >}}CharacterBody2D: Player
  {{< gd-icon Sprite2D >}} Sprite2D
  {{< gd-icon CollisionShape2D >}} CollisionShape2D
  {{< gd-icon AnimationPlayer >}} AnimationPlayer
```

Drag the spritesheet texture into the _Texture_ property of the {{< gd-icon Sprite2D >}}`Sprite2D`. You'll see the entire spritesheet displayed in the viewport. To slice it up into individual frames, expand the "Animation" section in the Inspector and set the _Hframes_ to `13` and _Vframes_ to `8`. _Hframes_ and _Vframes_ are the number of horizontal and vertical frames in your spritesheet.

<img src=\ alt=\
>

以下の手順を試してみてください：
1. 画像フレームプロパティを変更すると、画像がどのように変化するかを確認できます。これは後でアニメーション化するプロパティです。

### アニメーションの追加方法

Select the {{< gd-icon AnimationPlayer >}}`AnimationPlayer` and click the “Animation” button followed by “New"
. Name the new animation “idle”. Set the animation length to `2` and click the “Loop” button so that our animation will repeat (see below).

スクラバーが「0」時点で、{{< gd-icon Sprite2D >}}`Sprite2D`ノードを選択します。アニメーションのフレーム番号を「0」に設定し、値の隣にあるキーアイコンをクリックします。

![alt](/godot_recipes/4.x/img/sprite_animation_02.png)

If you try playing the animation, you'll see it doesn't appear to do anything. That's because the last frame (12) looks the same as the first (0), but we're not seeing any of the frames in-between (1-11). To fix this, change the "Update Mode" of the track from its default value of "Discrete" to "Continuous". You can find this button at the end of the track on the right side.

![alt](/godot_recipes/4.x/img/sprite_animation_03.png)

※この方法が有効なのは、フレームがすでに順序通りに並んでいることが前提です。そうでない場合は、タイムライン上で各_Frameを個別にキーフレーム化する必要があります。

<img src=\ alt=\>

Feel free to add the other animations yourself. For example, the "jump" animation is on frames `65` through `70`.

## 関連レシピ

<!-- - [Top-down character](http://kidscancode.org/godot_recipes/2d/topdown_movement/#option-1-8-way-movement) -->
- [プラットフォームキャラクター操作](http://kidscancode.org/godot_recipes/2d/platform_character/)
<!-- - [Controlling animation states](http://kidscancode.org/godot_recipes/animation/animation_state_machine/) -->