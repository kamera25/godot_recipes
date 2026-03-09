---
title: "Using the AnimationTree StateMachine"
weight: 5
draft: false
---

## 問題文

よくあるケースです：アニメーションの数が増えすぎて、シーン間の切り替え管理が困難になってきていませんか？コードが大量の `if` 文で埋め尽くされ、少し変更を加えるたびに全体が壊れてしまいそうになっていませんか？

## 解決策

アニメーション状態機械を作成するには `AnimationTree` (`<{ gd-icon AnimationTree }>`)を使用してください。これにより、アニメーションを整理できるだけでなく、最も重要な点として、それらの間の遷移を制御することが可能になります。

### はじめに

For this demo, we'll be using the excellent "Adventurer" sprite by Elthen. You can get this and lots of other great art at [https://elthen.itch.io/](https://elthen.itch.io/).

![alt](/godot_recipes/4.x/img/adventurer_sprite_sheet_v1.1.png)

We'll also assume you've already set up the character's animations using {{< gd-icon AnimationPlayer >}}`AnimationPlayer`. Using the above spritesheet, we have the following animations: "idle", "run", "attack1", "attack2", "hurt", and "die".

### アニメーションツリー

Add an {{< gd-icon AnimationTree >}}`AnimationTree` node to the scene. In its _Tree Root_ property, choose "New AnimationNodeStateMachine".

<img src=\ alt=\>

An {{< gd-icon AnimationTree >}}`AnimationTree` is a node that controls animations created in {{< gd-icon AnimationPlayer >}}`AnimationPlayer`. To let it access the existing animations, click "Assign" in the _Anim Player_ property and select your animation node.

以下は、状態機械を `AnimationTree` パネルに設定し始める方法です：

![alt](/godot_recipes/4.x/img/anim_tree_panel.png)

Note the warning. Set the _Active_ property to "On" in the Inspector.

Right-click and choose "Add Animation". Choose "idle", and you'll see a small box representing that animation. Press its "Play" button and you should see the animation play. Do the same to add boxes for the other animations.

Now we can add connections. Click the "Connect nodes" button and drag between nodes to connect them. As an example, let's use the two attack animations:

![alt](/godot_recipes/4.x/img/animation_tree_03.png)

When you select an animation, the tree will follow the connected path from the current node to the destination. However, in the configuration above, if you play "attack2" you won't see "attack1" along the way. That's because the default "switch mode" for a connection is "Immediate". Click the "Move/select" button and then click on the connection between "attack1" and "attack2". In the Inspector, change **Switch Mode** to "At End". Do the same with "attack2" to "idle". The connection icon changes from <i class="fas fa-play"></i> to <i class="fas fa-step-forward"></i>.

Now, with "idle" playing, if you click "attack2", you'll see the two attacks play in sequence.

But now the animation stops on "attack2". On its connection, set the **Advance/Mode** property to "Auto". This will make the tree go back to "idle" after playing both animations. Note that the connection icon turns green to show this.

![alt](/godot_recipes/4.x/img/animation_tree_05.gif)

アニメーションはトリガーされるたびに連続して再生されます。

### コード内での呼び出し状態

以下に、全てのアニメーションに関する完全なツリー構造を示します：

!

それでは、これらのアニメーションをスクリプトで使用するキャラクターを設定していきましょう。

```gdscript
extends CharacterBody2D

var state_machine
var run_speed = 80.0
var attacks = ["attack1", "attack2"]

@onready var state_machine = $AnimationTree["parameters/playback"]
```

`state_machine` は状態マシンへの参照を保持しており、これは `AnimationNodeStateMachinePlayback` 型です。特定のアニメーションを呼び出すには `travel()` メソッドを使用し、これにより指定されたアニメーションへの接続が辿られます。

```gdscript
func hurt():
    state_machine.travel("hurt")

func die():
    state_machine.travel("die")
    set_physics_process(false)
```

Here we have examples of functions we would call if the player is hurt or killed. For the other animations (running, attacking, etc.), we'll need to combine them with our input and movement code. `velocity` determines whether we should be showing "run" or "idle".

```gdscript
func get_input():
    var current = state_machine.get_current_node()
    velocity = Input.get_vector("move_left", "move_right", "move_up", "move_down") * run_speed
    if Input.is_action_just_pressed("attack"):
        state_machine.travel(attacks.pick_random())
        return
    # flip the character sprite left/right
    if velocity.x != 0:
        $Sprite2D.scale.x = sign(velocity.x)
    # choose animation
    if velocity.length() > 0:
        state_machine.travel("run")
    else:
        state_machine.travel("idle")
    move_and_slide()
```

Note that we're using `return` after traveling to the attack animations. This is so that we won't instead travel to the "run" or "idle" animations further down in the function.

<img src=\ alt=\
>

AnimationTreeStateMachineを使用して以下の処理を管理できます：

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/ai_behavior_demos](https://github.com/godotrecipes/ai_behavior_demos)

## 関連レシピ

```markdown
- [スプライトシートアニメーション](/godot_recipes/4.x/animation/spritesheet_animation/)
- [トップダウン型キャラクター操作](/godot_recipes/4.x/2d/topdown_movement/#option-1-8-way-movement)

