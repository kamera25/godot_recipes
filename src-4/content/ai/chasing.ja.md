---
title: "プレイヤーを追いかける"
weight: 1
draft: false
---

## 課題

プレイヤーを追いかける敵が欲しい。

## 解決策

敵をプレイヤー追跡モードに移行させる最初のステップは、敵が移動する必要のある方向を決定することです。ベクトル **A** から **B** への方向を求めるには、以下のように計算します。**B** - **A**。この結果を正規化すれば、方向ベクトルが得られます。

このアプローチは非常にシンプルです。毎フレーム、敵の速度ベクトルをプレイヤー方向へ向くように設定します。

```gdscript
velocity = (player.position - position).normalized() * speed
```

Godotの`Vector2`オブジェクトには、この処理を補助する組み込み機能があります。

```gdscript
velocity = position.direction_to(player.position) * speed
```

しかし、これでは敵がプレイヤーから遠距離にいても追跡できてしまいます。これを修正するには、敵に {{< gd-icon Area2D >}}`Area2D` を追加し、この「検出範囲」内にプレイヤーが入った場合にのみ追跡するようにします。

![alt](/godot_recipes/4.x/img/chase_01.png)

以下にサンプルコードを示します。

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

{{< gd-icon Area2D >}}`Area2D`からの`body_entered`シグナルと`body_exited`シグナルを接続しました。これで、敵が範囲内にいるか判別できるようになりました。

上記の説明では、プレイヤーだけが出入りすることを想定しています。これは、適切な衝突レイヤーとマスクを設定することで実現できます。

<video controls src="/godot_recipes/4.x/img/chase_02.webm"></video>

この手法は他の種類のゲームにも応用できます。重要なのは、敵からプレイヤーへの方向ベクトルを求めることです。

たとえば、ゲームがサイドスクロール形式であったり、移動に制限がある場合は、得られたベクトルの `x` 成分のみを使用して移動を判定できます。

### 制約事項

この方法による移動は非常に単純化されています。壁などの障害物を回避したり、プレイヤーに近づきすぎて停止したりすることはありません。

敵がプレイヤーに接近した際の対処はゲームデザインによって異なります。以下の選択肢が考えられます。
* 2つ目の小さいエリアを追加し、そこで敵を足止めして攻撃させるか
* 接触時にプレイヤーを吹き飛ばすノックバック効果を実装するか

さらに顕著な問題は、動きの速い敵キャラクターで発生します。プレイヤーが移動すると、このテクニックを使用する敵は瞬時に進行方向を変えます。より自然な動きを実現するためには、ステアリング挙動を使用することをオススメします。

より高度な動作については、本書の他のレシピを参照します。

## 関連レシピ

- [見下ろし型のキャラクター移動](/godot_recipes/4.x/ja/2d/topdown_movement/#option-1-8-way-movement)
- [追跡ミサイル](/godot_recipes/4.x/ja/ai/homing_missile/)
