---
title: "顶部到底部摩擦力"
weight: 3
draft: true
---

## 課題

トップダウン視点で操作するキャラクターに摩擦や加速度を追加し、よりスムーズな操作性を実現したいという。

## 解決策

```gdscript
extends CharacterBody2D

@export var speed = 200
@export var friction = 0.01
@export var acceleration = 0.1

var velocity = Vector2()

func get_input():
    var input = Vector2()
    if Input.is_action_pressed('right'):
        input.x += 1
    if Input.is_action_pressed('left'):
        input.x -= 1
    if Input.is_action_pressed('down'):
        input.y += 1
    if Input.is_action_pressed('up'):
        input.y -= 1
    return input

func _physics_process(delta):
    var direction = get_input()
    if direction.length() > 0:
        velocity = lerp(velocity, direction.normalized() * speed, acceleration)
    else:
        velocity = lerp(velocity, Vector2.ZERO, friction)
    velocity = move_and_slide(velocity)
```