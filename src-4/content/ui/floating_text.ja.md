---
title: "戦闘テキストを浮かせたい"
weight: 12
draft: false
---

## 課題

ダメージを受けたとき、浮かせながら数字を表示させたい。

![alt](/godot_recipes/4.x/img/fct_demo.gif)

## 解決策

この問題に取り組む方法はいくつかあります。例えば、ビットマップフォントを使用し、各数字をその構成桁から画像として生成した上で、`{{< gd-icon Sprite2D >}}` `Sprite2D`ノードを使って表示・移動させるといった手法が考えられます。

ただし、このレシピでは `{{< gd-icon Label >}}`Label` ノード（名前は「FCT」）を使用します。この方法であれば、フォントの変更が柔軟に行えるだけでなく、数字を文字列として表示するのも容易になります - さらには状況に応じて「miss」などの他のメッセージを表示することもできます。

この例では、"Xolonium.ttf" フォントを使用し、文字サイズを `28` ポイントに、アウトラインの色を黒、幅を `4` ピクセルに設定しています。

ラベルにスクリプトを追加します。

```gdscript
extends Label

func show_value(value, travel, duration, spread, crit=false):
```

浮動テキストを出現させる際に、この関数を呼び出してパラメータを設定します。

- `value` - 表示する数値（または文字列）
- `travel` - 移動方向を表す `Vector2` オブジェクト
- `duration` - テキストが表示される時間の長さ
- `spread` - この角度範囲内でランダムに動きが拡散される
- `crit` - `true` の場合、ダメージが「クリティカルヒット」であることを意味するフラグ

以下にこの関数の機能を説明します。

```gdscript
    text = value
    var movement = travel.rotated(rand_range(-spread/2, spread/2))
    rect_pivot_offset = rect_size / 2
```

まず、指定された値を設定し、与えられたスプレッド範囲（例：±90度）に基づいて移動をランダム化します。スケーリングもアニメーション化する可能性があるため、制御点の中心からスケールが開始されるよう `rect_pivot_offset` を中央に設定します。

```gdscript
    $Tween.interpolate_property(self, "rect_position",
            rect_position, rect_position + movement,
            duration, Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
    $Tween.interpolate_property(self, "modulate:a",
            1.0, 0.0, duration,
            Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
```

次に、補間する2つのプロパティを設定します。移動用の`position`と、表示制御用の`modulate.a`です。

```gdscript
    if crit:
        modulate = Color(1, 0, 0)
        $Tween.interpolate_property(self, "rect_scale",
            rect_scale*2, rect_scale,
            0.4, Tween.TRANS_BACK, Tween.EASE_IN)
```

クリティカルヒットの場合、色も変更してスケールアニメーションを追加し、より印象的な演出にします。注：ここでは便宜的に赤色をハードコードしていますが、本来は設定可能な値とすべきです。

```gdscript
    $Tween.start()
    yield($Tween, "tween_all_completed")
    queue_free()
```

最後に、{{< gd-icon Tween >}}`Tween` を開始し、処理が完了するまで待機した後、ラベルを削除します。

### フロートテキストマネージャー

次に、浮遊テキストの表示位置を管理し生成するための小さなノードを作成します。このノードは、浮動テキストエフェクトを表示させたいゲームエンティティにアタッチされます。

これは `Node2D` クラスのノードで「FCTManager」という名前です。このノードには以下のスクリプトが含まれています。

```gdscript
extends Node2D

var FCT = preload("res://FCT.tscn")

export var travel = Vector2(0, -80)
export var duration = 2
export var spread = PI/2

func show_value(value, crit=false):
    var fct = FCT.instance()
    add_child(fct)
    fct.show_value(str(value), travel, duration, spread, crit)
```

以下の箇所では、設定内容をインスペクターに表示して簡単に変更できます。ここで定義されている`show_value()`メソッドは、フローティングラベルを生成し、そのプロパティを設定します。

ゲーム内ユニットでは、このノードのインスタンスを作成して、テキストを表示させたい任意の位置に配置します。その後、ユニットの `take_damage()` メソッドに以下のようなコードを追加します。

```gdscript
$FCTManager.show_value(dmg, crit)
```

## まとめ

【最適化】多数の敵や弾が出現する場合、テキスト表示オブジェクトの頻繁な生成と破棄によりパフォーマンスが低下する可能性があります。この場合は、マネージャ内で固定数のテキストオブジェクトを生成し、アニメーション終了時に破棄するのではなく、表示／非表示を切り替える方法が有効です。


{{% notice note %}}
本デモで使用しているアートワークは[ルイス・ズノ氏](https://www.patreon.com/ansimuz)による作品です。
{{% /notice %}}

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

以下からプロジェクトのサンプルコードをダウンロードできます。[https://github.com/godotrecipes/floating_combat_text](https://github.com/godotrecipes/floating_combat_text)

![alt](/godot_recipes/4.x/img/fct_demo.png)

## 関連レシピ

[UI: ラベル](/godot_recipes/.x/ui/labels/)
[UI: ユニットHPバー](/godot_recipes/3.x/ui/unit_healthbar/) -->
