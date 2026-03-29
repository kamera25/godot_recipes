---
title: "Using CharacterBody2D"
weight: 1
draft: true
ghcommentid: 68
---

{{% notice note %}}
本チュートリアルはGodotレシピ集が公開される前に執筆されたものです。今後、当サイトの他のドキュメントと同様にフォーマットを更新する予定です。
{{% /notice %}}

Godot offers a number of collision objects to provide both collision detection and response. Trying to decide which one to use for your project can be confusing. You can avoid problems and simplify development if you understand how each each works and what their pros and cons are. In this tutorial, we'll look at the `CharacterBody2D` node and show some examples of how it can be used.

## 導入：物理ボディについて

ゲーム開発において、ゲーム内空間内の二つのオブジェクトが交差するか接触するかどうかを判断する必要が生じる場面は頻繁に存在します。これは「衝突検知」と呼ばれる処理です。衝突が検出された場合、通常は何らかのアクションを発生させたいものです。この部分を総称して「衝突応答」と呼びます。

Godot では3種類の物理ボディが提供されており、<a href="http://docs.godotengine.org/ja/latest/classes/class_physicsbody2d.html" target="_blank">`物理Body2D`</a> タイプに分類されます。

- {{< gd-icon StaticBody2D >}}`StaticBody2D`- {{< gd-icon StaticBody2D >}} `StaticBody2D`

スタティックボディとは、物理エンジンによって移動されないオブジェクトです。衝突検知には参加しますが、衝突に応じて移動することはありません。このタイプのボディは、環境の一部となるオブジェクトや、動的な挙動を必要としないオブジェクトに最もよく使用されます。

- [`RigidBody2D`]({{< gd-icon RigidBody2D >}}) `RigidBody2D`

このノードはシミュレーションされた2D物理を実装しています。直接リジッドボディを操作するのではなく、重力やインパルスなどの力を適用することで、物理エンジンがその結果生じる移動量を計算します。詳細は[Godot 3.0: リジッドボディ](/blog/2017/12/godot3_kyn_rigidbody1/)の記事をご覧ください。

- {{< gd-icon CharacterBody2D >}}`CharacterBody2D`

衝突検知機能を提供しますが、物理演算はしません。すべての移動処理はプログラムコードで実装する必要です。

## 衝突形状について

物理ボディは、任意の数の {{< gd-icon CollisionShape2D >}}`CollisionShape2D` オブジェクトを子要素として保持できます。これらの形状はオブジェクトの衝突判定範囲を定義し、他のオブジェクトとの接触検出に使用されます。

> ※注意：衝突検出を行うには、対象オブジェクトに少なくとも1つの`Shape2D`が割り当てられている必要があります。

最も一般的な方法は、オブジェクトの子要素として {{< gd-icon CollisionShape2D >}}`CollisionShape2D` または {{< gd-icon CollisionPolygon2D >}}`CollisionPolygon2D` を追加することです。これらのノードを使用すると、エディタワークスペース上で直接形状を描画できます。

> **注意:** エディタで衝突形状のスケールを変更する際は注意が必要です。インスペクタの「Scale」プロパティは常に `(1, 1)` に設定しておく必要があります。衝突形状のサイズを変更する場合は、必ずシェイプのハンドルを使用してください。

### 衝突レイヤーとマスクについて

Godotにおいて最も強力でありながらしばしば誤解されがちな衝突判定機能の一つが、「衝突レイヤーシステム」です。この仕組みを利用することで、多種多様なオブジェクト間で極めて複雑な相互作用を構築することが可能になります。核心となる概念は「レイヤー」と「マスク」です。各衝突オブジェクトは、32種類の異なる物理レイヤーと相互作用できるよう設計されています。

各プロパティを順番に見てみましょう:

-   **`衝突レイヤー`**
  オブジェクトが表示される物理層を定義します。デフォルトでは、すべてのボディはレイヤー `1` に配置されます。

 -    `collision_mask` は衝突検知対象のレイヤーを定義します。指定したマスク層に含まれないオブジェクトは、ボディによって無視されます。デフォルトでは、すべてのボディがレイヤー 1 をスキャンします。

また、レイヤーに名前を割り当てることもできます。「プロジェクト設定」内の「レイヤー名→2D物理」セクションをご確認ください。

![alt](/godot_recipes/3.x/img/k2d_layer_names.png?width=300)

身体のレイヤープロパティは、コードまたはインスペクタから直接設定できます。

![alt](/godot_recipes/3.x/img/k2d_layer_example.png?width=300)

**例：**

以下の構成で3つのノードがあります。

|レイヤー | マスク       |
|----------------|-------------|
|     **プレイヤー** | `1` | `2, 3` |
|     **敵キャラ**   | `2` | `1`    |
|     **コイン**     | `3` | `1`    |

このシナリオでは、「プレイヤー」ノードは「敵」と「コイン」の両方と衝突を検出します（スキャン対象レイヤーに含まれているため）。ただし、「敵」と「コイン」は互いに衝突を検出しません。なぜなら、彼らはそれぞれが属していないレイヤーのみをスキャンするように設定されているからです。

## キネマティックボディ

{{< gd-icon CharacterBody2D >}}`CharacterBody2D` is for implementing bodies that are to be controlled via code. They detect collisions with other bodies when moving, but are not affected by engine physics properties like gravity or friction. While this means that you have to write some code to create their behavior, it also means you have more precise control over how they move and react.

> **Note:** A {{< gd-icon CharacterBody2D >}}`CharacterBody2D` can be affected by gravity and other forces, but you must calculate the movement in code. The physics engine will not move a {{< gd-icon CharacterBody2D >}}`CharacterBody2D`.

### 移動と衝突判定

When moving a {{< gd-icon CharacterBody2D >}}`CharacterBody2D`, you should not set its `position` directly. Instead, you use the `move_and_collide()` or `move_and_slide()` methods. These methods move the body along a given vector and will instantly stop if a collision is detected with another body. After a {{< gd-icon CharacterBody2D >}}`CharacterBody2D` has collided, any _collision response_ must be coded manually.

> **注意:** キネマティックボディの移動は `_physics_process()` コールバック内のみで行ってください。

#### move_and_collide

このメソッドは1つの引数を取ります。ボディの相対移動を示す`Vector2`値です。通常は、これは速度ベクトルにフレーム時間ステップ（`delta`）を掛けたものとなります。もしエンジンがこのベクトル上のいずれかの位置で衝突を検知した場合、ボディはすぐに運動を停止します。この場合、メソッドは`KinematicCollision2D`オブジェクトを返します。

##### KinematicCollision2D

When a {{< gd-icon CharacterBody2D >}}`CharacterBody2D` detects a collision, Godot provides a <a href="http://docs.godotengine.org/en/latest/classes/class_kinematiccollision2d.html" target="_blank">`KinematicCollision2D`</a> object. This object contains data about the collision and the colliding object. Using this data you can calculate your collision response.

#### 移動とスライド処理

The `move_and_slide()` method is intended to simplify the collision response in the common case where you want one body to slide along the other. This is especially useful in platformers or top-down games, for example.

> **注意:** `move_and_slide()` 関数は内部で `delta` パラメータを使用してフレームベースの移動計算を自動的に行います。速度ベクトルに手動で `delta` を掛けたものを直接渡す必要はありません。

速度ベクトルに加え、`move_and_slide` には複数のパラメータが用意されており、スライド動作を細かくカスタマイズできます。

`floor_normal` - デフォルト値: `Vector2( 0, 0 )`

このパラメータでは、エンジンが床面として認識すべき表面を指定できます。これを設定すると、`is_on_floor()`、`is_on_wall()`、および `is_on_ceiling()` メソッドを使用して、対象オブジェクトがどの種類の表面に接触しているかを検出できるようになります。デフォルト値はすべての表面が壁として扱われることを意味します。

'slope_stop_min_velocity' - デフォルト値: '5'

これは、斜面に立ったときの最小速度です。これにより、静止状態の物体が坂を滑り落ちる現象を防ぎます。

`max_bounces` - デフォルト値: `4`

これは、物体の運動が停止するまでに発生する衝突の最大回数です。設定値を低くしすぎると、そもそも動きが発生しなくなる可能性があります。

`floor_max_angle` - デフォルト値: `0.785398`（ラジアン単位、約45度に相当）

これは、表面がもはや「床」として考慮されなくなる最大角度です。

### どちらを使用するべきか？

新規ユーザーからよく寄せられる質問の一つに「どの移動関数を使えばよいか？」というものがあります。
多くの場合、「よりシンプルだから」という理由から `move_and_slide()` が推奨されますが、必ずしもそうとは限りません。この概念を理解する一つの方法として、`move_and_slide()` は特殊なケースであり、`move_and_collide()` がより一般的なケースであると考えるとよいでしょう。例えば、以下の2つのコードスニペットはいずれも同じ衝突判定結果になります。

![alt](/godot_recipes/3.x/img/k2d_compare.gif)

{{< highlight gdscript>}}
var collision = move_and_collide(velocity * delta)
if collision:
	velocity = velocity.slide(collision.normal)
{{< /highlight >}}
{{< highlight gdscript>}}
velocity = move_and_slide(velocity)
{{< /highlight >}}

Anything you do with `move_and_slide()` can also be done with `move_and_collide()`,
it just might take a little more code. However, as we'll see in the examples below,
there are cases where `move_and_slide()` isn't the response you want.

## 使用例

以下の例で使用する[サンプルプロジェクト](/blog/img/KYN3.0_KinematicBody2D.zip)をダウンロードしてください。

## 基本動作

サンプルプロジェクトをダウンロード済みの場合、この例は「BasicMovement.tscn」シーンに含まれています。

For this example, Add a {{< gd-icon CharacterBody2D >}}`CharacterBody2D` with two children: a {{< gd-icon Sprite2D >}}`Sprite` and a {{< gd-icon CollisionShape2D >}}`CollisionShape2D`. As with many demos, we'll use the Godot "icon.png" as the {{< gd-icon Sprite2D >}}`Sprite`'s texture (drag it from the Filesystem dock to the "Texture" property of the `Sprite`). In the {{< gd-icon CollisionShape2D >}}`CollisionShape2D`'s "Shape" property, select "New RectangleShape2D" and size the rectangle to fit over the sprite image.

Attach a script to the {{< gd-icon CharacterBody2D >}}`CharacterBody2D` and add the following code:

{{< highlight gdscript >}}
extends CharacterBody2D

var speed = 250
var velocity = Vector2()

func get_input():
	# Detect up/down/left/right keystate and only move when pressed
	velocity = Vector2()
	if Input.is_action_pressed('ui_right'):
		velocity.x += 1
	if Input.is_action_pressed('ui_left'):
		velocity.x -= 1
	if Input.is_action_pressed('ui_down'):
		velocity.y += 1
	if Input.is_action_pressed('ui_up'):
		velocity.y -= 1
	velocity = velocity.normalized() * speed

func _physics_process(delta):
	get_input()
	move_and_collide(velocity * delta)
{{< /highlight >}}

このシーンを実行すると、`move_and_collide()`が想定通りに動作し、ボディが速度ベクトルに沿って移動することを確認できます。では、障害物を追加した場合にどうなるかを見てみましょう。矩形の衝突形状を持つ{{< gd-icon StaticBody2D >}}`StaticBody2D`オブジェクトを追加してください。視認性を高めるには、スプライトを使用するか、{{< gd-icon Polygon2D >}}`Polygon2D`を使用するか、あるいは「デバッグ」メニューから「可視衝突形状」を有効化する方法もあります。

Run the scene again and try moving into the obstacle. You'll see that the {{< gd-icon CharacterBody2D >}}`CharacterBody2D`
can't penetrate the obstacle. However, try moving into the obstacle at an angle and
you'll find that the obstacle acts like glue - it feels like the body gets stuck.

これは、衝突時の応答処理が定義されていないためです。`move_and_collide()` は単に衝突が発生した時点で物体の動きを停止させます。衝突に対して実装したい特定の応答ロジックをコーディングが必要です。

以下の変更を試してみてください。`move_and_slide(velocity)`に変更して再度実行してください。なお、速度計算から`delta`を削除していますのでご注意ください。

`move_and_slide()` は、衝突オブジェクトに沿って体を滑らせるというデフォルトの衝突応答を提供します。これは多くのゲームタイプで有用であり、必要な動作を得るために十分な場合があります。

次は、他の具体例をいくつか見ていきましょう。

### 跳ね返り/反射と衝突判定について

※スライディング衝突応答を不要とする場合について。このサンプルケース（「BounceandCollide.tscn」 - サンプルプロジェクト収録）では、キャラクターが弾丸を発射し、壁に当たって跳ね返る挙動を実現しています。

この例では、以下の3つのシーンを使用します。メインシーン（プレイヤーを含む）、弾丸シーン、壁シーンです。弾丸と壁は別々のシーンで定義されているため、インスタンス化ができます。

プレイヤーはW/Sキーで前進・後退操作し、マウスを使って狙いを定めます。以下にPlayer用のコードを示します（`move_and_slide()`関数を使用しています）：

{{< highlight gdscript >}}
extends CharacterBody2D

@export var Bullet: PackedScene
@export var speed: int

var velocity = Vector2()

func get_input():
	# add these actions in Project Settings -> Input Map
	velocity = Vector2()
	if Input.is_action_pressed('backward'):
		velocity = Vector2(-speed/3, 0).rotated(rotation)
	if Input.is_action_pressed('forward'):
		velocity = Vector2(speed, 0).rotated(rotation)
	if Input.is_action_just_pressed('mouse_click'):
		shoot()

func shoot():
	# "Muzzle" is a Marker2D placed at the barrel of the gun
	var b = Bullet.instantiate()
	b.start($Muzzle.global_position, rotation)
	get_parent().add_child(b)

func _physics_process(delta):
	get_input()
	var dir = get_global_mouse_position() - global_position
	# Don't move if too close to the mouse pointer
	if dir.length() > 5:
		rotation = dir.angle()
		velocity = move_and_slide(velocity)
{{< /highlight >}}

そして、弾丸のコード:

{{< highlight gdscript>}}
extends CharacterBody2D

var speed = 750
var velocity = Vector2()

func start(pos, dir):
	rotation = dir
	position = pos
	velocity = Vector2(speed, 0).rotated(rotation)

func _physics_process(delta):
	var collision = move_and_collide(velocity * delta)
	if collision:
		velocity = velocity.bounce(collision.normal)
		if collision.collider.has_method("hit"):
			collision.collider.hit()

func _on_VisibilityNotifier2D_screen_exited():
	queue_free()
{{< /highlight >}}

この処理は`_physics_process()`関数内で行われます。`move_and_collide()`を使用した後に衝突が発生した場合、`KinematicCollision2D`オブジェクトが返されます（発生しなかった場合は戻り値は`Nil`となります）。

衝突が検出された場合、衝突の法線ベクトルを用いて弾丸の速度を反射させます。`bounce()` は Vector2 クラスのメソッドです。

衝突するオブジェクト（`collider`）に`hit`メソッドが定義されている場合、
そちらも呼び出します。サンプルプロジェクトでは、この機能を可視化するために、壁に点滅効果を追加しています。

![alt](/godot_recipes/3.x/img/k2d_bullet_bounce.gif)

### ムーブアンドスライドを使ったプラットフォーマー開発

もう一つ例を挙げてみましょう。これはよく質問される2Dプラットフォーマーについてです。`move_and_slide()`関数は、機能的なキャラクターコントローラーを迅速に実装するのに最適です。サンプルプロジェクトをダウンロードした場合、この機能は"Platformer.tscn"ファイル内で確認できます。

本例では、スタティックボディ（StaticBody2D）オブジェクトで構成されるレベルを想定しています。形状やサイズは任意のもので構いません。サンプルプロジェクトではタイルマップを使用してレベルを配置していますが、このデモの目的上、個々のスタティックボディとして扱うことも同様にできます。

また、かわいらしい[Ansimuz作『サニーランド』アートパック](https://opengameart.org/content/sunny-land-2d-pixel-art-pack)をアートワークとキャラクターアニメーションに採用しています。

プレイヤーの本体のコードは次のとおりです:

{{< highlight gdscript >}}
extends CharacterBody2D

@export var run_speed: int
@export var jump_speed: int
@export var gravity: int

enum {IDLE, RUN, JUMP}
var velocity = Vector2()
var state
var anim
var new_anim

func _ready():
    change_state(IDLE)

func change_state(new_state):
    state = new_state
    match state:
        IDLE:
            new_anim = 'idle'
        RUN:
            new_anim = 'run'
        JUMP:
            new_anim = 'jump_up'

func get_input():
    velocity.x = 0
    var right = Input.is_action_pressed('ui_right')
    var left = Input.is_action_pressed('ui_left')
    var jump = Input.is_action_just_pressed('ui_select')

    if jump and is_on_floor():
        change_state(JUMP)
        velocity.y = jump_speed
    if right:
        change_state(RUN)
        velocity.x += run_speed
    if left:
        change_state(RUN)
        velocity.x -= run_speed
    $Sprite.flip_h = velocity.x < 0
    if !right and !left and state == RUN:
        change_state(IDLE)

func _process(delta):
    get_input()
    if new_anim != anim:
        anim = new_anim
        $AnimationPlayer.play(anim)

func _physics_process(delta):
    velocity.y += gravity * delta
    if state == JUMP:
        if is_on_floor():
            change_state(IDLE)
    velocity = move_and_slide(velocity, Vector2(0, -1))

    if position.y > 600:
        get_tree().reload_current_scene()
{{< /highlight >}}

![alt](/godot_recipes/3.x/img/k2d_platf_sample.gif?width=300)

現在、キャラクターの待機状態・走行状態・ジャンプ状態間の遷移を管理するため、非常に基本的なステートマシンを使用しています。

When using `move_and_slide()` the function returns a vector representing the
movement that remained after the slide collision occurred. Setting that value back
to the character's `velocity` allows us to smoothly move up and down slopes. Try
removing `velocity =` and see what happens if you don't do this.

また、床面の法線ベクトルとして `Vector2(0, -1)` を追加しました。このベクトルは真上を指しています。つまり、キャラクターがこの法線を持つ物体に衝突した場合、それは床と判定されることを意味します。

床法線ベクトルを使用することで、`is_on_floor()` 関数によるジャンプ動作を実現できます。この関数は、`move_and_slide()` 衝突処理の後、衝突物体の法線が指定された床ベクトルに対して45度以内になった場合にのみ `true` を返します（これは `floor_max_angle` 変数を調整することで変更できます）。

これにより、`is_on_wall()` を使用して壁ジャンプなどの他の機能も実装できます、
例えば。

## 結論

This introduction only scratches the surface of what's possible with {{< gd-icon CharacterBody2D >}}`CharacterBody2D`.
As with all Godot nodes, <a href="http://docs.godotengine.org/en/latest/classes/class_kinematicbody2d.html" target="_blank">
the API documentation</a> is your friend, so reference it frequently until you're
comfortable with the class methods.

運動体は非常に便利な仕組みなので、今後は『ノードの活用術』といった続編記事でさらに多くの活用法を探っていきたいと思います。その他に取り上げてほしい具体例やアイデアがあれば、ぜひコメント欄でご意見をお寄せください。

### <a href="/blog/img/KYN3.0_KinematicBody2D.zip">サンプルプロジェクトをダウンロード</a>
