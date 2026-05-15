---
title: "プロジェクトの設定"
weight: 1
draft: false
pre: "01. "
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

どこから始めればよいでしょうか？ゲームの種類やアイデアの具体性によって、答えは大きく異なります。この場合、事前にプロトタイプを作成し、さらにアイデアを固めておいたため、若干有利でした。とはいえ、当初の構想からは多少逸脱してしまいましたし、この連載も同様になるかもしれません。結果は時が経ってみないと分かりません。

大きなプロジェクトの場合、まず**設計書**から始めるのが一般的です。これは、簡単なメモ1枚程度のものから、ゲーム世界・ストーリー・メカニクスの詳細を網羅した500ページに及ぶ大作まで様々です。ここではそこまで複雑なものは必要ありませんので、まずは大まかな企画内容をご説明します。

## ゲームプラン

このゲームでは、プレイヤーは「キャラクター」を操作し、円形のフィールドから別の円形へジャンプしていきます。ジャンプはクリックまたはタップで開始され、次のサークルに着地できなければゲームオーバーとなります。スコアは生存時間に応じて加算され、難易度は徐々に上昇していきます - 移動するサークルや、サイズが小さくなるサークル、さらには消滅するサークルが登場するためです。コンセプトは、スピード感あふれる短時間で遊べる、「もっと上を目指せ」という感覚を刺激するゲームプレイです。可能な限り、アートスタイルはシンプルでクリーンなデザインを維持し、視覚効果やオーディオエフェクトを駆使して魅力を高めていきます。

{{% notice note %}}
まずはGLES3を使用して開始します。これがどのような影響を及ぼすかはまだ明確ではありません。モバイルテストフェーズに移行した時点で、GLES2への移行が必要かどうかを検討します。
{{% /notice %}}

また、このプロジェクトを[<i class="fab fa-github"></i> GitHubでフォローする](https://github.com/kidscancode/circle_jump)こともできます。

## はじめに

まず、プロジェクト設定から始めてください。画面サイズと動作仕様を定義が必要です。モバイルゲームとして開発するので、縦向き表示が必須となり、さまざまな端末の画面解像度に対応できるようが必要です。スマートフォンには数多くの画面解像度が存在するためです。

プロジェクト設定を開き、［表示／ウィンドウ］セクションに移動します。画面サイズを `(480, 854)` に、［携帯端末／向き］を「縦」に、［伸縮／モード］を「2D」に、そして［伸縮／アスペクト比］を「維持」にそれぞれ設定します。

次に、［入力デバイス／ポインティング］セクションで「マウスからタッチ操作をエミュレート」を有効にします。これにより、画面のタッチイベントのみを使用してコードを入力できる上に、PCプラットフォームではマウスを使ったプレイが実現できます。

### プロジェクト管理体制

整理整頓のため、ゲームオブジェクト用のフォルダ（`objects`）とUI専用フォルダ（`gui`）を作成します。画像や音声などのゲームアセットは`assets`フォルダに格納します。開始時点で使用するアセットはこちらからダウンロードできます。

{{% notice note %}}
プロジェクトファイルをこちらからダウンロードしましょう: [circle_jump_assets.zip](/godot_recipes/4.x/ja/files/circle_jump_assets.zip)
{{% /notice %}}

フォルダ構造とアセットの準備が整ったら、いよいよコーディング開始です！

## ゲームオブジェクト

作成するゲームオブジェクトは2つあります。プレイヤー（「ジャンパー」）と円形オブジェクトです。

### ジャンパー（Jumper）

移動と衝突判定には、`Area2D`を使用することにします。公平を期すために言えば、ここでは`CharacterBody2D`を使用しても問題ありませんし、同様に機能します。ただし、このゲームでは厳密な衝突検出は必要なく、ジャンパーが円に接触したかどうかだけを把握できれば十分です。以下のノードを追加しましょう：

* `Area2D` ("Jumper")
  * `Sprite`
  * `CollisionPolygon2D`
  * `VisibilityNotifier2D`

シーンを `res://objects/` に保存し、円の画像ファイル（`res://assets/images/jumper.png`）をスプライトの _Texture_ にドラッグします。すべてのゲーム画像は初期設定では白色になっていますので、後で動的に色付けする際に作業がしやすくなります。

アートワークが上向きに描かれているため、`Sprite2D`の［回転］プロパティを`90`に設定します。

`CollisionPolygon2D` を選択し、ジャンパーの三角形形状をカバーするように3点を追加します。

![alt](/godot_recipes/4.x/img/cj_01_01.png?width=200)

では、ボディ部分にスクリプトを追加し、その動作をコーディングしていきます。

まず、シグナルと変数について：

```gdscript
extends Area2D

var velocity = Vector2(100, 0)  # start value for testing
var jump_speed = 1000
var target = null  # if we're on a circle
```

次に、画面タッチを検知し、円形オブジェクト上にいる場合はジャンプ処理を実行します。

```gdscript
func _unhandled_input(event):
    if target and event is InputEventScreenTouch and event.pressed:
        jump()
```

ジャンプすると、円軌道を離れて一定速度で前進します。

```gdscript
func jump():
    target = null
    velocity = transform.x * jump_speed
```

円領域への進入を検知する`area_entered`シグナルを利用するので、これを接続します。円に接触すると、前進動作を停止します。

```gdscript
func _on_Jumper_area_entered(area):
    target = area
    velocity = Vector2()
```

円形フィールドに捕捉された場合、その周囲を回転したいと考えます。そこで円上にピボットポイントを追加し、その変形を適用することで、常に外側へ向き続けるようにします。それ以外の場合は、直線的に前進します。

```gdscript
func _physics_process(delta):
    if target:
        transform = target.orbit_position.global_transform
    else:
        position += velocity * delta
```

### カラーシェーダー

{{% notice tip %}}
シェーダーを使い始める方法については、「[シェーダー]（/godot_recipes/4.x/ja/shaders）」セクションを参照します。
{{% /notice %}}

以下の手順で進めてください。

1. `Sprite` にカスタムカラーを適用するため、小さなシェーダーを使用します
2. まず`Sprite`を選択してから、_Material_ プロパティで新しい`ShaderMaterial`を追加します
3. 追加した _Shader_ をクリックし、[シェーダー]メニューで「新規シェーダー」を選択、さらにそれをクリックしましょう
4. シェーダーエディタパネルが画面下部に表示されます

![alt](/godot_recipes/4.x/img/cj_01_02.gif)

以下はカラーシェーダーのコードです。ここでは色を指定するために `uniform` 変数を使用しており、インスペクターから直接設定するか、ゲームスクリプトから値を割り当てることができます。その後、テクスチャ上のすべての表示ピクセルがその色に置き換えられ、アルファ（透明度）値は保持されます。

```c
shader_type canvas_item;

uniform vec4 color : hint_color;

void fragment() {
    COLOR.rgb = color.rgb;
    COLOR.a = texture(TEXTURE, UV).a;
}
```

インスペクターに新たに「シェーダーパラメーター」セクションが表示され、カラー値を設定できるようになります。

![alt](/godot_recipes/4.x/img/cj_01_03.gif)

このシェーダーは他のシーンでも使用するため、［シェーダー］プロパティで「保存」を選択し、`res://objects/color.shader` として保存します。

### サークル（Circle）

2 つ目のゲームオブジェクトは円です。ゲームが進むにつれて何度もインスタンス化されます。最終的には移動や縮小など様々な動作を追加しますが、今回は最初の実装として、単にプレイヤーを捕捉する機能だけを実装します。

以下は開始ノードの設定です。

* `Area2D` ("Circle")
  * `Sprite`
  * `CollisionShape2D`
  * `Node2D` ("Pivot")
      * `Marker2D` ("OrbitPosition")

「ピボット」ノードを使って、プレイヤーが円軌道を描くようにします。「軌道位置」は円のサイズに応じてオフセットされ、プレイヤーはこの位置に追従します。

`res://assets/images/circle1_n.png` を `Sprite` のテクスチャとして使いましょう。そのついでに、先ほど作成した `color.shader` を使用するために、`ShaderMaterial` を追加し、「読み込み」を選択します。

`CollisionShape2D` に円形状を追加し、ルートノードにスクリプトをアタッチします。

```gdscript
extends Area2D

@onready var orbit_position = $Pivot/OrbitPosition
var radius = 100
var rotation_speed = PI

func _ready():
    init()

func init(_radius=radius):
    radius = _radius
    $CollisionShape2D.shape = $CollisionShape2D.shape.duplicate()
    $CollisionShape2D.shape.radius = radius
    var img_size = $Sprite.texture.get_size().x / 2
    $Sprite.scale = Vector2(1, 1) * radius / img_size
    orbit_position.position.x = radius + 25

func _process(delta):
    $Pivot.rotation += rotation_speed * delta
```

`init()`関数では、与えられた `radius` に基づいて円のサイズを設定します。衝突形状のサイズも、テクスチャのサイズに合わせて調整しましょう。

テスト用に `radius` の値を変えてシーンを実行してみてください。（後で `_ready()` 内で `init()` を呼び出す処理は停止します）

## メインシーン

これで動作テストが可能になりました。

`Node2D` を使用して「メイン」シーンを作成し、その中にジャンパーコンポーネントとサークルをインスタンス化します。ジャンパーがサークルに衝突するように配置します（デフォルトのジャンプ速度は `(100, 0)` です）。

試走してみてください。ジャンパーが円の内側に捕捉され、軌道を描き始めるはずです。マウスをクリックすると、ジャンプ台はその方向に向かって発射されます。

----------

#### GitHubでプロジェクトをフォローしましょう！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### この動画が気に入ったら？

{{< youtube wU6otgwaNQg >}}