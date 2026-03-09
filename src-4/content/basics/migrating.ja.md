---
title: "Migrating from 3.x"
weight: 5
draft: false
---

This is an evolving list of the main changes and "gotchas" to look out for if you're transitioning to 4.0.

## 新しい名称

Godot 4での最も大きな変化の一つは、ノード名、関数名、プロパティ名などの大量のリネームです。これらの多くは仕様の一貫性や可読性を向上させるために行われています。特に注意すべき主要な変更点をいくつかご紹介します：

* 2D/3D nodes - In Godot 3.x, 2D nodes had the "2D" suffix, but 3D nodes had none. This has been made consistent - they all now have "2D" or "3D" suffixes. For example: {{< gd-icon RigidBody2D >}}`RigidBody2D` vs. {{< gd-icon RigidBody3D >}}`RigidBody3D`.

* 3Dカテゴリにおいて、`空間`ノードは名称を{{< gd-icon Node3D >}}`Node3D`に統一されています

* 最も人気のあるノードの1つである `KinematicBody` が、{{< gd-icon CharacterBody2D >}}`CharacterBody2D`/{{< gd-icon CharacterBody3D >}}`CharacterBody3D` に名称変更されました。このノードに関するAPIの変更点については、以下をご覧ください。

* `{{< gd-icon PackedScene >}}`PackedScene` の `instance()` 関数は `instantiate()` に改名されました

- 位置プロパティ（`position`）およびグローバル位置プロパティ（`global_position`）は、3D空間において従来の翻訳プロパティ（`translation`）とグローバルな翻訳プロパティ（`global_translation`）に取って代わり、2Dとの一貫性が保たれます。

## シグナルと呼び出し可能オブジェクト

4.0ではシグナルの扱いが大幅に簡素化されています。`signal`はネイティブ型として扱われるようになったため、文字列を使用する機会が減り、オートコンプリートやエラーチェック機能が利用可能になりました。これは関数にも適用され、従来のような文字列参照ではなく、直接関数を指定できるようになりました。

以下に、シグナルの定義、接続、および送出の具体例を示します。

```gdscript
extends Node

signal my_signal

func _ready():
    my_signal.connect(signal_handler)

func _input(event):
    if event.is_action_pressed("ui_select"):
        my_signal.emit()

func signal_handler():
    print("signal received")
```

## Tweens（中間アニメーション）

Godot 3.5 で `SceneTreeTween` を使い始めた場合、Godot 4.0 の {{< gd-icon Tween >}}`Tween` の使用方法は馴染み深いものでしょう。

{{< gd-icon Tween >}}`Tween`はもはやノードとして存在しません。代わりに、必要な時に都度1回限りのトゥイーンアニメーションオブジェクトを作成する方式に変更されました。一度慣れてしまえば、従来の方法よりもはるかに強力で使いやすいものとなっています。

## AnimatedSprite[2D|3D]

3.x系バージョンに慣れているユーザーにとって最も大きな変化は、`playing`プロパティが廃止された点です。現在は{{< gd-icon AnimationPlayer >}}`AnimationPlayer`との整合性が大幅に改善されており、アニメーションを自動再生するには**SpriteFrames**パネルでオートプレイ機能を有効にするだけで済みます。コード側では`play()`メソッドと`stop()`メソッドを使用して、再生制御を行う形式に変更されました。

## キャラクターボディ [2D/3D]

このノードにおける最大の変更点は `move_and_slide()` 関数の使用方法です。もはやパラメータは一切不要となり、すべてが組み込みプロパティとして実装されました。これにはネイティブの `velocity`（速度）プロパティも含まれているため、ユーザーが独自定義する必要はなくなりました。

これらのノードの詳細な使用例については、[プラットフォームキャラクタ](/godot_recipes/4.x/2d/platform_character/)および／または[基本FPSキャラクタ](/godot_recipes/4.x/3d/basic_fps/)を参照してください。


## タイルマップ (TileMap)

4.0版では `TileMap` ノードが全面的にリニューアルされました。タイルセットの作成方法からタイルの描画・操作方法まで、ほぼすべてが完全に刷新されています。

Our "Using TileMaps" guide is coming soon.

## RNG (乱数生成器)

以下はGDScriptの組み込み乱数生成関数に対する変更点です：

* You no longer need to call `randomize()` - this is automatic. If you do want repeatable "randomness", use `seed()` to set it to a preselected value.

* `rand_range()` 関数は、浮動小数点数の場合は `randf_range()`、整数の場合は `randi_range()` にそれぞれ置き換えられました。

## レイキャスティング

コード内でレイキャストを実行する際、新たなAPIが導入されました。`PhysicsDirectSpaceState[2D|3D].intersect_ray()`関数には、専用オブジェクトをパラメータとして指定する必要があります。これによりレイの特性を正確に定義できます。例えば3次元空間でレイを描画する場合は：

```gdscript
var space = get_world_3d().direct_space_state
var ray = PhysicsRayQueryParameters3D.create(position, destination)
var collision = space.intersect_ray(ray)
if collision:
    print("ray collided")
```