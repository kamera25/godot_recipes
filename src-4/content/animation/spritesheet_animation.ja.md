---
title: "スプライトシートアニメーション"
weight: 1
draft: false
---

## 今回のお題

2Dアニメーションを含むスプライトシートを使いたい。

## 作り方

スプライトシートは2Dアニメーションの一般的な配布形式です。単一の画像ファイルに全てのアニメーションフレームを集約した形式で、効率的なデータ管理ができます。

このデモでは、Elthen氏制作の優れた「冒険者」スプライトを使用します。このアセットをはじめ、多くの高品質なアート素材は以下から入手できます。[https://elthen.itch.io/](https://elthen.itch.io/)

![alt](/godot_recipes/4.x/img/adventurer_sprite_sheet_v1.1.png)

{{% notice warning %}}
Godotが自動的に画像を切り分けできるように、スプライトシート内の画像は均一なグリッド状に配置します。不規則に配置されている場合、ここで説明する手法は使用できませんのでご注意ください。
{{% /notice %}}

### ノード設定

このアニメーション手法では、{{< gd-icon Sprite2D >}}`Sprite2D`ノードを使用してテクスチャを表示し、その後{{< gd-icon AnimationPlayer >}}`AnimationPlayer`でフレームの切り替えをアニメーション化します。これはあらゆる2Dノードで使用できますが、ここではデモンストレーション用に{{< gd-icon CharacterBody2D >}}`CharacterBody2D`ノードを使用しています。

以下のノードをシーンに追加します。

```
{{< gd-icon CharacterBody2D >}}CharacterBody2D: Player
  {{< gd-icon Sprite2D >}} Sprite2D
  {{< gd-icon CollisionShape2D >}} CollisionShape2D
  {{< gd-icon AnimationPlayer >}} AnimationPlayer
```

{{< gd-icon Sprite2D >}}`Sprite2D`コンポーネントの _Texture_ プロパティにスプライトシートテクスチャをドラッグ＆ドロップします。ビューポート内にすべてのスプライトシートが表示されます。個別のフレームに分割するには、インスペクターの「Animation」セクションを展開し、 _Hframes_ を `13`、 _Vframes_ を `8`に設定します。_Hframes_ と _Vframes_ は、それぞれ水平方向および垂直方向のフレーム数を指定するパラメーターです。

![alt](/godot_recipes/4.x/img/sprite_animation_01.png)

_Frame_ プロパティを変更してみて、画像がどのように変化するか見てみてください。これは後ほどアニメーション化するプロパティです。

### アニメーションの追加方法

以下の手順に従ってアニメーションを設定します。

1. 「{{< gd-icon AnimationPlayer >}}`AnimationPlayer`コンポーネントを選択します。
2. 「アニメーション」ボタンをクリックし、続いて「新規作成」を選択します。
3. 新しいアニメーションに「idle」という名前を付けます。
4. アニメーションの長さを `2` に設定します。
5. 「ループ」ボタンをクリックして、アニメーションが繰り返し再生されるようにします（詳細は以下を参照）。

スクラバーが`0`時点で、{{< gd-icon Sprite2D >}}`Sprite2D`ノードを選択します。アニメーションのフレーム番号を`0`に設定し、値の隣にあるキーアイコンをクリックします。

![alt](/godot_recipes/4.x/img/sprite_animation_02.png)

アニメーションを再生してみると、何も変化がないように見えます。これは最後のフレーム（12）が最初のフレーム（0）と全く同じ表示になっているためで、その間のフレーム（1～11）が全く反映されていないからです。これを修正するには、トラックの「更新モード」をデフォルト値の「離散」から「連続」に変更します。このボタンはトラック右側の端に配置されています。

![alt](/godot_recipes/4.x/img/sprite_animation_03.png)

この方法が有効なのは、フレームがすでに順序通りに並んでいることが前提です。そうでない場合は、タイムライン上で各 _Frame_ を個別にキーフレーム化が必要です。

![alt](/godot_recipes/4.x/img/sprite_animation_04.gif)

自由に他のアニメーションを追加します。例えば「ジャンプ」アニメーションはフレーム `65`～`70` に設定されています。

## 関連レシピ

- [プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)
<!-- - [アニメーション状態のコントロール](/godot_recipes/4.x/ja/animation/animation_state_machine/) -->