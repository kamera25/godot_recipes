---
title: "Path2D と PathFollow2D"
draft: false
ghcommentid: 94
---

## {{< gd-icon Path2D >}}`Path2D と {{< gd-icon PathFollow2D >}} PathFollow2D`

*パス* とは 2D 空間における点の連続であり、{{< gd-icon Curve2D >}}`Curve2D` リソースによって定義されます。{{< gd-icon Path2D >}}`Path2D` ノードを使用すると、2D 空間でパスを配置できるほか、エディター内で新規パスを作成することもできます。

パスには様々な用途があります。敵モブが辿る巡回経路、アニメーション効果のための曲がりくねった道、移動プラットフォームの動作パターンなどを作成できます。

### `Curve2D`について【{{<  gd-icon Curve2D >}}】

パスのデータはこのリソースオブジェクトに保持されています。これには曲線の数学的表現が含まれており、そのデータと対話するための方法がいくつか提供されています。[APIドキュメント](https://docs.godotengine.org/ja/stable/classes/class_curve2d.html)に詳細が記載されていますが、ここでは特に役立つメソッドをいくつか紹介します。

*  `add_point()` / `remove_point()` / `clear_points()`

コード内でパスのポイントを操作する必要がある場合、これらの関数が役立ちます。

* `get_closest_point()`

このメソッドは、空間内の任意の点に最も近い経路上のポイントを返します。

*  `get_closest_offset()`

上記と異なる点として、この方法は指定された地点に最も近い経路上の位置を返します。ただし、この位置は経路上に定義された2つの特定のポイント間に位置する場合もあります。

* `tesselate()`

このメソッドは曲線上の点のリストを返します。これらの点は、曲率が高い経路部分に密集して配置されます。

## 経路の描画方法

{{< gd-icon Path2D >}} `Path2D` ノードを選択すると、アイコンバーに以下の新しいアイコンが表示されます。

![alt](/godot_recipes/3.x/img/kyn_path2d_01.png)

アイコンのいずれかを選択すると、マウスカーソルの動作が変更されます。ホバーするとそれぞれの名前を確認できます。

※ **ポイント選択ツール** - クリック＆ドラッグで既存のポイントを移動できます。
※ **コントロール点設定ツール** - ポイントに調整ハンドルを追加し、カーブ形状を調整できます（詳細は後述）。
※ **新規ポイント追加ツール** - 空白部分をクリックすることで新しいポイントを作成します。
※ **ポイント削除ツール** - クリックすると指定したポイントを削除します。
※ **曲線閉じ処理ツール** - 曲線の最終ポイントと最初のポイントを接続してループ状に仕上げます。

「ポイントを追加」を選択し、エディターウィンドウ内でクリックしてポイントを作成します。

![alt](/godot_recipes/3.x/img/kyn_path2d_02.png)

より滑らかで丸みを帯びた曲線を作成するには、「制御点を選択」を選択し、カーブ上の任意の点をドラッグして「内向き」「外向き」ハンドルを調整してください。

![alt](/godot_recipes/3.x/img/kyn_path2d_03.png)

## ターゲットの追跡中

単体では{{< gd-icon Path2D >}} `Path2D`ノードにはほとんど機能がありません。経路に沿って移動するには、{{< gd-icon PathFollow2D >}} `PathFollow2D` ノードも併せて使用が必要です。これは親の {{< gd-icon Path2D >}} `Path2D` に沿って移動する役割を持つノードです。

ノードプロパティを調整：

* `offset` と `unit_offset` - これらのプロパティは経路上の起点からの距離を表します。`offset` はピクセル単位で測定され、`unit_offset` はパーセント値で示されます（例：`0` が開始位置、`.5` が中間点、`1.0` が終点）

* `rotate` - このブール値により、ノードが経路に沿って移動する際に回転するかどうかを制御します。

* `loop` - このブール値が `true` の場合、パス長を超えるオフセットは「巻き戻されます」。繰り返し可能な経路が必要な場合に使用してください。

例えば、この平面が経路に沿って移動する様子を考えてみます（経路を可視化するには、*デバッグ > ナビゲート表示* を設定してください。

![alt](/godot_recipes/3.x/img/kyn_path2d_04.gif)

これは、平面ノードを {{< gd-icon Sprite2D >}} スプライトとして {{< gd-icon PathFollow2D >}} 経路追従オブジェクトの子要素にし、以下の内容を `_process()` 関数に追加することで実現しています。

```gdscript
func _process(delta):
    $Path2D/PathFollow2D.offset += 250 * delta
```

"offset"を増やすと、ノードが経路に沿って移動します。

注意: {{< gd-icon PathFollow2D >}}`PathFollow2D` ノードの *回転* プロパティ により、パスに沿って移動する際、ノード自体とその子ノードが常に経路に沿った方向に向くように維持されます。

## 例

### 経路の探索

以下の例を[AI：場面に基づく操縦](/godot_recipes/4.x/ja/ai/context_map/)レシピからご覧ください。

![alt](/godot_recipes/3.x/img/ai_context_10.gif)

この例では、AIエージェントは壁や他のエージェントを回避するだけでなく、正しい進行方向に沿って移動を続けようとします。軌道上には以下の[{{< gd-icon Path2D >}} `Path2D`]が描画されており、エージェントはこれを参照して現在の進行方向を確認します。

```gdscript
func get_path_direction(pos):
    var offset = $Path2D.curve.get_closest_offset(pos)
    $Path2D/PathFollow2D.offset = offset
    return $Path2D/PathFollow2D.transform.x
```

任意の経路上の位置において、{{< gd-icon PathFollow2D >}} `PathFollow2D` の前方方向 (`transform.x`) は常に経路に沿っています。

## 関連レシピ

- [Interpolated Camera](/godot_recipes/3.x/3d/interpolated_camera/)
- [Inputs: Introduction](/godot_recipes/3.x/input/input_intro/)
- [CharacterBody3D: Movement](/godot_recipes/3.x/3d/kinematic_body/) -->

<!-- #### Videoが気に入ったら？ -->

{{< youtube Lx2d5cgMj5U >}} -->