---
title: "基本FPSキャラクター"
weight: 2
draft: false
tags: []
---

## 課題

ファーストパーソン・シューティングゲーム（FPS）用のキャラクターを作成する必要があります。

## 解決策

まず、`CharacterBody3D` ノードから始め、次に `CollisionShape3D` を追加します。この場合、最も一般的な選択肢は `CapsuleShape3D` 衝突形状です。ワールドの設定によっては、ここに他の形状も追加できますが、この例では基本に忠実に進めます。

サイズはすべて初期設定値のままにします（カプセルの高さは2メートルとなります）。地面と底面を揃えるため、高さを「+1.0」m移動させてください。

次に、ボディの子要素として `{{< gd-icon Camera3D >}}`Camera3D` を追加し、約 `1.6`m 持ち上げてください。

{{% notice style="note" title="キャラクターのボディはどこにある？" %}}
この例では、「ボディーレス」な状態、つまりプレイヤー用の表示メッシュを追加しないケースを考えます。環境によっては、プレイヤーの身体を表示する必要があるかどうかは異なるでしょう。
{{% /notice %}}

スクリプトをボディに添付し、まずいくつかのプロパティを定義することから始めましょう。

```gdscript
extends CharacterBody3D

var gravity = ProjectSettings.get_setting("physics/3d/default_gravity")
var speed = 5
var jump_speed = 5
var mouse_sensitivity = 0.002
```

def _physics_process():
    # 移動処理を行う関数
    # Note: 入力.get_vector()は前後/左右キーの組み合わせに基づいて2次元ベクトルを返す
    # このベクトルを使ってボディの速度成分 `x` と `z` を設定する（`y` は重力で自動的に管理されるため）
    # ベクトルをボディの `basis` で乗算することで、回転を考慮している - 前進は常にボディの前方ベクトルとなるように

```gdscript
func _physics_process(delta):
    velocity.y += -gravity * delta
    var input = 入力.get_vector("left", "right", "forward", "back")
    var movement_dir = transform.basis * Vector3(input.x, 0, input.y)
    velocity.x = movement_dir.x * speed
    velocity.z = movement_dir.z * speed

    move_and_slide()
    if is_on_floor() and 入力.is_action_just_pressed("jump"):
        velocity.y = jump_speed
```

入力マッピングに「W」「A」「S」「D」（標準設定）またはコントローラーの軸（好みに応じて選択可能）を使用して、適切な入力アクションを必ず追加してください。

以下の手順で「ワールド」シーンにプレイヤーを追加してください。床用に`StaticBody3D`ノードを、壁用に複数のノードを作成済みとします。

移動しようとすると、前後・左右に動けるものの、回転はできないことがわかります。次はこの点を処理していきます。

## 3D空間におけるマウス操作制御

まず第一に、マウスを動かすのと同じ方向にプレイヤーを左／右に回転させる必要があります。マウス入力は画面座標系で2次元的に表現されるため、マウスの水平方向（`x`）の動きを、垂直軸である`y`を軸にしたプレイヤー本体の回転に変換する必要があります。先ほど定義した`mouse_sensitivity`プロパティを使えば、マウス移動量がどれだけ回転角度に相当するかを調整可能です。

```gdscript
func _input(event):
    if event is 入力EventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
```

コードをもう一度実行してみると、マウスで回転操作ができるようになっていることが確認できるはずです。ただし、マウスカーソルがゲームウィンドウの外にはみ出してしまう場合があります。このタイミングで、マウスをキャプチャするコードを追加すると良いでしょう。詳細については[入力：マウスのキャプチャ](/godot_recipes/4.x/input/mouse_capture/)をご覧ください。

更新されたコードは次のようになります。

```gdscript
func _input(event):
    if event is 入力EventMouseMotion and 入力.mouse_mode == 入力.MOUSE_MODE_CAPTURED:
        rotate_y(-event.relative.x * mouse_sensitivity)
```

最後に、上下移動にはマウスの「y」モーションを使ってカメラを傾けます。完全に逆さまになるのは避けたいので、回転値は「clamp()」で70度という合理的な範囲に制限します。

```gdscript
func _input(event):
    if event is 入力EventMouseMotion and 入力.mouse_mode == 入力.MOUSE_MODE_CAPTURED:
        rotate_y(-event.relative.x * mouse_sensitivity)
        $Camera3D.rotate_x(-event.relative.y * mouse_sensitivity)
        $Camera3D.rotation.x = clampf($Camera3D.rotation.x, -deg_to_rad(70), deg_to_rad(70))
```

## 武器の所持について

![alt](/godot_recipes/4.x/img/fps_01.png)

FPSキャラクターには通常、前面に位置した武器の3Dメッシュが用意されています。これをセットアップするのは、Godotエディターのいくつかの便利な機能を使えば簡単に行えます。

武器モデルを{{< gd-icon Camera3D >}}`Camera3D`の子要素として追加します。その後、エディタービューメニューで「2つのビューポート」を選択し、そのうち1つをカメラプレビュー用に設定してください。これで、武器を自由に移動させながら、プレイヤー視点でどのように見えるかを容易に確認できるようになります。

個性を加えるには、`アニメーションPlayer` を使用して武器の位置をプレイヤーの移動に合わせて左右にアニメーションさせる方法がおすすめです。


## 関連レシピ

- [入力：マウスキャプチャーの使用方法](/godot_recipes/4.x/ja/input/mouse_capture/)


## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードしてください。[https://github.com/godotrecipes/basic_fps](https://github.com/godotrecipes/basic_fps)
