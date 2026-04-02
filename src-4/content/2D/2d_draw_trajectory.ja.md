---
title: "軌跡を描画"
weight: 13
draft: false
ghcommentid: 32
---

## 課題

戦車のような弾道射撃の軌道を描きたい。

## 解決策

### 設定手順

この例では、以下のレシピから「弾道弾丸」を使用します。

* [弾道弾の実装方法](/godot_recipes/4.x/ja/2d/ballistic_bullet/)

そして、以下のように設定されたタンクの配置です。ここでは弾丸が生成される箇所を示すために {{< gd-icon Marker2D >}} の `Marker2D` 要素を使用しています。

![alt](/godot_recipes/3.x/img/tank_01.png)

タンクのスクリプトでは、弾丸を以下のようにインスタンス化しています。

```gdscript
func _unhandled_input(event):
    if event.is_action_released("shoot") and can_shoot:
        var b = Bullet.instantiate()
        owner.add_child(b)
        b.transform = $Barrel/Muzzle.global_transform
        b.velocity = b.transform.x * muzzle_velocity
        b.gravity = gravity
        can_shoot = false
```

このインスタンスでは弾丸オブジェクトを作成し、「世界」ノード（戦車の所有者）の下に子要素として追加し、初期プロパティを設定します。なお、この例では重力定義に戦車を利用していますが、これは単なるデモンストレーション用です。実際のプロジェクトでは、グローバルな値を使用する方が望ましいでしょう。

以下に、初期設定の動作例をご紹介します。

![alt](/godot_recipes/3.x/img/tank_02.gif)

### ライン設定

メインシーン内（タンクと地面を含む部分）に、{{< gd-icon Line2D >}} `Line2D` を追加しました。これが軌跡を描画するための要素となります。

ラインの見た目を改善するため、**幅**を「15」に設定し、すべての**角処理**オプションを「丸み」に変更しました。さらに、**塗りつぶし**セクションにグラデーションを追加しました。

![alt](/godot_recipes/3.x/img/2d_tank_03.png)

### 線を引くこと

これで線を引く準備が整いました。目標は、投影された軌道に沿って移動しながら、進行状況に応じて線に点を追加していくことです。発射時の初速度と弾丸が使用する重力がわかっているので、同じ計算式を適用できます。

```gdscript
@onready var tank = $Tank
@onready var muzzle = $Tank/Barrel/Muzzle
@onready var line = $Line2D
var max_points = 250

func update_trajectory(delta):
    line.clear_points()
    var pos = muzzle.global_position
    var vel = muzzle.global_transform.x * tank.muzzle_velocity
    for i in max_points:
        line.add_point(pos)
        vel.y += tank.gravity * delta
        pos += vel * delta
        if pos.y > $Ground.position.y - 25:
            break

func _process(delta):
    if Input.is_action_pressed("shoot"):
        line.show()
        update_trajectory(delta)

func _on_Bullet_exploded(pos):
    tank.can_shoot = true
    line.hide()
```

`max_points`でラインに追加するポイント数の上限を設定します。`update_trajectory()`関数では、タンクから弾丸の初期位置と速度を取得します（この例では重力もタンク内で定義されています）。その後、これらの点を繰り返し処理し、各「ステップ」でポジションを、1フレーム中に弾丸が移動する量と同じだけ移動させます。

また、経路が地面の最上部位置に接した場合には描画を停止する`break`を追加しました。このケースではこれ以上描画を続けないためです。

最後に、撮影の有無に応じてラインの表示／非表示を切り替えます。

![alt](/godot_recipes/3.x/img/tank_04.gif)

## 関連レシピ

[2Dシューティングゲームの作成レシピ](/godot_recipes/4.x/ja/2d/2d_shooting/)
[2D弾道式弾丸システム](/godot_recipes/4.x/ja/2d/ballistic_bullet)