---
title: "Godot 3.x からの移行"
weight: 5
draft: false
---

これは、4.0への移行時に注意すべき主要な変更点と「落とし穴」をまとめた随時更新リストです。

## 新しい名称

Godot 4での最も大きな変化の一つは、ノード名、関数名、プロパティ名などの大量のリネームです。これらの多くは仕様の一貫性や可読性を向上させるために行われています。特に注意すべき主要な変更点をいくつかご紹介します。

* 2D/3Dノードの命名規則 - Godot 3.x では2Dノードに「2D」サフィックスが付いていた一方、3Dノードには何も付加されていませんでした。この不整合が解消され、現在ではすべてのノードが「2D」または「3D」を明示するようになりました。具体例：{{< gd-icon RigidBody2D >}}`RigidBody2D` と {{< gd-icon RigidBody3D >}}`RigidBody3D`。

* 3Dカテゴリにおいて、`Spatial`ノードは名称を{{< gd-icon Node3D >}}`Node3D`に統一されています

* 最も人気のあるノードの1つである `KinematicBody` が、{{< gd-icon CharacterBody2D >}}`CharacterBody2D`/{{< gd-icon CharacterBody3D >}}`CharacterBody3D` に名称変更されました。このノードに関するAPIの変更点については、以下をご覧ください。

* {{< gd-icon PackedScene >}}`PackedScene` の `instance()` 関数は `instantiate()` に改名されました

* `position`および`global_position`プロパティは、3D空間において従来の`translation`と`global_translation`に取って代わり、2Dとの一貫性が保たれます。

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

{{< gd-icon Tween >}}`Tween`はもはやノードとしてありません。代わりに、必要な時に都度1回限りのTweenアニメーションオブジェクトを作成する方式に変更されました。一度慣れてしまえば、従来の方法よりもはるかに強力で使いやすいものとなっています。

## AnimatedSprite[2D|3D]

3.x系バージョンに慣れているユーザーにとって最も大きな変化は、`playing`プロパティが廃止された点です。現在は{{< gd-icon AnimationPlayer >}}`AnimationPlayer`との整合性が大幅に改善されており、アニメーションを自動再生するには**SpriteFrames**パネルでオートプレイ機能を有効にするだけで済みます。コード側では`play()`メソッドと`stop()`メソッドを使用して、再生制御する形式に変更されました。

## キャラクターボディ [2D/3D]

このノードにおける最大の変更点は `move_and_slide()` 関数の使用方法です。パラメーターは一切不要となり、すべてが組み込みプロパティとして実装されました。ネイティブの `velocity`（速度）プロパティも含まれているため、独自に定義する必要はありません。

これらのノードの詳細な使用例については、[プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)および／または[基本FPSキャラクタ](/godot_recipes/4.x/ja/3d/basic_fps/)を参照してください。


## タイルマップ

4.0版では `TileMap` ノードが全面的にリニューアルされました。タイルセットの作成方法からタイルの描画・操作方法まで、ほぼすべてが完全に刷新されています。

私たちの「TileMap の使い方」ガイドが間もなく公開されます。

## 乱数生成

以下はGDScriptの組み込み乱数生成関数に対する変更点です。

* もう `randomize()` を呼び出す必要はありません。自動で処理されます。再現性のある「乱数」が必要な場合は、`seed()` で事前に設定した値を指定します。

* `rand_range()` は、浮動小数点数の場合は `randf_range()`、整数の場合は `randi_range()` にそれぞれ置き換えられました。

## レイキャスティング

コード内でレイキャストを実行するために、新たなAPIが導入されました。`PhysicsDirectSpaceState[2D|3D].intersect_ray()`関数には、専用オブジェクトをパラメーターとして指定します。これによりレイの特性を正確に定義できます。例えば3D空間でレイを描画する場合は。

```gdscript
var space = get_world_3d().direct_space_state
var ray = PhysicsRayQueryParameters3D.create(position, destination)
var collision = space.intersect_ray(ray)
if collision:
    print("ray collided")
```