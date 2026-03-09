---
title: "Changing Behaviors"
weight: 5
draft: true
---

## 問題定義
AI制御のエンティティに対して、異なる動作モードを切り替えられるようにしたい。

## 解決策

この例では、以下の行動パターンを持つ敵を想定してみましょう：

- **パトロール**

    「パトロール」状態では、事前に定義された経路に沿って移動します（経路が割り当てられていない場合は停止したままになります）。
    <!-- See [Path following](/godot_recipes/4.x/ai/path_follow/) for details. -->

- **追跡中**

    「追跡」状態では敵キャラクターがプレイヤーに向かって移動します。この動作を実装する方法については[プレイヤーを追跡する](/godot_recipes/4.x/ai/chasing/)を参照してください。

- **攻撃**

    この状態では、プレイヤーは近接攻撃の射程内にいるため、敵の動きが止まり、攻撃を発動します。
    <!-- See [Melee attacks](/godot_recipes/4.x/animation/melee_attacks/) for how to make melee attacks. -->

これらの行動はそれぞれ状態を表しており、敵は同時に複数の状態を保有することはできません。プレイヤーが近づくなどの特定のイベントが発生すると、別の状態に遷移します。

状態遷移を決定するために、敵キャラには2つの{{< gd-icon Area2D >}}`Area2D`ノードが配置されています。1つは「DetectRadius」と名付けた外側のエリア、もう1つは「AttackRadius」という内側のエリアです。プレイヤーがこれらの領域に入ったり出たりすることで、対応する動作がトリガーされます。

![alt](/godot_recipes/4.x/img/behaviors_01.png)

本例では「攻撃半径」の形状として矩形を選択していますが、これは敵の攻撃範囲が長方形であるためです。ただし、「検出半径」よりも小さい任意の形状で問題ありません。

両方のエリアの「body_entered」信号と「body_exited」信号を接続してください。衝突レイヤーを使用している場合（使用すべきですが）、プレイヤーのみ、あるいは追跡／攻撃対象として指定した他のボディのみを検出できるように設定してください。

それでは敵のスクリプトを確認してみましょう：


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