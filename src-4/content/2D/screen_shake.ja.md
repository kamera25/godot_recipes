---
title: "スクリーンシェイク"
weight: 6
draft: true
ghcommentid: 28
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

「画面シェイク」エフェクトを作成したい。

## 解決策

「画面揺れ」効果は、ゲームに躍動感を加えるための効果的な手法です。適切に使えば非常に効果的ですが、使いすぎるとプレイヤーから反感を買うことになります。このゲームへの実装を検討する際には、この点をよく考慮し、慎重に使用するようにしてください。

このエフェクトの仕組みはシンプルです。爆発や重い物体が障害物に衝突するなど、何らかのイベントが発生したときに、カメラを短時間だけ徐々に、かつ段階的に移動させたい場合に適しています。

このエフェクトを実装する方法は複数あります。今回のレシピでは、以下のGDC講演で解説されているテクニックを模倣していきます。

{{< youtube tu-Qe66AvtY >}}

要約すると、このカメラには `trauma(トラウマ)` プロパティが追加され、カメラの揺れ具合を測定します。何かが起きてカメラを揺らすべき状況が発生するたびに、その衝撃量に応じて trauma に加算します。大規模なイベントなら大量に、小規模なものなら少量ずつ増加させます。時間が経つにつれて、この traumaは自然に減少していきます。

### 外傷

まず、カメラの実装から始めてください。{{< gd-icon Camera2D >}}`Camera2D` ノードを使用して新規シーンを作成し、名前を`ShakeCamera2D`に設定します。その後、スクリプトをアタッチしてください。

まず、シェイク動作を制御するパラメーターを定義します。

```gdscript
extends Camera2D

@export var decay = 0.8  # How quickly the shaking stops [0, 1].
@export var max_offset = Vector2(100, 75)  # Maximum hor/ver shake in pixels.
@export var max_roll = 0.1  # Maximum rotation in radians (use sparingly).
@export var target: NodePath # Assign the node this camera will follow.

var trauma = 0.0  # Current shake strength.
var trauma_power = 2  # Trauma exponent. Use [2, 3].
```

`trauma_power` は `trauma` とカメラの実際の移動量との関係を表します（例: `amount = trauma * trauma`）。通常は正方形関係(2)またはキューブ関係(3)が最も効果的ですが、自由に実験してみてください。

さらに、カメラインスタンスを任意の場所に配置し、追従させるターゲットノードを指定できる `target` 変数を追加しました。

```gdscript
func _ready():
    randomize()

func add_trauma(amount):
    trauma = min(trauma + amount, 1.0)
```

`add_trauma()` 関数は、揺れを開始または強化するために使用する機能です。引数には `0` から `1` の間の値を指定してください。

```gdscript
func _process(delta):
    if target:
        global_position = get_node(target).global_position
    if trauma:
        trauma = max(trauma - decay * delta, 0)
        shake()
```

`process()` 関数内では、カメラをターゲット位置に移動させます。もし外傷が発生している場合は、`decay` 関数を使ってその影響を軽減した後、`shake()` を呼び出してカメラの動きを調整します。

### ランダム変位

The `shake()` function applies random camera movements based on the current `trauma` level (raised to the specified power). In 2D, we need to calculate two translational motions and one rotational motion. Using a random number between `-1` and `1` is a simple and effective way to generate movement in either direction.

```gdscript
func shake():
    var amount = pow(trauma, trauma_power)
    rotation = max_roll * amount * rand_range(-1, 1)
    offset.x = max_offset.x * amount * rand_range(-1, 1)
    offset.y = max_offset.y * amount * rand_range(-1, 1)
```

![alt](/godot_recipes/4.x/img/shake_rand01.gif)

これは良さそうですが、もっと見栄え良くできます。

### ノイズの使用について

この `rand_range()` を使った移動の欠点は、フレームごとにランダム値が大きく変化するため、操作感が不安定になりやすい点です。より「自然な」ランダム性を得るためには、「ノイズ」と呼ばれる概念を活用する方法があります。

ノイズ、またはより正確には「*勾配ノイズ*」と呼ばれる手法は、より自然な見た目の「ランダム」パターンを生成するための技術です。この目的のために、Godotでは[FastNoiseLite](https://docs.godotengine.org/en/latest/classes/class_opensimplexnoise.html)クラスが提供されています。

{{% notice info %}}
最も広く知られているグラジエントノイズアルゴリズムは、[パーリンノイズ](https://ja.wikipedia.org/wiki/Perlinノイズ)と呼ばれています。このアルゴリズムとその後継である[シンプレックスノイズ](https://ja.wikipedia.org/wiki/Simplex_noise)は特許で保護されているため、Godotでは[OpenSimplex](https://en.wikipedia.org/wiki/OpenSimplex_noise)という別のアルゴリズムを使用してノイズを生成しています。
{{% /notice %}}

`FastNoiseLite` は、3D空間上に点の「雲」を生成することで動作します。各点には`-1`から`1`までの値が割り当てられます。以下に、`FastNoiseLite` によって生成されたノイズの具体例を2つ示します。画像では、各ピクセルの色がその位置におけるノイズ値に対応しています。

![alt](/godot_recipes/4.x/img/2d_noise_example.png)

ご覧のとおり、「ノイジー」な性質ではありますが、特定のピクセルを選択すると、その周辺ピクセルは予測不能に変動するものの、急激に極端な値から別の極端値へと飛び移るようなことはありません。動作特性は用途に応じて調整可能ですが、ここではFastNoiseLiteの詳細な設定方法については割愛します。より詳しい情報については、以下の[関連レシピ](#関連レシピ)セクションをご覧ください。

以下のコードをスクリプトの最上部に追加してください。

```gdscript
@onready var noise = FastNoiseLite.new()
var noise_y = 0

func _ready():
	randomize()
	noise.seed = randi()
	noise.period = 4
	noise.octaves = 2
```

次に、`shake()`関数内で：

```gdscript
noise_y += 1
rotation = max_roll * amount * noise.get_noise_2d(noise.seed, noise_y)
offset.x = max_offset.x * amount * noise.get_noise_2d(noise.seed*2, noise_y)
offset.y = max_offset.y * amount * noise.get_noise_2d(noise.seed*3, noise_y)
```

`get_noise_2d()` は指定された座標 `(x, y)` におけるノイズ値を返します。3つのオフセットすべてに同じノイズ値を使用するのは避けるため、ここでは恣意的に異なる（かつ離れた）3つの `x` 値を選び、それぞれの点で連続的に増加する `noise_y` 値を使ってグラデーションに沿って「移動」させる手法を採用しています。

![alt](/godot_recipes/4.x/img/shake_noise01.gif)

{{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。[screen_shake.zip](/godot_recipes/4.x/ja/files/screen_shake.zip)
{{% /notice %}}

## 関連レシピ

- [ノイズジェネレーター](/godot_recipes/4.x/ja/math/noise/)
- [プラットフォームキャラクター実装](/godot_recipes/4.x/ja/ai/platform_character)

#### この動画が気に入ったら？

<!-- {{< youtube C-Sn55e5wnk >}} -->