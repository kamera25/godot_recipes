---
title: "近接攻撃"
weight: 3
draft: false
ghcommentid: 53
---

## 課題

剣やパンチなどの近接攻撃を実装したいということですね。

## 解決策

本例では、既に攻撃アニメーションが設定されたキャラクターが存在すると仮定します。説明のために、以下の2種類の攻撃を使用する：

[画像: attack2.png]

![alt](/godot_recipes/3.x/img/attack1.png)

Area2D``Area2D`を使用して剣がターゲットに命中したことを検出できますが、実際に有効化する必要があるのはスイング動作中のみです。アニメーションと同期させるためには、この活性化をアニメーションPlayerで制御します。

シーンに `Area2D` と `CollisionShape2D` を追加します。ヒットボックスには矩形形状を使用し、剣が振り上げフレームで完全にカバーされるようにサイズを調整します。

![alt](/godot_recipes/3.x/img/melee_attack_01.png)

アニメーションを最初のフレームに移動し、領域の [無効] プロパティを確認します。キーフレームアイコンをクリックしてアニメーションにトラックを追加します。次に、剣が伸びているフレームまでアニメーションを進め、[無効] を解除した状態でもう1つのキーフレームを追加します。最後に、スイングの終わりまで進み、再度 [無効] を有効にしてキーフレームを作成します。

![alt](/godot_recipes/3.x/img/melee_attack_02.gif)

Now connect this new area's `area_entered` signal (or, depending on your game setup, `body_entered`). For simplicity in this demo, let's assume any body capable of taking damage has properly defined {{< gd-icon Area2D >}}`Area2D` components and is grouped under the "hurtbox" category.

```gdscript
func _on_SwordHit_area_entered(area):
    if area.is_in_group("hurtbox"):
        area.take_damage()
```

これで実際に試してみて、ターゲットが剣の当たり判定範囲内にいればダメージが発生するか確認できるはずです。

![alt](/godot_recipes/3.x/img/melee_attack_03.gif)

### ヒットボックスサイズの変更方法

複数の攻撃アニメーションがある場合、ダメージ範囲の大きさが統一されていないことがあります。上記のアニメーション例では、最初の動きは広範囲をカバーする斜め上方向への振り下ろし攻撃です。この処理に対応するため、衝突形状の_Extents_プロパティに対するアニメーショントラックも追加する必要があります。この値を設定して各アニメーションの開始時にキーフレームとして登録してください。

![alt](/godot_recipes/3.x/img/melee_attack_04.gif)

![alt](/godot_recipes/3.x/img/melee_attack_05.gif)

## 関連レシピ

[トップダウン型キャラクター制御](http://kidscancode.org/godot_recipes/2d/topdown_movement/#option-1-8-way-movement)
[アニメーション状態の管理方法](http://kidscancancode.org/godot_recipes/animation/animation_state_machine/)

#### この動画が気に入ったら？

{{< youtube AaJopFFkmNo >}}