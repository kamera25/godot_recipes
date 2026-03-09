---
title: "Arcade-style Airplane"
weight: 12
draft: false
---

## 問題文

3D空間で飛行機のコントローラーを作りたいが、完全なフライトシミュレーター機能は不要です。

## 解決策

このレシピでは、「簡素化された」航空機コントローラーを作成します。ここで言う「簡素化」とは、基本機能だけに絞り込むことを意味します。私たちが目指しているのは、飛行機の操縦感覚――特別な訓練なしですぐに飛び立て、最小限の操作体系で簡単に飛行を楽しめるような体験です。

{{% notice note %}}
このレシピは厳密な飛行シミュレーターではありません。航空力学を再現しているわけではないので、本物の飛行機のように飛ぶわけではありません。ここでは正確性よりもシンプルさと「楽しさ」を追求しています。
{{% /notice %}}

### ノード設定

このシーンでは `CharacterBody3D` を使用します。実際の飛行力学（揚力、抗力など）はシミュレートしないため、この場合 `RigidBody3D` は必要ありません。

以下にモデルのセットアップをご説明します：

![alt](/godot_recipes/4.x/img/kb_plane_01.png)

衝突判定用に円筒を使用し、機体のサイズに合わせて調整しています。これにより、デモで必要となる地面との接触検出が可能になります。

スクリプトを実行する前に、航空機のプロパティを確認しましょう：

```gdscript
extends CharacterBody3D

# Can't fly below this speed
var min_flight_speed = 12
# Maximum airspeed
var max_flight_speed = 40
# Turn rate
var turn_speed = 0.75
# Climb/dive rate
var pitch_speed = 0.5
# Wings "autolevel" speed
var level_speed = 3.0
# Throttle change speed
var throttle_delta = 50
# Acceleration/deceleration
var acceleration = 6.0

# Current speed
var forward_speed = 0
# Throttle input speed
var target_speed = 0
# Lets us change behavior when grounded
var grounded = false

var turn_input = 0
var pitch_input = 0
```

### 操作方法

このデモではゲームコントローラーを使用していますが、お好みでキーボード入力を追加することも可能です。

![alt](/godot_recipes/4.x/img/kb_plane_02.png)

この機能は入力値を取得し、設定された値を反映します。なお、スロットルの増減操作は「actual_speed」ではなく「target_speed」を変更することに注意してください。これにより、現在の速度から目標速度までスムーズに加速・減速が可能になります。

```gdscript
func get_input(delta):
    # Throttle input
    if Input.is_action_pressed("throttle_up"):
        target_speed = min(forward_speed + throttle_delta * delta, max_flight_speed)
    if Input.is_action_pressed("throttle_down"):
        var limit = 0 if grounded else min_flight_speed
        target_speed = max(forward_speed - throttle_delta * delta, limit)

    # Turn (roll/yaw) input
    turn_input = Input.get_axis("roll_right", "roll_left")

    # Pitch (climb/dive) input
    pitch_input =  Input.get_axis("pitch_down", "pitch_up")
```

### 移動

モーション処理は `_physics_process()` 内で行われ、まず速度を目標値にリニア補間した後、`move_and_slide()` 関数を使用して移動とスライディングを行います：

```gdscript
func _physics_process(delta):
    get_input(delta)
    # Accelerate/decelerate
    forward_speed = lerpf(forward_speed, target_speed, acceleration * delta)

    # Movement is always forward
    velocity = -transform.basis.z * forward_speed

    move_and_slide()
```

テスト方法：テストシーンにこの平面を追加してください（`{{< gd-icon Camera3D >}}` カメラの設定を忘れずに）。`"throttle_up"`入力を押すと、平面が前方へ加速する様子が確認できるはずです。

{{% notice tip %}}
[補間カメラ機能](/godot_recipes/4.x/3d/interpolated_camera/) をこのデモで実装しています。
{{% /notice %}}

![alt](/godot_recipes/4.x/img/kb_plane_03.gif)

次に、飛行機のピッチ角度を変更する処理を追加しましょう。`_physics_process()` 内の `get_input()` 呼び出し直後に以下を追加してください：

```gdscript
transform.basis = transform.basis.rotated(transform.basis.x, pitch_input * pitch_speed * delta)
```

シーンを再度実行し、上下にパンしてみてください：

![alt](/godot_recipes/4.x/img/kb_plane_04.gif)

その後、ターン入力用に以下を追加してください：

```gdscript
transform.basis = transform.basis.rotated(Vector3.UP, turn_input * turn_speed * delta)
```

![alt](/godot_recipes/4.x/img/kb_plane_05.gif)

注意してほしいのですが、機体が旋回する際に、その動きがやや不自然に見えます。航空機はターン時に「バンク」（傾き）しますので、メッシュの回転角度を変更することでこれをアニメーション化しましょう：

```gdscript
mesh.rotation.z = lerpf(mesh.rotation.z, -turn_input, level_speed * delta)
```

![alt](/godot_recipes/4.x/img/kb_plane_06.gif)

```
mesh は、平面シーン内の {{< gd-icon MeshInstance3D >}}`MeshInstance3D` オブジェクトへの参照です（例では `$cartoon_plane`）。

ロール量は「turn_input」値に関連しているため、緩やかなターンでは傾きが少なくなります。直進すると自動的に機体が水平になります。

これで完了です！基本的な飛行制御が正常に動作するようになり、快適に操縦できるはずです。各種プロパティを調整して、それらが動きにどう影響するか試してみてください。

### 着陸/離陸時

上記の方法は空中移動には適していますが、地上での挙動を考えると不十分です。ここでは、非常に簡易的なアプローチ（「簡易」という表現は非常に基本的な方法を意味します - 実際のゲーム要件によっては、さらに拡張が必要になるでしょう）を用いて着陸シミュレーションを実装します。

まず、地上走行時と空中飛行時を明確に区別する必要があります。地上では速度を0に減速できますが、空中では最低限の対気速度を維持しなければなりません。また、地上走行中は旋回時にバンク（傾斜）しないようにする必要があります（翼が地面に接触して損傷する危険があるため）。

```gdscript
func _physics_process(delta):
    get_input(delta)
    transform.basis = transform.basis.rotated(transform.basis.x, pitch_input * pitch_speed * delta)
    transform.basis = transform.basis.rotated(Vector3.UP, turn_input * turn_speed * delta)

    # Bank when turning
    if grounded:
        mesh.rotation.z = 0
    else:
        mesh.rotation.z = lerpf(mesh.rotation.z, -turn_input, level_speed * delta)

    # Accelerate/decelerate
    forward_speed = lerpf(forward_speed, target_speed, acceleration * delta)

    # Movement is always forward
    velocity = -transform.basis.z * forward_speed

    # Landing
    if is_on_floor():
        if not grounded:
            rotation.x = 0
        grounded = true
    else:
        grounded = false
    move_and_slide()
```

その間、`get_input()`関数では、減速時と降下時にも`grounded`を考慮に入れ、`min_flight_speed`以上の速度に達している場合にのみ離陸を許可するようにします：

```gdscript
func get_input(delta):
    # Throttle input
    if Input.is_action_pressed("throttle_up"):
        target_speed = min(forward_speed + throttle_delta * delta, max_flight_speed)
    if Input.is_action_pressed("throttle_down"):
        var limit = 0 if grounded else min_flight_speed
        target_speed = max(forward_speed - throttle_delta * delta, limit)

    # Turn (roll/yaw) input
    turn_input = Input.get_axis("roll_right", "roll_left")
    if forward_speed <= 0.5:
        turn_input = 0

    # Pitch (climb/dive) input
    pitch_input = 0
    if not grounded:
        pitch_input -= Input.get_action_strength("pitch_down")
    if forward_speed >= min_flight_speed:
        pitch_input += Input.get_action_strength("pitch_up")
```

![alt](/godot_recipes/4.x/img/kb_plane_07.gif)

### 全文スクリプト

以下が完全なスクリプトです：

{{% expand "Click to expand..." %}}

```gdscript
extends CharacterBody3D

# Can't fly below this speed
var min_flight_speed = 12
# Maximum airspeed
var max_flight_speed = 40
# Turn rate
var turn_speed = 0.75
# Climb/dive rate
var pitch_speed = 0.5
# Wings "autolevel" speed
var level_speed = 3.0
# Throttle change speed
var throttle_delta = 50
# Acceleration/deceleration
var acceleration = 6.0

# Current speed
var forward_speed = 0
# Throttle input speed
var target_speed = 0
# Lets us change behavior when grounded
var grounded = false

var turn_input = 0
var pitch_input = 0

var tracer_scene = preload("res://tracer.tscn")
var can_shoot = true

@onready var mesh = $cartoon_plane

func _ready():
    $cartoon_plane/AnimationPlayer.play("prop_spin")

func get_input(delta):
    # Throttle input
    if Input.is_action_pressed("throttle_up"):
        target_speed = min(forward_speed + throttle_delta * delta, max_flight_speed)
    if Input.is_action_pressed("throttle_down"):
        var limit = 0 if grounded else min_flight_speed
        target_speed = max(forward_speed - throttle_delta * delta, limit)

    # Turn (roll/yaw) input
    turn_input = Input.get_axis("roll_right", "roll_left")
    if forward_speed <= 0.5:
        turn_input = 0

    # Pitch (climb/dive) input
    pitch_input = 0
    if not grounded:
        pitch_input -= Input.get_action_strength("pitch_down")
    if forward_speed >= min_flight_speed:
        pitch_input += Input.get_action_strength("pitch_up")
#	pitch_input =  Input.get_axis("pitch_down", "pitch_up")

func _physics_process(delta):
    get_input(delta)
    transform.basis = transform.basis.rotated(transform.basis.x, pitch_input * pitch_speed * delta)
    transform.basis = transform.basis.rotated(Vector3.UP, turn_input * turn_speed * delta)

    # Bank when turning
    if grounded:
        mesh.rotation.z = 0
    else:
        mesh.rotation.z = lerpf(mesh.rotation.z, -turn_input, level_speed * delta)

    # Accelerate/decelerate
    forward_speed = lerpf(forward_speed, target_speed, acceleration * delta)

    # Movement is always forward
    velocity = -transform.basis.z * forward_speed

    # Landing
    if is_on_floor():
        if not grounded:
            rotation.x = 0
        grounded = true
    else:
        grounded = false
    move_and_slide()
```

{{% /expand%}}

## まとめ

このテクニックは、様々なアーケードスタイルの飛行ゲームに応用可能です。例えば、マウス操作の場合、`InputEventMouseMotion` の `relative`プロパティを使用してピッチとヨー入力を設定する方法が有効です。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/3d_airplane_demo](https://github.com/godotrecipes/3d_airplane_demo)
