---
title: "アーケード風宇宙船"
weight: 9
draft: false
ghcommentid: 97
tags: []
---

## 課題

アーケード／映画のようなスタイルで飛行する3D宇宙船を作りたい。リアルな物理演算は求めず、ドッグファイト主体の『スター・ウォーズ』風の宇宙戦闘スタイルで。

## 解決策

この機能を実現するため、船のモデルには {{< gd-icon CharacterBody3D >}}`CharacterBody3D` クラスを使用します。ピッチ（前後傾斜）、ロール（横転）、ヨー（回転）の3軸入力により、それぞれ対応する軸を中心にボディの基底ベクトルが回転します。移動方向は常に前方を指すようになっています。

{{% notice note %}}
これは{{< gd-icon RigidBody3D >}}`RigidBody3D`を使用することで実現可能で、同様の結果が得られます。以下にリンクするサンプルプロジェクトでは、リジッドボディ版も含まれていますので、ぜひご参照ください。
{{% /notice %}}

### アセット

宇宙船モデルは以下のアセットパックに含まれています。

[Quaternius 制作「Ultimate Spaceships Pack」](https://quaternius.com/packs/ultimatespaceships.html)

「処刑人」級の艦船モデルを選択しました。

![alt](/godot_recipes/4.x/img/3d_ship_01.png)

ご自由にお好みのデザインをお選びください。

### 設定手順

操作対象の宇宙船に対応する `gltf` ファイルを選択し、*インポート*タブをクリックしてください。*ルートタイプ*を {{< gd-icon CharacterBody3D >}} `CharacterBody3D` に変更します。次に『再インポート』をクリックします。その後、`gltf`ファイルをダブルクリックすると、新しいシーンが生成され、その中に {{< gd-icon KinematicBody3D >}} `CharacterBody3D` をルートとする子オブジェクトとして {{< gd-icon MeshInstance3D >}} `MeshInstance` が表示されます。ボディに {{< gd-icon CollisionShape3D >}} `CollisionShape3D`を追加してください。

*プロジェクト設定 > インプットマップ* にて、以下の入力を設定してください。

* `roll_right` / `roll_left` （ロール操作）
* `pitch_up` / `pitch_down` （ピッチ操作）
* `yaw_right` / `yaw_left` （ヨー操作）
* `throttle_up` / `throttle_down` （スロットル操作）

キーまたはコントローラー入力を割り当てることができます。アナログスティックの入力が最も適しています。

### 移動

スクリプトを起動するには、前進動作を処理します。スロットルボタンを滑らかに押すと、速度が段階的に増減します。

```gdscript
extends CharacterBody

@export var max_speed = 50.0
@export var acceleration = 0.6

var forward_speed = 0

func get_input(delta):
    if Input.is_action_pressed("throttle_up"):
        forward_speed = lerp(forward_speed, max_speed, acceleration * delta)
    if Input.is_action_pressed("throttle_down"):
        forward_speed = lerp(forward_speed, 0, acceleration * delta)

func _physics_process(delta):
    get_input(delta)
    velocity = -transform.basis.z * forward_speed
    move_and_collide(velocity * delta)
```

テスト用シーンを作成し、{{< gd-icon Camera3D >}}`Camera3D` コンポーネントを試してみます。固定カメラを使用するか、［追従カメラ](/godot_recipes/4.x/ja/3d/interpolated_camera/) を採用することもできます。宇宙船が加速と減速を適切に行うことを確認した上で、次のステップに進んでください。

![alt](/godot_recipes/4.x/img/3d_ship_02.gif)

### 回転角度設定

現在、3軸方向の回転処理が対応可能になりました。以下の変数をスクリプトの先頭に追加してください。

```gdscript
@export var pitch_speed = 1.5
@export var roll_speed = 1.9
@export var yaw_speed = 1.25

var pitch_input = 0.0
var roll_input = 0.0
var yaw_input = 0.0
```

三軸速度は艦船の「操作性」に直接影響を及ぼします。最適なフライトのために、ぜひ試行錯誤してみてください。

次に、`get_input()` 関数に以下の行を追加して3軸入力を取得します。

```gdscript
pitch_input = Input.get_axis("pitch_down", "pitch_up")
roll_input = Input.get_axis("roll_right", "roll_left")
yaw_input = Input.get_axis("yaw_right", "yaw_left")
```

Finally, we need to rotate the ship's `Basis` according to the inputs. Note how each input affects one axis of rotation:

```gdscript
transform.basis = transform.basis.rotated(transform.basis.z,
    roll_input * roll_speed * delta)
transform.basis = transform.basis.rotated(transform.basis.x,
    pitch_input * pitch_speed * delta)
transform.basis = transform.basis.rotated(transform.basis.y,
    yaw_input * yaw_speed * delta)
transform.basis = transform.basis.orthonormalized()
```

![alt](/godot_recipes/4.x/img/3d_ship_04.gif)

### 改善点

現在の回転モーションは少し「ぎこちない」感じがします。船が瞬時に回転を開始したり停止したりするため、やや不自然な動きになっています。これは `lerp()` 関数を使うことで改善できます。さらに、コントロールの「浮遊感」を調整する設定変数を設けることでより自然な挙動を実現できるでしょう。

```gdscript
@export var input_response = 8.0
```

以下の内容に従って、`get_input()` 内の 3 軸入力を変更してください。

```gdscript
pitch_input = lerp(pitch_input, Input.get_axis("pitch_down", "pitch_up"),
        input_response * delta)
roll_input = lerp(roll_input, Input.get_axis("roll_right", "roll_left"),
        input_response * delta)
yaw_input = lerp(yaw_input, Input.get_axis("yaw_right", "yaw_left"),
        input_response * delta)
```

今は停止や方向転換時に、わずかな慣性が働くようになっています。

![alt](/godot_recipes/4.x/img/3d_ship_03.gif)

### ロール/ヨー軸の連動設定

この操作体系には1つの問題点があります。それは操作性に難がある点です。ヨーの入力に別途スティックを必要とするため、特に射撃や他のコントロールと組み合わせた場合、スムーズな操作が困難になります。多くのゲームでは、この問題を解決するためにロール入力と連動して少量のヨー回転も発生させる仕様にしています。これを実装するには、`yaw_speed`を`roll_speed`の1/4～1/2程度に設定するのが適切です。

In the `get_input()` function, change the line getting `yaw_input` to the following:

```gdscript
yaw_input = roll_input
```

ロールとヨーの速度を調整することで、ゲームプレイに変化をもたらす楽しい実験ができます。例えば、ヨーを主要軸としロールを小さくした場合、どのような挙動になるでしょうか？他の軸と連動させるとどう変わるでしょう？もしゲームに複数種類の船が登場するなら、それぞれ異なる値を設定することで、飛行スタイルや性能にバリエーションを持たせることができます。

### まとめ

これで準備完了！飛行できます！このコントローラーは、思い描く宇宙ゲームを始めるのに最適なスタート地点です。さらに機体やエフェクトをいくつか追加すれば、いよいよ本番モードに突入できます。

<video width="500" controls src="/godot_recipes/4.x/img/3d_ship_05.webm"></video>

### 全スクリプト

以下に全てのスクリプトを示します。

```gdscript
extends CharacterBody3D

@export var max_speed = 50.0
@export var acceleration = 0.6
@export var pitch_speed = 1.5
@export var roll_speed = 1.9
@export var yaw_speed = 1.25  # Set lower for linked roll/yaw
@export var input_response = 8.0

var forward_speed = 0.0
var pitch_input = 0.0
var roll_input = 0.0
var yaw_input = 0.0

func get_input(delta):
    if Input.is_action_pressed("throttle_up"):
        forward_speed = lerp(forward_speed, max_speed, acceleration * delta)
    if Input.is_action_pressed("throttle_down"):
        forward_speed = lerp(forward_speed, 0.0, acceleration * delta)

    pitch_input = lerp(pitch_input, Input.get_axis("pitch_down", "pitch_up"),
            input_response * delta)
    roll_input = lerp(roll_input, Input.get_axis("roll_right", "roll_left"),
            input_response * delta)
    # yaw_input = lerp(yaw_input, Input.get_axis("yaw_right", "yaw_left"),
            input_response * delta)
    yaw_input = roll_input

func _physics_process(delta):
    get_input(delta)
    transform.basis = transform.basis.rotated(transform.basis.z,
            roll_input * roll_speed * delta)
    transform.basis = transform.basis.rotated(transform.basis.x,
            pitch_input * pitch_speed * delta)
    transform.basis = transform.basis.rotated(transform.basis.y,
            yaw_input * yaw_speed * delta)
    transform.basis = transform.basis.orthonormalized()
    velocity = -transform.basis.z * forward_speed
    move_and_collide(velocity * delta)
```

<!-- {{% notice note %}}
    プロジェクトファイルをこちらからダウンロードしてください。[https://github.com/kidscancode/3d_spaceship_demo](https://github.com/kidscancode/3d_spaceship_demo)
    {{% /notice %}} -->


## 関連レシピ

- [補間カメラの実装](/godot_recipes/4.x/ja/3d/interpolated_camera/)


<!-- #### Videoが気に入ったら？ -->

{{< youtube 8oywBn_bLeU >}} -->

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらでダウンロードできます。[https://github.com/godotrecipes/3d_spaceship](https://github.com/godotrecipes/3d_spaceship)
