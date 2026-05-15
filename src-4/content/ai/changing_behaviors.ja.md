---
title: "動作の変更"
weight: 5
draft: true
---

## 問題定義
AI制御のエンティティに対して、異なる動作モードを切り替えられるようにしたい。

## 作り方

この例では、以下の行動パターンを持つ敵を想定してみます。

- **パトロール**

    「パトロール」状態では、事前に定義された経路に沿って移動します（経路が割り当てられていない場合は静止します）。
    <!-- 詳細は[経路追従](/godot_recipes/4.x/ai/path_follow/)を参照しましょう -->

- **追跡中**

    「追跡」状態では敵キャラクターがプレイヤーに向かって移動します。この動作を実装する方法については[プレイヤーを追跡する](/godot_recipes/4.x/ai/chasing/)を参照します。

- **攻撃**

    この状態では、プレイヤーが近接攻撃の範囲内にいるため、敵は移動を停止し、攻撃を実行します。
    <!-- 近接攻撃の作成方法については、[こちらを参照](/godot_recipes/4.x/animation/melee_attacks/) ください -->

これらの行動はそれぞれ状態を表しており、敵は同時に複数の状態を保有することはできません。プレイヤーが近づくなどの特定のイベントが発生すると、別の状態に遷移します。

状態遷移を決定するために、敵キャラには2つの{{< gd-icon Area2D >}}`Area2D`ノードが配置されています。1つは「DetectRadius」と名付けた外側のエリア、もう1つは「AttackRadius」という内側のエリアです。プレイヤーがこれらの領域に入ったり出たりすることで、対応する動作がトリガーされます。

![alt](/godot_recipes/4.x/img/behaviors_01.png)

本例では`AttackRadius(攻撃半径` の形状として矩形を選択していますが、これは敵の攻撃範囲が長方形であるためです。ただし、`DetectRadius(検出半径)`よりも小さい任意の形状で問題ありません。

両方のエリアの`body_entered`シグナルと`body_exited`シグナルを接続します。衝突レイヤーを使用している場合（使用すべきですが）、プレイヤーのみ、あるいは追跡／攻撃対象として指定した他のボディのみを検出できるように設定します。

それでは敵のスクリプトを見てみましょう。


```gdscript
extends CharacterBody2D

@export var patrol_path : Path2D

var run_speed = 25.0
var attacks = ["attack1", "attack2"]

enum states {PATROL, CHASE, ATTACK, DEAD}
var state = states.PATROL
var target = null
var player = null
var current_patrol_point = 0
var patrol_points = []
```

```gdscript
func _ready():
    if patrol_path:
        patrol_points = patrol_path.curve.get_baked_points()

func _physics_process(delta):
    $Label.text = str(states.keys()[state])
    velocity = Vector2.ZERO
    choose_action()
    if target:
        if target.x > position.x:
            $Sprite2D.scale.x = 1
        elif target.x < position.x:
            $Sprite2D.scale.x = -1
        if state != states.ATTACK:
            velocity = position.direction_to(target) * run_speed

    if velocity.length() > 0:
        anim_state.travel("run")
    move_and_slide()

func choose_action():
    var current_anim = anim_state.get_current_node()
    if current_anim in attacks:
        return
    match state:
        states.DEAD:
            set_physics_process(false)
        states.PATROL:
            if !patrol_path:
                anim_state.travel("idle")
                target = null
                return
            target = patrol_points[current_patrol_point]
            if position.distance_to(target) < 5:
                current_patrol_point = wrapi(current_patrol_point + 1, 0, patrol_points.size())
        states.CHASE:
            target = player.position
        states.ATTACK:
            target = player.position
            anim_state.travel(attacks.pick_random())

func _on_detect_radius_body_entered(body):
    player = body
    state = states.CHASE

func _on_attack_radius_body_entered(body):
    state = states.ATTACK

func _on_detect_radius_body_exited(body):
    player = null
    state = states.PATROL

func _on_attack_radius_body_exited(body):
    state = states.CHASE

```