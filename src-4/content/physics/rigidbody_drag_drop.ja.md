---
title: "RigidBody2D: ドラッグ＆ドロップ操作"
weight: 4
draft: false
---

## 課題

マウスでリジッドボディを選択して移動させたい場合。

## 解決策

リジッドボディを扱う際には注意が必要です。Godotの物理演算エンジンがこれらの動きを制御しており、これに干渉すると予期しない結果を招くことがあります。重要なのは、オブジェクトの`mode`プロパティを活用する点です。これは2Dでも3Dでも同様に適用されます。

### ボディ設定

はじめに、リジッドボディオブジェクトを作成します。まず{{< gd-icon Sprite2D >}}`Sprite2D`と{{< gd-icon CollisionShape2D >}}`CollisionShape2D`を追加してください。さらに物理特性を設定したい場合は`PhysicsMaterial`も追加できます。このマテリアルでは _Bounce（反発係数）_ と _Friction（摩擦係数）_ のプロパティを調整できます。

物理演算エンジンの制御から一時的に解放するために、リジッドボディの「フリーズ」プロパティを使用します。ドラッグ操作中も移動可能にしておく必要があるため、デフォルト値である「静的モード」ではなく、**凍結モード**を「運動学的」に設定します。

体を「pickable」というグループに配置します。この設定により、メインシーンで複数のpick可能オブジェクトインスタンスを使用可能になります。Bodyにスクリプトをアタッチし、その`_input_event`シグナルに接続してください。

```gdscript
extends RigidBody2D

signal clicked

var held = false

func _on_input_event(viewport, event, shape_idx):
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if event.pressed:
            print("clicked")
            clicked.emit(self)
```

マウスクリックを検知すると、ボディへの参照を含むシグナルを発報します。複数のボディが存在する可能性があるため、メインシーン側で各ボディがドラッグ可能かどうか、あるいは既に「ホールド」状態にあるかどうかを管理する仕組みを設けます。

ボディがドラッグされている間は、その位置をマウスカーソルに合わせて更新します。

```gdscript
func _physics_process(delta):
    if held:
        global_transform.origin = get_global_mouse_position()
```

最後に、これらの関数はボディがピックアップされた時とドロップされた時に呼び出すものです。`freeze`を`true`に変更すると物理演算エンジンの処理から除外されます。ただし、他のオブジェクトはこの物体に衝突する可能性がある点に注意してください。もしこれを望まない場合は、ここで`collision_layer`および/または`collision_mask`も無効化できます。ただその場合、ドロップ時には再度有効化することを忘れないでください。

```gdscript
func pickup():
    if held:
        return
    freeze = true
    held = true

func drop(impulse=Vector2.ZERO):
    if held:
        freeze = false
        apply_central_impulse(impulse)
        held = false
```

`drop`関数内では、`freeze`を再び`false`に設定した後、ボディは物理エンジンの制御下に戻ります。オプションで衝撃値を指定することで、リリース時にオブジェクトを『投げる』機能を追加することも可能になります。

### メインシーン

メインシーンを作成し、静的な障害物を配置するか、{{< gd-icon TileMap >}}`TileMap`を使用して、選択可能なボディのインスタンスを作成してください。

メインシーン用のスクリプトです。まず、シーンで使用可能なすべてのボディに対して `clicked` シグナルを接続するところから始めます。

```gdscript
extends Node2D

var held_object = null

func _ready():
    for node in get_tree().get_nodes_in_group("pickable"):
        node.clicked.connect(_on_pickable_clicked)
```

次に、シグナルを接続する関数について説明します。接続された関数では`held_object`変数を設定して現在ドラッグ中のものを記録し、ボディの`pickup()`メソッドを呼び出してオブジェクトのピックアップ操作を開始します。

```gdscript
func _on_pickable_clicked(object):
    if !held_object:
        object.pickup()
        held_object = object
```

最後に、ドラッグ中にマウスボタンを離す場合、その逆の操作を実行できます。

```gdscript
func _unhandled_input(event):
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT:
        if held_object and !event.pressed:
            held_object.drop(Input.get_last_mouse_velocity())
            held_object = null
```

物体に衝撃力を適用するために `get_last_mouse_velocity()` を使用している点には注意が必要です! 特に質量値が小さい場合、リジッドボディは高速で発射される可能性があります。適切なスケールに調整し、最大値に制限をかけることをオススメします。最適な設定を見つけるには実験が必要です。

<video controls src="/godot_recipes/4.x/img/rbody_drag.webm"></video>

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらからダウンロードできます。 [https://github.com/godotrecipes/rigidbody_drag_drop](https://github.com/godotrecipes/rigidbody_drag_drop)

## 関連レシピ

