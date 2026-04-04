---
title: "CharacterBody2D"
draft: true
ghcommentid:
---

## {{< gd-icon CharacterBody2D >}}CharacterBody2D

Godot では、ゲーム開発で使用できる衝突判定関連の各種オブジェクトを提供しています。それぞれの動作原理を理解することで、作成するゲームオブジェクトに最適なものを選ぶ判断ができるようになります。

{{% notice tip %}}
ほとんどの3Dノードは、2D対応バージョンと同様の方法で動作します。
{{% /notice %}}

### ノードのプロパティ

* **モーションモード** - このプロパティには2つのオプションがあります。

    * 「フローティング」

    浮遊モードは見下ろし型のゲーム向けに設計されています。このモードでは、すべての衝突判定が「壁」として扱われます。

    * 「接地」（デフォルト）

    これはプラットフォーマースタイルのゲームで使用するモードです。このモードを選択すると、エンジンに対して「上方向」を指定する必要があり、これによって床面・壁面* 天井面として認識される表面が決定されます。デフォルトの「上方向」は`(0, -1)`に設定されています。


### 移動方法

身体を動かす場合、直接 `position` プロパティを設定するのは避けるべきです（テレポートさせたい場合を除く）。代わりに提供されている移動メソッドを使いましょう。これらのメソッドは衝突を検知し、適切に応答できます。各メソッドの使い方を以下に具体例とともに説明します。

* `move_and_collide()`

このメソッドには `distance` というパラメーターが必要です。これは、指定されたフレーム内で対象物体を移動させたいベクトルを指定します。通常は `velocity` ベクトルに `delta` を掛けたものを渡します（もちろん `delta` は距離を表す値です）。

move_and_collide()` を使用して移動する場合、ボディは他のオブジェクトと衝突すると直ちに移動を停止します。返される値は {{< gd-icon KinematicCollision2D >}}`KinematicCollision2D` オブジェクトであり、衝突に関する情報（関与する物体、法線ベクトルなど）を含む便利なデータ構造です。

* `move_and_slide()`

この方法は、プラットフォーマーや見下ろし型ゲームのように、片方の物体がもう一方に沿って滑る一般的な衝突応答を提供します。

`move_and_slide()` はパラメーターを受け取りません。組み込みの `velocity` プロパティを設定するだけで、自動的に `delta` を適用して移動量を計算します。

### 衝突検出について

この挙動は使用する手法によって異なります。`move_and_collide()` を使用する場合、衝突に関するデータを含む `KinematicCollision2D` オブジェクトが返ります。

When using `move_and_slide()`, it's a little trickier, as it's possible to have multiple collisions occur in a single frame (for example when moving into a corner). For this situation, there is `get_slide_collision_count()` and `get_slide_collision()`.

以下に、衝突した対象を示すコードスニペットを2つ紹介します。どちらの場合も、事前に`velocity`変数が適切に設定されているものとします。

```gdscript
# Using move_and_collide()
var collision = move_and_collide(velocity * delta)
if collision:
    print("I collided with ", collision.get_collider().name)

# Using move_and_slide()
move_and_slide()
for i in get_slide_collision_count():
    var collision = get_slide_collision(i)
    print("I collided with ", collision.get_collider().name)
```

### どの移動方法を使用しますか？

### 使用例

衝突とスライドの比較（同じ処理するコード）

1. プラットフォームキャラクター（リンク）

詳細については[プラットフォームキャラクター]レシピを参照してください（/godot_recipes/4.x/ja/2d/platform_character/）。

2. 見下ろし型シューティングゲーム（リンク）
