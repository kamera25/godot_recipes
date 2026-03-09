---
title: "Spritesheet animation"
weight: 1
draft: false
---

## 問題文

あなたは2Dアニメーションを含むスプライトシートを使用したいと考えています。

## 解決策

スプライトシートは2Dアニメーションの一般的な配布形式です。単一の画像ファイルに全てのアニメーションフレームを集約した形式で、効率的なデータ管理が可能です。

このデモでは、Elthen氏制作の優れた「冒険者」スプライトを使用します。このアセットをはじめ、多くの高品質なアート素材は以下から入手できます：[https://elthen.itch.io/](https://elthen.itch.io/)。

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

{{< gd-icon Sprite2D >}}`Sprite2D`コンポーネントの _Texture_プロパティにスプライトシートテクスチャをドラッグ＆ドロップしてください。ビューポート内に完全なスプライトシートが表示されます。個別のフレームに分割するには、インスペクターの「Animation」セクションを拡大し、_Hframes_を `13`、_Vframes_を `8`に設定します。_Hframes_と_Vframes_は、それぞれ水平方向および垂直方向のフレーム数を指定するパラメータです。

<img src="/godot_recipes/4.x/img/sprite_animation_01.png" alt="Sprite Animation 01">

以下の手順を試してみてください：
1. 画像フレームプロパティを変更すると、画像がどのように変化するかを確認できます。これは後でアニメーション化するプロパティです。

### アニメーションの追加方法

以下の手順に従ってアニメーションを設定します：

1. 「AnimationPlayer」コンポーネントを選択します。
2. 「アニメーション」ボタンをクリックし、続いて「新規作成」を選択します。
3. 新しいアニメーションに「idle」という名前を付けます。
4. アニメーションの長さを `2` に設定します。
5. 「ループ」ボタンをクリックして、アニメーションが繰り返し再生されるようにします（詳細は以下を参照）。

スクラバーが「0」時点で、{{< gd-icon Sprite2D >}}`Sprite2D`ノードを選択します。アニメーションのフレーム番号を「0」に設定し、値の隣にあるキーアイコンをクリックします。

![alt](/godot_recipes/4.x/img/sprite_animation_02.png)

アニメーションを再生してみると、何も変化がないように見えます。これは最後のフレーム（12）が最初のフレーム（0）と全く同じ表示になっているためで、その間のフレーム（1～11）が全く反映されていないからです。これを修正するには、トラックの「更新モード」をデフォルト値の「離散」から「連続」に変更してください。このボタンはトラック右側の端に配置されています。

![alt](/godot_recipes/4.x/img/sprite_animation_03.png)

※この方法が有効なのは、フレームがすでに順序通りに並んでいることが前提です。そうでない場合は、タイムライン上で各_Frameを個別にキーフレーム化する必要があります。

<img src="/godot_recipes/4.x/img/sprite_animation_04.gif" alt="スプライトアニメーション">

自由に他のアニメーションを追加してください。例えば「ジャンプ」アニメーションはフレーム 65～70 に設定されています。

## 関連レシピ

<!-- - [Top-down character](http://kidscancode.org/godot_recipes/2d/topdown_movement/#option-1-8-way-movement) -->
- [プラットフォームキャラクター操作](http://kidscancode.org/godot_recipes/2d/platform_character/)
<!-- - [Controlling animation states](http://kidscancode.org/godot_recipes/animation/animation_state_machine/) -->