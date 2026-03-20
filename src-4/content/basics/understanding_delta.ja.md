---
title: "理解しよう！'delta'"
weight: 3
draft: false
ghcommentid: 12
---

## 課題

この`delta`パラメータ（delta time）は、ゲーム開発において誤解されがちな概念です。本チュートリアルでは、どのように使用されるのか、フレームレートに依存しない移動の重要性、そしてGodotにおける実践的な使用例について解説します。

## 解決策

問題を具体的に説明するため、画面上を移動する「スプライト」ノードを考えてみましょう。画面幅が600ピクセルで、スプライトがこのスクリーン全体を横切るのに5秒かかる場合、必要な移動速度は以下の計算で求められます。

```
600 pixels / 5 seconds = 120 pixels/second
```

この実装により、ゲームが60フレーム/秒で動作している場合でも、毎フレーム正確に移動量を計算して表示できます。fps_factorはFPSレートに応じて調整するための係数です。

```
120 pixels/second * 1/60 second/frame = 2 pixels/frame
```

{{% notice tip %}}
上記のすべての計算において、単位が統一されていることに注目してください。常に計算式で使用する単位に注意を払いましょう。これにより、ミスを防ぐことができます。
{{% /notice %}}

以下に必要なコードを示します。

```gdscript
extends Node2D

# Desired movement in pixels/frame
var movement = Vector2(2, 0)

func _process(delta):
    $Sprite.position += movement
```

このコードを実行すると、スプライトが画面を横切るのに5秒かかることがわかります。

![alt](/godot_recipes/4.x/img/delta_01.gif)

このコードだと、コンピュータが他のタスクでリソースを消費している場合に問題が発生します。これは「ラグ」と呼ばれます。コード自体の問題や他の実行中アプリケーションに起因する可能性があります。この状況では、フレームの長さが増加になります。極端な例として、フレームレートが半減した場合を考えてみましょう。各フレームの処理時間が60分の1秒から30分の1秒になります。`2` ピクセル/フレームで移動しているスプライトの場合、画面端に到達するまでにこれまでの2倍の時間がかかることになります。

![alt](/godot_recipes/4.x/img/delta_02.gif)

たとえ微小なフレームレートの変動があったとしても、動きの速さが一定に保たれなければなりません。これが銃弾など高速で移動する物体であれば、速度が落ちるのを避けたいです。この移動動作を _フレームレートに依存しない_ ようにする必要があります。

### フレームレート問題の修正について

`_process()`関数を使用する場合、自動的にエンジンから渡されるパラメータとして`delta`が含まれます（これは`_physics_process()`と同様で、物理関連コード用に使用されます）。これは時間間隔を表す浮動小数点数値であり、直前のフレームから経過した時間の長さを示します。通常この値は1/60秒、つまり約0.0167秒に相当します。

この情報があれば、各フレームの移動量を考える必要がなくなり、希望するピクセル単位速度（上記計算結果の「120」）のみを考慮すれば済むようになります。

エンジンの `delta` 値にこの数値を掛けることで、各フレームでピクセルを移動する量が決定されます。フレーム時間が変動した場合でも自動的に調整されるため、手動での設定は不要です。

```
# 60 frames/second
120 pixels/second * 1/60 second/frame = 2 pixels/frame

# 30 frames/second
120 pixels/second * 1/30 second/frame = 4 pixels/frame
```

注：フレームレートが半分に低下した場合（すなわちフレーム時間が2倍になった場合）、速度を維持するには、フレームごとの移動量も2倍にする必要があります。

この計算を使用するようにコードを変更しましょう。

```gdscript
extends Node2D

# Desired movement in pixels/second.
var movement = Vector2(120, 0)

func _process(delta):
    $Sprite.position += movement * delta
```

現在毎秒 30 フレームで動作させている場合、移動時間は以下のように一定に保たれています。

![alt](/godot_recipes/4.x/img/delta_03.gif)

フレームレートが著しく低下した場合、動きは滑らかさを失いますが、時間間隔自体は維持されます。

![alt](/godot_recipes/4.x/img/delta_04.gif)

### デルタを運動方程式と併用する方法

動きがより複雑になったらどうしましょう？基本的な考え方は同じです。単位は常に秒を使用し、フレームは使用しないようにし、各フレームごとに `delta` で乗算してください。

{{% notice tip %}}
ピクセル単位や秒単位で考えると、現実世界での測定方法に直結するため直感的にも理解しやすいですよね。「重力加速度は毎秒100ピクセル/秒なので、ボールが2秒後には毎秒200ピクセルの速さになっている」といった具合です。フレーム単位で扱う場合は「加速をピクセル/フレーム/フレームという単位で計算しなければ」と考えなければなりません。実際に試してみてください…あまり自然ではありませんよ。
{{% /notice %}}

たとえば、重力を適用している場合、これは加速度です。各フレームごとに速度に一定の値が加算されます。上記の例と同様に、これによりノードの位置が変化します。

以下のコードで`delta`と`target_fps`を調整してみると効果が確認できます。

```gdscript
extends Node2D

# Acceleration in pixels/sec/sec.
var gravity = Vector2(0, 120)
# Acceleration in pixels/frame/frame.
var gravity_frame = Vector2(0, .033)

# Velocity in pixels/sec or pixels/frame.
var velocity = Vector2.ZERO

var use_delta = false
var target_fps = 60

func _ready():
    Engine.target_fps = target_fps

func _process(delta):
    if use_delta:
        velocity += gravity * delta
        $Sprite.position += velocity * delta
    else:
        velocity += gravity_frame
        $Sprite.position += velocity
```

フレームごとに時間ステップで `velocity(速度)` と `position(位置)` を更新している点に注意してください
各フレームで更新される量については、フレームレートに依存せず適切に変化させるため、必ず `delta` を掛けてください。

#### 運動関数の活用について

上記の例では簡略化のため`Sprite`を使用していますが、実際には2D/3D空間における移動ボディを使用する場合、それぞれに適した移動メソッドを使用します。また`move_and_slide()`関数については、速度ベクトルを扱うため若干混乱が生じやすい点に注意が必要で、距離計算のために速度に`delta`を掛ける必要はありません。これは関数側で自動的に処理されます。ただし、加速度などの他の計算には依然として`delta`を掛けるひつようがあります。

```gdscript
# Sprite movement code:
velocity += gravity * delta
position += velocity * delta

# Kinematic body movement code:
velocity += gravity * delta
move_and_slide()
```

加速を適用する際に `delta` を考慮しない場合、フレームレートの変動の影響を受けやすくなります。この影響は運動挙動に「より微妙な形」で現れます。発生した場合は辻褄が合わない動作となりますが、その原因を特定する微々たる影響のためとても困難です。

{{% notice tip %}}
`move_and_slide()`関数を使用する場合でも、重力や摩擦などの他の物理量に対しても適切に`delta`を適用が必要です。
{{% /notice %}}

## 関連するレシピ

<!-- - [KinematicBody2Dの使用](/godot_recipes/3.x/physics/godot3_kinematic2d/) -->