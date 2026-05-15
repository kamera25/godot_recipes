---
title: "3Dで自動車を作ろう：カメラで追いかけよう"
weight: 3
draft: false
ghcommentid: 43
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

車（またはその他の物体）を追跡できる「追従カメラ」を実装したい。

## 解決策

{{% notice note %}}
Godot には組み込みの `InterpolatedCamera` ノードが用意されており、ここで説明している機能の大部分をすでに実装しています。ただし、このノードを使用しない理由は2つあります。まず、キャラクターボディを追いかける際にカクツキが発生しやすい点、次に Godot 4.0 で廃止予定となっている点です。とはいえ、独自のセットアップは非常に簡単ですので、ご安心ください。<i class='far fa-smile-beam'></i>
{{% /notice %}}

### カメラのセットアップ方法

新しいシーンを{{< gd-icon Camera3D >}}`Camera3D`で追加します。名前は`ChaseCamera`とし、保存してからスクリプトを追加します。

`ChaseCamera`には追跡対象の`target`が設定されます。また、必要に応じてこのターゲットを変更する機能も実装します。

```gdscript
extends Camera

@export var lerp_speed = 10.0

var target = null

func _physics_process(delta):
    if !target:
        return
    global_transform = global_transform.interpolate_with(target.global_transform, lerp_speed * delta)

func _on_change_camera(t):
    target = t
```

この設定で重要なのは`lerp_speed`パラメーターのみです。これはカメラが位置を更新する速度を調整する値です。値を小さくするとカメラは車の動きに「遅れて」追従し、大きく設定すると常に車両に固定された状態になります。

### ターゲットの設定

複数の異なるカメラポジションを設定したいと考えています。例えば、近距離用と遠距離用の2種類、あるいは真下を見下ろすアングルなどです。車オブジェクトに  {{< gd-icon Node3D >}}`Node3D` を追加し、名前を `CameraPositions` とします。さらにこのオブジェクトに、必要な数だけ {{< gd-icon Marker3D >}}`Marker3D` を配置します。

{{< gd-icon Marker3D >}}`Marker3D` をお好みの位置に移動・配置します。位置の **-Z** 軸は車両に向けるようにします。

{{% notice tip %}}
作業効率を上げるため、一時的に {{< gd-icon Camera3D >}}`Camera` を適切な位置に配置し、「プレビュー」モードを使用して、{{< gd-icon Marker3D >}}`Marker3D` が正確に狙いたい方向を指すように調整する方法が有効です（作業完了後はカメラを削除してください）。
![alt](/godot_recipes/4.x/img/3d_car_09.png)
{{% /notice %}}

カメラと通信するために、位置変更が必要な時にシグナルを発します。以下のコードを車のスクリプトに追加します。

```gdscript
extends "res://cars/car_base.gd"

signal change_camera

var current_camera = 0
@onready var num_cameras = $CameraPositions.get_child_count()

func _ready():
    emit_signal("change_camera", $CameraPositions.get_child(current_camera))

func _input(event):
    if event.is_action_pressed("change_camera"):
        current_camera = wrapi(current_camera + 1, 0, num_cameras)
        emit_signal("change_camera", $CameraPositions.get_child(current_camera))
```

インプットマップにカメラ切り替え用のアクションを追加します。ここではTabキーと右ショルダーボタンを使用しています。

![alt](/godot_recipes/4.x/img/3d_car_07.png)

### 接続方法

メインシーンに`ChaseCamera`インスタンスを追加し、`現在`のカメラとして設定します。その後、車の`change_camera`シグナルをカメラの`_on_change_angle()`関数に接続します。



ゲームを起動し、カメラ切替ボタンを押して試してみてください。

![alt](/godot_recipes/4.x/img/3d_car_08.gif)

## 関連レシピ

- [運動車：基本モデル](/godot_recipes/4.x/ja/3d/kinematic_car/car_base/)
- [2D: 車両のステアリング制御レシピ](/godot_secrets/3.x/2d/car_steering)
- [入力アクション設定](/godot_recipes/4.x/ja/input/input_actions/)
- [3D: CharacterBody3Dの移動機能](/godot_recipes/4.x/ja/3d/kinematic_body/)

#### この動画が気に入ったら？

