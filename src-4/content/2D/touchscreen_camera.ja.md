---
title: "タッチスクリーンカメラ"
weight: 12
draft: false
ghcommentid: 31
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

モバイルゲームには、タッチ操作対応の2Dカメラが必要です。

## 解決策

このレシピでは、複数のタッチ操作に対応した汎用2Dカメラを作成します。

* ドラッグで画面移動
* 2本指でピンチイン/アウトすると拡大縮小できます

### 設定手順

当社のカメラは内蔵ノードを拡張するため、新しいシーンに {{< gd-icon Camera2D >}}`Camera2D` を追加し、「TouchCamera」と名前を付けてください。保存後、スクリプトをアタッチします。

以下に必要となる変数を示します。

```gdscript
extends Camera2D

@export var target: NodePath

# Optional: export these properties for convenient editing.
var target_return_enabled = true
var target_return_rate = 0.02
var min_zoom = 0.5
var max_zoom = 2
var zoom_sensitivity = 10
var zoom_speed = 0.05

var events = {}
var last_drag_distance = 0
```

もし「ターゲット」が設定されている場合、カメラはその対象物を追いかける、または自動的にその位置に戻ることができます。その他のカメラ動作を制御するプロパティ：

- `target_return_enabled` - これを `true` に設定すると、ドラッグ後にカメラは自動的にターゲット位置に復帰します。
- `target_return_rate` - カメラがターゲット位置に戻る速度を調整します。
- `min_zoom` / `max_zoom` - ズームの最小/最大倍率制限値を設定します。
- `zoom_sensitivity` - ピンチ操作によるズーム感度を設定します - これは「ズーム動作」が開始されるために必要なピクセル単位の動きを指定します。
- `zoom_speed` - ズーム操作をより滑らかに実行するためのパラメータです。

以下のプロパティも `export` することで、インスペクターで調整できるようになります。

その他の変数はカメラの状態を追跡します。`events` は辞書型変数で、アクティブなタッチスクリーンイベントを保持し、各イベントは`index`をキーとして管理されます。`last_drag_distance`は、ピンチジェスチャにおける2つのドラッグイベント間の移動距離を記録します。

`_process()`関数内では、ターゲットへの移動処理を行います（ターゲットリターンが有効で、タッチイベントが未発生の場合）。

```gdscript
func _process(delta):
    if target and target_return_enabled and events.size() == 0:
        position = lerp(position, get_node(target).position, target_return_rate)
```

これにより、カメラを自由に移動させることができ、タッチを離すと自動的にプレイヤー視点に戻ります。

これでジェスチャーの追加準備が整いました。まずは「パン」操作から始めてください。

### パン

※このジェスチャーは、プロジェクト設定の「入力デバイス」→「ポインティング」で「マウスからタッチをエミュレート」を有効化することでパソコンでテストできます。

マウスイベントやキーボードイベントと同様、タッチイベントも`InputEvent`を継承し、同じ入力優先度に従います。処理には`_unhandled_input()`関数を使用するため、他のノード（例：{{< gd-icon Control >}}`Control`ノード）が先にイベントを処理できます。

```gdscript
func _unhandled_input(event):
    if event is InputEventScreenTouch:
        if event.pressed:
            events[event.index] = event
        else:
            events.erase(event.index)
```

まず、タッチイベント（`InputEventScreenTouch`）をチェックしています。このイベントを`events`辞書に追加してください。イベントの`index`プロパティが辞書のキーとして使います。また、このイベントが「押されていない」（つまりタッチが終了した場合）には削除します。

次は、タッチ動作の後に発生するドラッグ操作について処理が必要です。

```gdscript
    if event is InputEventScreenDrag:
        events[event.index] = event
        if events.size() == 1:
            position += event.relative.rotated(rotation) * zoom.x
```

ドラッグイベントが発生した場合も同様に辞書に追加してください。なお、この場合は既存の値を更新する形になります - 例えば最初のタッチイベント時点で既に存在していたインデックス`0`が、今回はドラッグイベントとして再登録されることになります。

単一のイベントのみがアクティブな場合、これは1本指でのドラッグ操作であるため、カメラの位置をそれに応じて調整できます。ただし、移動量を現在の`zoom`値に基づいてスケーリングする必要がある点に注意してください。そうしないと、ズームイン時にドラッグの動きが不自然に大きく、ズームアウト時には小さくなってしまいます。同様に、カメラが回転している場合、その回転も相対的な値に適用が必要です。これにより、ドラッグ操作が適切な方向にカメラを動かすようになります。

モバイルデバイスから直接キャプチャした例をご紹介します。黄色の円がタッチ位置を示しています。

<video controls src="/godot_recipes/4.x/img/touch_camera_01.webm"></video>

### ズーム機能

{{% notice note %}}
このジェスチャーはコンピュータではテストできません。2回のタッチ操作が必要ですが、マウスではこの動作をエミュレートできないためです。
{{% /notice %}}

「ピンチ」操作でカメラのズーム機能が作動します。これは2回連続のドラッグイベントを検知した場合に発生します。ドラッグ方向が同じ方向に移動する場合はズームイン、反対方向に移動する場合はズームアウトします。

```gdscript
if event is InputEventScreenDrag:
    events[event.index] = event
    if events.size() == 1:
        position += event.relative.rotated(rotation) * zoom.x

    elif events.size() == 2:
        var drag_distance = events[0].position.distance_to(events[1].position)
        if abs(drag_distance - last_drag_distance) > zoom_sensitivity:
            var new_zoom = (1 + zoom_speed) if drag_distance < last_drag_distance else (1 - zoom_speed)
            new_zoom = clamp(zoom.x * new_zoom, min_zoom, max_zoom)
            zoom = Vector2.ONE * new_zoom
            last_drag_distance = drag_distance
```

アクティブなドラッグイベントが2件ある場合の処理を記述
"drag_distance" は各イベント間の距離を示し、前回計測した距離と比較して増減を確認可能
"zoom_speed" は倍率係数で、ズームイン時は「1.05」倍、アウト時は「0.95」倍に調整する
計算結果が指定された範囲を超えないように制限を施し、新しい "zoom" 値を設定
最後に次回イベント用に "last_drag_distance" を更新

<video controls src="/godot_recipes/4.x/img/touch_camera_02.webm"></video>

## まとめ

これを底本にして、ニーズに合わせて活用できます。以下に、試せる提案をいくつかご紹介します。

* ズーム動作を滑らかにするには`lerp()`を使いましょう。
* ズームは自動的にデフォルトレベルに戻ります。
* ダブルタップでリセットできます。
* さらにジェスチャーを追加可能 - 例：3本指操作など。

完全な参考として、以下にフルバージョンの「TouchCamera.gd」スクリプトを記載します。

```gdscript
extends Camera2D

@export var target: NodePath

var target_return_enabled = true
var target_return_rate = 0.02
var min_zoom = 0.5
var max_zoom = 2
var zoom_sensitivity = 10
var zoom_speed = 0.05

var events = {}
var last_drag_distance = 0


func _process(delta):
    if target and target_return_enabled and events.size() == 0:
        position = lerp(position, get_node(target).position, target_return_rate)


func _unhandled_input(event):
    if event is InputEventScreenTouch:
        if event.pressed:
            events[event.index] = event
        else:
            events.erase(event.index)

    if event is InputEventScreenDrag:
        events[event.index] = event
        if events.size() == 1:
            position += event.relative.rotated(rotation) * zoom.x
        elif events.size() == 2:
            var drag_distance = events[0].position.distance_to(events[1].position)
            if abs(drag_distance - last_drag_distance) > zoom_sensitivity:
                var new_zoom = (1 + zoom_speed) if drag_distance < last_drag_distance else (1 - zoom_speed)
                new_zoom = clamp(zoom.x * new_zoom, min_zoom, max_zoom)
                zoom = Vector2.ONE * new_zoom
                last_drag_distance = drag_distance
```

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。 [2d_touch_camera.zip](/godot_recipes/4.x/ja/files/2d_touch_camera.zip)
{{% /notice %}} -->

## 関連レシピ

- [入力操作: Input Actions](/godot_recipes/4.x/ja/input/input_actions/)
- [マウスドラッグでのユニットの選択](/godot_recipes/4.x/ja/input/multi_unit_select/)

#### この動画が気に入ったら？

{{< youtube jRMhJSwd-Xw >}}
