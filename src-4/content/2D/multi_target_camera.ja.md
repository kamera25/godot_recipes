---
title: "マルチターゲットカメラ"
weight: 11
draft: false
---

## 今回のお題

複数のオブジェクトを同時に画面上に表示し続けるために、移動・ズーム機能を備えたダイナミックなカメラシステムを作りたいです。

2人用ゲームで両プレイヤーを画面内に表示したまま、互いに近づき離れていく様子を表現する場合などです。

![alt](/godot_recipes/4.x/img/multi_cam_01.gif)

## 作り方

シングルプレイヤーモードでは、カメラをプレイヤーに追従させるのが一般的な手法です。しかし、ここでは2人以上のプレイヤーやその他の重要オブジェクトが常に画面に表示され続ける必要があるため、同様の方法は適用できません。

以下の3つの機能をカメラに実装が必要です。

1. ターゲットを任意の数だけ追加/削除可能
2. カメラの位置をターゲット群の中心点に固定表示
3. すべてのターゲットが画面内に収まるようズームレベルを調整

以下の手順で新規シーンを作成し、{{< gd-icon Camera2D >}}`Camera2D`コンポーネントを追加してスクリプトを割り当てます。作業が完了したら、このカメラをゲームに統合します。

スクリプトの動作原理を分解して説明します。

{{% notice note %}}
スクリプトの全文は[記事の末尾](#全スクリプト)で確認できます。
{{% /notice %}}

以下にスクリプトの開始部分を示します。

```gdscript
extends Camera2D

@export var move_speed = 30 # camera position lerp speed
@export var zoom_speed = 3.0  # camera zoom lerp speed
@export var min_zoom = 5.0  # camera won't zoom closer than this
@export var max_zoom = 0.5  # camera won't zoom farther than this
@export var margin = Vector2(400, 200)  # include some buffer area around targets

var targets = []  # Array of targets to be tracked.

@onready var screen_size = get_viewport_rect().size
```

これらの設定によりカメラ動作を調整できるようになります。すべてのカメラ変更を `lerp()` で補間処理するため、移動速度やズーム速度を低く設定した場合、突然の変化に対してカメラが「追いつく」まで若干の遅延が生じます。

最大・最小ズーム値は、ゲーム中のオブジェクトの大きさや、どこまで接近または遠ざけたいかによっても変わります。適宜調整します。

プロパティ`margin`を使用すると、ターゲット要素の周囲に余分なスペースが追加され、可視領域の端にぴったりと配置されないようになります。

最後に、ターゲット配列を取得し、ビューポートサイズを確認することで、適切なスケール計算ができるようになります。

```gdscript
func add_target(t):
    if not t in targets:
        targets.append(t)

func remove_target(t):
    if t in targets:
        targets.erase(t)
```

ターゲットの追加/削除については、2つの補助関数を用意しています。ゲームプレイ中にこれらを使用することで、追跡対象を変更できます（「プレイヤー3がゲームに参加しました！」）。また、同じターゲットを複数同時に追跡することは避けたいため、既に存在する場合は追加を拒否する仕組みになっています。

機能の大部分は `_process()` メソッドで実装されています。まず、カメラの移動処理から見ていきます。

```gdscript
func _process(delta):
    if !targets:
        return
    # Keep the camera centered between the targets
    var p = Vector2.ZERO
    for target in targets:
        p += target.position
    p /= targets.size()
    position = lerp(position, p, move_speed * delta)
```

ここでは、ターゲットの位置を繰り返し処理し、共通の中心点を見つけます。`lerp()`関数を使うことで、スムーズに移動させることができます。

次に、ズーム機能について説明します。

```gdscript
# Find the zoom that will contain all targets
var r = Rect2(position, Vector2.ONE)
for target in targets:
    r = r.expand(target.position)
r = r.grow_individual(margin.x, margin.y, margin.x, margin.y)
var z
if r.size.x > r.size.y * screen_size.aspect():
    z = 1 / clamp(r.size.x / screen_size.x, min_zoom, max_zoom)
else:
    z = 1 / clamp(r.size.y / screen_size.y, min_zoom, max_zoom)
zoom = lerp(zoom, Vector2.ONE * z, zoom_speed)
```

ここでの主要な機能は`Rect2`によるものです。すべてのターゲットを包含する長方形を見つける必要があり、これは`expand()`メソッドを使用することで取得できます。その後、この矩形に`margin`分の大きさを追加します。

以下の画面では、長方形が描画されている様子を確認できます（デモプロジェクトで「Tab」キーを押すとこの描画機能を有効にできます）。

![alt](/godot_recipes/4.x/img/multi_cam_02.gif)

次に、矩形が画面のアスペクト比に対して横長か縦長かに応じて適切なスケーリング係数を求め、事前に定義した最大値/最小値の範囲内で正規化します。

## 全スクリプト

```gdscript
extends Camera2D

@export var move_speed = 30 # camera position lerp speed
@export var zoom_speed = 3.0  # camera zoom lerp speed
@export var min_zoom = 5.0  # camera won't zoom closer than this
@export var max_zoom = 0.5  # camera won't zoom farther than this
@export var margin = Vector2(400, 200)  # include some buffer area around targets

var targets = []

@onready var screen_size = get_viewport_rect().size

func _process(delta):
    if !targets:
        return

    # Keep the camera centered among all targets
    var p = Vector2.ZERO
    for target in targets:
        p += target.position
    p /= targets.size()
    position = lerp(position, p, move_speed * delta)

    # Find the zoom that will contain all targets
    var r = Rect2(position, Vector2.ONE)
    for target in targets:
        r = r.expand(target.position)
    r = r.grow_individual(margin.x, margin.y, margin.x, margin.y)
    var z
    if r.size.x > r.size.y * screen_size.aspect():
        z = 1 / clamp(r.size.x / screen_size.x, max_zoom, min_zoom)
    else:
        z = 1 / clamp(r.size.y / screen_size.y, max_zoom, min_zoom)
    zoom = lerp(zoom, Vector2.ONE * z, zoom_speed * delta)

    # For debug
    get_parent().draw_cam_rect(r)

func add_target(t):
    if not t in targets:
        targets.append(t)

func remove_target(t):
    if t in targets:
        targets.remove(t)
```

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/multitarget_camera](https://github.com/godotrecipes/multitarget_camera)
