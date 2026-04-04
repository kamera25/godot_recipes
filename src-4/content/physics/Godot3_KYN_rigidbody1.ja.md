---
title: "リジッドボディを使用"
weight: 1
draft: true
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

{{% notice note %}}
本チュートリアルはGodotレシピ集が公開される前に執筆されたものです。今後、当サイトの他のドキュメントと同様にフォーマットを更新する予定です。
{{% /notice %}}

このチュートリアルでは、リジッドボディを使用するべきタイミング（および使用すべきでないタイミング）や、仕組みの解説、さらには思い通りに制御するための便利なテクニックをいくつかご紹介します。具体例ではRigidBody2Dを使用しますが、ここで学ぶ内容は3Dモデルにも同様に適用できます。

## はじめに

<a href="http://docs.godotengine.org/ja/latest/classes/class_rigidbody2d.html" target="_blank"><svg width="18" height="18" class="icon-icon_rigid_body_2d">
<use xlink:href="/blog/img/symbol-defs.svg#icon-icon_rigid_body_2d"></svg> `RigidBody2D`</a> とは、Godot において物理シミュレーションを提供するオブジェクトです。これはつまり、直接 RigidBody2D を操作するわけではないということです。代わりに力（重力、衝撃など）を加えると、Godot の内蔵物理エンジンが衝突・反発・回転などの運動結果を計算してくれます。

RigidBody2Dの動作は「質量」「摩擦」「反発」などのプロパティを通じて変更できます。
これらの設定はインスペクタから行えます。

![alt](/godot_recipes/4.x/img/rigidbody_properties.png)

The body's behavior is also affected by the world, via the _Project Settings -> Physics_
properties, or by entering an <a href="http://docs.godotengine.org/ja/latest/classes/class_area2d.html"><svg width="18" height="18" class="icon-icon_area_2d" target="_blank"><use xlink:href="/blog/img/symbol-defs.svg#icon-icon_area_2d"></svg> `Area2D`</a> that is overriding the global physics properties.

## RigidBody2Dを使う

リジッドボディを使用する主な利点の一つは、コードを1行も書かなくても、多くの動作機能が「無料」で手に入る点です。例えば、落下ブロックを使った簡易的な『Angry Birds』風ゲームを作る場合を考えてみます。必要なのはブロックと発射体用にRigidBody2Dを作成し、各プロパティを設定するだけです。積み重なり、落下、跳ね返りといった物理演算処理はすべて自動的に物理エンジンが担当してくれます。

### ブロックの積み重ね方

Start by creating a RigidBody2D for the block and adding <a href="http://docs.godotengine.org/ja/latest/classes/class_sprite.html" target="_blank"><svg width="18" height="18" class="icon-icon_sprite"><use xlink:href="/blog/img/symbol-defs.svg#icon-icon_sprite"></svg>`Sprite`</a> and
<a href="http://docs.godotengine.org/ja/latest/classes/class_collisionshape2D.html" target="_blank"><svg width="18" height="18" class="icon-icon_collision_shape_2d"><use xlink:href="/blog/img/symbol-defs.svg#icon-icon_collision_shape_2d"></svg>`CollisionShape2D`</a>
children:

![alt](/godot_recipes/4.x/img/rigidbody_block_scene.png)

スプライトにテクスチャを追加し、矩形の衝突形状を設定します。**重要** ： 衝突形状のスケールは__変更しないでください__。一般的にこれは推奨されない方法であり、予期しない衝突挙動を引き起こす原因となります。常に形状内のサイズハンドルを使用し、外側の`Node2D`由来のスケーリングハンドルは使わないようにしてください。

> ※重要：本サンプルで使用しているテクスチャは、Kenney.nl の[物理アセットパック](http://kenney.nl/assets/physics-assets)を使用しています。このパッケージには、さまざまな形状・材質のブロックが多数収録されています。

※「再生」を押すとブロックがゆっくりと下方に落ちていくのが確認できるでしょう。これはデフォルトで設定されているグローバルな重力によるものです。この設定は「プロジェクト設定」→［物理］→［2D］セクションで確認できます。また、インスペクターで「Block」オブジェクトの`Gravity Scale`プロパティを変更してみるのもよいでしょう。私は値を`3`に設定しています。

メインシーンを作成します（通常は<a href="http://docs.godotengine.org/ja/latest/classes/class_node.html" target="_blank"><svg width="18" height="18" class="icon-icon_node"><use xlink:href="/blog/img/symbol-defs.svg#icon-icon_node"></svg>Node</a>を使用します）。
地面と壁として機能させるため、長方形の衝突形状を持つ<a href="http://docs.godotengine.org/ja/latest/classes/class_staticbody2d.html" target="_blank"><svg width="18" height="18" class="icon-icon_staticbody2d"><use xlink:href="/blog/img/symbol-defs.svg#icon-icon_static_body_2d"></svg>StaticBody2D</a>ノードをいくつか追加してください。

インスタンス化したブロックを複製します（Windows では Ctrl+D、macOS では Command+D）。これで綺麗なスタックを作成できます。例えば：

![alt](/godot_recipes/4.x/img/rigidbody_scene1.png)

### 投射物

以下の手順に従って作成してください。
* Blockと同じノード構成で、名前を「ボール」に変更した新しいシーンを作成します。
* 球体テクスチャのいずれかと、円形の衝突判定形状を選択してください。
* このインスタンスをメインシーンに配置し、ブロックスタックの側面などに設置してください。

リジッドボディを動かすには、何らかの初速度が必要です。以下の方法で物体に初期速度を設定できます。「線形プロパティ」＞「速度」。試しにこれを `(500, 0)` に設定してみてください。

![alt](/godot_recipes/4.x/img/rigidbody_vel.gif)

また、ボールの `Friction（摩擦力）`と `Bounce（反発係数）`プロパティも調整できます。これらはどちらもゼロから1の範囲内で設定できます。個人的には「0.5」前後の反発係数が好みです。

> 重要：物理ボディのスケール変更は絶対に行わないでください！試行した場合、警告が表示され、
> シーンを実行すると、物理エンジンが自動的にスケールを初期値`(1, 1)`にリセットします。

### 力の作用

Linear velocityをリセットして`(0, 0)`に設定します。では、ボールを投げて動かす場合は？リジッドボディの速度や位置は手動で直接設定するべきではありません - これらは「現実世界」の物理法則を再現するためのものです。現実の世界では、物体が突然別の場所へ移動したり、静止状態から高速に移動したりすることはありません。こうした操作を試みると、物理エンジンがそれを拒否し、予期しない動きが生じる原因となります。代わりに、特定の方向に加速度を発生させる力を適用が必要です（これはニュートンの第二法則としても知られています）。Godotの物理オブジェクトも全く同じ仕組みで動作します。

リジッドボディに力を加えるには、以下の2つの関数から選択できます。

- `add_force()`

物体に連続的な力を加えます。ロケットの推進力のように、一定の力で加速を続ける様子を想像してください。なお、これは既存のすべての力に加算されるものです。除去されるまで、この力は継続的に作用し続けます。

- `apply_impulse()`

身体に「瞬間的な『力』」を瞬時に加えます。野球のバットでボールを叩く動作を想像してください。

クリック、ドラッグ、マウスボタンを放した時にボールを蹴るように「apply_impulse()」を使用します。

「プロジェクト設定」を開き、「インプット」タブで「クリック」という新しいアクションを追加します。
これを左マウスボタンに接続してください。

次に、ボールにスクリプトを追加し、以下のコードを記述します。

{{< highlight swift >}}
extends RigidBody2D

var dragging
var drag_start = Vector2()

func _input(event):
    if event.is_action_pressed("click") and not dragging:
        dragging = true
        drag_start = get_global_mouse_position()
    if event.is_action_released("click") and dragging:
        dragging = false
        var drag_end = get_global_mouse_position()
        var dir = drag_start - drag_end
        apply_impulse(Vector2(), dir * 5)
{{< /highlight >}}

このスクリプトでは、マウスボタンが押されたときに `dragging` を有効にし、クリック位置を記録します。ボタンを離すと、クリックポイントからリリースポイントまでのベクトルを求め、それを用いてインパルスを適用します（スケールを調整するために `5` で乗算）。 `apply_impulse()` は第1引数として `offset` も取ります。これにより、必要に応じてボディを中心以外の地点で「ヒット」させることができます。例えば、これを `Vector2(25, 0)` に設定すると、ボールを発射する際にスピンを加えることができます。

![alt](/godot_recipes/4.x/img/rigidbody_impulse.gif)

## リジッドボディの制御について

より直接的なリジッドボディ制御が必要になるケースがあります。例えば：
古典的なゲーム『アステロイド』のリメイクを作ろうとしている場合を考えてみます。プレイヤーの宇宙船は、左右矢印キーで回転させ、上矢印キーを押すと前進するように設計が必要です。

以下が私の船で使用している画像です。

![alt](/godot_recipes/4.x/img/ship_red.png)

また、[OpenGameArt](http://opengameart.org/) もチェックして、「素敵な宇宙背景画像」（ただしこれは完全に任意です）を検索することをオススメします。

上記と同様に、以下のノード構造を用いて艦船用の新規シーンを作成してください。

- `RigidBody2D`
    - `Sprite`
    - `CollisionShape2D`

> 注意：Godot 3.0では、0度は右方向（**x** 軸に沿って）を指します。
> このため、`Sprite` に `Rotation` を 90度追加する必要があります。そうすることで
> スプライトの向きが物体の方向と一致するようになります。

デフォルトでは、物理設定により物体の速度と回転運動に適度な_減衰効果が付与されます_。
宇宙空間には摩擦がないため、本来はいかなる種類の減衰も適用すべきではありません。
しかし「スペースインベーダー」風のゲーム感を出すため、キーを離すと船が即座に停止するようにしたいので、
船の`Angular -> Damp`パラメータを`5`に設定してください。

{{< highlight swift >}}
extends RigidBody2D

@export var engine_thrust: int
@export var spin_thrust: int

var thrust = Vector2()
var rotation_dir = 0
var screensize

func _ready():
    screensize = get_viewport().get_visible_rect().size

func get_input():
    if Input.is_action_pressed("ui_up"):
        thrust = Vector2(engine_thrust, 0)
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
    set_applied_force(thrust.rotated(rotation))
    set_applied_torque(rotation_dir * spin_thrust)

{{< /highlight >}}

このスクリプトの動作について説明します。変数`engine_thrust`と`spin_thrust`は、宇宙船の加速速度と旋回性能を制御します。インスペクタではそれぞれ500、25000に設定してください（トルク単位のため数値が大きくなります）。
変数`thrust`は宇宙船のエンジン状態を示します。走行中時は(0, 0)、動力がオンの場合は`engine_thrust`の長さを持つベクトルとなります。
`rotation_dir`は宇宙船の旋回方向を表現します。`screensize`変数には画面サイズを保持し、後ほど使用します。

next,
次に、`input()` 関数はキー状態を取得し、宇宙船の `thrust` を
オン/オフに設定するとともに、回転方向 (`rotation_dir`) を正または負に設定します。この
関数は毎フレーム `_process()` 内で呼び出されます。

最後に、物理関連の処理は`_physics_process()`内で行う必要があります。ここではまず、船が向いている`方向`に沿って`推力`を適用するために`set_applied_force()`を使用しています。その後、`set_applied_torque()`を使用して船を回転させます。

シーンを再生してください - 自由に空を飛べるはずです。

![alt](/godot_recipes/4.x/img/rigidbody_ship1.gif)

## 位置問題

もう一つの『アステロイド』の特徴的な要素として、画面が循環表示（ラップ・アラウンド）されるという点があります。プレイヤーが片側から画面外へ出ると、反対側に瞬時に移動します。ただし、先に述べたように、物理エンジンを破綻させることなくリジッドボディの位置を変更することはできないという根本的な問題があります。この点はリジッドボディを扱う際に非常に大きな課題となります。

よくある間違いとして、次のようなコードを`_physics_process()`関数に追加しようとするケースがあります。

{{< highlight swift >}}
func _physics_process(delta):
    if position.x > screensize.x:
        position.x = 0
    if position.x < 0:
        position.x = screensize.x
    if position.y > screensize.y:
        position.y = 0
    if position.y < 0:
        position.y = screensize.y
    set_applied_force(thrust.rotated(rotation))
    set_applied_torque(rotation_dir * spin_thrust)
{{< /highlight >}}

これは見事に失敗し、プレイヤーを画面の端に閉じ込めてしまう（時折グリッチも発生）。なぜこれが機能しないのでしょうか？ドキュメントには `_physics_process()` は物理関連処理用だと書いてありますよね？

正確には違います。`_physics_process()` は物理時間ステップに同期されていますが、だからといってあらゆる処理に使えるわけではありません。ただし、解決策はドキュメントに記載されていますのでご安心ください。

[RigidBody2Dドキュメント](http://docs.godotengine.org/ja/latest/classes/class_rigidbody2d.html#description)より引用すると：

> リジッドボディの位置や直線速度をフレームごとに、あるいは頻繁に変更することは避けるべきです。状態に直接影響を与えたい場合は、物理演算の状態を直接操作できる `_integrate_forces` メソッドを使用してください。

[_integrate_forces の説明](http://docs.godotengine.org/ja/latest/classes/class_rigidbody2d.html#class-rigidbody2d-integrate-forces)：

> オブジェクトのシミュレーション状態を読み取り、**安全に変更**できます。物体の位置やその他の物理特性を直接変更する必要がある場合は、`_physics_process` の代わりにこの関数を使用してください。

このように、`_physics_process()` の代わりに `_integrate_forces()` を使用が必要です。これにより、<a href="http://docs.godotengine.org/ja/latest/classes/class_physics2ddirectbodystate.html" target="_blank">Physics2DDirectBodyState</a> オブジェクトにアクセスできるようになります。物理状態オブジェクトには、非常に有用な情報が豊富に含まれているので、ぜひリンク先のドキュメントを参照されることを強くオススメします。
特に重要な情報は、物体の <a href="http://docs.godotengine.org/ja/latest/classes/class_transform2d.html" target="_blank">Transform2D</a> です。
（変換についての詳細な説明はこの文書の範囲を超えますので、より詳しい情報は[行列と変換](http://docs.godotengine.org/ja/latest/learning/features/math/matrices_and_transforms.html)を参照してください。）

Bodyの位置はトランスフォームの `origin` に含まれています。`_physics_process()` を `_integrate_forces()` に変更し、以下のコードを追加してください。

{{< highlight swift >}}
func _integrate_forces(state):
    set_applied_force(thrust.rotated(rotation))
    set_applied_torque(rotation_dir * spin_thrust)
    var xform = state.get_transform()
    if xform.origin.x > screensize.x:
        xform.origin.x = 0
    if xform.origin.x < 0:
        xform.origin.x = screensize.x
    if xform.origin.y > screensize.y:
        xform.origin.y = 0
    if xform.origin.y < 0:
        xform.origin.y = screensize.y
    state.set_transform(xform)
{{< /highlight >}}

物理エンジンはそのまま正常に動作し続け、すべてが期待通りの挙動を示します。

![alt](/godot_recipes/4.x/img/rigidbody_ship2.gif)

## 結論

適切に使用すれば、リジッドボディはGodotのツールキットにおいて強力な機能となります。しかし、多くのユーザーが誤って目的と異なる使い方をしたり、その動作原理を十分に理解していなかったために問題に直面することがよくあります。

