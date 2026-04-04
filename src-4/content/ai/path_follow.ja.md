---
title: "パスを追従する"
weight: 2
draft: false
ghcommentid: 72
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

以下のような事前に定義された経路を移動するキャラクターが必要です。警備員が巡回する場面や、車両が道路を走るシーンなど。

## 解決策

この問題に対処する方法は複数あります。本ソリューションでは、エディター内でパスを描画するための便利な方法として、Godotの{{< gd-icon Path2D >}}`Path2D`ノード（3Dの場合は{{< gd-icon Path3D >}} `Path`）を使用します。

以下の方法ができます。メインシーン、マップ、またはその他適切な場所に{{< gd-icon Path2D >}}`Path2D`を子要素として追加できます。ただし、巡回エンティティの子要素に設定しないようご注意ください - そうすると経路がプレイヤーと一緒に移動してしまいます！

### 経路の描画

{{< gd-icon Path2D >}}`Path2D`ノードを追加すると、ビューポート上部に新しいボタンが表示されます。

![alt](/godot_recipes/3.x/img/path2d_buttons.png)

「ポイント追加」ボタンを選択してクリックし、追加を開始します。閉じた曲線を作成したい場合は、「曲線を閉じる」ボタンをクリックすると最後の点が最初の点に接続されます。

「制御点」モードを使用して、線の「曲線度」を調整できます。

### 経路に沿った移動

以下のタグを使用して経路に沿って自動移動させることができます。{{< gd-icon PathFollow2D >}}`PathFollow2D`。ただし、キネマティックボディを使用している場合、この方法は衝突判定に問題を引き起こす可能性があります。これはボディの移動メソッドを利用していないためです。このため、代わりに経路上の各点を「目標」として設定し、ボディがその方向へ移動するようにします。

```gdscript
extends CharacterBody2D

var move_speed = 100
@export var patrol_path: NodePath
var patrol_points
var patrol_index = 0
var velocity = Vector2.ZERO

func _ready():
    if patrol_path:
        patrol_points = get_node(patrol_path).curve.get_baked_points()
```

`patrol_path`をエクスポートすることで、インスペクター内で直接パスノードを割り当てることができます。その後、そのノードが割り当てられていれば、`_ready()`関数内でラインを構成するポイント情報を取得可能です。

次のステップとして、現在パス上で選択されている点を移動先として使用できます。十分に近づけると、曲線の次のポイントに移動し、`wrapi()` 関数を使用して終点に到達したら最初のポイントに戻るループ処理を行います。

```gdscript
func _physics_process():
    if !patrol_path:
        return
    var target = patrol_points[patrol_index]
    if position.distance_to(target) < 1:
        patrol_index = wrapi(patrol_index + 1, 0, patrol_points.size())
        target = patrol_points[patrol_index]
    velocity = (target - position).normalized() * move_speed
    velocity = move_and_slide(velocity)
```

## 関連レシピ

