---
title: "オブジェクトヘルスバー"
weight: 10
draft: false
---

## 課題

移動しても回転せずに2Dユニットに追従するヘルスバーが欲しいとのこと。

## 解決策

ノードとして `TextureProgressBar` を使用してください。Godot 4ではプロパティやテクスチャの扱い方は基本的に同様ですが、構造をより明確にするため `@onready` と `@export` を使用しています。

### ノード設定

from gdscript import *

class HealthDisplay(Node2D):
    def _ready():
        # 1. ヘルス表示用の `Node2D` を作成
        self.add_subnode(TextureProgressBar())

        # 2. 進捗バーを追加
        progress_bar = self.get_node("TextureProgressBar")

        # 3. 各色のテクスチャを設定
        progress_bar.set_property("Textures > Progress", [green_texture, yellow_texture, red_texture])


### スクリプト (`health_display.gd`)

```gdscript
extends Node2D

var bar_red = preload("res://assets/barHorizontal_red.png")
var bar_green = preload("res://assets/barHorizontal_green.png")
var bar_yellow = preload("res://assets/barHorizontal_yellow.png")

@onready var healthbar = $TextureProgressBar

func _ready():
    hide()
    # Check if parent has health properties
    var parent = get_parent()
    if parent and "max_health" in parent:
        healthbar.max_value = parent.max_health

func _process(_delta):
    # Keep the healthbar horizontal even if the unit rotates
    global_rotation = 0

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

> ［重要］
> ■ **Godot 3 から 4 への移行ポイントまとめ**:
> - 旧: `TextureProgress` → 新: `TextureProgressBar`
> - `parent` オブジェクトのプロパティを確認するには `in` 演算子を使用する（例: `"max_health" in parent`）
> - 常に `_process` 内で `global_rotation = 0` を指定し、UI がワールド空間で正しく向きを保つようにする
