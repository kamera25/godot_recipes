---
title: "3D空間に浮かぶHPバー"
weight: 5
draft: false
ghcommentid: 35
---

## 課題

3Dゲームオブジェクト（敵キャラクター、プレイヤーキャラなど）用に、フローティング表示の「HPバー」をつけたい。

## 解決策

この解決策として、既存の {{< gd-icon TextureProgressBar >}}`TextureProgressBar` ノードをベースにした 2D HPバーを再利用します。すでにテクスチャが設定されており、値と色を更新するためのコードも実装済みです。既に同様のシステムをお持ちの場合は、それをそのまま使用していただいて構いません。サンプルではこのシーンを「Healthbar2D」と名付けます。

![alt](/godot_recipes/4.x/img/healthbar_example.gif)

必要なアセットがある場合、バーで使用している以下の3つの画像を紹介します。

![alt](/godot_recipes/4.x/img/barHorizontal_green_mid%20200.png)

![alt](/godot_recipes/4.x/img/barHorizontal_yellow_mid%20200.png)

![alt](/godot_recipes/4.x/img/barHorizontal_red_mid%20200.png)

{{% notice note %}}
既存のオブジェクトを再利用すれば、大幅に作業時間を節約できます。HPバーやカメラ、その他一般的なコンポーネントが必要なたびにゼロから作り直す必要はありません。
{{% /notice %}}

### プロジェクト設定

例として使用する「モブ」の開始点として、{{< gd-icon CharacterBody3D >}}`CharacterBody3D`ノードを設定します。このノードは自動で出現し、直線的に移動するプログラムが組まれています。また、以下のコードでダメージ処理を実装します。

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

{{< gd-icon Sprite3D >}}`Sprite3D`を使用することで、2D画像を3D空間で表示することが可能です。新しいシーンに追加し、「Healthbar3D」という名前を付けます。まず設定とサイズ調整を行いますので、 _Texture_ プロパティに緑色のバー画像を設定します。

{{< gd-icon Sprite3D >}}`Sprite3D`は通常の3Dオブジェクトと同様に動作します。カメラを移動させると、視点が変わるためです。ただし、HPバーは常にカメラの方を向くようにして、いつでも確認できるようにしたいです。

インスペクターで、 _Flags_ セクションの _Billboard_ を「Enabled(有効)」に設定します。

続いてカメラを動かして、テクスチャが常にプレイヤー側を向いているか確認します。

![alt](/godot_recipes/4.x/img/3d_bars02.gif)

このシーンのインスタンスを`Mob`シーンに追加し、バーをモブの体の上に配置します。

![alt](/godot_recipes/4.x/img/3d_bars04.png)

### ビューポートテクスチャ

{{< gd-icon Sprite3D >}}`Sprite3D` ノードが静的なテクスチャを表示するのではなく、{{< gd-icon TextureProgressBar >}}`TextureProgressBar` を表示したいです。これは、テクスチャをエクスポートできる {{< gd-icon SubViewport >}}`SubViewport` ノードを使用することで実現できます。

以下の手順で操作します。
1. {{< gd-icon SubViewport >}}`SubViewport` を {{< gd-icon Sprite3D >}}`Sprite3D` の子要素として追加します。
2. インスペクタウィンドウで、_Transparent BG_ 設定を **オン** に設定します。

さらに、HPバーテクスチャのサイズに合わせてビューポートのサイズを設定する必要があり、そのサイズは`(200, 26)`です。

インスタンス化する際に、`HealthBar2D` を {{< gd-icon Viewport >}}`Viewport` の子要素として配置します。シーン構成は以下のようになるはずです。

![alt](/godot_recipes/4.x/img/3d_bars_03a.png)

もし {{< gd-icon SubViewport >}}`SubViewport` が {{< gd-icon Sprite3D >}}`Sprite3D` の子要素でなかった場合、インスペクター上で直接スプライトのテクスチャとして設定できます。しかしこれは子要素であるため、適切なタイミングで準備が整っていない可能性があります。そのため、以下のように {{< gd-icon Sprite3D >}}`Sprite3D` にアタッチされたスクリプト内で設定します。

```gdscript
extends Sprite3D

func _ready():
    texture = $SubViewport.get_texture()
```

### 作ったものを統合しよう

モブの `_on_input_event()` メソッド内で、HPを減少させた後に以下を追加します。

```gdscript
$HealthBar3D.update(health, max_health)
```

以下の内容を `HealthBar3D.gd` に追加します。

```gdscript
func update_health(_value, _max_value):
    $SubViewport/HealthBar2D.update_health(_value, _max_value)
```

このコードは、2Dバーに既に存在するupdateメソッドを呼び出しています。進捗バーの値を設定するとともに、バーの色を選択しています。

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

クリックしてモブのHPゲージが変化する様子を確認します。

![alt](/godot_recipes/4.x/img/3d_bars_05a.gif)


### まとめ

このテクニックを使えば、{{< gd-icon Node2D >}}`Node2D`ノードはもちろん、{{< gd-icon Control >}}`Control`ノード全般（例：{{< gd-icon Label >}}`Label`や{{< gd-icon VideoStreamPlayer >}}`VideoStreamPlayer`など）を3D空間に表示できます。さらに、{{< gd-icon SubViewport >}}`SubViewport`を使えば、2Dゲーム全体を3D空間に「投影」することもできます。

<!-- ## 関連レシピ

- [オブジェクトのHPバー（2D）](/godot_recipes/4.x/ui/unit_healthbar/) -->

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトコードはこちらからダウンロードできます。[https://github.com/godotrecipes/3d_object_healthbars](https://github.com/godotrecipes/3d_object_healthbars)
