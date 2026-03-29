---
title: "CharacterBody3Dの移動"
weight: 4
draft: false
ghcommentid: 34
---

## 課題

プレイヤー操作可能な3Dキネマティックボディが要ります。

## 解決策

このレシピでは、こちらの可愛らしいタンクモデルを使用します。

![alt](/godot_recipes/3.x/img/3d_kinematic_01.png)

このモデルは[Itch.io](https://gtibo.itch.io/mini-tank)で入手できます。他のお好きなモデルを使用しても構いません。ここでは戦車固有の機能は特に実装しません。

モデルをシーンに追加することはできますが、以下の追加ノードが必要となります：

![alt](/godot_recipes/3.x/img/3d_kinematic_02.png)

For the collision shape, we're just going to use a `BoxShape` aligned and sized with the tank's treads. `CamPos` is a {{< gd-icon Marker3D >}}`Marker3D` we'll use to place our following camera. It's placed behind and above the tank, angled down.

また、個別の {{< gd-icon MeshInstance3D >}}`MeshInstance` ノードを **Y** 軸を中心に `180` 度回転させました。これは元々 **+Z** 方向を向いてモデル化されていたためですが、Godot では **-Z** が前方方向となるため、戦車が逆向きに見えるようにはしたくないからです。

スクリプトを追加する前に、「プロジェクト設定」を開き、「インプットマップ」タブで以下の入力を追加してください。

入力操作 | キー
:------------|:---
前進 | **W**
後退 | **S**
右移動 | **D**
左移動 | **A**

それでは、必要な変数から始めつつ、スクリプトを追加しましょう。

```gdscript
extends CharacterBody3D

@export var gravity = Vector3.DOWN * 10
@export var speed = 4
@export var rot_speed = 0.85

var velocity = Vector3.ZERO
```

`speed` は戦車の移動速度（前進/後退）を、`rot_speed` は旋回速度をそれぞれ定義します。

{{% notice tip %}}
`export` を使ってプロパティを宣言すると、インスペクタで簡単に調整できるようになります。
{{% /notice %}}

Using the `CharacterBody3D.move_and_slide()` method makes our movement code quite simple:

```gdscript
func _physics_process(delta):
    velocity += gravity * delta
    get_input(delta)
    velocity = move_and_slide(velocity, Vector3.UP)
```

このコードでは、重力による下方向への加速度を現在速度に加算し、ユーザー入力を取得し（詳細は後述）、move_and_slide()関数を呼び出しています。この時、velocity変数と上方向を示すベクトル(0, 1)をup_directionパラメータとして渡しています。

{{% notice tip %}}
`move_and_slide()` から返される `velocity` ベクトルを必ず取得してください。これを行わないと、物体が表面に沿って滑る動きの利点が得られなくなります。
{{% /notice %}}

次に必要なのは `get_input()` 関数を定義することです。ここでは入力操作を処理して適用します。

```gdscript
func get_input(delta):
    var vy = velocity.y
    velocity = Vector3.ZERO
    if Input.is_action_pressed("forward"):
        velocity += -transform.basis.z * speed
    if Input.is_action_pressed("back"):
        velocity += transform.basis.z * speed
    if Input.is_action_pressed("right"):
        rotate_y(-rot_speed * delta)
    if Input.is_action_pressed("left"):
        rotate_y(rot_speed * delta)
    velocity.y = vy
```

これをもう少し詳しく見ていきましょう。プレイヤー入力は水平方向の移動に影響を与えるべきです。地面に沿った前後移動と、戦車の中心周りの回転です。**Y軸方向**の移動は、重力の影響を受けるべきものであり、つまり毎フレーム`0`に設定すべきではありません。これが、新しい速度ベクトルを水平移動用に割り当てる間、その値を一時的に保持するために`vy`変数を使用している理由です。そして最後に、この値を新たに追加します。

前方/後方移動にはキャラクターのローカル座標系の Z 軸を使用しています。
これにより、身体の「ローカル」前方方向へ正しく移動します。

以下が実際に動作するタンクのシーンです。テスト環境として、地面には{{< gd-icon StaticBody3D >}}`StaticBody`平面を、カメラには戦車の`CamPos`座標を参照するように設定した{{< gd-icon Camera3D >}}`InterpolatedCamera`を配置しました。

<video controls src="/godot_recipes/3.x/img/3d_kinematic_03.webm"></video>

## まとめ

これはあらゆる種類の運動学的キャラクターの動作基盤です。ここからジャンプ、射撃、AI挙動などを追加できます。このレシピを拡張した具体例については、関連するレシピを参照してください。

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。 [floating_text.zip](/godot_recipes/4.x/ja/files/floating_text.zip)
{{% /notice %}} -->

## 関連レシピ

- [3D入門](/godot_recipes/4.x/ja/g101/3d/)
- [入力アクション](/godot_recipes/4.x/ja/input/input_actions/)

#### この動画が気に入ったら？

{{< youtube rOA8i_clm1Y >}}
