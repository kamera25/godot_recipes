---
title: "Moving Platforms"
weight: 5
draft: false
---

## 問題文

2Dプラットフォーマーゲームには移動プラットフォームが必要です。

## 解決策

この問題には複数のアプローチ方法があります。ここではプラットフォーム部分に `{{< gd-icon AnimatableBody2D >}}AnimatableBody2D` を使用し、`{{< gd-icon Tween >}}Tween` で移動させる手法を採用します。これにより、多様な動作パターンを実現しながら、必要なコード量を最小限に抑えることができます。

{{% notice info %}}
この移動プラットフォームの実装方法は、トゥイーンではなく {{< gd-icon AnimationPlayer >}}`AnimationPlayer` を使用することでも可能です。基本的なセットアップ手順は同様ですが、代わりにトゥイーンコードの代わりにボディの `position` プロパティをアニメーション化します。
{{% /notice %}}

### セットアップ方法

まずは[プラットフォームキャラクター](/godot_recipes/4.x/2d/platform_character/)レシピを使用して、基本的なプラットフォーマーのセットアップから始めましょう。このレシピで定義されている基本移動機能は、指定されたプラットフォームと問題なく連携します。もしレシピをカスタマイズしていたり、独自の実装を使用している場合でも、動作原理は同じですのでご安心ください。

### プラットフォームの作成

プラットフォームシーンには以下のノードが含まれています：

- {{< gd-icon Node2D >}}`Node2D` ("MovingPlatform"): The `Node2D` parent is there to act as the "anchor" or start point for the platform. We'll animate the platform's `position` relative to this parent node.
  - {{< gd-icon AnimatableBody2D >}}`AnimatableBody2D`: This represents the platform itself. This is the node that will move.
    - {{< gd-icon Sprite2D >}}`Sprite2D`: You can use a sprite sheet here, individual images, or even a {{< gd-icon TileMap >}}`TileMap`.
    - {{< gd-icon CollisionShape2D >}}`CollisionShape2D`: Don't make the hitbox too big, or the player will appear to be "hovering" off the edge of the platform.

Set up the {{< gd-icon Sprite2D >}}`Sprite2D`'s **Texture** and the collision shape appropriately. In the {{< gd-icon AnimatableBody2D >}}`AnimatableBody2D`, set the **Sync to Physics** property "On". Since we're moving the body in code, this ensures that it's moved during the physics step, keeping it in sync with the player and other physics bodies.

次にルートノードにスクリプトを追加します：{{< gd-icon Node2D >}}`Node2D`:

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

※ `set_process_mode()`：物理演算処理段階でのみ移動が行われるようにします。
※ `set_loops()`：トゥイーン再生を繰り返す設定です。
※ `set_parallel(false)`：デフォルトでは、すべての `tween_property()` 変更が同時に実行されます。これを無効にすると、2つの動作が順次行われます：オフセットの一方端に移動した後、開始位置に戻るという流れになります。

翻訳された2つのプロパティを使用することで、プラットフォームの移動を調整できます。`offset`を設定してトゥイーンが開始点から相対的に移動する位置を指定し、`duration`を設定してサイクルを完了するまでの時間を決定します。

自分のレベル／ワールドにプラットフォームを追加し、実際に試してみてください：

<video controls src="/godot_recipes/4.x/img/moving_platform4.webm" autoplay="true"></video>

## <i class="fas fa-code-branch"></i> Download This Project

プロジェクトコードはこちらからダウンロードできます: [https://github.com/godotrecipes/2d_moving_platforms](https://github.com/godotrecipes/2d_moving_platforms)

## 関連レシピ

* [プラットフォームキャラクタ](/godot_recipes/4.x/2d/platform_character/)

<!-- #### この動画が気に入ったら？

*Coming soon*
{{< youtube C-Sn55e5wnk >}} -->