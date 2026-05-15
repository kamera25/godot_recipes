---
title: "CharacterBody3Dの移動"
weight: 4
draft: false
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 今回のお題

プレイヤー操作可能な3Dキャラクターボディが必要となります。

## 作り方

このレシピでは、こちらの可愛らしいタンクモデルを使用します。

![alt](/godot_recipes/4.x/img/3d_kinematic_01.png)

このモデルは[Itch.io](https://gtibo.itch.io/mini-tank)で入手できます。他のお好きなモデルを使用しても構いません。ここでは戦車固有の機能は特に実装しません。

このアセットの場合、ダウンロードには OBJファイルが含まれており、シーンとしてインポートした方が作業が効率的になります。

![alt](/godot_recipes/4.x/img/obj_as_scene.png)

モデルをシーンに追加することはできますが、以下の追加ノードが必要となります。

![alt](/godot_recipes/4.x/img/mini_tank_nodes.png)

衝突判定形状については、戦車の履帯と位置・サイズを合わせた `BoxShape` を使用します。`CamPos` は、後続カメラを配置するための {{< gd-icon Marker3D >}}`Marker3D` です。戦車の後方かつ上部、やや下向きに配置されます。

また、個別の {{< gd-icon MeshInstance3D >}}`MeshInstance` ノードを **Y** 軸を中心に `180` 度回転させました。これは元々 **+Z** 方向を向いてモデル化されていたためですが、Godot では **-Z** が前方方向となるため、戦車が逆向きに見えるようにはしたくないからです。

スクリプトを追加する前に、「プロジェクト設定」を開き、「インプットマップ」タブで以下の入力を追加します。

入力操作 | キー
:------------|:---
前進 | **W**
後退 | **S**
右移動 | **D**
左移動 | **A**

それでは、必要な変数から始めつつ、スクリプトを追加します。

```gdscript
extends CharacterBody3D

@export var speed = 4.0
@export var turn_speed = 0.8
```

`speed` は戦車の移動速度（前進/後退）を、`rot_speed` は旋回速度をそれぞれ定義します。

{{% notice tip %}}
`@export` でプロパティを宣言しておけば、インスペクタで簡単に調整できるようになります。
{{% /notice %}}

`move_and_slide()`メソッドを使用することで、移動コードが非常に簡潔になります。

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

これをもう少し詳しく見ていきます。プレイヤー入力は水平方向の移動に影響を与えるべきです。地面に沿った前後移動と、戦車の中心周りの回転です。**Y軸方向**の移動は、重力の影響を受けるべきものであり、つまり毎フレーム`0`に設定すべきではありません。これが、新しい速度ベクトルを水平移動用に割り当てる間、その値を一時的に保持するために`vy`変数を使用している理由です。そして最後に、この値を新たに追加します。

前方/後方移動にはキャラクターの `transform.basis.z` を使用しています。
これにより、身体の「ローカル」前方方向へ正しく移動します。

「これが動作中の戦車です。テスト用シーンとして、地面には {{< gd-icon `StaticBody3D` >}} `StaticBody3D`、カメラには [補間付きカメラ](/godot_recipes/4.x/ja/3d/interpolated_camera/index.html) レシピを使用した {{< gd-icon Camera3D >}}`Camera3D` を配置しています。

<video controls src="/godot_recipes/4.x/img/3d_kinematic_09.webm"></video>

## まとめ

これはあらゆる種類の運動学的キャラクターの動作基盤です。ここからジャンプ、射撃、AI挙動などを追加できます。このレシピを拡張した具体例については、関連するレシピを参照します。

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードをダウンロードする：[https://github.com/godotrecipes/characterbody3d_examples](https://github.com/godotrecipes/characterbody3d_examples)

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます。 [floating_text.zip](/godot_recipes/4.x/ja/files/floating_text.zip)
{{% /notice %}} -->

## 関連レシピ

- [3D入門](/godot_recipes/4.x/ja/g101/3d/)
- [入力アクション](/godot_recipes/4.x/ja/input/input_actions/)

