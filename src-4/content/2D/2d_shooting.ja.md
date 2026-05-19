---
title: "投射物の発射"
weight: 2
draft: false
ghcommentid: 26
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 今回のお題

プレイヤー／モブなどから投射物を発射させたい。

## 作り方

### 弾丸の設定

まず、インスタンス化可能な「弾丸」オブジェクトを設定します。使用するノードは以下の通りです。

```
{{< gd-icon Area2D >}} Area2D: Bullet
    {{< gd-icon Sprite2D >}} Sprite2D
    {{< gd-icon CollisionShape2D >}} CollisionShape2D
```

{{< gd-icon Sprite2D >}}`Sprite2D`のテクスチャは、好きな画像を使用できます。以下は例です。

![alt](/godot_recipes/4.x/img/laserRed01.png)

ノードの設定とスプライトおよび衝突判定形状を構成します。テクスチャが上向きに配置されている場合（上記例のように）は、{{< gd-icon Sprite2D >}}`Sprite` ノードを `90°` 回転させて右方向に向け、親オブジェクトの「前方」方向に一致するように調整します。

スクリプトを追加し、{{< gd-icon Area2D >}}`Area2D`の`body_entered`シグナルに接続します。

```gdscript
extends Area2D

var speed = 750

func _physics_process(delta):
    position += transform.x * speed * delta

func _on_Bullet_body_entered(body):
    if body.is_in_group("mobs"):
        body.queue_free()
    queue_free()
```

この例では、オブジェクトが何かを衝突した場合、即座に弾丸を除去します。また、「mobs」グループにタグ付けされた対象物もすべて削除します。

### 射撃

弾丸の出現位置を設定が必要です。{{< gd-icon Marker2D >}}`Marker2D`コンポーネントを追加し、弾丸を出現させたい場所に配置します。以下は具体例で、銃身の先端に設置しています。「Muzzle」という名前を付けています。

![alt](/godot_recipes/4.x/img/2d_shoot_01.gif)

「プレイヤーが回転するにつれ、Muzzleの`transform`は銃に対して常に同じ向きを保つことに注目します。これは弾丸をスポーンさせる際に非常に便利です。変換行列を使用することで、適切な位置と方向を簡単に取得できるからです。新しい弾丸の`transform`は、単にMuzzleのものと等しく設定するだけで済みます。

{{% notice tip %}}
この手法は「回転・移動」スタイルに限らず、あらゆる文字タイプに適用できます。単に、弾丸を表示させたい位置に {{< gd-icon Marker2D >}}`Marker2D` タグを挿入するだけで済みます。
{{% /notice %}}

キャラクタースクリプトで、インスタンス化用の弾丸シーンを保持する変数を追加します。

```gdscript
@export var Bullet : PackedScene
```

入力アクションが定義されているか確認します。

```gdscript
    if Input.is_action_just_pressed("shoot"):
        shoot()
```

これで`shoot()`関数内では、弾丸インスタンスを生成しツリーに追加できます。よくあるミスとして、プレイヤーノードの子要素として直接追加してしまうケースがあります

```gdscript
func shoot():
    var b = Bullet.instantiate()
    add_child(b)
    b.transform = $Muzzle.transform
```

問題は、弾丸がプレイヤーの子オブジェクトであるため、プレイヤーが移動または回転した際に影響を受ける点です。

![alt](/godot_recipes/4.x/img/2d_shoot_02.gif)

この問題を解決するには、弾丸をワールドに追加が必要です。ここではプレイヤーのシーンルートノードを参照する `owner` 変数を使います。ただし、銃口の **グローバル** 変換行列も適用する必要がある点に注意します。これを行わないと、弾丸が想定した位置に表示されない可能性があります。

```gdscript
func shoot():
    var b = Bullet.instantiate()
    owner.add_child(b)
    b.transform = $Muzzle.global_transform
```

![alt](/godot_recipes/4.x/img/2d_shoot_03.gif)

## 関連レシピ

<!-- - [Top-down character](/godot_recipes/4.x/ja/2d/topdown_movement/) -->
- [ゲーム数学：トランスフォーム操作](/godot_recipes/4.x/math/transforms/)
<!-- - [AI: Homing missiles](/godot_recipes/4.x/ja/ai/homing_missile/) -->

<!-- #### Videoが気に入ったら？ -->

{{< youtube 7axJJYont6Y >}} -->

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらからダウンロードできます。[https://github.com/godotrecipes/2d_shooting](https://github.com/godotrecipes/2d_shooting)
