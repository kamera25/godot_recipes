---
title: "RigidBody2D"
draft: true
ghcommentid: 99
tags: []
---

## `{{< gd-icon RigidBody2D >}}`RigidBody2D`

{{< gd-icon RigidBody2D >}}`RigidBody2D`はGodotが提供する物理シミュレーション用のボディコンポーネントです。これはつまり、ユーザーが直接{{< gd-icon RigidBody2D >}}`RigidBody2D`を操作するものではないということを意味します。代わりに、重力や衝撃力などの各種フォースを適用すると、Godot組み込みの物理エンジンが衝突検知・弾性挙動・回転運動などを含む最終的な移動計算を自動で行います。

{{% notice warning %}}
Setting a {{< gd-icon RigidBody2D >}}`RigidBody2D`'s physical properties, such as `position` or `linear_velocity` directly will not work correctly. The physics engine controls these values.
{{% /notice %}}

The body’s behavior is also affected by the world, via the Project Settings -> 物理 properties, or by entering an {{< gd-icon Area2D >}}`Area2D` that is overriding the global physics properties.

適切に使用すれば、リジッドボディはGodotツールキットの中でも強力な武器となります。しかし、多くのユーザーが誤った用途で使ったり、その仕組みを正確に理解していないためにトラブルに見舞われることがあります。

[API ドキュメント](https://docs.godotengine.org/ja/stable/classes/class_rigidbody2d.html)

### ノードのプロパティ

以下に主要な特性をご説明します。

モード（`mode`）

剛体には4つの異なるモードが存在し、それぞれその挙動に影響を与えます。

1. リジッド - これがデフォルトモードです。オブジェクトは物理的な剛体として動作し、衝突や外力の影響を受けます。
1. 静的 - このモードでオブジェクトは静止状態を保ちます。{{< gd-icon StaticBody2D >}}`StaticBody2D`と同様の挙動をします。
1. キャラクター - このモードではオブジェクトの動作は通常のリジッドモードと同じですが、回転はしません。
1. キネマティック - このモードではオブジェクトは {{< gd-icon KinematicBody2D >}}`KinematicBody2D`と同様に、コードによる制御でのみ移動できます。**注記:** これは `move_and_slide()` といった {{< gd-icon KinematicBody2D >}}`KinematicBody2D`の補助関数を利用できるという意味ではありません。すべての移動と衝突応答は手動で実装が必要です。

* 重力スケール設定（`gravity_scale`）

この値はボディに適用される重力を乗算します。総重力は **プロジェクト設定** の「デフォルト重力」値と、{{< gd-icon Area2D >}} `Area2D` ノードによって追加で適用された任意の重力の合計です。

* 定常力
     * 作用力（`applied_force`）

    このプロパティを使用すると、体に作用する総力を取得または設定できます。

  * 適用トルク（'applied_torque`）

    このプロパティを使用することで、身体に適用されている総トルクの取得または設定ができます。

* 連続CD（`continuous_cd`）

※高速移動する物体が障害物を貫通してしまう場合、この機能を有効にする必要があるかもしれません。「連続衝突判定」は、移動後に個別に衝突チェックを行うのではなく、経路に沿って継続的に物体を動かすことで衝突を事前に予測します。精度は向上しますが処理負荷も大きくなるため、使用には注意が必要です。

### 便利な機能

剛性体に力を加えるには、以下の2つの関数から選択できます。

* `add_force()` / `add_central_force()`

物体に連続的な力を加えます。ロケットの推進力をイメージすると分かりやすいでしょう。この力は継続的に働き、徐々に速度を上げていきます。なお、これは既存のすべての力に追加されるものです。取り除くまで力は持続して作用し続けます。

* `apply_impulse()` / `apply_central_impulse()`

瞬時に「力強さ」を与える動作です。野球のバットでボールを打つ様子をイメージしてください。

* `_integrate_forces()`


### 衝突検出機能

デフォルトでは、`RigidBody2D` オブジェクトが他の空間内の物体と衝突・相互作用しても、その衝突は報告されません。

衝突情報を剛性体から取得する場合は、`contact_monitor` を `true` に設定が必要です。これを行うと、`body_entered` などのシグナルが有効になります。さらに、`contacts_reported` を調整することで、報告される衝突の数を指定することもできます。

### 剛体の制御について

硬い物体をより直接的に制御する必要があるケースもあります。例えば、クラシックゲーム『Asteroids』のリメイクを作ろうとしている場合を考えてみましょう。プレイヤーの宇宙船は左右矢印キーで回転させ、上矢印が押されたときに前進するようにしなければなりません。

デフォルトでは、プロジェクト設定で設定した**減衰効果**がボディの速度と回転を抑制します。宇宙空間には摩擦がないため、本来はこのような減衰は存在しないはずです。ただし、「スペースインベーダー」風のゲーム体験を実現するためには、キーを離すと機体が徐々に停止し、回転も自然に止まるようにしたいところです。これを実現するため、インスペクター画面で以下の値を設定します。
- 角加速度減衰係数：`5`
- 直線加速度減衰係数：`1`

以下がコードです：

```gdscript
extends RigidBody2D

export var engine_thrust = 500
export var spin_thrust = 15000

var thrust = Vector2()
var rotation_dir = 0
var screensize

func _ready():
    screensize = get_viewport().get_visible_rect().size

func get_input():
    if Input.is_action_pressed("ui_up"):
        thrust = transform.x * engine_thrust
    else:
        thrust = Vector2()
    rotation_dir = 0
    if Input.is_action_pressed("ui_right"):
        rotation_dir += 1
    if Input.is_action_pressed("ui_left"):
        rotation_dir -= 1

func _process(delta):
    get_input()

func _physics_process(delta):
    applied_force = thrust
    applied_torque = rotation_dir * spin_thrust
```

Let’s walk through what this script is doing. The two variables, `engine_thrust` and `spin_thrust` control how fast the ship can accelerate and turn. `thrust` will represent the ship’s engine state: `(0, 0)` when coasting, or a vector with the length of `engine_thrust` when powered on. `rotation_dir` will represent what direction the ship is turning. The `screensize` variable will capture the size of the screen, which we’ll be using later.

次に、`input()` 関数はキー状態を取得し、宇宙船の推進モードを有効/無効に設定するとともに、回転方向（`rotation_dir`）を正または負方向に決定します。この関数は `_process()` 内で毎フレーム呼び出されます。

最終的に、物理関連の処理は`_physics_process()`関数内で呼び出されるべきです。この部分では、船が向いている方向に沿って推力を発生させるために`applied_force`を設定します。さらに、船を回転させるため`applied_torque`も適切に設定します。

シーンを再生 - 自由に飛行できるはずです：

![alt](/godot_recipes/3.x/img/rigidbody_ship1.gif)

#### ポジション問題

「アステロイド」のもう一つの特徴は、画面がループ構造になっている点です。プレイヤーが片側からはみ出すと、反対側にテレポートします。ただし、前述のように、物理エンジンを壊さずに剛体の位置を変更することはできないという課題がありました。これは剛体を操作する際に重大な問題を引き起こします。

以下のような方法を試すことができます。

```gdscript
func _physics_process(delta):
    if position.x > screensize.x:
        position.x = 0
    if position.x < 0:
        position.x = screensize.x
    if position.y > screensize.y:
        position.y = 0
    if position.y < 0:
        position.y = screensize.y
    applied_force = thrust
    applied_torque = rotation_dir * spin_thrust
```

ただし、画面の端に引っかかって動けなくなるという大失敗をしてしまいますよ。

[RigidBody2D ドキュメント](https://docs.godotengine.org/ja/stable/classes/class_rigidbody2d.html) から引用すると：

* リジッドボディの位置や線形速度をフレームごとに、あるいは頻繁に変更するのは避けるべきです。状態を直接操作する必要がある場合は、物理演算の状態を直接取得できる `_integrate_forces` メソッドを使用してください。

 _physics_process() の代わりに `_integrate_forces()` を使用するべきです。この関数では、ボディの [物理2DDirectBodyState](http://docs.godotengine.org/en/stable/classes/class_physics2ddirectbodystate.html) を安全に変更できるからです。
 関連するドキュメントをぜひ参照してください。物理状態オブジェクトには非常に便利な情報がたくさん含まれています。場合、最も重要なのはボディの [Transform2D](http://docs.godotengine.org/en/stable/classes/class_transform2d.html) に関する情報です。

したがって、`_integrate_forces()` に移動して以下のようにコードを記述します。

```gdscript
func _integrate_forces(state):
    applied_force = thrust
    applied_torque = rotation_dir * spin_thrust
    if position.x > screensize.x:
        state.transform.origin.x = 0
    if position.x < 0:
        state.transform.origin.x = screensize.x
    if position.y > screensize.y:
        state.transform.origin.y = 0
    if position.y < 0:
        state.transform.origin.y = screensize.y
```

物理状態に基づいてボディの 'transform' を調整することで、エンジンは正常に動作し続け、期待通りの結果が得られます。

![alt](/godot_recipes/3.x/img/rigidbody_ship2.gif)

<!-- #### Videoが気に入ったら？ -->

{{< youtube  >}} -->