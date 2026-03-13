---
title: "Object Healthbars"
weight: 10
draft: false
---

## Problem

You want a health bar that follows a 2D unit as it moves, without rotating with the unit.

## Solution

Use a `TextureProgressBar` node. In Godot 4, the properties and texture handling remain similar, but we use `@onready` and `@export` for better structure.

### Node Setup

1. Create a `Node2D` named `HealthDisplay`.
2. Add a `TextureProgressBar` as a child.
3. Assign your green, yellow, and red bar textures to the **Textures > Progress** property.

### Script (`health_display.gd`)

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

> [!NOTE]
> **Godot 3 to 4 Migration Summarized**:
> - `TextureProgress` -> `TextureProgressBar`.
> - Use the `in` operator to check for properties on the parent: `"max_health" in parent`.
> - Always use `global_rotation = 0` in `_process` to keep the UI oriented correctly in world space.
