---
title: "3D 運動力学カー：チェイスカメラ"
weight: 3
draft: false
ghcommentid: 43
---

## 課題

以下のような「追従カメラ」をお探しですね：車（またはその他の物体）を追跡できる機能。

## 解決策

{{% notice note %}}
Godot には組み込みの `InterpolatedCamera` ノードが用意されており、ここで説明している機能の大部分をすでに実装しています。ただし、このノードを使用しない理由は2つあります。第一に、キネマティックボディを追いかける際にカクツキが発生しやすい点、次に Godot 4.0 で廃止予定となっている点です。とはいえ、独自のセットアップは非常に簡単ですので、ご安心ください。<i class='far fa-smile-beam'></i>
{{% /notice %}}

### カメラのセットアップ方法

新しいシーンを《《<gd-icon Camera3D>》》`カメラ`で追加します。名前は「ChaseCamera」とし、保存してからスクリプトを追加してください。

「ChaseCamera」には追跡対象の「target」が設定されます。また、必要に応じてこのターゲットを変更する機能も実装します。

```gdscript
extends Camera

export var lerp_speed = 10.0

var ターゲット = null;

func _physics_process(delta):
    if !target:
        return
    global_transform = global_transform.interpolate_with(target.global_transform, lerp_speed * delta)

func _on_change_camera(t):
    target = t
```

この設定で重要なのは「lerp_speed」パラメータのみです。これはカメラが位置を更新する速度を調整する値です。値を小さくするとカメラは車の動きに「遅れて」追従し、大きく設定すると常に車両に固定された状態になります。

### ターゲットの設定

複数の異なる追跡カメラ位置を設定できるようにしたいと考えています。例えば、近接視点と遠距離視点、あるいは真下を見下ろすアングルなどです。車両オブジェクトに {{< gd-icon Node3D >}}`Spatial`コンポーネントを追加し、名前を `CameraPositions` と名付けてください。このコンポーネントに追加の {{< gd-icon Position3D >}}`Position3D`コンポーネントを複数追加します - 必要な数だけ自由に設定できます。

各 `Position3D` 要素を各自選択した異なる位置に移動・配置してください。位置の **-Z** 軸は車両方向を指すように設定します。

{{% notice tip %}}
作業を効率的に進めるために、一時的に {{< gd-icon Camera3D >}}`カメラ` を適切な位置に配置し、"プレビュー"モードを使用して、{{< gd-icon Position3D >}}`Position3D`が正しい方向を向くように調整することをお勧めします（作業が完了したらカメラは削除できます）。
![alt](/godot_recipes/3.x/img/3d_car_09.png)
{{% /notice %}}

カメラと通信するために、位置変更が必要な時にシグナルを発します。以下のコードを車のスクリプトに追加してください。

```gdscript
extends "res://cars/car_base.gd"

signal change_camera

var current_camera = 0
onready var num_cameras = $CameraPositions.get_child_count()

func _ready():
    emit_signal("change_camera", $CameraPositions.get_child(current_camera))

func _input(event):
    if event.is_action_pressed("change_camera"):
        current_camera = wrapi(current_camera + 1, 0, num_cameras)
        emit_signal("change_camera", $CameraPositions.get_child(current_camera))
```

インプットマップにカメラ切り替え用のアクションを追加します。ここではTabキーと右ショルダーボタンを使用しています：

<img src="/godot_recipes/3.x/img/3d_car_07.png" alt="">

### 接続方法

メインシーンに`ChaseCamera`インスタンスを追加し、現在のカメラとして設定してください。その後、車の`change_camera`シグナルをカメラの`_on_change_angle()`関数に接続します。



ゲームを起動し、カメラ切替ボタンを押して試してみてください。

![alt](/godot_recipes/3.x/img/3d_car_08.gif)

## 関連レシピ

[キネマティックカー：基本モデル](/godot_recipes/3.x/3d/kinematic_car/car_base/)
- [2D: ステアリング操作レシピ](/godot_recipes/3.x/2d/car_steering)
- [入力アクション設定](http://kidscancode.org/godot_recipes/input/input_actions/)
- [3D: キネマティックボディの移動制御](/godot_recipes/3.x/3d/kinematic_body/)

#### この動画が気に入ったら？

