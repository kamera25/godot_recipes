---
title: "近接攻撃"
weight: 3
draft: false
ghcommentid: 53
---

## 課題

剣やパンチなどの近接攻撃を実装したいという。

## 解決策

本例では、既に攻撃アニメーションが設定されたキャラクターが存在すると仮定します。説明のために、以下の2種類の攻撃を使用する：

![alt](/godot_recipes/3.x/img/attack2.png)

![alt](/godot_recipes/3.x/img/attack1.png)

{{< gd-icon Area2D >}}`Area2D` を使用して剣がターゲットに命中したことを検出できますが、実際に有効化する必要があるのはスイング動作中のみです。アニメーションと同期させるためには、この活性化をアニメーションPlayerで制御します。

シーンに `Area2D` と `CollisionShape2D` を追加します。ヒットボックスには矩形形状を使用し、剣が振り上げフレームで完全にカバーされるようにサイズを調整します。

![alt](/godot_recipes/3.x/img/melee_attack_01.png)

Move the animation to the first frame and check the _Disabled_ property of the area. Click the keyframe icon to add a track to the animation. Then advance the animation to the frame where the sword is extended, and add another keyframe with _Disabled_ unchecked. Finally, advance to the end of the swing and keyframe _Disabled_ on once more.

![alt](/godot_recipes/3.x/img/melee_attack_02.gif)

新しいエリアの`area_entered`シグナル（またはゲームの設定によっては、`body_entered`）を接続します。このデモでは、ダメージを受け取れる任意のボディには{{< gd-icon Area2D >}}`Area2D`が定義され、「hurtbox」というグループ内に配置されているとしましょう。

```gdscript
func _on_SwordHit_area_entered(area):
    if area.is_in_group("hurtbox"):
        area.take_damage()
```

これで実際に試してみて、ターゲットが剣の当たり判定範囲内にいればダメージが発生するか確認できるはずです。

![alt](/godot_recipes/3.x/img/melee_attack_03.gif)

### ヒットボックスサイズの変更方法

When you have more than one attack animation, the size of the affected area may not be the same. In the above attack animations, the first one is an upward sweeping attack that covers more area. To handle this, we also need to add an animation track for the collision shape's _Extents_ property. Set this and keyframe it at the start of each animation.

![alt](/godot_recipes/3.x/img/melee_attack_04.gif)

![alt](/godot_recipes/3.x/img/melee_attack_05.gif)

## 関連レシピ

[見下ろし型キャラクター制御](http://kidscancode.org/godot_recipes/2d/topdown_movement/#option-1-8-way-movement)
[アニメーション状態の管理方法](http://kidscancancode.org/godot_recipes/animation/animation_state_machine/)

#### この動画が気に入ったら？

{{< youtube AaJopFFkmNo >}}