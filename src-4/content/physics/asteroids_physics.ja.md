---
title: "Asteroids-style Physics (using RigidBody2D)"
weight: 12
draft: false
---

## 問題文

```
「Astroids」のような半リアルな宇宙船を作成するため、`RigidBody2D`を使いたいと考えていますか。

## 解決策

````{{< gd-icon RigidBody2D >}}`RigidBody2D` を使用する際には少し注意が必要です。Godotの物理エンジンによって制御されるため、直接移動させるのではなく力を加える必要があります。剛性ボディを扱う前に、[RigidBody2D APIドキュメント](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html)を必ず確認することを強くお勧めします。これからこの例を進めていく過程で、このドキュメントを参照しながら進めていきましょう。

本例では、以下のノード設定を使用します：

```
{{< gd-icon RigidBody2D >}} RigidBody2D (Ship)
     {{< gd-icon Sprite2D >}} Sprite2D
     {{< gd-icon CollisionShape2D >}} CollisionShape2D
```

{{% notice style="tip" title="Sprite orientation" %}}
Don't forget to orient your sprite correctly. An object that is not rotated should be pointing along the **+X** axis, i.e. to the right. If your sprite's art is drawn facing in another direction, rotate the {{< gd-icon Sprite2D >}}`Sprite2D` (not the parent body) to align it correctly.
{{% /notice %}}

以下の入力を「入力マップ」で使用します：

|入力方法|キー|
|-------|---|
|`thrust`| **w** または ↑|
|`rotate_right`| **d** または →|
|`rotate_left`| **a** または ←|

スクリプトをボディに追加し、いくつかの変数を定義しましょう：

```gdscript
extends RigidBody2D

@export var engine_power = 800
@export var spin_power = 10000

var thrust = Vector2.ZERO
var rotation_dir = 0
```

The first two variables are how we'll control the ship's "handling". `engine_power` is going to affect acceleration and top speed. `spin_power` controls how fast the ship rotates.

`thrust` と `rotation_dir` は入力操作によって設定されます。次にその方法を確認しましょう：

```gdscript
func get_input():
    thrust = Vector2.ZERO
    if Input.is_action_pressed("thrust"):
        thrust = transform.x * engine_power
    rotation_dir = Input.get_axis("rotate_left", "rotate_right")
```

If we're pressing the `"thrust"` input, we'll set the `thrust` vector to the ship's forward direction, while `rotation_dir` will be `+/-1` based on the rotate inputs.

これらの値を `_physics_process()` で適用することで飛行を開始できます：

```gdscript
func _physics_process(_delta):
    get_input()
    constant_force = thrust
    constant_torque = rotation_dir * spin_power
```

It works, but you'll notice that it's very hard to control. The rotation is too fast, and it accelerates to a high speed before going offscreen. This is where we want to break from "real" space physics. In space, there's no friction, but our Asteroids-style ship will be a lot easier to control if it coasted to a stop when we're not thrusting. We can control this with *damping*.

{{< gd-icon RigidBody2D >}}`RigidBody2D`プロパティ内では、**直線／減衰**と**角速度／減衰**の設定があります。これらをそれぞれ**1**と**2**に設定すると、移動/回転の動きが遅くなり、さらに停止させる効果も生じます。

これらの値を自由に調整し、`エンジン出力` と `回転力` との関係を試してみて下さい。

### 画面巻き戻し機能

画面の端を越えたときの移動処理は本当に「テレポート」です：船が画面右端から外れると、瞬時に左辺に移動します。ただし、単に`position`を変更しようとした場合、すぐに元に戻ってしまうことに気付くでしょう。これは、物理エンジンも位置制御を行っているためです。

この問題の解決策として、リジッドボディの `_integrate_forces()` コールバックを使用することが有効です。この関数内では、物理エンジンが行っている処理と干渉することなく、オブジェクトの物理特性を安全に更新できます。

スクリプトの上部に画面サイズを設定しましょう：

```gdscript
@onready var screensize = get_viewport_rect().size
```

次に新しい機能を追加します：

```gdscript
func _integrate_forces(state):
    var xform = state.transform
    xform.origin.x = wrapf(xform.origin.x, 0, screensize.x)
    xform.origin.y = wrapf(xform.origin.y, 0, screensize.y)
    state.transform = xform
```

ご覧の通り、`_integrate_forces()` 関数には `state` というパラメータが含まれています。このオブジェクトはボディの [PhysicsDirectBodyState2D](https://docs.godotengine.org/en/stable/classes/class_physicsdirectbodystate2d.html) です。ここには、力、速度、位置など、現在の物理特性がすべて保持されています。

州レベルでは、現在の変換行列を取得し、`wrapf()` 関数を使用して画面全体を覆うように変更した後、元の状態に復元します。

以下が実際の表示例です：

※訳注: 画像ファイルのパスは日本語版環境に合わせて修正する必要があります

### 歪み補正機能

Let's look at one more example of using `_integrate_forces()` to alter the body's state without issues. Let's add a "warp" mechanic - when the player presses the `"warp"` input, the ship will teleport to a random spot on the screen.

まず、このために新規変数を追加します：

```gdscript
var teleport_pos = null
```

```python
def get_input():
    # ランダムな位置を設定
    position = random.randint(0, 2)  # 0, 1, または 2のいずれかの位置に移動
    return position
```

```gdscript
    if Input.is_action_just_pressed("warp"):
        teleport_pos = Vector2(randf_range(0, screensize.x), randf_range(0, screensize.y))
```

最終的に、`_integrate_forces()` 関数では、`teleport_position` が設定されている場合、まずその値を適用した後にリセットします：

```gdscript
    if teleport_pos:
        physics_state.transform.origin = teleport_pos
        teleport_pos = null
```

![alt](/godot_recipes/4.x/img/asteroids_warp.gif)

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/asteroids_support](https://github.com/godotrecipes/asteroids_support)
