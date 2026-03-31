---
title: "車のステアリング操作"
weight: 3
draft: false
ghcommentid: 22
---

## 課題

2D見下ろし方式カーコントローラーを作成したい。

## 解決策

この問題に取り組む際、初心者はしばしば実際の車とはかけ離れた挙動のゲームを作ってしまいがちです。アマチュアが作ったカーゲームでよく見られる典型的な失敗例をご紹介します。

- 自動車は中心軸を中心に旋回するものではありません。別の言い方をすれば、後輪が左右に滑ることはありません。（ドリフト走行時はこの限りではないが、その点については後述します）- 自動車は動いている時にのみ方向転換が可能で、その場で回転することはできません。。
- 自動車は列車ではありません。レールに縛られていません。高速で曲がる際にはある程度の横滑り（ドリフト）が伴うべきです。

2Dカー物理の実装には様々なアプローチ方法があり、主に「リアル志向」か「アーケードスタイル」かによって選択が分かれます。このソリューションでは、リアリティよりもアクション性を優先する「アーケードレベル」の現実感を追求していきます。

{{% notice note %}}
以下の方法は、こちらのアルゴリズムに基づいています。 http://engineeringdotnet.blogspot.com/2010/04/simple-2d-car-physics-in-games.html
{{% /notice %}}

以下のレシピは5つのセクションに分かれており、それぞれが車の異なる動作要素を追加します。必要に応じて自由に組み合わせてご使用ください。

### シーン設定

以下が車シーンの設定内容です。

```
{{< gd-icon CharacterBody2D >}} CharacterBody2D
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
    {{< gd-icon Camera2D >}} Camera2D
```

このデモでは、[Kenneyのレーシングパック](https://kenney.nl/assets/racing-pack)のアートワークを使用します。{{< gd-icon CapsuleShape2D >}}`CapsuleShape2D`は衝突判定に最適な形状です。これにより、車が障害物に引っかかるような鋭い角を防ぐことができます。

以下の4つの入力操作も使用します。「右旋回」「左旋回」「加速」「ブレーキ」。お好みのキー割り当てを設定してください。

### その1：動き

最初のステップは、前述のアルゴリズムに基づいて動作をコーディングすることです。

以下の変数から始めてください。

```gdscript
extends CharacterBody2D

var wheel_base = 70  # Distance from front to rear wheel
var steering_angle = 15  # Amount that front wheel turns, in degrees

var steer_direction
```

'wheelbase' をスプライトに適した値に設定してください。

`steer_direction` には車輪の回転量が設定されます。

{{% notice note %}}
キーボード操作を使用している場合、ターンはオン／オフの二択になります。アナログジョイスティックを使用する場合は、代わりにスティックの移動距離に応じてこの値を調整できます。
{{% /notice %}}


```gdscript
func _physics_process(delta):
    get_input()
    calculate_steering(delta)
    move_and_slide()
```

各フレームでは、入力のチェックとステアリング計算が必要です。その後、算出された「速度」を `move_and_slide()` 関数に渡します。これら2つの関数については次に定義します。

```gdscript
func get_input():
    var turn = Input.get_axis("steer_left", "steer_right")
    steer_direction = turn * deg_to_rad(steering_angle)
    velocity = Vector2.ZERO
    if Input.is_action_pressed("accelerate"):
        velocity = transform.x * 500
```

ここではユーザー入力を確認し、移動速度を設定します。注意：速度「500」は一時的なもので、動きのテスト用です。これについては次のセクションで対処します。

以下に、リンク先のアルゴリズムを実装します。

```gdscript
func calculate_steering(delta):
    # 1. Find the wheel positions
    var rear_wheel = position - transform.x * wheel_base / 2.0
    var front_wheel = position + transform.x * wheel_base / 2.0
    # 2. Move the wheels forward
    rear_wheel += velocity * delta
    front_wheel += velocity.rotated(steer_direction) * delta
    # 3. Find the new direction vector
    var new_heading = rear_wheel.direction_to(front_wheel)
    # 4. Set the velocity and rotation to the new direction
    velocity = new_heading * velocity.length()
    rotation = new_heading.angle()
```

プロジェクトを実行すると、車が動き始め、方向転換するはずです。ただし現在の動作はまだ不自然で、車の動きが瞬時に開始・停止します。これを改善するため、計算に加速度を追加します。

### その2：加速について

以下の設定変数と、車全体の加速を追跡するための変数が必要になります。

```gdscript
var engine_power = 900  # Forward acceleration force.

var acceleration = Vector2.ZERO
```

入力コードを変更して、車の `velocity` を直接変更するのではなく、加速度を適用するようにします。

```gdscript
func get_input():
    var turn = Input.get_axis("steer_left", "steer_right")
    steer_direction = turn * deg_to_rad(steering_angle)
    if Input.is_action_pressed("accelerate"):
        acceleration = transform.x * engine_power
```

一旦加速度が得られたら、以下のように速度に適用できます。

```gdscript
func _physics_process(delta):
    acceleration = Vector2.ZERO
    get_input()
    calculate_steering(delta)
    velocity += acceleration * delta
    move_and_slide()
```

今から車を走らせると、徐々に速度が上がっていきます。注意：まだ減速する方法はないんですよ！

### その3：摩擦・抗力について

自動車には2種類の異なる減速力が作用します。摩擦力と空気抵抗です。

- 摩擦力は路面が車に及ぼす抵抗力です。砂地では非常に強いですが、氷上では極めて小さくなります。この力は速度に比例し、スピードが速いほど大きくなります。

* ドラッグは空気抵抗によって生じる力です。車両の断面積が大きいほど影響が大きくなります - 流線型のレースカーに比べて大型トラックやバンの方がより大きな抗力を受けます。ドラッグの値は速度の二乗に比例します。

これにより、低速走行時には摩擦抵抗がより顕著になる一方、高速域では空気抵抗が支配的になります。これら両方の力を計算に含めます。さらに、これらの量の値は、車の最高速度――エンジン出力がもはや空気抵抗に打ち勝てなくなる点――を示す指標にもなります。

以下にこれらの数量に対する初期値を示します。

```gdscript
var friction = -55
var drag = -0.06
```

このグラフから分かるように、これらの値は、速度が`600`に達した時点で、抗力が摩擦力を上回ることを示しています。

![alt](/godot_recipes/4.x/img/car_graph_friction.png)

こちらのツールで値を変更してその影響を確認できます。
[https://www.desmos.com/calculator/e4ayu3xkip](https://www.desmos.com/calculator/e4ayu3xkip)

関数 _physics_process() では、現在の摩擦係数を計算する関数を呼び出し、それを加速度力に適用します。

```gdscript
func _physics_process(delta):
    acceleration = Vector2.ZERO
    get_input()
    apply_friction(delta)
    calculate_steering(delta)
    velocity += acceleration * delta
    velocity = move_and_slide(velocity)

func apply_friction(delta):
    if acceleration == Vector2.ZERO and velocity.length() < 50:
        velocity = Vector2.ZERO
    var friction_force = velocity * friction * delta
    var drag_force = velocity * velocity.length() * drag * delta
    acceleration += drag_force + friction_force
```

まず、最低速度を設定してください。これにより、摩擦力が完全に車の速度をゼロにさせない場合でも、車両が極端に低速で前進し続けるのを防ぐことができます。

その後、これら2つの力を計算し、合計加速度に加算します。どちらも負の値なので、車には逆方向に作用になります。

<video controls src='/godot_recipes/4.x/img/car_friction.webm'></video>

### その4：リバース／ブレーキ操作

以下の 2 つの設定変数も必要です。

```gdscript
var braking = -450
var max_speed_reverse = 250
```

`get_input()`で入力できるようにしましょう。

```gdscript
    if Input.is_action_pressed("brake"):
        acceleration = transform.x * braking
```

これは停止時には問題ありませんが、リバースギアに入れたときに正常に動作しない問題があります。現在、加速は常に「進行方向」（前進）に対して適用されているため、バック走行時に逆方向に加速することができません。リバース時は後方への加速度を加える必要があります。

```gdscript
func calculate_steering(delta):
    var rear_wheel = position - transform.x * wheel_base / 2.0
    var front_wheel = position + transform.x * wheel_base / 2.0
    rear_wheel += velocity * delta
    front_wheel += velocity.rotated(steer_angle) * delta
    var new_heading = (front_wheel - rear_wheel).normalized()
    var d = new_heading.dot(velocity.normalized())
    if d > 0:
        velocity = new_heading * velocity.length()
    if d < 0:
        velocity = -new_heading * min(velocity.length(), max_speed_reverse)
    rotation = new_heading.angle()
```

2つのベクトルの内積を利用することで、前進しているか後退しているかを判断できます。ベクトルが一致している場合、結果は正の値になります。移動方向が車の進行方向と逆向きの場合、内積は負の値となり、後方に移動していることが確認されます。

<video controls src='/godot_recipes/4.x/img/car_reverse.webm'></video>

### その5：ドリフト/スライド操作

ここで止めても十分満足のいく運転体験が得られるでしょう。ただ、車がまだ「レールに乗っている」ような感覚です。最高速で走行していても、カーブは完璧にクリアされ、まるでタイヤが完全に路面を掴んでいるみたいです。

高速時（あるいは低速でもお好みで）には、駆動力によってタイヤが滑り、車体が「魚の尾のように」左右に滑る動きが生じるはずです。

```gdscript
var slip_speed = 400  # Speed where traction is reduced
var traction_fast = 2.5 # High-speed traction
var traction_slow = 10  # Low-speed traction
```

これらの値は、ステアリング計算時に適用します。現在の設定では、速度が瞬時に新しい進行方向に切り替わるようになっています。代わりに、補間処理（`lerp()`）を使用して、車両が新しい方向に完全に向きを変えることなく、部分的にしか旋回しないようにします。その際、「トラクション」値がタイヤの「粘着性」を決定します。

```gdscript
func calculate_steering(delta):
    var rear_wheel = position - transform.x * wheel_base / 2.0
    var front_wheel = position + transform.x * wheel_base / 2.0
    rear_wheel += velocity * delta
    front_wheel += velocity.rotated(steer_angle) * delta
    var new_heading = (front_wheel - rear_wheel).normalized()
    # choose which traction value to use - at lower speeds, slip should be low
    var traction = traction_slow
    if velocity.length() > slip_speed:
        traction = traction_fast
    var d = new_heading.dot(velocity.normalized())
    if d > 0:
        velocity = lerp(velocity, new_heading * velocity.length(), traction * delta)
    if d < 0:
        velocity = -new_heading * min(velocity.length(), max_speed_reverse)
    rotation = new_heading.angle()
```

ここでは、使用する牽引値を選択し、`velocity`に`lerp()`を適用します。

<video controls src='/godot_recipes/4.x/img/car_drift.webm'></video>

### 調整項目

この時点で、車両の挙動を制御する多数の設定項目が存在します。これらを調整することで、車の運転特性を大きく変更できます。さまざまな値を試す作業をより簡単にするため、以下にレシピ用プロジェクトをダウンロードしてください。ゲームを起動すると、走行中に車の挙動を変更可能なスライダーパネルが表示されます（`<Tab>`キーでスライダーパネルの表示/非表示を切り替え可能）。

![alt](/godot_recipes/4.x/img/car_sliders.png)

<!-- {{% notice note %}}
プロジェクトファイル: [car_steering.zip](/godot_recipes/4.x/files/car_steering.zip)
{{% /notice %}} -->

## 関連レシピ

- [ゲーム数学：補間](/godot_recipes/4.x/ja/math/interpolation/)

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます。[https://github.com/godotrecipes/2d_car_estrada](https://github.com/godotrecipes/2d_car_estrada)
