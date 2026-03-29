---
title: "プラットフォームキャラクター"
weight: 1
draft: false
ghcommentid: 16
---

## 課題

2Dプラットフォーマースタイルのキャラクターを作成したいです。

## 解決策

経験が少ない開発者は、プラットフォームキャラクターをプログラミングするのがいかに複雑かを知って驚くことがよくあります。Godotには組み込みツールが用意されているものの、ゲームごとに解決策が異なるため、万能な答えはありません。このチュートリアルでは、ダブルジャンプやしゃがみ動作、ウォールジャンプ、アニメーションといった機能について詳しく掘り下げることはしません。ここではプラットフォーマー移動の基本原理に焦点を当てます。他の課題については、残りのレシピを参照してください。

{{% notice tip %}}
{{< gd-icon \ RigidBody2D >}}`\ RigidBody2D` を使用してプラットフォーマーキャラクターを作成することはできますが、ここでは {{< gd-icon \ CharacterBody2D >}}`\ CharacterBody2D` に焦点を当てます。運動制御ボディはプラットフォームゲームに最適です。このようなゲームでは、リアルな物理挙動よりも反応の良いアーケードライクな操作感が重視されるためです。
{{% /notice %}}

まず `\ CharacterBody2D` ノードを作成し、その上に `Sprite2D` と `CollisionShape2D` を追加してください。

以下のスクリプトをキャラクターノードのルートに追加してください。なお、ここでは[インプットマップ]で定義した入力アクション（`"walk_right"`、`"walk_left"`、および `"jump"`）を使用しています。詳細は [入力Actions](/godot_recipes/4.x/ja/input/input_actions/) をご覧ください。

```gdscript
extends CharacterBody2D

@export var speed = 1200
@export var jump_speed = -1800
@export var gravity = 4000


func _physics_process(delta):
    # Add gravity every frame
    velocity.y += gravity * delta

    # Input affects x axis only
    velocity.x = Input.get_axis("walk_left", "walk_right") * speed

    move_and_slide()

    # Only allow jumping when on the ground
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_speed
```

「speed」、「gravity」、「jump_speed」に用いる値は、プレイヤースプライトのサイズに大きく依存します。このサンプルではプレイヤーテクスチャが `108x208` ピクセルです。もしスプライトが小さい場合は、より小さい値を使用が必要です。また、ゲーム操作が速く反応するように、適切な高数値を設定することが重要です。重力を低く設定すると浮遊感の強いゲームプレイになり、逆に高く設定するとすぐに地面に戻って再びジャンプできる状態になります。

※ここで注意：`move_and_slide()` を使用した後に `is_on_floor()` をチェックしています。`move_and_slide()` 関数はこのメソッドの値を設定するため、その前にチェックすると前フレーム時点の値が取得されてしまう点にご注意ください。

### 摩擦力と加速度について

上記のコードは優れた出発点であり、これを基盤として多種多様なプラットフォームコントローラーを実装できます。ただし一つ欠点として、移動が瞬間的に行われる点が挙げられます。より自然な操作感を得るには、キャラクターが最大速度まで徐々に加速し、入力がなくなると自然に減速して停止する仕組みの方が適切です。

この動作を実現する効果的な方法の一つが線形補間(lerp）を使用することです。移動中は現在速度と最大速度の間で補間し、停止時は現在速度から0まで補間します。補間量を調整することで、さまざまな移動スタイルを実現できます。

{{% notice tip %}}
線形補間の概要については、[ゲーム数学：補間](/godot_recipes/4.x/ja/math/interpolation/)をご覧ください。
{{% /notice %}}

```gdscript
extends CharacterBody2D

@export var speed = 1200
@export var jump_speed = -1800
@export var gravity = 4000
@export_range(0.0, 1.0) var friction = 0.1
@export_range(0.0 , 1.0) var acceleration = 0.25


func _physics_process(delta):
    velocity.y += gravity * delta
    var dir = Input.get_axis("walk_left", "walk_right")
    if dir != 0:
        velocity.x = lerp(velocity.x, dir * speed, acceleration)
    else:
        velocity.x = lerp(velocity.x, 0.0, friction)

    move_and_slide()
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_speed
```

「摩擦係数」 と 「加速度」 の値を変更して、ゲームの操作性にどのような影響があるか試してみましょう。例えば氷ステージの場合、これらの値を非常に低く設定することで、キャラクターの動きがより鈍くなるように調整できます。

![alt](/godot_recipes/4.x/img/platformer1.gif)

## 結論

このコードは、独自のプラットフォームコントローラーを構築するための基礎を提供します。壁ジャンプなどのより高度なプラットフォーマー機能については、本セクションの他のレシピを参照してください。

<!--
このレシピを使用したサンプルプロジェクトをダウンロードするには：

{{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。[platform_character.zip](/godot_recipes/4.x/files/platform_charactor4.zip)
{{% /notice %}} -->

<!-- ## 関連レシピ -->

<!-- - [入力入門](/godot_recipes/4.x/ja/input/input_intro/)
- [キネマティック摩擦](/godot_recipes/4.x/ja/physics/kinematic_friction/) -->

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードしてください。[https://github.com/godotrecipes/2d_platform_basic](https://github.jp/godotrecipes/2d_platform_basic)
