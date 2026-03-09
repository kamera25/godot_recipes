---
title: "Character Controller"
weight: 10
draft: false
---

## 問題文

Godot環境でリグ設定済みのアニメーション3Dキャラクターをインポートし、{{< gd-icon AnimationTree >}}`AnimationTree`を使ってそのアニメーションを設定したところですね。次は移動機能を実装する必要があります：キャラクタコントローラが必要です。

## 解決策

```
このレシピでは、既にキャラクターモデルとアニメーションをインポートしており、アニメーションの遷移やブレンド処理用に {{< gd-icon AnimationTree >}}`AnimationTree` が適切に設定されていることを前提に進めます。まだ準備ができていない場合は、[アセットのインポート方法](/4.x/3d/assets/importing_assets/) および [キャラクターアニメーションについて](/4.ex/3d/assets/character_animation/) を参照してください。参考までに、ここでは [セクション説明](/godot_recipes/4.x/3d/assets/) でリンクされているアートパックを使用しています。

### 衝突の追加

We've chosen {{< gd-icon CharacterBody3D >}}`CharacterBody3D` as the root node of the imported scene, and it's complaining about a missing collision shape, so let's fix that first. Add a {{< gd-icon CollisionShape3D >}}`CollisionShape3D` child and choose {{< gd-icon CapsuleShape3D >}}`CapsuleShape3D` as its **Shape** property.

カプセルのサイズと位置を調整し、キャラクターの全身を覆うようにします。参考までに、私が使用した数値は以下の通りです：

![alt](/godot_recipes/4.x/img/3dchar_capsule.png)

インポートしたリグは、足部分が「地面」に位置するように配置されています（つまり身体の中心位置に合わせた設定です）。この方法は後で便利になります。プレイヤーが中央に立つ場合、空中に浮いた状態ではなく、実際に地面に立っている状態で表示されるようになるからです。

```json
"If you're familiar with Godot's 3D orientation, you'll also notice that the character is facing the **+Z** direction, which is backwards. Select the {{< gd-icon Skeleton3D >}}`Skeleton3D` node and set its **Y** Rotation to `180` to correct this.",

### 入力操作

以下のキー操作を使用しています：`前進`、`後退`、`左移動`、`右移動`、`ジャンプ`。お好みで任意のキー/ボタンに割り当ててください。

### カメラ機能

プレイヤーを追従する3Dカメラの実装方法には様々なものがあります。この例では、カメラ用マウントとして `{{< gd-icon SpringArm3D >}}`SpringArm3D` を採用します。

《{{< gd-icon SpringArm3D >}}》`SpringArm3D`ノードはレイキャストを実行した後、その子オブジェクトを衝突点に移動させることで動作します。これをカメラに応用すると、プレイヤーとカメラの間に障害物が一切入らない状態を実現でき、この長さを調整することでズーム機能を実装することも可能です。

ルートノードの子として追加し、その後に `{{< gd-icon Camera3D >}}`Camera3D` をその子要素として追加してください。

春季アームのプロパティで、**スプリング長**を `5`、**マージン**を `0.1`、**位置**を `(0, 2.5, 0)` に設定します。

```yaml
# スプリングアームがプレイヤーのカプセル形状と衝突しないようにするため、ルートコンポーネント{{< gd-icon CharacterBody3D >}}`CharacterBody3D`の衝突レイヤーを`2`に設定します。これにより、スプリングアームはレイヤー`1`をチェック対象から除外できるため、カメラがプレイヤーの頭部に当たる現象を防止できます。

````
{{% notice style="info" title="衝突レイヤーの整理" %}}
最終的には、プレイヤーオブジェクト、環境要素、敵キャラクターなど、さまざまなゲームオブジェクトに対する衝突レイヤーを適切に管理する必要があります：
{{% /notice %}}

### 移動

これでプレイヤーにスクリプトを追加する準備が整いました。まずは必要な変数から始めましょう：

```gdscript
extends CharacterBody3D
class_name Knight

@export var speed = 5.0
@export var acceleration = 4.0
@export var jump_speed = 8.0

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
var jumping = false
```

以下に、アクセスが必要なノードに関する参考情報を示します：

```gdscript
@onready var spring_arm = $SpringArm3D
@onready var model = $Rig
@onready var anim_tree = $AnimationTree
@onready var anim_state = $AnimationTree.get("parameters/playback")
```

```markdown
以下のプロパティを確認できます：

!

`anim_state` はアニメーション状態マシンへの参照で、これを使用して異なるアニメーション間の遷移を呼び出すことができます。設定方法については、[キャラクターアニメーション](/4.x/3d/assets/character_animation/) レシピを参照してください。

移動処理は、プレイヤーの入力を取得して`move_and_slide()`関数を呼び出すことで実現されます：

```gdscript
func _physics_process(delta):
    velocity.y += -gravity * delta
    get_move_input(delta)

    move_and_slide()
```

プレイヤーの入力は水平方向の動きにのみ適用すべきです（**X軸**と**Z軸**）。重力が作用しているのは**Y軸**であるためです。このため、一時的に`velocity.y`をゼロに設定し、必要な入力を適用した後、処理終了後に元の値に戻します。

注: 入力ベクトルはカメラの回転に基づいて回転されます。つまり、キャラクターはカメラが向いている方向に前進します。

```gdscript
func get_move_input(delta):
    var vy = velocity.y
    velocity.y = 0
    var input = Input.get_vector("left", "right", "forward", "back")
    var dir = Vector3(input.x, 0, input.y).rotated(Vector3.UP, spring_arm.rotation.y)
    velocity = lerp(velocity, dir * speed, acceleration * delta)
    velocity.y = vy
```

その前に、これは機能をテストする絶好の機会です。地面に大きな `{{< gd-icon StaticBody3D >}}StaticBody3Ld` を使ったクイックテストシーンを作成するか、ダンジョンパックアセットを使用してシーン制作を開始してください。

あなたは前進／後退／左移動／右移動ができるようになります（まだアニメーションはありません）。

### カメラ操作

それでは、カメラ機能を動作させましょう。マウス操作でカメラ制御ができるようにします。感度を調整できる変数を追加します。

```gdscript
@export var mouse_sensitivity = 0.0015
```

その後、マウスの動きを検知し、それに応じてスプリングアームを回転させます。アームを**X**軸周りに回転させると上下に傾きます（マウスのy軸方向の動きが反映されます）。また、**Y**軸周りの回転は向きを変えます（マウスのx軸方向の動きが反映されます）。さらに、カメラの傾斜角度が過度にならないように制限を設けます。

```gdscript
func _unhandled_input(event):
    if event is InputEventMouseMotion:
        spring_arm.rotation.x -= event.relative.y * mouse_sensitivity
        spring_arm.rotation_degrees.x = clamp(spring_arm.rotation_degrees.x, -90.0, 30.0)
        spring_arm.rotation.y -= event.relative.x * mouse_sensitivity
```

実際に操作してみると、「前進」を押すとキャラクターがカメラの向き方向に移動することを確認できるはずです。

現在は、キャラクターを回転させて、移動方向を向くようにさせる必要があります。

回転速度用の変数を追加します。これにより、新しい方位に瞬時にスナップするのを防ぎます。

```gdscript
@export var rotation_speed = 12.0
```

次に、`_physics_process()` 関数の `move_and_slide()` 呼び出し後に以下を追加してください：

```gdscript
    if velocity.length() > 1.0:
        model.rotation.y = lerp_angle(model.rotation.y, spring_arm.rotation.y, rotation_speed * delta)
```

```python
import math

def lerp_angle(a, b, t):
    """線形補間により角度 a を角度 b に滑らかに変化させる関数。範囲 [0, 360] 内で動作する。"""
    normalized_a = a % 360
    normalized_b = b % 36ang

### アイダブルアールアニメーション作品

移動と回転が実装できたところで、次はアニメーションの選択に進みましょう。基本的な考え方は、キャラクターの水平速度（*x/z軸方向の動き*）を取得し、それを使って作成した`IWR`ブレンドスペース内のブレンド位置を設定することです。

# get_move_input() 関数内で、プレイヤーの速度を設定しています。その後、ブレンド位置を設定することができます：
blend_position = calculate_blend_position()
if blend_position > 0.5:  # 何らかの閾値チェック
    player.set_velocity(speed * 2)  # スピードを倍増させる例

```gdscript
    velocity = lerp(velocity, dir * speed, acceleration * delta)
    var vl = velocity * model.transform.basis
    anim_tree.set("parameters/IWR/blend_position", Vector2(vl.x, -vl.z) / speed)
```

```bash

注意: このパラメータパスは、{{< gd-icon AnimationTree >}}`AnimationTree`インスペクターを確認することで取得できます。実際にスクリプトウィンドウにドラッグ＆ドロップして入力することも可能です。

### 攻撃方法

攻撃動作については、まず「攻撃」という入力アクションを追加します。このコマンドは左マウスボタンに割り当てています。

{{< gd-icon AnimationTree >}} の `AnimationTree` には3つの異なる攻撃が存在するため、それらをリスト化します：

```gdscript
var attacks = [
    "1h_slice_diagonal",
    "1h_slice_horizontal",
    "1h_attack_chop"
]
```

それから、`_unhandled_input()` 関数内で、アクションが押されたときにリストからランダムなアニメーションを選択するようにします：

```gdscript
    if event.is_action_pressed("attack"):
        anim_state.travel(attacks.pick_random())
```

### ジャンプ動作

ジャンプモーションは複数のアニメーションが連動するため、やや複雑です。参考までに、状態マシンの設定手順を以下に示します：

![alt](/godot_recipes/4.x/img/anim_tree_jumping.png)

まず、「ジャンプ開始」アニメーションに移行するために `jumping = true` を設定します。これにより状態機械での遷移がトリガーされます。

```gdscript
    if is_on_floor() and Input.is_action_just_pressed("jump"):
        velocity.y = jump_speed
        jumping = true
        anim_tree.set("parameters/conditions/grounded", false)
    anim_tree.set("parameters/conditions/jumping", jumping)
```

次に、地面に接地したタイミングを把握する必要があります。これにより、「Jump_Idle」アニメーションから移行可能になります。これを実現するためには、前フレームと比較することで接地状態を追跡する必要があります。上部に新しい変数を追加しましょう：

```gdscript
var last_floor = true
```

そして最初の`if`文の後にこの`if`ステートメントがあります：

```gdscript
    # We just hit the floor after being in the air
    if is_on_floor() and not last_floor:
        jumping = false
        anim_tree.set("parameters/conditions/grounded", true)
    last_floor = is_on_floor()
```

最終的に、段差から飛び降りた際に「Jump_Idle」に直接移行する仕組みがあります：

```gdscript
    # We're in the air, but we didn't jump
    if not is_on_floor() and not jumping:
        anim_state.travel("Jump_Idle")
        anim_tree.set("parameters/conditions/grounded", false)
```

## まとめ

機能する制御可能なキャラクターにチェイスカメラと複数のアニメーションを追加しました。次は何が必要でしょうか？

[セクションの説明](/godot_recipes/4.x/3d/assets/) を参照すると、3D作業のさらなる事例や、ダウンロード可能なGodotプロジェクトなどの例を確認できます。

#### 関連動画

{{< youtube AW3rT-7J8ag >}}

