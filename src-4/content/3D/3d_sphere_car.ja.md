---
title: "アーケードスタイルのカーゲーム"
weight: 12
draft: false
---

## 課題

アーケードスタイルのカーゲームを作りたい場合、リアルな物理演算よりもシンプルさを重視するでしょう。このレシピでは、転がる球体を使って楽しく操作可能な車を作成する方法をご紹介します。

<video width="500" controls src="/godot_recipes/4.x/img/3d_sphere_car_01.webm"></video>

## 解決策

ドライビングゲームを作成する方法は数多くあります。各ゲームに求められるリアリズムのレベルは異なります。軽量なアーケードスタイルのカーモデルを作りたい場合、Godotの{{< gd-icon VehicleBody3D >}}`VehicleBody3D`ノードが提供するすべての機能（サスペンションシステムや個別にモデリングされた車輪など）は必要ないかもしれません。

その代わり、駆動物理処理は単一の {{< gd-icon RigidBody3D >}}`RigidBody3D` 球体で処理します。球体自体は視認できない状態にし、車のメッシュをこの球体の位置に配置することで、あたかも球体が車を動かしているかのような視覚効果を実現します。

上記のプレビュー映像でご覧いただけるように、完成した結果は驚くほど良好です（実際にプレイするのもとても楽しいです！）。引き続きお読みいただければ、必要なコード量も驚くほど少ないことがお分かりいただけるでしょう。

### 入力値

制御用に、以下の4つの入力を［インプットマップ］に追加します。

- `accelerate(加速)`
- `brake(ブレーキ)`
- `steer_left(左折)`
- `steer_right(右折)`

キーボード入力、ゲームパッド、または両方を使用できます。ただし、操作性を重視するなら、アナログスティックの使用をオススメします。

### ノード設定

The car is made with two main nodes: a {{< gd-icon RigidBody3D >}}`RigidBody3D` sphere for the physics, and a {{< gd-icon MeshInstance3D >}}`MeshInstance3D` to display the car body. Here's the scene layout:

```
{{< gd-icon RigidBody3D >}} RigidBody3D (Car)
     {{< gd-icon CollisionShape3D >}} CollisionShape3D (Sphere)
     {{< gd-icon Node3D >}} CarMesh (Imported model)
```

以下に、各ノードの動作原理を説明します。「加速」を押すと、{{< gd-icon RigidBody3D >}}`RigidBody3D` に対してオブジェクト（{{< gd-icon MeshInstance3D >}}`CarMesh`）が向いている方向に力が加わります。一方、旋回入力を入力すると、{{< gd-icon MeshInstance3D >}}`CarMesh`が回転します。ボールが転がる際、この動きに伴って車のメッシュも移動します（ここではボール自体の回転は考慮しません）。

#### カーメッシュ

以下が使用する車種の詳細です。

![alt](/godot_recipes/4.x/img/3d_sphere_car_02.png)

{{% notice note %}}
ケンニーの『カーキット』でこの車種や他のモデルを入手できます。以下のURLからダウンロードできます。
[https://kenney.nl/assets/car-kit](https://kenney.nl/assets/car-kit)。すべてのアセットをダウンロードできます。使いたいものだけを選んでいただいて構いません。このキットには複数のフォーマット形式のモデルが含まれていますが、プロジェクトに必要な全てを使用する必要はありません。Godotでの使用にはGLTF形式を推奨します。{{% /notice %}}

GLTFモデルを使用する場合、インポート設定で調整する必要はありません。

以下は「suv」モデルをインポートした際のノードツリーの表示例です。

![alt](/godot_recipes/4.x/img/3d_sphere_car_04a.png)

注：ホイールと車体はそれぞれ別のメッシュです。これにより、ステアリング時に車輪が回転するなど、視覚的な演出を簡単に追加できます。

#### ボール

{{< gd-icon CollisionShape3D >}}`CollisionShape3D` に球形状を追加します。ここでは半径を `1` に設定していますが、異なる走行挙動を得るには、ボールのサイズを調整して実験してみてください。

以下の方法でボディの設定を調整できます。

- **Angular Damp: `10`** - このプロパティはドライビングのフィーリングに大きな影響を与えます。値が大きいほど、車はより速く停止します。
- **Gravity Scale: `5`** - Godotのデフォルトの重力（`9.8`）は、特にアクション性の高いゲームを目指す場合、少し浮遊感があるように感じられます。この設定は、ジャンプや坂道など、ワールド内の起伏を扱う場合に特に重要になります。必要であれば、**プロジェクト設定**でグローバルに設定することも可能です。
- **物理 Material/Bounce: `0.1`** - この値を調整することは非常に楽しいですが、0.5を超える値には注意してください！

デモ用にデバッグ用として、衝突形状に球状メッシュも追加しました。必須機能ではありませんが、ボールが転がる様子を視覚的に確認できるとトラブルシューティング時に便利です。

#### RayCast

最後に、{{< gd-icon RayCast3D >}}`RayCast3D`ノードを{{< gd-icon MeshInstance3D >}}`CarMesh`の子要素として追加します。**ターゲット位置**は`(0, -1, 0)`に設定してください。

![alt](/godot_recipes/4.x/img/3d_sphere_car_03.png)

これを地面検知に使用します。車両が空中にある間はステアリングと加速制御が使えなくなります。また、ゲームのコースが平坦でない場合に、この機能を使って車メッシュを斜面に合わせることもできます。

これでコーディングを開始する準備が整いました。

### スクリプト

まずスクリプトで使用するノード参照をいくつか定義します。

```gdscript
extends RigidBody3D

@onready var car_mesh = $CarMesh
@onready var body_mesh = $CarMesh/suv2
@onready var ground_ray = $CarMesh/RayCast3D
@onready var right_wheel = $CarMesh/suv2/wheel_frontRight
@onready var left_wheel = $CarMesh/suv2/wheel_frontLeft
```

次に、車両の動作を制御する変数について説明します。各変数の機能についてはコメントを参照してください。

```gdscript
# Where to place the car mesh relative to the sphere
var sphere_offset = Vector3.DOWN
# Engine power
var acceleration = 35.0
# Turn amount, in degrees
var steering = 18.0
# How quickly the car turns
var turn_speed = 4.0
# Below this speed, the car doesn't turn
var turn_stop_limit = 0.75

# Variables for input values
var speed_input = 0
var turn_input = 0
```

インスペクターからこれらを調整したい場合は、`@export` を指定できます。

`_physics_process()`では、車が向いている方向に基づいてボディに力を加え、さらに車オブジェクトをボールの位置に配置し続けます。

```gdscript
func _physics_process(delta):
    car_mesh.position = position + sphere_offset
    if ground_ray.is_colliding():
        apply_central_force(-car_mesh.global_transform.basis.z * speed_input)
```

次の手順は入力値を取得することですが、その前に光線が地面と衝突しているかどうかも確認します。

```gdscript
func _process(delta):
    if not ground_ray.is_colliding():
        return
    speed_input = Input.get_axis("brake", "accelerate") * acceleration
    turn_input = Input.get_axis("steer_right", "steer_left") * deg_to_rad(steering)
    right_wheel.rotation.y = turn_input
    left_wheel.rotation.y = turn_input
```

{{% notice tip %}}
この時点で実際に操作を試してみます。前進・後退は可能になるはずです（ただしまだステアリング操作はできません）。
{{% /notice %}}

Next, still in the `_process()` function, we'll rotate the car mesh based on the rotation input. We'll use `slerp()` (spherical linear interpolation) to do this smoothly:

```gdscript
# rotate car mesh
if linear_velocity.length() > turn_stop_limit:
    var new_basis = car_mesh.global_transform.basis.rotated(car_mesh.global_transform.basis.y, turn_input)
    car_mesh.global_transform.basis = car_mesh.global_transform.basis.slerp(new_basis, turn_speed * delta)
    car_mesh.global_transform = car_mesh.global_transform.orthonormalized()
```

{{% notice warning %}}
浮動小数点演算の精度限界により、数値変換を繰り返し回転させると、スケールが変動したり、軸方向が不整合となり歪みが生じる可能性があります。定期的に変換を回転させるスクリプトでは、`orthonormalized()` を使用して誤差が累積する前に補正を行うことが推奨されます。
{{% /notice %}}

この段階で再び試してみることをオススメします。車の制御や走行が可能になり、ほぼ期待通りに動くようになります。ただし、運転感覚をさらに向上させるために、追加すべき点がいくつかあります。

### 仕上げ作業

#### 1. 斜面との整合性を確保

**修正が必要な箇所**

If you've tried driving on a slope, you've seen that the car mesh doesn't tilt at all, it always remains level. That looks unnatural, so let's use the process described in [CharacterBody3D: 表面に位置合わせ](/godot_recipes/3.x/3d/3d_align_surface/) to fix that.

追加するコードは `_process()` 内でメッシュを回転させた後に配置してください。

```gdscript
if ground_ray.is_colliding():
    var n = ground_ray.get_collision_normal()
    var xform = align_with_y(car_mesh.global_transform, n)
    car_mesh.global_transform = car_mesh.global_transform.interpolate_with(xform, 10.0 * delta)
```

align関数（前回同様に`orthonormalized()`を使用している点に注目してください）。

```gdscript
func align_with_y(xform, new_y):
    xform.basis.y = new_y
    xform.basis.x = -xform.basis.z.cross(new_y)
    xform.basis = xform.basis.orthonormalized()
    return xform.orthonormalized()
```

#### 2. 車輪を回転させる

フロントホイールがハンドル操作に応じて動くようにすると、よりリアルに見えます。スクリプトの上部にフロントホイールメッシュに関する参照を追加してください。

```gdscript
@onready var right_wheel = $CarMesh/suv2/wheel_frontRight
@onready var left_wheel = $CarMesh/suv2/wheel_frontLeft
```

入力を取得した直後に以下を追加してください。

```gdscript
    # rotate wheels for effect
    right_wheel.rotation.y = rotate_input
    left_wheel.rotation.y = rotate_input
```

![alt](/godot_recipes/4.x/img/3d_sphere_car_05.gif)

### 3. 体幹を傾ける

このスクリプトでは視覚的な魅力を大幅に向上させます。ターン速度に基づいて車のボディを傾斜させる機能を追加します。スクリプト上部に変数を追加して：

```gdscript
var body_tilt = 35
```

この数値が小さいほど、傾斜効果が強くなります。SUVモデルの場合、`35`から`40`の範囲で最適な結果が得られます。

次に、車のメッシュを回転させた直後に以下を追加してください（`if` 文内です）：

```gdscript
# tilt body for effect
var t = -rotate_input * ball.linear_velocity.length() / body_tilt
body_mesh.rotation.z = lerp(body_mesh.rotation.z, t, 10 * delta)
```

違いを観察してください。

![alt](/godot_recipes/4.x/img/3d_sphere_car_06.gif)

### クレジット表記
>
> 本デモプロジェクトでは以下のオープンソース／クリエイティブ・コモンズ素材を使用しています。
> - 車両モデル：Kenney氏制作の[ケンニー・カーキット](https://kenney.nl/assets/car-kit)
> - コースデータ：Keith氏による[モジュール式レーシングカートトラック（起伏のある地形テーマ）](https://fertile-soil-productions.itch.io/modular-racekart-track-hilly-terrain-theme)、Fertile Soil Productions提供


## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます。[https://github.com/godotrecipes/3d_car_sphere](https://github.com/godotrecipes/3d_car_sphere)

## 関連レシピ

* [入力アクション](/godot_recipes/4.x/ja/input/input_actions/)
