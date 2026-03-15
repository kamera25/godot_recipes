---
title: "撮影中"
weight: 5
draft: false
pre: "05. "
---

「Bullet」シーンでは、プレイヤーが射撃するたびに再利用可能なオブジェクトを生成できます。

## プレイヤーへの追加方法

以下のコードを「Player」スクリプトに追加しましょう。

```gdscript
@export var cooldown = 0.25
@export var bullet_scene : PackedScene
var can_shoot = true
```

以下の2つの`@export`変数を使用すると、インスペクターで設定可能なため、クールタイムを調整できます。プロパティをクリックして`bullet.tscn`ファイルを選択する形で`bullet_scene`を設定してください。

`can_shoot`はプログラミング用語で言うところの「フラグ」です。これはある条件を制御するブール型変数です。この場合、プレイヤーが射撃可能かどうかを決定します。クール期間中、この変数は`false`に設定されます。

次に、`Bullet`と同様に`start()`関数を追加します。これにより、プレイヤーの初期値を設定できるほか、ゲームが再起動するたびにこれらの値をリセットできるようになります。

```gdscript
func _ready():
    start()

func start():
    position = Vector2(screensize.x / 2, screensize.y - 64)
    $GunCooldown.wait_time = cooldown
```

これにより、プレイヤーは画面の中央下部に配置され、最適なスタート位置となります。また、クールタイムタイマーが適切な待機時間を設定することを保証します。

`shoot()`関数は、『射撃』入力が押されるたびに呼び出されるようになります。

```gdscript
func shoot():
    if not can_shoot:
        return
    can_shoot = false
    $GunCooldown.start()
    var b = bullet_scene.instantiate()
    get_tree().root.add_child(b)
    b.start(position + Vector2(0, -8))
```

この関数の最初の処理は、プレイヤーが射撃可能かどうかを確認することです。もし許可されていない場合、`return`文によって即座に関数が終了します。

プレイヤーが射撃可能状態の場合、フラグを`false`に設定し、クールタイムタイマーを開始します。その後、新しい弾丸オブジェクトを作成しゲームに追加し、その`start()`関数を呼び出して正しい位置に配置します（プレイヤーの宇宙船すぐ上）。

この関数を呼び出せるのは、プレイヤーがキーを押している時です。`_process()` 関数の末尾、`position.clamp()` 行の後にこれを追加してください。

```gdscript
if Input.is_action_pressed("shoot"):
    shoot()
```

さらに、`GunCooldown` の `timeout` シグナルも接続が必要です。

```gdscript
func _on_gun_cooldown_timeout():
    can_shoot = true
```

クールタイムが終了したら、再び射撃を許可できます。

シーンを実行して、撮影アクションを押してみてください。

![alt](/godot_recipes/4.x/img/2d_101_17.gif)

{{% notice style="note" title="ツリーへのインスタンス追加について" %}}
注意：新規に生成した弾丸はシーンツリーのルートノード（`get_tree().root`）の下に子要素として追加されたことに留意してください。プレイヤー船の子要素としては追加していません。これは重要な点です。もし弾丸を船の子要素にしていた場合、船が移動するたびにそれらが「固定」されてしまうからです。
{{% /notice %}}

## 次のステップ

シューティングゲームは撃つ対象がなければ面白くありません。敵キャラの作成に取り掛かりますが、その前にプレイヤーや敵、その他のゲーム内オブジェクトを配置するシーンを作成が必要です。

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_04/" icon="fas fa-arrow-left" %}}前のステップ{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_06/" icon="fas fa-arrow-right" icon-position="right" %}}次のステップ{{% /button %}} |
|------|------:|
