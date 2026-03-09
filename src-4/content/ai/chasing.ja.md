---
title: "Chasing the player"
weight: 1
draft: false
---

## 問題文

プレイヤーを追いかける敵が欲しいようですね。

## 解決策

敵をプレイヤー追跡モードに移行させる最初のステップは、敵が移動する必要のある方向を決定することです。ベクトル **A** から **B** への方向を求めるには、以下のように計算します：**B** - **A**。この結果を正規化すれば、方向ベクトルが得られます。

このアプローチは非常にシンプルです。毎フレーム、敵の速度ベクトルをプレイヤー方向へ向くように設定します。

```gdscript
velocity = (player.position - position).normalized() * speed
```

Godotの`Vector2`オブジェクトには、この処理を補助する組み込み機能があります：

```gdscript
velocity = position.direction_to(player.position) * speed
```

However, this would allow the enemy to chase the player from any distance, even if it's far away. To fix this, we can add an {{< gd-icon Area2D >}}`Area2D` to the enemy, and only chase the player when it's inside this "detect radius".

![alt](/godot_recipes/4.x/img/chase_01.png)

以下にサンプルコードを示します：

```gdscript
extends CharacterBody2D

var run_speed = 25
var player = null

func _physics_process(delta):
    velocity = Vector2.ZERO
    if player:
        velocity = position.direction_to(player.position) * run_speed
    move_and_slide()

func _on_DetectRadius_body_entered(body):
    player = body

func _on_DetectRadius_body_exited(body):
    player = null
```

我们将连接了 `area2d` 中的 `body_entered` 和 `body_exited` 信号，这样敌机就能知道它是否处于有效范围内。

上記の説明では、プレイヤーが出入りする唯一のオブジェクトであると仮定しています。これは通常、適切な衝突レイヤーとマスクを設定することで実現されます。

<video controls src="/godot_recipes/4.x/img/chase_02.webm"></video>

この概念は他の種類のゲームにも応用可能です。重要なのは、敵からプレイヤーへの方向ベクトルを求めることです：

たとえば、あなたのゲームがサイドスクロール形式であったり、移動に制限がある場合は、得られたベクトルの `x` 成分のみを使用して移動を判定できます。

### 制限事項

注意点：この方法では移動が非常に単純化され、壁などの障害物を回避したり、プレイヤーに近づきすぎて停止することはありません。

敵がプレイヤーに接近した際の対処はゲームデザインによって異なります。以下の選択肢が考えられます：
・2つ目の小さいエリアを追加し、そこで敵を足止めして攻撃させるか
・接触時にプレイヤーを吹き飛ばすノックバック効果を実装するか

さらに顕著な問題は、動きの速い敵キャラクターで発生します。プレイヤーが移動すると、このテクニックを使用する敵は瞬時に進行方向を変えます。より自然な動きを実現するためには、ステアリング挙動を使用することをお勧めします。

より高度な動作については、本書の他のレシピを参照してください。

## 関連レシピ

- 【トップダウン移動】（/godot_recipes/4.x/2d/topdown_movement/#option-1-8-way-movement）
- 【ホーミングミサイル】（/godot_recipes/4.x/ai/homing_missile/）
