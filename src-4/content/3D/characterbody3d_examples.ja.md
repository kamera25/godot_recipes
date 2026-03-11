---
title: "CharacterBody3D: Movement"
weight: 4
draft: false
---

## 課題

プレイヤー操作可能な3Dキャラクターボディが必要です。

## 解決策

このレシピでは、こちらの可愛らしいタンクモデルを使用します。

![alt](/godot_recipes/4.x/img/3d_kinematic_01.png)

このモデルは[Itch.io](https://gtibo.itch.io/mini-tank)で入手できます。他のお好きなモデルを使用しても構いません。ここでは戦車固有の機能は特に実装しません。

このアセットの場合、ダウンロードには OBJファイルが含まれており、シーンとしてインポートした方が作業が効率的になります：

画像: /godot_recipes/4.x/img/obj_as_scene.png

モデルをシーンに追加することは可能ですが、以下の追加ノードが必要です：

![alt](/godot_recipes/4.x/img/mini_tank_nodes.png)

衝突形状については、戦車の履帯に合わせて整列・サイズ調整した `BoxShape` を使用します。`CamPos` は、後続カメラを配置するための {{< gd-icon Position3D >}}`Position3D` 変数です。タンクの後方かつ上部に位置するように配置し、下向きに角度が付けられています。

また、個別の {{< gd-icon MeshInstance3D >}}`MeshInstance` ノードを **Y** 軸を中心に `180` 度回転させました。これは元々 **+Z** 方向を向いてモデル化されていたためですが、Godot では **-Z** が前方方向となるため、戦車が逆向きに見えるようにはしたくないからです。

スクリプトを追加する前に、「プロジェクト設定」を開き、「入力マップ」タブで以下の入力を追加してください：

入力操作 | キー
:------------|:---
前進 | **W**
後退 | **S**
右移動 | **D**
左移動 | **A**

それでは、必要な変数から始めつつ、スクリプトを追加しましょう：

```gdscript
extends CharacterBody3D

@export var speed = 4.0
@export var turn_speed = 0.8
```

`speed` は戦車の移動速度（前進/後退）を、`rot_speed` は旋回速度をそれぞれ定義します。

{{% notice tip %}}
`@export` でプロパティを宣言しておけば、インスペクターで簡単に調整できるようになります。
{{% /notice %}}

```python
# 移動処理の実装例
def move_and_slide(self, dx, dy):
    if self.is_walking:
        self.position[0] += dx
        self.position[1] += dy
        # 移動中は速度をリセットしない

    else:
        # 静止時は速度を完全にリセット
        self.velocity = [0, 0]
```

この実装により、移動状態の判定が簡素化され、コードがより直感的になります。

```gdscript
func _physics_process(delta):
    velocity.y -= gravity * delta
    get_input(delta)
    move_and_slide()
```

このコードでは、重力による下向き加速度を現在の速度に加算し、ユーザー入力を取得し（詳細は後述）、`move_and_slide()` 関数を呼び出しています。

次に必要なのは `get_input()` 関数を定義することです。ここでは入力操作を処理して適用します。

```gdscript
func get_input(delta):
    var vy = velocity.y
    velocity = Vector3.ZERO
    var move = Input.get_axis("back", "forward")
    var turn = Input.get_axis("right", "left")
    velocity += -transform.basis.z * move * speed
    rotate_y(turn_speed * turn * delta)
    velocity.y = vy
```

```python
# 変数の初期化と基本的な計算処理を完了
```

このコードでは以下の操作を行っています：

1. **プレイヤー入力に基づく水平移動**：
   - 前方/後方方向への地面に沿った移動と、戦車中心軸周りの回転は、それぞれ別のベクトル（`vx`と`rotation`）で管理します。
   - `Y`方向の動きは重力のみの影響を受けるように設計しています。これは毎フレーム0にリセットすべきではないためです。そのため、一時的に`vy`変数にその値を保持し、水平移動用の新たな速度ベクトルを設定した後、最後にそれを追加しています。

```python
# 前方/後方移動にはキャラクターのローカル座標系の Z 軸を使用しています。
# これにより、身体の「ローカル」前方方向へ正しく移動します。

```gdscript
import panda3d.core as p3d

class MainNodePath(Spatial):
    def __init__(self, root_node_path):
        super().__init__()
        self.root_node_path = root_node_path

    # ... (その他の初期化コード) ...

    def update_transforms(self):
        for node in self.get_children():
            if isinstance(node, StaticBody3D):
                p3d.TransformNode("transform_node")
                    .set_translation(p3d.Vector3())
                    .set_rotation_axisangle(p3d.Vector3(), p3d.Vector3(), 0)
                    .set_scale(p3d.Vector3(0.5, 0.5, 0.5))

            elif isinstance(node, Camera3D):
                # 補間カメラの設定を適用
                pass
```

<video controls src="/godot_recipes/4.x/img/3d_kinematic_09.webm"></video>

## まとめ

これはあらゆる種類の運動学的キャラクターの動作基盤です。ここからジャンプ、射撃、AI挙動などを追加できます。このレシピを拡張した具体例については、関連するレシピを参照してください。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードをダウンロードする：[https://github.com/godotrecipes/characterbody3d_examples](https://github.jp/godotrecipes/characterbody3d_examples)

<!-- {{% notice note %}}
Download the project file here: [floating_text.zip](/godot_recipes/3.x/files/floating_text.zip)
{{% /notice %}} -->

## 関連レシピ

・[3D入門](/godot_recipes/4.x/ja/g101/3d/)
・[入力アクション](/godot_recipes/4.x/ja/input/input_actions/)

