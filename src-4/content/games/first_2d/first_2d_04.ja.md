---
title: "Bullet Scene"
weight: 4
draft: false
pre: "04. "
---

プレイヤーが自由に画面内を移動できるようになった今、その次のステップとして「射撃」システムを実装していきましょう。

## 再利用可能なオブジェクト

The player will fire many "bullets" during the game, but all of them will be identical. A bullet needs to do the following:

・プレイヤーのすぐ前方に出現
・画面外に到達するまで前進移動
・敵キャラとの衝突を検知

Since all bullets will do these same things, we can save ourselves a great deal of work by designing one "prototype" bullet, and using that as the blueprint for creating as many duplicates as we need. Godot's scene system is ideal for this.

## 弾丸シーン

メニューから**シーン→新規シーン**を選択するか、ビューポート上部のタブにある**＋**アイコンをクリックすることで、新しいシーンを作成できます。

```

以下にノードの設定を示します：

* `Area2D` - この`Bullet`に名前を付ける
        * `Sprite2D`
        * `CollisionShape2D`
        * `VisibleOnScreenNotifier2D`

アセットパックフォルダから、`Player_charged_beam (16 x 16).png`画像ファイルを、{{< gd-icon Sprite2D >}}`Sprite2D`コンポーネントの**テクスチャ**プロパティにドラッグ＆ドロップしてください。

船舶画像と同様に、ここにも複数のバージョンが存在するため、***Hframes**を`2`に設定し、一度に表示する画像を1つだけにしましょう。

```
`CollisionShape2D`の形状を、先ほど`Player`シーンで設定した方法と同じように設定してください。

## 弾丸スクリプト

ノード「Bullet」にスクリプトをアタッチし、移動の基本設定から始めましょう：

```gdscript
extends Area2D

@export var speed = -250

func start(pos):
    position = pos

func _process(delta):
    position.y += speed * delta
```

このスクリプトはプレイヤー用のものと類似しているので、見覚えがあると思います。変更しているのは`position.y`だけです。弾丸を垂直に真上へ発射させるためです。

定義した`start()`関数に注目してください。これにより、プレイヤーが移動して異なる位置から弾丸を発射するため、弾丸の初期`位置`を設定することが可能になります。

### 信号の接続方法

次に、`弾丸`ノードを選択してから、**インスペクター**の横にある**ノード**タブをクリックしてください。

![alt](/godot_recipes/4.x/img/2d_101_16.png?width=350)

これはこのノードが送信可能なすべてのシグナル一覧です。シグナルはGodotで何かが発生したことを通知する仕組みです。この場合、`area_entered` シグナルを使用することで、この弾丸が他の {{< gd-icon Area2D >}}`Area2D` ノードに接触するたびに検知できます。

以下の手順に従って操作してください：

You'll notice that you're back in the script editor, looking at `bullet.gd`, and a new function as been added. It has a green "connected" icon next to its name to show that a signal is connected to it. This function will be called whenever the area touches something, so let's add some code here:

```gdscript
func _on_area_entered(area):
    if area.is_in_group("enemies"):
        area.explode()
        queue_free()
```

ここで弾が敵に当たったかどうかを確認します（詳細は後述）。当たった場合は、敵に対して爆発処理を実行した後、弾オブジェクトを削除します。

以下の手順に従って、{{< gd-icon VisibleOnScreenNotifier2D >}}`VisibleOnScreenNotifier2D` の `screen_exited` シグナルも接続してください：

```gdscript
func _on_visible_on_screen_notifier_2d_screen_exited():
    queue_free()
```

### 次のステップ

これで弾丸シーンは完了です。それでは、プレイヤーに射撃機能を追加していきましょう。

| {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_03/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_05/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
