---
title: "補間カメラ"
weight: 2
draft: false
ghcommentid: 88
---
## 課題

対象物を滑らかに追従できる3Dカメラが必要となります（補間機能が必要となります）。

## 解決策

{{% notice info %}}
Godotに標準搭載されている`InterpolatedCamera`ノードは非推奨となっており、Godot 4.0リリース時に廃止される予定です。
{{% /notice %}}

以下のスクリプトをシーン内の{{< gd-icon Camera3D >}}`Camera3D`ノードにアタッチします。3つの`export`プロパティにより、以下のように選択できます。

* `lerp_speed` - カメラの移動速度。値を小さくすると「動きが鈍い」印象になります
* `target` - カメラのターゲットノードを選択します
* `offset` - ターゲットに対するカメラの相対位置設定です

以下に、実際にカメラを使用した例をご紹介します。

```gdscript
extends Camera3D

@export var lerp_speed = 3.0
@export var target: Node3D
@export var offset = Vector3.ZERO

func _physics_process(delta):
    if !target:
        return

    var target_xform = target.global_transform.translated_local(offset)
    global_transform = global_transform.interpolate_with(target_xform, lerp_speed * delta)

    look_at(target.global_transform.origin, target.transform.basis.y)
```

`_physics_process()`関数内では、カメラの位置を`target`の位置（と、`offset`を加算した値）に補間します。

### 使用例

* `lerp_speed`: 3.0
* `offset`: (0, 7, 5)


<video width="500" controls src="/godot_recipes/4.x/img/3d_sphere_car_07.webm"></video>