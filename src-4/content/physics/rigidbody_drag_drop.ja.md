---
title: "RigidBody2D: Drag and Drop"
weight: 4
draft: false
---

## 問題文

マウスで剛体を選択して移動させたい場合。

## 解決策

リジッドボディを扱う際には注意が必要です。Godotの物理演算エンジンがこれらの動きを制御しており、これに干渉すると予期しない結果を招くことがあります。重要なのは、オブジェクトの`mode`プロパティを活用する点です。これは2Dでも3Dでも同様に適用されます。

### ボディ設定

はじめに、剛体オブジェクトを作成します。まず{{< gd-icon Sprite2D >}}`Sprite2D`と{{< gd-icon CollisionShape2D >}}`CollisionShape2D`を追加してください。さらに物理特性を設定したい場合は`PhysicsMaterial`も追加できます。このマテリアルでは_Bounce_（反発係数）と_Friction_（摩擦係数）のプロパティを調整可能です。

We're going to use the rigid body's `freeze` property to remove it from the control of the physics engine while we're dragging it. Since we still want it to be movable, we need to set the **Freeze Mode** to "Kinematic", rather than the default value of "Static".

Place the body in a group called "pickable". We'll use this to allow for multiple instances of the pickable object in the main scene. Attach a script to the body and connect the its `_input_event` signal.

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

체중이 드래그 중인 경우, 마우스의 위치에 따라 그 위치를 업데이트합니다.

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

In the `drop` function, after we change `freeze` back to `false, the body will return to the physics engine's control. By passing in an optional impulse value, we can add the ability to "throw" the object on release.

### メインシーン

メインシーンを作成し、静的な障害物を配置するか、{{< gd-icon TileMap >}}`TileMap`を使用して、選択可能なボディのインスタンスをいくつか作成してください。

メインシーン用のスクリプトです。まず、シーンで使用可能なすべてのボディに対して `clicked` シグナルを接続するところから始めます。

```gdscript
extends Node2D

var held_object = null

func _ready():
    for node in get_tree().get_nodes_in_group("pickable"):
        node.clicked.connect(_on_pickable_clicked)
```

```plaintext
次に、シグナルを接続する関数について説明します。接続された関数では`held_object`変数を設定して現在ドラッグ中のものを記録し、ボディの`pickup()`メソッドを呼び出してオブジェクトのピックアップ操作を開始します。
```

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

```python
# 物体に衝撃力を適用するために `get_last_mouse_velocity()` を使用している点に注意 - 取り扱いには注意が必要です! 特に質量値が小さい場合、剛性体は高速で発射される可能性があります。適切なスケールに調整し、最大値にクランプすることをお勧めします。最適な設定を見つけるには実験が必要です。

<video controls src="/godot_recipes/4.x/img/rbody_drag.webm"></video>

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらからダウンロードできます: [https://github.com/godotrecipes/rigidbody_drag_drop](https://github.com/godotrecipes/rigidbody_drag_drop)

## 関連レシピ

