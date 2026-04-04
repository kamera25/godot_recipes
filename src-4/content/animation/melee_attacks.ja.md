---
title: "近接攻撃"
weight: 3
draft: false
ghcommentid: 53
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

剣やパンチなどの近接攻撃を実装したい。

## 解決策

本例では、既に攻撃アニメーションが設定されたキャラクターが存在すると仮定します。説明のために、以下の2種類の攻撃を使用する：

![alt](/godot_recipes/3.x/img/attack2.png)

![alt](/godot_recipes/3.x/img/attack1.png)

{{< gd-icon Area2D >}}`Area2D` を使用して剣がターゲットに命中したことを検出できますが、実際に有効化する必要があるのはスイング動作中のみです。アニメーションと同期させるためには、この活性化をAnimationPlayerで制御します。

シーンに {{< gd-icon Area2D >}}`Area2D` と {{< gd-icon CollisionShape2D >}}`CollisionShape2D` を追加します。ヒットボックスには矩形形状を使用し、剣が振り上げフレームで完全にカバーされるようにサイズを調整します。

![alt](/godot_recipes/3.x/img/melee_attack_01.png)

アニメーションを最初のフレームに移動し、領域の [無効] プロパティを確認します。キーフレームアイコンをクリックしてアニメーションにトラックを追加します。次に、剣が伸びているフレームまでアニメーションを進め、[無効] を解除した状態でもう1つのキーフレームを追加します。最後に、スイングの終わりまで進み、再度 [無効] を有効にしてキーフレームを作成します。

![alt](/godot_recipes/3.x/img/melee_attack_02.gif)

新しいエリアの`area_entered`シグナル（またはゲームの設定によっては、`body_entered`）を接続します。このデモでは、ダメージを受け取れる任意のボディには{{< gd-icon Area2D >}}`Area2D`が定義され、「hurtbox」というグループ内に配置されているとします。

```gdscript
func _on_SwordHit_area_entered(area):
    if area.is_in_group("hurtbox"):
        area.take_damage()
```

これで実際に試してみて、ターゲットが剣の当たり判定範囲内にいればダメージが発生するか確認できるはずです。

![alt](/godot_recipes/3.x/img/melee_attack_03.gif)

### ヒットボックスサイズの変更方法

複数の攻撃アニメーションがある場合、ダメージ範囲の大きさが統一されていないことがあります。上記のアニメーション例では、最初の動きは広範囲をカバーする斜め上方向への振り下ろし攻撃です。この処理に対応するため、衝突形状の _Extents_ プロパティに対するアニメーショントラックも追加が必要です。この値を設定して各アニメーションの開始時にキーフレームとして登録してください。

![alt](/godot_recipes/3.x/img/melee_attack_04.gif)

![alt](/godot_recipes/3.x/img/melee_attack_05.gif)

## 関連レシピ

[見下ろし型キャラクター制御](/godot_recipes/4.x/ja/2d/topdown_movement/#option-1-8-way-movement)
[アニメーション状態の管理方法](http://kidscancancode.org/godot_recipes/animation/animation_state_machine/)

#### この動画が気に入ったら？

{{< youtube AaJopFFkmNo >}}