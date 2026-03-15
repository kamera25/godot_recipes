---
title: "敵兵"
weight: 7
draft: false
pre: "07. "
---

プレイヤーが射撃できるようになったので、今度は撃つ対象を与えましょう。

## シーンの設定

敵キャラには `Area2D` を使用します。これは、プレイヤーの弾丸との重複判定や、直接衝突検出を行う必要があるためです。

以下に必要となるノードを列挙します。

```
Enemy: {{< gd-icon Area2D >}} Area2D
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
    {{< gd-icon AnimationPlayer >}} AnimationPlayer
    MoveTimer: {{< gd-icon Timer >}} Timer
    ShootTimer: {{< gd-icon Timer >}} Timer
```

※「インスペクター」横の **ノード** タブをクリックします。**グループ** セクションに「enemies」と入力し、**追加** をクリックしてください。弾丸コードで指定したように、これは「enemies」グループ内のオブジェクトを探します。

スプライトの**テクスチャ**に`Bon_Bon (16 x 16).png`を追加し、**アニメーション/フレーム数**を`4`に設定してください。

以前と同じように矩形の衝突形状を追加し、サイズを調整してください。タイマーノードの両方で**ワンショット**を有効にします。

{{< gd-icon アニメーションPlayer >}}`アニメーションPlayer` において、「バウンス」というアニメーションを追加し、ループ再生と自動再生を設定します。アニメーションパネルの下部にある**スナップ値**を `0.05` に設定してください。

スプライトノードを選択し、**テクスチャ** と **フレーム数** の横にあるキーアイコンをクリックしてトラックを作成します。これは、後でこれらのプロパティに異なる値を使用する「爆発」アニメーションを追加するためです。

次に、必要な各**フレーム**値を設定していきます。まずは`10ミリ秒`ごとに以下の順番でフレームを設定します。`2`, `1`, `0`, `3`。最後にもう一度`0`を設定してすぐ後ろに配置します。これにより、スプライトが徐々に大きくなり、最後に少し弾むような「脈動」アニメーションが完成します。このセットアップは以下のようになるはずです：

![alt](/godot_recipes/4.x/img/2d_101_20.png)

再生ボタンを押して実際に動作を確認してみてください。必要に応じて調整していただいても結構です。

次に、「explode」というアニメーションを追加します。長さを 0.4 秒に設定してください。

スプライトの**テクスチャ**を `Explosion (16 x 16).png` に変更し、そのプロパティにキーフレームを適用します。この画像は敵キャラ画像と異なるフレーム数を持っているため、**Hフレーム**も `6` に変更し、同様にキーフレームを設定する必要があります。

現在のキーフレームを時間 0 時点で「0」に、時間 0.4 時点で「5」に設定してください。アニメーションを実行して動作を確認しましょう。

## 敵キャラ用スクリプト

敵ユニットは画面上部のグリッド状に配置されて出現します。一定時間後にプレイヤー方向へ降下を開始し、破壊されない場合は画面上部に復帰します。また、定期的にプレイヤーに対して攻撃を仕掛けてきます。

スクリプトを追加し、変数から始めましょう。

```gdscript
extends Area2D

var start_pos = Vector2.ZERO
var speed = 0

@onready var screensize  = get_viewport_rect().size
```

The `start_pos` variable is going to keep track of the enemy's starting position so that after it moves, it can return to its original location. We'll set it when the enemy is spawned and we call its `start()` function.

```gdscript
func start(pos):
    speed = 0
    position = Vector2(pos.x, -pos.y)
    start_pos = pos
    await get_tree().create_timer(randf_range(0.25, 0.55)).timeout
    var tween = create_tween().set_trans(Tween.TRANS_BACK)
    tween.tween_property(self, "position:y", start_pos.y, 1.4)
    await tween.finished
    $MoveTimer.wait_time = randf_range(5, 20)
    $MoveTimer.start()
    $ShootTimer.wait_time = randf_range(4, 20)
    $ShootTimer.start()
```

敵キャラを出現させる際、この関数を呼び出して画面内の位置ベクトルを渡します。ここで重要なのは、実際には画面上部に配置される点です（`y`座標が負値）。これは、Tweenアニメーションを使用して画面に出現する様子を表現するためです。また、2つのタイマー値はランダム化しており、すべての敵が同時に移動・攻撃を開始しないように制御しています。

両方のタイマーの `timeout` シグナルを接続してください。

```gdscript
func _on_timer_timeout():
    speed = randf_range(75, 100)

func _on_shoot_timer_timeout():
    $ShootTimer.wait_time = randf_range(4, 20)
    $ShootTimer.start()
```

タイマーが切れた時点で移動を開始でき、同時に射撃も行いますが、まだ弾丸を作成していないため、その部分は後で実装します。現在「速度」変数を変更しているので、これを使って移動できるようになります。

```gdscript
func _process(delta):
    position.y += speed * delta
    if position.y > screensize.y + 32:
        start(start_pos)
```

今、「速度」が 0 でない場合、敵が画面を下方向に移動するのが見えるでしょう。画面下から消えてしまうと、最初からやり直しになります。

すでに弾丸シーンのコードで敵に当たったときに `explode()` を呼び出す処理は書いてあるので、これも追加しましょう。

```gdscript
func explode():
    speed = 0
    $AnimationPlayer.play("explode")
    set_deferred("monitoring", false)
    died.emit(5)
    await $AnimationPlayer.animation_finished
    queue_free()
```

この関数では、移動を停止し、爆発アニメーションを再生した後、処理が終了した時点で敵オブジェクトを削除します。`set_deferred()` 呼び出しにより、敵オブジェクトの `モニタリング` 機能を確実に無効化しています。これは、爆発中の敵に別の弾丸が当たらないようにするためです。

スクリプトの冒頭に `died` シグナルを追加してください。

```gdscript
signal died
```

このシグナルを使って、メインシーンにプレイヤーが得点を獲得したことを通知します。

## 敵キャラクターの出現

それでは、「メイン」シーンに移動して、これらの敵キャラクターをゲームに追加しましょう。「メイン」シーンにスクリプトを追加し、まず敵キャラ用シーンを読み込むことから始めます。

```gdscript
extends Node2D

var enemy = preload("res://enemy.tscn")
var score = 0
```

通常、敵はゲーム開始ボタンを押してプレイを開始するまで出現しませんが、まだその段階に達していないので、ここではすぐに敵を出現させます。

```gdscript
func _ready():
    spawn_enemies()

func spawn_enemies():
    for x in range(9):
        for y in range(3):
            var e = enemy.instantiate()
            var pos = Vector2(x * (16 + 8) + 24, 16 * 4 + y * 16)
            add_child(e)
            e.start(pos)
            e.died.connect(_on_enemy_died)
```

これにより、27体の敵キャラクターが生成され、画面上部半分にグリッド状に配置されます。また、各敵キャラの「死亡」シグナルを適切に接続する必要があるため、この機能を実装する関数を作成します。

```gdscript
func _on_enemy_died(value):
    score += value
```

まだスコアを表示する方法がありませんが、すぐに対応します。

シーンを再生すると、画面上部から敵の集団が次々と出現し、定期的に画面下へ落ちていく様子が確認できるはずです。次に、これらに攻撃動作を追加していきましょう。

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_06/" icon="fas fa-arrow-left" %}} 前の手順{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_08/" icon="fas fa-arrow-right" icon-position="right" %}}次の手順{{% /button %}} |
|------|------:|
