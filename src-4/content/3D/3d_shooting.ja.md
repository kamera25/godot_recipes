---
title: "投射物の発射"
weight: 5
draft: false
ghcommentid: 36
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 今回のお題

プレイヤー／モブなどから投射物を発射させたい。

## 作り方

この例では、[CharacterBody3D：移動操作](/godot_recipes/4.x/ja/3d/kinematic_body/) で設定した「ミニ戦車」を使用します。

### 弾丸の設定

まず、インスタンス化可能な「弾丸」オブジェクトを設定します。使用するノードは以下の通りです。

```
{{< gd-icon Area3D >}} Area3D: Bullet
    {{< gd-icon MeshInstance3D >}} MeshInstance
    {{< gd-icon CollisionShape3D >}} CollisionShape
```

メッシュには、Godotに標準で備わっているプリミティブ形状を使用するか、以下のようなものを作成できます。

![alt](/godot_recipes/4.x/img/3d_shoot_01.png)

{{% notice note %}}
ここに掲載している弾丸モデルを使用したい場合は、[Kenney's "Blaster Kit"](https://www.kenney.nl/assets/blaster-kit)から入手できます。
{{% /notice %}}

メッシュを {{< gd-icon MeshInstance3D >}}`MeshInstance` に追加し、衝突形状もそれに合わせてスケール調整します。

{{% notice warning %}}
必ず {{< gd-icon MeshInstance3D >}}`MeshInstance` を `Area3D` ノードの前方方向（**-Z** 軸）と揃えてください。そうしないと、弾丸が正しく飛んでいるように見えませんよ！
{{% /notice %}}

スクリプトを追加し、{{< gd-icon Area3D >}}`Area3D`の`body_entered`シグナルを接続します。

```gdscript
extends Area3D

signal exploded

@export var muzzle_velocity = 25
@export var g = Vector3.DOWN * 20

var velocity = Vector3.ZERO


func _physics_process(delta):
    velocity += g * delta
    look_at(transform.origin + velocity.normalized(), Vector3.UP)
    transform.origin += velocity * delta


func _on_Shell_body_entered(body):
    emit_signal("exploded", transform.origin)
    queue_free()
```

カスタムの重力ベクトル `g` を使用することで、戦車の砲弾が綺麗な弧を描くように、大砲からどのように飛ぶかを制御できます。もし、飛び道具を直線的に移動させたい場合は、`_physics_process()` で重力を適用している行を削除します。

`look_at()` をフレームごとに使用すると、弾丸は常に進行方向を向くようになります。

また、`exploded`シグナルも発出します。これを利用して爆発エフェクトやダメージ効果を実装できます（ただし詳細な実装は別のレシピで解説します）。

### 射撃

タンク内（または射撃オブジェクト）の任意の位置に、弾丸が出現させたい場所に {{< gd-icon Marker3D >}}`Marker3D` 子要素を追加します。今回の戦車の場合、砲身の先端部分に配置します。

![alt](/godot_recipes/4.x/img/3d_shoot_02.png)

次に、インスタンス化する弾シーンを追加する方法です。

```gdscript
@export var Bullet: PackedScene
```

そして、`_process()` または `_unhandled_input()`（入力をキャプチャしている箇所）に、以下のコードを追加して弾丸を生成します。

```gdscript
if Input.is_action_just_pressed("shoot"):
    var b = Bullet.instantiate()
    owner.add_child(b)
    b.transform = $Cannon/Muzzle.global_transform
    b.velocity = -b.transform.basis.z * b.muzzle_velocity
```

これで完了です。シーンを実行して実際に試してみます。

<video controls src="/godot_recipes/4.x/img/3d_shoot_03.webm"></video>

<!-- {{% notice note %}}
プロジェクトファイルはこちらよりダウンロードできます。[3d_shooting.zip](/godot_recipes/4.x/ja/files/3d_shooting.zip)
{{% /notice %}} -->

## 関連レシピ

- [CharacterBody3D: 移動方法](/godot_recipes/4.x/ja/3d/characterbody3d_examples/)
- [初めてのGodot: 3D入門](/godot_recipes/4.x/ja/g101/3d/)

<!-- #### Videoが気に入ったら？ -->

{{< youtube 7axJJYont6Y >}} -->