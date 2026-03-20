---
title: "アニメーションツリーを使う"
weight: 5
draft: false
---

## 課題

アニメーションの数が増えすぎて、シーン間の切り替え管理が困難になってきていませんか？コードが大量の `if` 文で埋め尽くされ、少し変更を加えるたびに全体が壊れてしまいそうになっていませんか？

## 解決策

アニメーション状態機械を作成するには {{< gd-icon AnimationTree >}}`AnimationTree` を使用してください。これにより、アニメーションを整理できるだけでなく、最も重要な点として、それらの間の遷移を制御することが可能になります。

### はじめに

本デモでは、Elthen氏作の素晴らしいスプライト「Adventurer」を使用しています。この素材を含め、他にも数多くの高品質なアート作品は[https://elthen.itch.io/](https://elthen.itch.io/)で入手できます。

![alt](/godot_recipes/4.x/img/adventurer_sprite_sheet_v1.1.png)

We'll also assume you've already set up the character's animations using {{< gd-icon AnimationPlayer >}}`AnimationPlayer`. Using the above spritesheet, we have the following animations: "idle", "run", "attack1", "attack2", "hurt", and "die".

### アニメーションツリー

シーンに `{{< gd-icon AnimationTree >}}`AnimationTree` ノードを追加します。［ツリールート］プロパティで「新規アニメーションノードステートマシン」を選択してください。

![alt](/godot_recipes/4.x/img/animation_tree_01.png)

{{< gd-icon AnimationTree >}}`AnimationTree`で作成されたアニメーションを制御するノードです。既存のアニメーションにアクセスさせるには、_Anim Player_ プロパティ内の「割り当て」ボタンをクリックし、使用するアニメーションノードを選択してください。

以下は、状態機械を `AnimationTree` パネルに設定し始める方法です：

![alt](/godot_recipes/4.x/img/anim_tree_panel.png)

警告に注意してください。インスペクターで 「_アクティブ」プロパティを「オン」に設定します。

右クリックして「アニメーションを追加」を選択します。「待機」を選択すると、そのアニメーションを表す小さなボックスが表示されます。「再生」ボタンを押すとアニメーションが実行されるはずです。他のアニメーションを追加する場合も同じ手順で行ってください。

接続を追加できるようになりました。「ノードを接続」ボタンをクリックして、ノード間でドラッグして接続してください。例として、この2つの攻撃アニメーションを使いましょう。

![alt](/godot_recipes/4.x/img/animation_tree_03.png)

アニメーションを選択すると、ツリーは現在のノードから目的地まで接続経路に沿って追従します。ただし、上記の設定では「attack2」を再生しても途中で「attack1」は表示されません。これは、接続におけるデフォルトの「スイッチモード」が「即時」に設定されているためです。まず「移動/選択」ボタンをクリックし、次に「attack1」と「attack2」間の接続ポイントをクリックします。インスペクターで「**スイッチモード**」を「終点時」に変更してください。同様の操作を「attack2」から「idle」に対しても行います。接続アイコンが <i class="fas fa-play"></i> から <i class="fas fa-step-forward"></i> へと変化します。

「idle」が再生されている状態で「attack2」をクリックすると、二つの攻撃が順番に再生されるようになります。

しかし、現在「attack2」アニメーションが停止しています。接続時には、**進行状況/モード**プロパティを「自動」に設定してください。これにより、両方のアニメーション再生後にツリーが「待機」状態に戻ります。なお、接続アイコンが緑色に変化することでこの状態が表示されます。

![alt](/godot_recipes/4.x/img/animation_tree_05.gif)

アニメーションはトリガーされるたびに連続して再生されます。

### コード内での呼び出し状態

以下に、全てのアニメーションに関する完全なツリー構造を示します。

![alt](/godot_recipes/4.x/img/anim_sm_final.png)

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

以下は、プレイヤーがダメージを受けたり死亡した場合に呼び出される関数の例です。
他のアニメーション（移動、攻撃など）については、入力処理や移動制御コードと組み合わせる必要があります。`velocity`変数によって、「走行」状態を表示するか「待機」状態を表示するかを決定します。

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

注意：攻撃アニメーションに移動した後に`return`文を使用しています。これは、関数の後半で「走り」アニメーションや「待機」アニメーションに誤って移動しないようするためです。

![alt](/godot_recipes/4.x/img/animation_tree_07.gif)

AnimationTreeStateMachine を使用して以下の処理を管理できます。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/ai_behavior_demos](https://github.com/godotrecipes/ai_behavior_demos)

## 関連レシピ

- [スプライトシートアニメーション](/godot_recipes/4.x/ja/animation/spritesheet_animation/)
- [見下ろし型キャラクター操作](/godot_recipes/4.x/ja/2d/topdown_movement/#option-1-8-way-movement)

