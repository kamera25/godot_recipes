---
title: "Collision Layers and Masks"
weight: 3
draft: false
---

## Introduction

Collision layers and masks are essential for controlling which objects interact with each other in Godot 4.

### The System

- **Collision Layer**: Which layer(s) the object **lives on**.
- **Collision Mask**: Which layer(s) the object **scans for collisions**.

### Example Configuration

| Node | Layer | Mask | Interaction |
| :--- | :--- | :--- | :--- |
| **Player** | 1 | 2, 3 | Scans for Enemies and Coins |
| **Enemy** | 2 | 1 | Scans for the Player |
| **Coin** | 3 | (None) | Doesn't need to scan anything |

### Setting Names

In Godot 4, you can name your layers in **Project Settings > Layer Names > 2D Physics**. This makes it much easier to manage in the Inspector.

### Accessing via Code

In Godot 4, you can use `get_collision_layer_value(layer_number)` and `set_collision_layer_value(layer_number, value)` for easier bit manipulation.

```gdscript
# Enable layer 2
set_collision_layer_value(2, true)

# Check if masking layer 3
if get_collision_mask_value(3):
    print("Scanning layer 3")
```

> [!NOTE]
> **Godot 3 to 4 Migration Summarized**:
> - The inspector UI for layers has been improved.
> - New helper methods like `set_collision_layer_value()` replace the need for complex bitwise math (`1 << (layer - 1)`).
