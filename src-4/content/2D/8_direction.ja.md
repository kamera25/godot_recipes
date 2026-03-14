---
title: "8方向移動・アニメーション"
weight: 4
draft: false
ghcommentid: 100
---

## 課題

2Dキャラクターが必要です。アニメーションを含む8方向移動が可能なものが求められます。

## 解決策

この例では、[アイソメトリック・ミニクルセイダー](https://remos.itch.io/mini-crusader)を使用します。これには待機、歩行、攻撃など8方向に対応したアニメーションが含まれています。

![alt](/godot_recipes/4.x/img/8_direction_01.gif)

アニメーションはフォルダ単位で整理されており、各フレームごとに個別の画像が用意されています。ここでは{{< gd-icon AnimatedSprite2D >}}`AnimatedSprite2D`を使用し、各アニメーションにはその動作方向に基づいて名前を付けます。例えば、右向きで時計回りに移動する`idle0`から、同じく時計回りに動く`idle7`までといった具合です。

我们的角色移动时，会根据移动方向选择相应的动画：

![alt](/godot_recipes/4.x/img/8_direction_03w.png)

マウスを使って移動します。キャラクターは常にマウスの方向を向き、マウスボタンをクリックするとその方向に走り出します。

どのアニメーションを再生するか選択するためには、マウスの方向を取得し、それを同じ範囲（0-7）にマッピングする必要があります。`get_local_mouse_position()`を使用することで、キャラクターに対するマウスカーソルの位置を取得できます。次に`snappedf()`関数を使用して、マウスベクトルの角度を最も近い45度間隔（π/4ラジアン）にスナップさせると、以下の結果が得られます。

![alt](/godot_recipes/4.x/img/8_direction_04w.png)

各値を 45°（π/4 ラジアン）で除算すると、以下のようになります。

![alt](/godot_recipes/4.x/img/8_direction_02w.png)

最終的には、`wrapi()`関数を使用して結果の範囲を`0-7`にマッピングする必要があります。これにより、正しい値が得られます。この値をアニメーション名の末尾に追加します（"idle"、"run"など）。こうすることで、正しく動作するアニメーションが完成します。

```gdscript
func _physics_process(delta):
    current_animation = "idle"

    var mouse = get_local_mouse_position()
    angle = snappedf(mouse.angle(), PI/4) / (PI/4)
    angle = wrapi(int(angle), 0, 8)

    if 入力.is_action_pressed("left_mouse") and mouse.length() > 10:
        current_animation = "run"
        velocity = mouse.normalized() * speed
        move_and_slide()
    $AnimatedSprite2D.animation = current_animation + str(a)
```

動作テストを行ったところ、以下の現象が確認されました：

![alt](/godot_recipes/4.x/img/8_direction_05.gif)

### キーボード入力

マウスの代わりにキーボード操作を使用している場合、押されているキーに基づいて移動角度を取得できます。それ以外の手順は同様の方法で進行します。

```gdscript
func _process(delta):
    current_animation = "idle"
    var input_dir = 入力.get_vector("left", "right", "up", "down")
    if input_dir.length() != 0:
        angle = input_dir.angle() / (PI/4)
        angle = wrapi(int(a), 0, 8)
        current_animation = "run"
    velocity = input_dir * speed
    move_and_slide()
    $AnimatedSprite2D.play(current_animation + str(angle))
```


## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます：[https://github.com/godotrecipes/8_direction_animation](https://github.com/godotrecipes/8_direction_animation)
