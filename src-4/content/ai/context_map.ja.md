---
title: "場面に基づく操縦"
weight: 10
draft: false
ghcommentid: 75
---

## 課題

経路を追従し、障害物を避け、世界を移動する方法について他の判断もできるAI制御オブジェクトがほしい。

## 解決策

「ステアリング挙動」とは、この問題を解決するために使用可能な様々なアルゴリズムの総称です。どの手法を採用するかは、ゲームの特性、オブジェクトが存在する世界の種類、そして求める「知性」のレベルによって異なります。

この例では、「状況に基づく振舞い(Context Behavior)」と呼ばれる手法を採用します。これは、オブジェクトが移動方法を選択するために十分なワールドの情報を得ることを目的とするものです。本テーマについてさらに詳しく知りたい方は、以下の関連リンクを参照してください。

* [Andrew Fray: Context Behaviours Know How to Share](https://andrewfray.wordpress.com/2013/03/26/context-behaviours-know-how-to-share/)

* [ジェームズ・キーツ：AIコンテキスト行動管理](https://jameskeats.com/portfolio/contextbhvr.html)

デモ用として、汎用的な「エージェント」オブジェクトを使用します。このゲームでは例えば、トラックを走る車、ダンジョンを巡回するモンスター、あるいはその他の種類のゲーム内エンティティなどが考えられます。エージェントは{{< gd-icon CharacterBody2D >}}`CharacterBody2D`コンポーネントを使用しますが、この手法はどのタイプのオブジェクトにも適用可能だということを覚えておいてください。アルゴリズムの核心は、対象が移動方向を選択する仕組みにあり、実際の移動方法は完全に別の問題となります。

### アルゴリズムについて

まず、エージェントがすべての方向に放射線状に広がる複数の光線を持っていると仮定しましょう（使用する本数については後で説明します。とりあえずここでは8本を使用しましょう）

![alt](/godot_recipes/3.x/img/ai_context_01.png)

エージェントのスクリプト内では、エージェントが移動したい方向を追跡するための配列「`interest`」を定義します。

![alt](/godot_recipes/3.x/img/ai_context_04.png)

もちろん、全て同じ方向なら動けません。あらゆる方向に均等に移動したいはずです！そこで、特定の方向への優先性があると仮定しましょう。主に前進したい場合を考えます：

![alt](/godot_recipes/3.x/img/ai_context_03.png)

この場合、`interest`配列は以下のようになります。

![alt](/godot_recipes/3.x/img/ai_context_05.png)

最も強い願望は前進することですが、左前方や右前方も許容範囲内です。しかし、障害物が現れた場合は？

![alt](/godot_recipes/3.x/img/ai_context_06.png)

次に、好ましくない方向を示す第2の配列「danger」を導入します。

![alt](/godot_recipes/3.x/img/ai_context_07.png)

これら2つの配列を組み合わせることで、`危険度`に含まれる`興味度`方向を除去することが可能です。残った`興味度`方向を合計すると、障害物から離れる新しい方向ベクトルが得られます。

![alt](/godot_recipes/3.x/img/ai_context_08.png)

要約すると：

1. オブジェクトの「関心」方向を特定する
1. 「危険」を含む方向をすべて特定する
1. 危険な「関心」方向がある場合はすべて除外する
1. 残った「関心」方向を合算して新たな進行方向を決定する

### 興味を見つける方法

これはエージェントの目標内容によって異なります。もしその目的が『プレイヤーを追跡すること』であれば、`興味度`値はプレイヤー方向へ高くなるべきです。複数のターゲットを設定することも可能で、より近い目標ほど高い`興味度`を持ちますが、障害物によって無効化された場合、スコアが低い他の目標が優先されます。

このデモでは、何らかのレースゲームを作っていると仮定しましょう。AI制御の車はサーキットを周回が必要です。その`interest`配列はコースに沿って前方を指すように設定すべきで、そうしないと逆走を開始してしまいます。

これを実現する方法はいくつかありますが、エージェントが実装の詳細を知る必要がないよう、トラックがどの方向に進むべきかを位置情報に基づいて指示するシステムを構築します。いつでも「どの方向が正しいか」と聞けば、トラックがその指示を伝えてくれます。

### コード例

以下にエージェントのコードを示します。まずはエクスポートした値から始めましょう。移動パラメータと、後で容易に調整できるようにしたいその他の値です。例えば `look_ahead` は、`danger` レイが障害物を検出する範囲を指定します。

※注：「光線数」は調整可能な設定となっています。これにより、お客様の用途に最適な数値を見つけることができます。以下では、光線数が多い場合のメリット・デメリットについて詳しく解説します。


```gdscript
extends CharacterBody2D

@export var max_speed = 350
@export var steer_force = 0.1
@export var look_ahead = 100
@export var num_rays = 8

# context array
var ray_directions = []
var interest = []
var danger = []

var chosen_dir = Vector2.ZERO
var velocity = Vector2.ZERO
var acceleration = Vector2.ZERO
```

次の `_ready()` 関数では、配列を適切にサイズ調整し、`ray_directions` 配列に実際のレイベクトルを格納します。これらは `num_rays` に基づいて円周上に均等に配置されます。最初は回転していない状態なので、`Vector2.RIGHT` が前方方向となります。

```gdscript
func _ready():
    interest.resize(num_rays)
    danger.resize(num_rays)
    ray_directions.resize(num_rays)
    for i in num_rays:
        var angle = i * 2 * PI / num_rays
        ray_directions[i] = Vector2.RIGHT.rotated(angle)
```

In `_physics_process()` we'll populate the context arrays and execute the movement. Note we've broken the steps of the algorithm in to separate functions. Once we've found our chosen direction, we turn towards it as much as possible (based on `steer_force`) and move.

```gdscript
func _physics_process(delta):
    set_interest()
    set_danger()
    choose_direction()
    var desired_velocity = chosen_dir.rotated(rotation) * max_speed
    velocity = velocity.linear_interpolate(desired_velocity, steer_force)
    rotation = velocity.angle()
    move_and_collide(velocity * delta)
```

それでは、アルゴリズムを構成する3つの主要な機能について説明します。まず、`interest`配列の設定についてです。前述の通り、世界（この場合は`owner`）に対して、どちらの方向に移動すべきかを指示するよう求めます。

各光線の方向に対して、与えられた経路方向との *内積* を計算します。二つの平行なベクトルの内積は 1、直交するベクトルの場合は 0 となることを思い出してください。負の値は無視します - 値が 0 の場合は、その方向へ進む必要がないことを意味します。

例えば、使用する光線が32本の場合、`interest`は以下のようになります。

![alt](/godot_recipes/3.x/img/ai_context_09.png)

安全対策として、案内してくれる所有者がいない場合は、自動的に前進を試みる設定になっています。

```gdscript
func set_interest():
    # Set interest in each slot based on world direction
    if owner and owner.has_method("get_path_direction"):
        var path_direction = owner.get_path_direction(position)
        for i in num_rays:
            var d = ray_directions[i].rotated(rotation).dot(path_direction)
            interest[i] = max(0, d)
    # If no world path, use default interest
    else:
        set_default_interest()

func set_default_interest():
    # Default to moving forward
    for i in num_rays:
        var d = ray_directions[i].rotated(rotation).dot(transform.x)
        interest[i] = max(0, d)
```

次に、`danger`配列を埋めます。`物理2DDirectSpaceState`を使用して、各方向にレイをキャストします。衝突があった場合、その位置に`1`を追加します。

```gdscript
func set_danger():
    # Cast rays to find danger directions
    var space_state = get_world_2d().direct_space_state
    for i in num_rays:
        var result = space_state.intersect_ray(position,
                position + ray_directions[i].rotated(rotation) * look_ahead,
                [self])
        danger[i] = 1.0 if result else 0.0
```

最後に、コンテキスト配列を使用して方向を選択できます。`danger` 配列をループ処理し、危険が存在する場所のすべての `interest` 値をゼロに設定します。その後、残りの興味ベクトルをすべて加算して正規化します。

```gdscript
func choose_direction():
    # Eliminate interest in slots with danger
    for i in num_rays:
        if danger[i] > 0.0:
            interest[i] = 0.0
    # Choose direction based on remaining interest
    chosen_dir = Vector2.ZERO
    for i in num_rays:
        chosen_dir += ray_directions[i] * interest[i]
    chosen_dir = chosen_dir.normalized()
```

### 実際の使用例

実際に試してみましょう！ここでは、`{{< gd-icon Path2D >}}` `Path2D`と衝突判定用のポリゴンを使ってトラックを作成してみました。

![alt](/godot_recipes/3.x/img/ai_context_11.png)

このシーンのスクリプトには、`get_path_direction()` 関数が含まれています。位置を指定すると、この関数はパス上で最も近い点を検出し、その位置に `PathFollow2D` を配置することで進行方向を取得します。

```gdscript
func get_path_direction(pos):
    var offset = path.curve.get_closest_offset(pos)
    path_follow.offset = offset
    return path_follow.transform.x
```

エージェントの移動速度をランダム化してバリエーションを加えました。速いエージェントが低速のエージェントをうまく避けながら進む様子に注目してください。

![alt](/godot_recipes/3.x/img/ai_context_10.gif)

### まとめ

この方法は非常に柔軟性が高く拡張性に優れており、以下のように複雑かつ多様な動作を生成できます。

以下に、適応策／改善点に関する追加提案をいくつか挙げます。

* 危険度レベル

危険度配列を初期化する際には、単に 0 や 1 を使うのではなく、オブジェクトまでの距離に基づいて「危険スコア」を計算してください。そして、その値を直接削除するのではなく、`interest` から減算します。遠方にあるオブジェクトは影響が小さく、近くにあるものほど影響力が強くなります。

* 回避策：

危険な要素が関心を打ち消すのではなく、逆方向への関心を*高める*ことも考えられます。

## 関連レシピ

- [ベクトル：内積と外積の活用](/godot_recipes/3.x/math/dot_cross_product/)

#### この動画が気に入ったら？

{{< youtube dzqtF_CmX-I >}}
