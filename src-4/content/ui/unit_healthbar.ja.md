---
title: "オブジェクトヘルスバー"
weight: 10
draft: false
ghcommentid: 60
---

## 課題

ゲーム中のユニットに、移動に合わせて追従するヘルスバーを表示させたいということですね。

[画像リンク](/godot_recipes/3.x/img/unit_healthbar_preview.png)

## 解決策

プログレスバーの表示には、`TextureProgress`ノードを使用できます（{{< gd-icon TextureProgressBar >}}）。これは、通常の`ProgressBar`ノードと似ていますが、プログレスバー自体にテクスチャを適用できる点が異なります。バーの長さは健康状態を示しますが、さらにテクスチャの色も変更可能です。この機能を活用するために、3種類の異なる配色のバーを使用してみましょう。

![alt](/godot_recipes/3.x/img/barHorizontal_green.png)
![alt](/godot_recipes/3.x/img/barHorizontal_yellow.png)
![alt](/godot_recipes/3.x/img/barHorizontal_red.png)

このバーをゲームの任意のユニットに追加できるようにするため、これを独立したシーンとして作成します。まず `{{<  gd-icon Node2D>}}`Node2D` と `{{<  gd-icon TextureProgressBar >}}`TextureProgress` 子ノードで始めましょう。ルートノードにスクリプトを追加します。

<img src="/godot_recipes/3.x/img/unit_healthbar_nodes.png">

緑色のバーをプロパティ「テクスチャ/進捗」(_Textures/Progress_)内にドラッグし、その値を`100`に設定してください。バーが中心位置になり、原点よりも上部にくるように調整します。

![alt](/godot_recipes/3.x/img/unit_healthbar_layout.png)

```gdscript
extends Node2D

var bar_red = preload("res://assets/barHorizontal_red.png")
var bar_green = preload("res://assets/barHorizontal_green.png")
var bar_yellow = preload("res://assets/barHorizontal_yellow.png")

onready var healthbar = $HealthBar
```

スクリプトはまず3本のカラーバーを読み込みます。これらは体力が低下するにつれて変化します。また、プログレスバーへの参照も保持します。

```gdscript
func _ready():
    hide()
    if get_parent() and get_parent().get("max_health"):
        healthbar.max_value = get_parent().max_health
```

class HealthDisplay:
    def __init__(self, unit):
        self.unit = unit
        if hasattr(unit, "max_health"):
            self.max_value = getattr(unit, "max_health")  # デフォルト値は100
        else:
            self.max_value = 100  # 最大ヘルス値が明示されていない場合はデフォルト値を使用

        self.bar_hidden = True

    def update_status_bar(self):
        if self.unit.is_alive():
            return ""

        health_ratio = self.unit.current_health / self.max_value
        width = int(health_ratio * 100)  # ヘルス比率をバー幅に変換

        if not self.bar_hidden and width < 100:
            self.render_health_bar()

    def render_health_bar(self):
        # 健康ゲージのレンダリング処理を実装する（例：コンソールに表示）
        print("Health Bar: [=======>]", end="")


```gdscript
func _process(delta):
    global_rotation = 0
```

この設定により、バーの回転を防止します。常に接続されているユニットの上に固定された状態で表示されます。

```gdscript
func update_healthbar(value):
    healthbar.texture_progress = bar_green
    if value < healthbar.max_value * 0.7:
        healthbar.texture_progress = bar_yellow
    if value < healthbar.max_value * 0.35:
        healthbar.texture_progress = bar_red
    if value < healthbar.max_value:
        show()
    healthbar.value = value
```

最終的に、ユニットのヘルス値が変化するたびに呼び出せる関数が完成しました。この関数はバーの表示値を更新し、残りの割合に応じて適切なテクスチャを適用します。

このユニットに取り付けると、バーが大きすぎるように見える場合があります。インスタンス化された `HealthDisplay` の _Scale_ プロパティを調整して、ユニットのサイズに合わせて表示を変更できます。

以下に、このシステムを実際に使用した事例をご紹介します。この例のプロジェクトは以下のリンクからダウンロード可能です。

<video controls src="/godot_recipes/3.x/img/tower_def_demo.webm"></video>

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます：[tower_defense_demo.zip](/godot_recipes/3.x/files/tower_confeito_demonstrativo.zip)
{{% /notice %}} -->