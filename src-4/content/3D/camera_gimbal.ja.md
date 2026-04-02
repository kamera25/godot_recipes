---
title: "カメラジンバル"
weight: 2
draft: false
---

## 課題

以下の機能を備えたカメラコントローラーが必要となります。マウスまたはキーボード操作で、回転中も水平を保ちつつ、ターゲットを追従できるもの。

## 解決策

以下の手順を試してみてください。`Camera3D`ノードを1つ取得し、**X軸**（ギズモ上の赤いリング）を中心にわずかに回転させた後、続いて**Z軸**（青いリング）を中心に少し回転させます。次に、**X軸**方向の回転を逆方向に反転させ、「プレビュー」ボタンをクリックしてください。カメラが斜めに傾いた状態になっていることが確認できるはずです。

この問題を解決するには、カメラを_ジンバル・マウント_に取り付ける必要があります。これは、移動時も物体の水平を保つよう設計された装置です。2つの{{< gd-icon Node3D >}}`Node3D`ノードを使用することで、左右方向と上下方向の回転を個別に制御できる簡易ジンバルを作成できます。

ノードの設定は以下のようにしてください。

```
{{< gd-icon Node3D >}} Node3D: CameraGimbal
    {{< gd-icon Node3D >}} Node3D: InnerGimbal
        {{< gd-icon Camera3D >}} Camera3D
```

{{< gd-icon Camera3D >}}`Camera3D` の**変換/位置**を `(0, 0, 4)` に設定してください。

以下にジンバルの仕組みを説明します。外側ノードは**Y軸方向のみ**回転可能で、内側ノードは**X軸方向のみ**回転できます。手動で試したい場合は、まず「ーカル空間を使用」（メニューバーのロックアイコン隣にあるキューブアイコン - ショートカットキーは「T」）に切り替えることを忘れないでください。必ず外側ノードの_緑色リング_のみを、内側ノードの_赤色リング_のみを操作してください。カメラノードには一切触れないよう注意してください。

<video controls src="/godot_recipes/4.x/img/gimbal_01.webm"></video>

実験が完了したら、すべての回転値を`0`にリセットしてください。

### キーボード操作

キーボード操作から始めてください。その後、マウスを使用するオプションも追加します。必要な操作と割り当てられた入力は以下の通りです。

   アクション名 | キー
--------|------
`"cam_up"` | Wキー
`"cam_down"` | Sキー
`"cam_right"` | Dキー
`"cam_left"` | Aキー
`"cam_zoom_in"` | マウスホイール上方向回転
`"cam_zoom_out"` | マウスホイール下方向回転

以下に初期スクリプトを示します。前述の通り、各 `Node3D` をその局所座標系内で特定軸周りに回転させることに注意してください。

```gdscript
extends Node3D

var rotation_speed = PI/2

func get_input_keyboard(delta):
    # Rotate outer gimbal around y axis
    var y_rotation = Input.get_axis("cam_left", "cam_right")
    rotate_object_local(Vector3.UP, y_rotation * rotation_speed * delta)
    # Rotate inner gimbal around local x axis
    var x_rotation = Input.get_axis("cam_up", "cam_down")
    x_rotation = -x_rotation if invert_y else x_rotation
    inner.rotate_object_local(Vector3.RIGHT, x_rotation * rotation_speed * delta)

func _process(delta):
    get_input_keyboard(delta)
```

以下の手順でテストシーンを作成してください。

1. `MeshInstance3D`を使用してテスト用シーンを作成します
2. そのシーン内に`CameraGimbal`インスタンスを配置し、動作をテストします

アップ/ダウンコントロールを操作すると、カメラがぐるりと一回転してしまい、最終的には上下逆さまになってしまいます。これを防止するために、回転角度に上限を設定しましょう。

```gdscript
func _process(delta):
    get_input_keyboard(delta)
    $InnerGimbal.rotation.x = clamp($InnerGimbal.rotation.x, -1.4, -0.01)
```

`-1.4` の値を指定すると、カメラをほぼ90度上向きにしつつ、最小角度を非常に小さく設定することで地面へのクリップを防止します。他の値も自由に試してみてください。

### マウス操作

マウスとキーボードの制御を簡単に切り替えられるよう、「mouse_control」というフラグを追加します。

```gdscript
# mouse properties
var invert_y = false
var invert_x = false
var mouse_control = false
var mouse_sensitivity = 0.005

func _unhandled_input(event):
    if mouse_control and event is InputEventMouseMotion:
        if event.relative.x != 0:
            var dir = 1 if invert_x else -1
            rotate_object_local(Vector3.UP, dir * event.relative.x * mouse_sensitivity)
        if event.relative.y != 0:
            var dir = 1 if invert_y else -1
            $InnerGimbal.rotate_object_local(Vector3.RIGHT, dir * event.relative.y * mouse_sensitivity)

func _process(delta):
    if !mouse_control:
        get_input_keyboard(delta)
```

このコードは、水平方向のマウス操作を外側ジンバルの**Y軸回転**に、垂直方向の操作を内側ジンバルの**X軸回転**に変換する仕組みになっています。さらに、`invert_x` と `invert_y` フラグを追加し、いずれかの軸に対して動きを反転させることができるようにしました。多くのプレイヤーはどちらか一方の方式を好むため、両方のオプションを用意しておくのがベストです。

また、`_process()` 関数では、マウス操作時のキーボード入力を無効化しています。

マウスを急激に動かすと、上下移動に問題が生じることに気付くかもしれません。`event.relative.y` の値が大きい場合、制限された値の反対側に「スキップ」する現象が発生します。この問題を解決するには、垂直方向のマウス移動を合理的な範囲に制限すればよいでしょう。上記コードの `y` 部分を以下のように変更してください。

```gdscript
if event.relative.y != 0:
    var dir = 1 if invert_y else -1
    var y_rotation = clamp(event.relative.y, -30, 30)
    $InnerGimbal.rotate_object_local(Vector3.RIGHT, dir * y_rotation * mouse_sensitivity)
```

このプロジェクトでは、ゲームプレイ中にマウス入力を取得する必要も出てくるでしょう。詳細は本ドキュメント末尾の関連リンクレシピをご覧ください。

### カメラのズーム機能

カメラのズーム機能は、ジンバルシステムの「スケール」を変化させることで動作します。

```gdscript
# zoom settings
var max_zoom = 3.0
var min_zoom = 0.5
var zoom_speed = 0.09

var zoom = 1.5

func _unhandled_input(event):
    if event.is_action_pressed("cam_zoom_in"):
        zoom -= zoom_speed
    if event.is_action_pressed("cam_zoom_out"):
        zoom += zoom_speed
    zoom = clamp(zoom, min_zoom, max_zoom)

func _process(delta):
    scale = lerp(scale, Vector3.ONE * zoom, zoom_speed)
```

`lerp()` を使用してズームレベルを変更すると、より滑らかなズーミングが可能になります。

![alt](/godot_recipes/4.x/img/gimbal_02.gif)

### ターゲットの追跡中

カメラジンバルのセットアップが完了したら、以下の手順でターゲットを追跡できるようになります。

```gdscript
@export var target : Node3D

func _process(delta):
    if target:
        global_position = target.global_position
```

シーン内のカメラを選択し、「インスペクター」を使用して追跡したいノードを選択してください。

## 最終スクリプト

参考までに、カメラ設定の全変数を含む完全なスクリプトを掲載します。この内容を参考にプロジェクト環境で設定してください。

```gdscript
extends Node3D

@export var target : Node3D

@export_range(0.0, 2.0) var rotation_speed = PI/2

# mouse properties
@export var mouse_control = false
@export_range(0.001, 0.1) var mouse_sensitivity = 0.005
@export var invert_y = false
@export var invert_x = false

# zoom settings
@export var max_zoom = 3.0
@export var min_zoom = 0.4
@export_range(0.05, 1.0) var zoom_speed = 0.09

var zoom = 1.5

@onready var inner = $InnerGimbal

func _unhandled_input(event):
    if Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
        return
    if event.is_action_pressed("cam_zoom_in"):
        zoom -= zoom_speed
    if event.is_action_pressed("cam_zoom_out"):
        zoom += zoom_speed
    zoom = clamp(zoom, min_zoom, max_zoom)
    if mouse_control and event is InputEventMouseMotion:
        if event.relative.x != 0:
            var dir = 1 if invert_x else -1
            rotate_object_local(Vector3.UP, dir * event.relative.x * mouse_sensitivity)
        if event.relative.y != 0:
            var dir = 1 if invert_y else -1
            var y_rotation = clamp(event.relative.y, -30, 30)
            inner.rotate_object_local(Vector3.RIGHT, dir * y_rotation * mouse_sensitivity)

func get_input_keyboard(delta):
    # Rotate outer gimbal around y axis
    var y_rotation = Input.get_axis("cam_left", "cam_right")
    rotate_object_local(Vector3.UP, y_rotation * rotation_speed * delta)
    # Rotate inner gimbal around local x axis
    var x_rotation = Input.get_axis("cam_up", "cam_down")
    x_rotation = -x_rotation if invert_y else x_rotation
    inner.rotate_object_local(Vector3.RIGHT, x_rotation * rotation_speed * delta)

func _process(delta):
    if !mouse_control:
        get_input_keyboard(delta)
    inner.rotation.x = clamp(inner.rotation.x, -1.4, -0.01)
    scale = lerp(scale, Vector3.ONE * zoom, zoom_speed)
    if target:
        global_position = target.global_position
```

## 関連レシピ

[マウス操作のキャプチャ方法](/godot_recipes/4.x/ja/input/mouse_capture/)
[3D入門ガイド](/godot_recipes/4.x/ja/g101/3d/) →

<!-- #### Videoが気に入ったら？ -->

{{< youtube 4NLrfxNt3ps >}} -->