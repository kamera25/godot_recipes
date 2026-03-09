---
title: "3D Unit Healthbars"
weight: 5
draft: false
ghcommentid: 35
---

## 問題文

You want a floating "healthbar" for your 3D game objects (mobs, characters, etc.).

## 解決策

For this solution, we're going to re-use a 2D healthbar based on a {{< gd-icon TextureProgressBar >}}`TextureProgressBar` node. It's already set up with textures and code for updating the value and color. If you already have something similar, feel free to use it here. In the example, we'll name this scene "Healthbar2D".

<img src=\ alt=\>

必要なアセットがある場合、バーで使用している以下の3つの画像を紹介します：

![alt](/godot_recipes/4.x/img/barHorizontal_green_mid%20200.png)

![alt](/godot_recipes/4.x/img/barHorizontal_yellow_mid%20200.png)

![alt](/godot_recipes/4.x/img/barHorizontal_red_mid%20200.png)

既存のオブジェクトを再利用すれば、大幅に作業時間を節約できます。ヘルスバーやカメラ、その他一般的なコンポーネントが必要なたびにゼロから作り直す必要はありません。
{{% /notice %}}

### プロジェクト設定

For our example "mob", we'll start with a {{< gd-icon CharacterBody3D >}}`CharacterBody3D` node. It's programmed to spawn and travel in a straight line. It also has the following code to handle damage:

```gdscript
func _on_input_event(_camera, event, _position, _normal, _shape_idx):
    if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
        health -= 1
        if health <= 0:
            queue_free()
```

![alt](/godot_recipes/4.x/img/3d_bars01a.gif)

単位をクリックするたびに1ダメージが与えられます。合計10ダメージを与えると、そのユニットは破壊されます。この状態を2Dバーを使って視覚的に表現する必要があります。

### 2Dを3Dに変換

We can display a 2D image in 3D using a {{< gd-icon Sprite3D >}}`Sprite3D`. Add one to a new scene and name it "Healthbar3D". First, we'll get it configured and sized, so set the _Texture_ property to the green bar image.

The {{< gd-icon Sprite3D >}}`Sprite3D` acts like any other 3D object - as we pan the camera around, our perspective on it changes. However, we want the healthbar to always "face" toward the camera so that we can see it.

In the Inspector, under _Flags_, set _Billboard_ to "Enabled".

続いてカメラを動かして、テクスチャが常にプレイヤー側を向いているか確認してください。

![alt](/godot_recipes/4.x/img/3d_bars02.gif)

このシーンのインスタンスを「Mob」シーンに追加し、バーをモブの体の上に配置してください。

![alt](/godot_recipes/4.x/img/3d_bars04.png)

### ビューポートテクスチャ

```
私たちは `Sprite3D` ノードが静的なテクスチャを表示するのではなく、2D `TextureProgressBar` を表示したいと考えています。これは、テクスチャをエクスポートできる `SubViewport` ノードを使用することで実現可能です。

```plaintext
以下の手順で操作してください：
1. {{< gd-icon SubViewport >}} `SubViewport` を {{< gd-icon Sprite3D >}} `Sprite3D` の子要素として追加します。
2. インスペクターウィンドウで、_Transparent BG_ 設定を **オン** に設定してください。
```

さらに、ヘルスバーテクスチャのサイズに合わせてビューポートのサイズを設定する必要があり、そのサイズは`(200, 26)`です。

インスタンス化する際に、`HealthBar2D` を {{< gd-icon Viewport >}}`Viewport` の子要素として配置してください。シーン構成は以下のようになるはずです：

![alt](/godot_recipes/4.x/img/3d_bars_03a.png)

もし `SubViewport` が `Sprite3D` の子要素でなかった場合、インスペクター上で直接スプライトのテクスチャとして設定できます。しかしこれは子要素であるため、適切なタイミングで準備が整っていない可能性があります。このため、以下のように `Sprite3D` にアタッチされたスクリプト内で設定する必要があります：

```gdscript
extends Sprite3D

func _ready():
    texture = $SubViewport.get_texture()
```

### 全体を統合して接続する方法

モブの `_on_input_event()` メソッド内で、ヘルスを減少させた後に以下を追加してください：

```gdscript
$HealthBar3D.update(health, max_health)
```

以下の内容を `HealthBar3D.gd` に追加してください：

```gdscript
func update_health(_value, _max_value):
    $SubViewport/HealthBar2D.update_health(_value, _max_value)
```

このコードは、2Dバーに既に存在するupdateメソッドを呼び出しています。進捗バーの値を設定するとともに、バーの色を選択しています：

```gdscript
func update_health(_value, _max_value):
    value = _value
    if value < _max_value:
        show()
    texture_progress = bar_green
    if value < 0.75 * _max_value:
        texture_progress = bar_yellow
    if value < 0.45 * _max_value:
        texture_progress = bar_red
```

クリックしてモブの体力ゲージが変化する様子を確認しましょう。

![alt](/godot_recipes/4.x/img/3d_bars_05a.gif)


### まとめ

You can use this technique to display any other {{< gd-icon Node2D >}}`Node2D` or {{< gd-icon Control >}}`Control` nodes, such as {{< gd-icon Label >}}`Label`, {{< gd-icon VideoStreamPlayer >}}`VideoStreamPlayer`, etc. You can even use the {{< gd-icon SubViewport >}}`SubViewport` to "project" an entire 2D game in 3D space.

<!-- ## 関連するレシピ

- [Object Healthbars (2D)](/godot_recipes/4.x/ui/unit_healthbar/) -->

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらからダウンロードできます：[https://github.com/godotrecipes/3d_object_healthbars](https://github.com/godotrecipes/3d_object_healthbars)
