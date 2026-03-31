---
title: "3Dで自動車を作ろう：ベースモデル"
weight: 1
draft: false
ghcommentid: 41
---

## Problem

3Dドライビング/レーシングゲームを作りたいが、どこから手をつければいいかわからない。

## Solution

{{% notice note %}}
3D環境においても、車両は基本的に地面に留まる性質があります。このため、移動処理の多くは実質的に2Dと同様の扱いができます。車の動作コードの大部分は、[2D用カーステアリングレシピ](/godot_recipes/4.x/ja/2d/car_steering)と非常に似た構造になります。このチュートリアルに進む前に、必ずそのレシピを確認しておくことをオススメします。
{{% /notice %}}

Godot does provide a {{< gd-icon VehicleBody3D >}}`VehicleBody` node, which is based on {{< gd-icon RigidBody3D >}}`RigidBody` and includes a complex simulation of engine, braking, suspension, etc. However, this introduces a lot of complexity and tends to be overkill for most casual racing/driving games. For that reason, we're going with a CharacterBody3D based solution here.

{{% notice info %}}
VehicleBody3D`車両ボディ`の操作方法について詳しく知りたい方には、[Bastiaan Olij氏によるこのシリーズ動画](https://youtu.be/B5vE-nNszxA)を強くオススメします。
{{% /notice %}}

### 車両設定手順

コーディングを開始する前に、まず自動車の3Dモデルを見つけてGodotにインポートする必要があります。

#### モデルのインポート方法

以下はこのデモンストレーションで使用する車両モデルです。

![alt](/godot_recipes/3.x/img/3d_car_01.png)

{{% notice note %}}
ケンニーの『カーキット』でこの車種やその他のモデルを見つけることができます。以下のリンクから入手できます。
[https://kenney.nl/assets/car-kit](https://kenney.nl/assets/car-kit)。キット全体をダウンロードすれば、後で他の車両も使用できます。
{{% /notice %}}

車を読み込むには、`"Models/GLTF format"`フォルダ内で該当モデルを探してください。今回は`sedanSports.glb`を使用します。このファイルを新規Godotプロジェクトにインポートし、できれば`res://assets/cars/`のような専用フォルダにまとめておくと良いでしょう。

Select the file in Godot and go to the "Import" tab. Change the _Root Type_ to "CharacterBody3D" and click "Reimport". Now we're ready to use this car.

#### Setting up the {{< gd-icon KinematicBody3D >}} CharacterBody3D

`sedanSports.glb`ファイルをダブルクリックし、「新規継承」を選択してください。以下のように新しいシーンが作成されます。

![alt](/godot_recipes/3.x/img/3d_car_02.png)

Note the individual meshes for each of the car's parts. There's also a stray "tmpParent" {{< gd-icon Node3D >}}`Node3D` node, but we can ignore that.

The {{< gd-icon KinematicBody3D >}}`CharacterBody3D` has a warning about missing collision shapes, so we'll need to fix that first. We're going to add 3 {{< gd-icon CollisionShape3D >}}`CollisionShape`s: a {{< gd-icon BoxShape3D >}}`BoxShape` for the car's body, and a {{< gd-icon CylinderShape3D >}}`CylinderShape` for each of the front and rear axles.

形状設定が完了したら、以下のような表示になるはずです。

![alt](/godot_recipes/3.x/img/3d_car_03.png)

{{% notice tip %}}
前面と背面の形状を一致させるには、どちらか一方を作成してサイズ設定した後、複製するだけで構いません。また、各ノードに適切な名前を付けることをオススメします。{{< gd-icon CollisionShape3D >}}`CollisionShape`ノードには `CollisionBody`、`CollisionWheelsFront`、`CollisionWheelsRear`といった名称が適切でしょう。
{{% /notice %}}

### 基本スクリプト

人間が操作する場合とAIが制御する場合の両方に対応できる自動車システムを構築したいです。どちらのケースでも、動作コードの大部分は共通化可能です - 実際には入力方法が異なるだけです。このため、両者で共有可能な基本カースクリプトを活用できます。

新規スクリプト「car_base.gd」を作成します。まずは変数の定義から始めてください。車の動作を調整するためのエクスポート変数と、状態を追跡するためのその他の変数を用意します。

```gdscript
extends CharacterBody3D

# Car behavior parameters, adjust as needed
@export var gravity = -20.0
@export var wheel_base = 0.6  # distance between front/rear axles
@export var steering_limit = 10.0  # front wheel max turning angle (deg)
@export var engine_power = 6.0
@export var braking = -9.0
@export var friction = -2.0
@export var drag = -2.0
@export var max_speed_reverse = 3.0

# Car state properties
var acceleration = Vector3.ZERO  # current acceleration
var velocity = Vector3.ZERO  # current velocity
var steer_angle = 0.0  # current wheel angle
```

※ 「重力」変数を使用する代わりに、「プロジェクト設定」でグローバル値を設定することもできます。別々に定義すれば、ゲームオブジェクトごとに異なる挙動を実現できます。最適な方法はプロジェクトの要件次第ですので、状況に応じて選択してください。

* `engine_power` と `braking` は車の加速・減速時に適用されます。

*  `drag` と `friction` については[こちらで詳しく説明しています](/godot_recipes/4.x/ja/2d/car_steering/#part-3-frictiondrag)。

The rest of the script will be very similar to the 2D version, which a few changes to work correctly with {{< gd-icon Node3D >}}`Node3D`s and `Transform`s.

まず`_physics_process()`から見ていきます。

ここでは、コントロールを適用する前に車が地面に接地しているかを確認します。空中では操舵は不可能ですからね！その後、標準的な移動方程式を適用します。

車が斜面から滑り落ちるのを防ぐ `move_and_slide_with_snap()` を使用している点に注意してください（トラックに坂道がある場合）。スナップ基準には車のローカル下方向ベクトルを使用しています。これも正しく坂道を処理するためです。

```gdscript
func _physics_process(delta):
    if is_on_floor():
        get_input()
        apply_friction(delta)
        calculate_steering(delta)
    acceleration.y = gravity
    velocity += acceleration * delta
    velocity = move_and_slide_with_snap(velocity, -transform.basis.y, Vector3.UP, true)
```

この機能は摩擦力（車の速度に比例）と空気抵抗（速度の二乗に比例）を適用します。これによりパワーを加えていない時の減速効果が得られるだけでなく、車両の最高速度も決定されます。

```gdscript
func apply_friction(delta):
    if velocity.length() < 0.2 and acceleration.length() == 0:
        velocity.x = 0
        velocity.z = 0
    var friction_force = velocity * friction * delta
    var drag_force = velocity * velocity.length() * drag * delta
    acceleration += drag_force + friction_force
```

最後に、2次元自動車の場合と同じ簡略化された「自転車」モデルを用いて旋回角度を計算します。新たな速度が算出されたら、`look_at()`関数で車体を正しい方向に向けます。ここではドリフトやトラクションは考慮していません（これらについては後ほど扱います）。

また、車両の進行方向ベクトルと速度ベクトルの内積を計算することで、逆向き判定も可能になります。

```gdscript
func calculate_steering(delta):
    var rear_wheel = transform.origin + transform.basis.z * wheel_base / 2.0
    var front_wheel = transform.origin - transform.basis.z * wheel_base / 2.0
    rear_wheel += velocity * delta
    front_wheel += velocity.rotated(transform.basis.y, steer_angle) * delta
    var new_heading = rear_wheel.direction_to(front_wheel)

    var d = new_heading.dot(velocity.normalized())
    if d > 0:
        velocity = new_heading * velocity.length()
    if d < 0:
        velocity = -new_heading * min(velocity.length(), max_speed_reverse)
    look_at(transform.origin + new_heading, transform.basis.y)
```

最後に、車両の制御方法を決定する関数を作成します。これは個別の車両ごとにオーバーライドします。プレイヤーが操作する車両ではキーボード／ゲームパッド入力を、コンピュータが制御する車両ではAIによる判断を実装します。

```gdscript
func get_input():
    # Override this in inherited scripts for controls
    pass
```

### プレイヤー操作

これでプレイヤー操作を追加できるようになりました。以下が入力マッピングの設定です。

![alt](/godot_recipes/3.x/img/3d_car_04.png)

アナログスティック付きゲームパッドをお持ちの場合は、ぜひそれをご使用になることを強くオススメします。キーボード操作ではオン/オフしか制御できないため、「ハンドル」を最大限に回転させるしかありません。アナログスティックを使えば、はるかに快適な操作体験が得られます。いずれの操作方法でもコードが正しく動作するよう、しっかり対応いたします。

Here's the script to attach to the car {{< gd-icon KinematicBody3D >}} `CharacterBody3D`:

```gdscript
extends "res://cars/car_base.gd"

func get_input():
    var turn = Input.get_action_strength("steer_left")
    turn -= Input.get_action_strength("steer_right")
    steer_angle = turn * deg2rad(steering_limit)
    $tmpParent/sedanSports/wheel_frontRight.rotation.y = steer_angle*2
    $tmpParent/sedanSports/wheel_frontLeft.rotation.y = steer_angle*2
    acceleration = Vector3.ZERO
    if Input.is_action_pressed("accelerate"):
        acceleration = -transform.basis.z * engine_power
    if Input.is_action_pressed("brake"):
        acceleration = -transform.basis.z * braking
```

最初に、ステアリング入力を取得します。これにより、値が -1 から 1 の範囲に収まります。この値を、最大許容角度に基づいてラジアン単位の角度に変換します。

次のステップでは、ステアリング操作をより分かりやすく視覚的にフィードバックするため、ホイールメッシュを回転させます。通常、ドライバーは車からある程度離れた位置から見るため、効果を強調するために2倍に拡大しています。

ステアリング操作後、加速／ブレーキ入力を確認して車両の「加速度」を設定します。

![alt](/godot_recipes/3.x/img/3d_car_05.gif)

### まとめ

これは基本的な車コントローラーの実装です。ゲーム開発の出発点として自由にお使いください。さらに機能を追加したい場合は、以下に挙げるフォローアップレシピで扱うトピックを参考にしてください。

* 牽引およびドリフト走行
* チェイスカメラ制御と撮影操作
* AI／NPCコントロール（ステアリング、障害物回避、コース追従）
* 傾斜地やスロープの走行処理

{{% notice note %}}
ダウンロードはこちら：[https://github.com/kidscancode/3d_car_tutorial/releases](https://github.com/kidscancode/3d_car_tutorial/releases)
{{% /notice %}}

## Related recipes

- [2D: Car Steering recipe](/godot_recipes/3.x/2d/car_steering)
- [Input Actions](http://kidscancode.org/godot_recipes/input/input_actions/)
- [3D: CharacterBody3D Movement](/godot_recipes/3.x/3d/kinematic_body/)

#### Like video?

{{< youtube WhwSKyGjQq0 >}}

