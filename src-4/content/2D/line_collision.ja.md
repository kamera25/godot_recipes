---
title: "Line2D Collision"
weight: 12
draft: false
---

## 問題文

衝突検出を `{{<  gd-icon Line2D >}}Line2D` に対して行いたいとのことですね。

## 解決策

### ノード設定

以下のノードをシーンに追加し、必要に応じてラインを描いてください：

```
{{< gd-icon Line2D >}} Line2D
    {{< gd-icon StaticBody2D >}} StaticBody2D
```

まだボディに衝突形状を追加しないでください！

```markdown
{{% notice note %}}
衝突ではなく線との重複を検出したい場合は、代わりに {{< gd-icon Area2D >}}`Area2D` を使用することも可能です。
{{% /notice %}}

次に、ボディに衝突形状を追加する必要があります。以下の2つのオプションがあります：

### オプション 1：{{< gd-icon SegmentShape2D >}} `SegmentShape2D`の使用

```markdown
{{< gd-icon SegmentShape2D >}}`SegmentShape2D` は線分衝突形状です。この手法の目的は、直線上の各点ペアに対して個別のセグメント衝突を作成することです。

```gdscript
extends Line2D

func _ready():
    for i in points.size() - 1:
        var new_shape = CollisionShape2D.new()
        $StaticBody2D.add_child(new_shape)
        var segment = SegmentShape2D.new()
        segment.a = points[i]
        segment.b = points[i + 1]
        new_shape.shape = segment
```

### オプション2：`{{< gd-icon RectangleShape2D >}}`RectangleShape2D`を使用する場合

: SegmentShape2D`セグメント形状2Dは幅成分を持たないため、線の衝突判定に厚みが必要な場合には、代わりに矩形の衝突判定を使用することをお勧めします。

```gdscript
extends Line2D

func _ready():
    for i in points.size() - 1:
        var new_shape = CollisionShape2D.new()
        $StaticBody2D.add_child(new_shape)
        var rect = RectangleShape2D.new()
        new_shape.position = (points[i] + points[i + 1]) / 2
        new_shape.rotation = points[i].direction_to(points[i + 1]).angle()
        var length = points[i].distance_to(points[i + 1])
        rect.extents = Vector2(length / 2, width / 2)
        new_shape.shape = rect
```

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます：[https://github.com/godotrecipes/line2d_collision](https://github.com/godotrecipes/line2d_collision)
