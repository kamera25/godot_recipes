---
title: "Interpolated Camera"
weight: 2
draft: false
ghcommentid: 88
---
## 問題文

対象物を滑らかに追従できる3Dカメラが必要です（補間機能が必要）。

## 解決策

{{% notice info %}}
Godotに標準搭載されている`InterpolatedCamera`ノードは非推奨となっており、Godot 4.0リリース時に廃止される予定です。
{{% /notice %}}

以下のスクリプトをシーン内の`<gd-icon Camera3D>` `Camera3D`ノードに添付してください。3つの`export`プロパティにより、以下のように選択できます：

* `lerp_speed` - the camera's movement speed. Lower values result in a "lazier" camera.
* `target` - choose the camera's target node.
* `offset` - position of the camera relative to the target.

以下に、実際にカメラを使用した例をいくつかご紹介します。

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

```php
function _physics_process(){
    $this->interpolateCameraPositionWithTarget();
}
```

// 物理処理関数内でカメラの位置をターゲット位置（＋オフセット値）に補間しています

### 使用例

* `lerp_speed`: 3.0
* `offset`: (0, 7, 5)


<video width="500" controls src="/godot_recipes/4.x/img/3d_sphere_car_07.webm"></video>