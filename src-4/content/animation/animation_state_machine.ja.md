---
title: "アニメーション状態の制御中"
weight: 4
draft: false
ghcommentid: 54
---

## 課題

よくあるケースです：アニメーションの数が増えすぎて、シーン間の切り替え管理が困難になってきていませんか？コードが大量の `if` 文で埋め尽くされ、少し変更を加えるたびに全体が壊れてしまいそうになっていませんか？

## 解決策

アニメーション状態機械を作成するには `アニメーションTree` (`<{ gd-icon アニメーションTree }>`)を使用してください。これにより、アニメーションを整理できるだけでなく、最も重要な点として、それらの間の遷移を制御することが可能になります。

### はじめに

本デモでは、Elthen氏作の素晴らしいスプライト「Adventurer」を使用しています。この素材を含め、他にも数多くの高品質なアート作品は[https://elthen.itch.io/](https://elthen.itch.io/)で入手できます。

![alt](/godot_recipes/3.x/img/adventurer_sprite_sheet_v1.1.png)

We'll also assume you've already set up the character's animations using {{< gd-icon アニメーションPlayer >}}`アニメーションPlayer`. Using the above spritesheet, we have the following animations: "idle", "run", "attack1", "attack2", "hurt", and "die".

### アニメーションツリー

シーンに `{{< gd-icon アニメーションTree >}}`アニメーションTree` ノードを追加します。［ツリールート］プロパティで「新規アニメーションノードステートマシン」を選択してください。

<img src="/godot_recipes/3.x/img/animation_tree_01.png" alt="アニメーションツリーのスクリーンショット">

アニメーションPlayer >}}`アニメーションPlayer`で作成されたアニメーションを制御するノードです。既存のアニメーションにアクセスさせるには、_Anim Player_ プロパティ内の「割り当て」ボタンをクリックし、使用するアニメーションノードを選択してください。

以下は、状態機械を `アニメーションTree` パネルに設定し始める方法です：

![alt](/godot_recipes/3.x/img/animation_tree_02.png)

警告に注意してください。インスペクターで 「_アクティブ」プロパティを「オン」に設定します。

右クリックして「アニメーションを追加」を選択します。「待機」を選択すると、そのアニメーションを表す小さなボックスが表示されます。「再生」ボタンを押すとアニメーションが実行されるはずです。他のアニメーションを追加する場合も同じ手順で行ってください。

これで接続を追加できるようになりました。「ノードを接続」ボタンをクリックし、ノード間でドラッグして接続してください。

![alt](/godot_recipes/3.x/img/animation_tree_03.png)

アニメーションを選択すると、ツリーは現在のノードから目的地まで接続経路に沿って移動します。ただし、上記の設定で「attack2」を再生すると、その途中に「attack1」が表示されることはありません。これは、デフォルトの接続「スイッチモード」が「即時」に設定されているためです。まず「Move/select」ボタンをクリックしてから、「attack1」から「attack2」への接続をクリックしてください。インスペクターで _Switch Mode_ を「AtEnd」に変更します。同様に、「attack2」から「idle」までについても同様の操作を行ってください。接続アイコンが <i class="fas fa-play"></i> から <i class="fas fa-step-forward"></i> に変わります。

「idle」が再生されている状態で「attack2」をクリックすると、二つの攻撃が順番に再生されるようになります。

アニメーションは「attack2」で停止します。接続時に、［自動進行］プロパティを「有効」に設定してください。これにより、ツリーは両方のアニメーションを再生した後に「待機」状態に戻ります。この操作を確認するため、接続アイコンが緑色に変わりますのでご注意ください。

![alt](/godot_recipes/3.x/img/animation_tree_05.gif)

### コード内での呼び出し状態

以下に、全てのアニメーションに関する完全なツリー構造を示します。

![alt](/godot_recipes/3.x/img/animation_tree_06.png)

「死」ノードを終了ポイントに設定しました。到達後はアニメーションが停止します。左下には連続攻撃のシーケンスを配置しています。

それでは、これらのアニメーションをスクリプトで使用するキャラクターを設定していきましょう。

```gdscript
extends KinematicBody2D

var state_machine
var run_speed = 80
var attacks = ["attack1", "attack2"]
var velocity = Vector2.ZERO

func _ready():
    state_machine = $アニメーションTree.get("parameters/playback")
```

`state_machine` は状態マシンへの参照を保持しており、これは `アニメーションNodeStateMachinePlayback` 型です。特定のアニメーションを呼び出すには `travel()` メソッドを使用し、これにより指定されたアニメーションへの接続が辿られます。

```gdscript
func _physics_process(delta):
    get_input()
    velocity = move_and_slide(velocity)

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
    velocity = Vector2.ZERO
    if 入力.is_action_just_pressed("big_attack"):
        state_machine.travel("attack1 2")
        return
    if 入力.is_action_just_pressed("attack"):
        state_machine.travel(attacks[randi() % 2])
        return
    if 入力.is_action_pressed("move_right"):
        velocity.x += 1
        $Sprite.scale.x = 1
    if 入力.is_action_pressed("move_left"):
        velocity.x -= 1
        $Sprite.scale.x = -1
    if 入力.is_action_pressed("move_up"):
        velocity.y -= 1
    if 入力.is_action_pressed("move_down"):
        velocity.y += 1
    velocity = velocity.normalized() * run_speed
    if velocity.length() != 0:
        state_machine.travel("run")
    if velocity.length() == 0:
        state_machine.travel("idle")
```

注意：攻撃アニメーションに移動した後に`return`文を使用しています。これは、関数の後半で「走り」アニメーションや「待機」アニメーションに誤って移動しないようするためです。

![alt](/godot_recipes/3.x/img/animation_tree_07.gif)

## 関連レシピ

- [スプライトシートアニメーション](/godot_recipes/3.x/animation/spritesheet_animation/)
- [トップダウン型キャラクター操作](/godot_recipes/3.x/2d/topdown_movement/#option-1-8-way-movement)

#### この動画が気に入ったら？

{{< youtube 0bq2OIjHxk4 >}}