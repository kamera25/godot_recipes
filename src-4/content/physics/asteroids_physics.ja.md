---
title: "アステロイド風物理演算（RigidBody2Dを使用）"
weight: 12
draft: false
---

## 課題

「Astroids」のような半リアルな宇宙船を作成するため、{{< gd-icon RigidBody2D >}}`RigidBody2D`を使いたい。

## 解決策

{{< gd-icon RigidBody2D >}}`RigidBody2D` を使用する際には少し注意が必要です。Godotの物理エンジンによって制御されるため、直接移動させるのではなく力を加える必要があります。リジッドボディを扱う前に、[RigidBody2D APIドキュメント](https://docs.godotengine.org/ja/stable/classes/class_rigidbody2d.html)を必ず確認することを強くオススメします。これからこの例を進めていく過程で、このドキュメントを参照しながら進めていきます。

本例では、以下のノード設定を使用します。

```
{{< gd-icon RigidBody2D >}} RigidBody2D (Ship)
     {{< gd-icon Sprite2D >}} Sprite2D
     {{< gd-icon CollisionShape2D >}} CollisionShape2D
```

{{% notice style="tip" title="Spriteの向き" %}}
必ずスプライトを正しく配置してください。回転していないオブジェクトは **+X軸** 方向に向くようにしてください（つまり右方向を向いている状態）。スプライトのアートワークが別の方向を向いて描かれている場合は、 {{< gd-icon Sprite2D >}}`Sprite2D`（親ボディではなく）を適切に整列させるために回転させてください。
{{% /notice %}}

以下の入力を「インプットマップ」で使用します。

|アクション|キー|
|-------|---|
|`thrust`| **w** または ↑|
|`rotate_right`| **d** または →|
|`rotate_left`| **a** または ←|

RigidBody2Dにスクリプトを追加し、変数を定義します。

```gdscript
extends RigidBody2D

@export var engine_power = 800
@export var spin_power = 10000

var thrust = Vector2.ZERO
var rotation_dir = 0
```

最初の2つの変数は、船の「操縦性」を制御する方法を決定します。`engine_power`は加速と最高速度に影響を与えます。`spin_power`は船が回転する速さを調整します。

`thrust` と `rotation_dir` は入力操作によって設定されます。次にその方法を確認してください。

```gdscript
func get_input():
    thrust = Vector2.ZERO
    if Input.is_action_pressed("thrust"):
        thrust = transform.x * engine_power
    rotation_dir = Input.get_axis("rotate_left", "rotate_right")
```

もし`"thrust"`入力が有効になっている場合、`thrust`ベクトルを船の進行方向に設定します。一方、`rotation_dir`は回転入力に応じて `+/-1` に設定されます。

これらの値を `_physics_process()` で適用することで飛行を開始できます。

```gdscript
func _physics_process(_delta):
    get_input()
    constant_force = thrust
    constant_torque = rotation_dir * spin_power
```

動作はしますが、コントロールが非常に難しいのがお分かりでしょう。回転速度が速すぎて、画面外へ出る前に急激に加速してしまいます。ここで「実際の」宇宙物理の法則から脱却したい点があります。宇宙空間には摩擦がありませんが、弊社開発の『アステロイド』風宇宙船の場合、推力をかけていない時には自然に減速するようになれば、より簡単に操縦できるようになります。この制御には「減衰効果」が有効です。

{{< gd-icon RigidBody2D >}}`RigidBody2D`プロパティ内では、**直線／減衰**と**角速度／減衰**の設定があります。これらをそれぞれ**1**と**2**に設定すると、移動/回転の動きが遅くなり、さらに停止させる効果も生じます。

これらの値を自由に調整し、`engine_power` と `rotation_dir` との関係を試してみて下さい。

### 画面巻き戻し機能

画面の端を越えたときの移動処理は本当に「テレポート」です。船が画面右端から外れると、瞬時に左辺に移動します。ただし、単に`position`を変更しようとした場合、すぐに元に戻ってしまうことに気付くでしょう。これは、物理エンジンも位置制御を行っているためです。

この問題の解決策として、リジッドボディの `_integrate_forces()` コールバックを使用することが有効です。この関数内では、物理エンジンが行っている処理と干渉せずに、オブジェクトの物理特性を安全に更新できます。

スクリプトの上部に画面サイズを設定してください。

```gdscript
@onready var screensize = get_viewport_rect().size
```

次に新しい機能を追加してください。

```gdscript
func _integrate_forces(state):
    var xform = state.transform
    xform.origin.x = wrapf(xform.origin.x, 0, screensize.x)
    xform.origin.y = wrapf(xform.origin.y, 0, screensize.y)
    state.transform = xform
```

ご覧の通り、`_integrate_forces()` 関数には `state` というパラメーターが含まれています。このオブジェクトはボディの [PhysicsDirectBodyState2D](https://docs.godotengine.org/ja/stable/classes/class_physicsdirectbodystate2d.html) です。ここには、力、速度、位置など、現在の物理特性がすべて保持されています。

状態から現在の変換行列を取得し、`wrapf()` 関数を使用して画面全体を覆うように変更した後、元の状態に復元します。

以下が実際の表示例です。

![alt](/godot_recipes/4.x/img/asteroids_wrap.gif)

### 歪み補正機能

`_integrate_forces()`を使用して、問題なくボディの状態を変更できるもう一つの例を見てみてください。『ワープ』機構を追加するとします。プレイヤーが`"warp"`がアサインされた入力を押すと、船が画面内のランダムな位置に瞬間移動するようにします。

まず、このために新規変数を追加してください。

```gdscript
var teleport_pos = null
```

`get_input()` でランダムな座標をセットします。

```gdscript
    if Input.is_action_just_pressed("warp"):
        teleport_pos = Vector2(randf_range(0, screensize.x), randf_range(0, screensize.y))
```

最終的に、`_integrate_forces()` 関数では、`teleport_position` が設定されている場合、まずその値を適用した後にリセットします。

```gdscript
    if teleport_pos:
        physics_state.transform.origin = teleport_pos
        teleport_pos = null
```

![alt](/godot_recipes/4.x/img/asteroids_warp.gif)

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/asteroids_support](https://github.com/godotrecipes/asteroids_support)
