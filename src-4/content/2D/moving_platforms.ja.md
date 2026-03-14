---
title: "移動式プラットフォーム"
weight: 5
draft: false
---

## 課題

2Dプラットフォーマーゲームには移動プラットフォームが必要です。

## 解決策

この問題には複数のアプローチ方法があります。ここではプラットフォーム部分に `{{< gd-icon AnimatableBody2D >}}AnimatableBody2D` を使用し、`{{< gd-icon Tween >}}Tween` で移動させる手法を採用します。これにより、多様な動作パターンを実現しながら、必要なコード量を最小限に抑えることができます。

{{% notice info %}}
この移動プラットフォームの実装方法は、Tweenではなく {{< gd-icon アニメーションPlayer >}}`アニメーションPlayer` を使用することでもできます。基本的なセットアップ手順は同様ですが、代わりにTweenコードの代わりにボディの `position` プロパティをアニメーション化します。
{{% /notice %}}

### セットアップ方法

まずは[プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)レシピを使用して、基本的なプラットフォーマーのセットアップから始めましょう。このレシピで定義されている基本移動機能は、指定されたプラットフォームと問題なく連携します。もしレシピをカスタマイズしていたり、独自の実装を使用している場合でも、動作原理は同じですのでご安心ください。

### プラットフォームの作成

プラットフォームシーンには以下のノードが含まれています：

- {{< gd-icon Node2D >}} ノード `Node2D` ("MovingPlatform")：この親ノードは「アンカー」またはプラットフォームの起点として機能します。アニメーションでは、この親ノードを基準としたプラットフォームの位置変化を制御します。
  - {{< gd-icon AnimatableBody2D >}} ノード `AnimatableBody2D`：これは実際に移動するプラットフォーム本体を表します。このノードが移動対象となります。
    - {{< gd-icon Sprite2D >}} ノード `Sprite2D`：ここではスプライトシート、個別の画像、あるいは {{< gd-icon TileMap >}} ノードとしてタイルマップを使用することもできます。
    - {{< gd-icon CollisionShape2D >}} ノード `CollisionShape2D`：ヒットボックスの大きさが大きすぎると、プレイヤーがプラットフォームの端から「浮いて」見える原因になるので注意してください。

{{< gd-icon Sprite2D >}}`Sprite2D`の**テクスチャ**と衝突形状を適切に設定してください。{{< gd-icon AnimatableBody2D >}}`AnimatableBody2D`では、**物理演算同期** プロパティを「オン」に設定します。コードでボディを動かしているため、これにより物理演算ステップ時に正しく移動され、プレイヤーや他の物理オブジェクトと連動した動きを維持できます。

次にルートノードにスクリプトを追加します。{{< gd-icon Node2D >}}`Node2D`:

```gdscript
extends Node2D

@export var offset = Vector2(0, -320)
@export var duration = 5.0

func _ready():
    start_tween()

func start_tween():
    var tween = get_tree().create_tween().set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)
    tween.set_loops().set_parallel(false)
    tween.tween_property($AnimatableBody2d, "position", offset, duration / 2)
    tween.tween_property($AnimatableBody2d, "position", Vector2.ZERO, duration / 2)
```

以下の機能をスムーズに動作させるために、`Twien` のオプションをいくつか活用しています：

* `set_process_mode()`：物理演算処理段階でのみ移動が行われるようにします。
* `set_loops()`：Tween再生を繰り返す設定です。
* `set_parallel(false)`：デフォルトでは、すべての `tween_property()` 変更が同時に実行されます。これを無効にすると、2つの動作が順次行われます：オフセットの一方端に移動した後、開始位置に戻るという流れになります。

翻訳された2つのプロパティを使用することで、プラットフォームの移動を調整できます。`offset`を設定してTweenが開始点から相対的に移動する位置を指定し、`duration`を設定してサイクルを完了するまでの時間を決定します。

自分のレベル／ワールドにプラットフォームを追加し、実際に試してみてください。

<video controls src="/godot_recipes/4.x/img/moving_platform4.webm" autoplay="true"></video>

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらからダウンロードできます。 [https://github.com/godotrecipes/2d_moving_platforms](https://github.com/godotrecipes/2d_moving_platforms)

## 関連レシピ

- [プラットフォームキャラクタ](/godot_recipes/4.x/ja/2d/platform_character/)

<!-- #### Videoが気に入ったら？ -->

※近日公開予定
{{< youtube C-Sn55e5wnk >}} -->