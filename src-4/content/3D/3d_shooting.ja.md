---
title: "投射物の発射"
weight: 5
draft: false
ghcommentid: 36
---

## 課題

プレイヤー／モブなどから投射物を発射させたい。

## 解決策

この例では、[『キネマティックボディ：移動』チュートリアル](/godot_recipes/3.x/3d/kinematic_body/) で作成した「ミニタンク」モデルを使用します。

### 弾丸の設定

まず、インスタンス化可能な「弾丸」オブジェクトを設定します。使用するノードは以下の通りです。

```
{{< gd-icon Area3D >}} Area: Bullet
    {{< gd-icon MeshInstance3D >}} MeshInstance
    {{< gd-icon CollisionShape3D >}} CollisionShape
```

メッシュには、Godotに標準で備わっているプリミティブ形状を使用するか、以下のようなものを作成できます。

![alt](/godot_recipes/3.x/img/3d_shoot_01.png)

{{% notice note %}}
ここに掲載している弾丸モデルを使用したい場合は、[ケニーの『武器パック』](https://kenney.nl/assets/weapon-pack)から入手できます。
{{% /notice %}}

メッシュを `{{< gd-icon MeshInstance3D >}} MeshInstance` に追加し、衝突形状もそれに合わせてスケール調整してください。

{{% notice warning %}}
`MeshInstance` を `Area`ノードの前方方向（**-Z軸**）に合わせて整列させることを忘れないでください。そうしないと、弾丸が正しく飛んでいるように見えません！
{{% /notice %}}

スクリプトを追加し、{{< gd-icon Area3D >}}`Area3D`の`body_entered`シグナルに接続してください。

```gdscript
extends Area

signal exploded

export var muzzle_velocity = 25
export var g = Vector3.DOWN * 20

var velocity = Vector3.ZERO


func _physics_process(delta):
    velocity += g * delta
    look_at(transform.origin + velocity.normalized(), Vector3.UP)
    transform.origin += velocity * delta


func _on_Shell_body_entered(body):
    emit_signal("exploded", transform.origin)
    queue_free()
```

カスタムの重力ベクトル `g` を使用することで、戦車の砲弾が綺麗な弧を描くように、大砲からどのように飛ぶかを制御できます。もし、飛び道具を直線的に移動させたい場合は、`_physics_process()` で重力を適用している行を削除してください。

Using `look_at()` each frame turns the bullet to point in its direction of travel.

また、`exploded`シグナルも発出します。これを利用して爆発エフェクトやダメージ効果を実装できます（ただし詳細な実装は別のレシピで解説します）。

### 撮影について

タンク（または射撃を行っているオブジェクト）内に、弾丸が出現する位置に `{{< gd-icon Position3D >}}`Position3D` 子要素を追加します。例として戦車の場合、砲身の先端に配置します。

![alt](/godot_recipes/3.x/img/3d_shoot_02.png)

次に、インスタンス化する弾シーンを追加する方法です：

```gdscript
export (PackedScene) var Bullet
```

そして、`_process()` または `_unhandled_input()`（入力をキャプチャしている箇所）に、以下のコードを追加して弾丸を生成してください。

```gdscript
if Input.is_action_just_pressed("shoot"):
    var b = Bullet.instance()
    owner.add_child(b)
    b.transform = $Cannon/Muzzle.global_transform
    b.velocity = -b.transform.basis.z * b.muzzle_velocity
```

これで完了です。シーンを実行して実際に試してみましょう。

<video controls src="/godot_recipes/3.x/img/3d_shoot_03.webm"></video>

<!-- {{% notice note %}}
プロジェクトファイルはこちらよりダウンロードできます。[3d_shooting.zip](/godot_recipes/3.x/files/3d_shooting.zip)
{{% /notice %}} -->

## 関連レシピ

- [動力体システム：移動操作](/godot_recipes/3.x/3d/kinematic_body/)
- [Godot入門編：3Dの基礎](/godot_recipes/3.x/g101/3d/)

<!-- #### Videoが気に入ったら？ -->

{{< youtube 7axJJYont6Y >}} -->