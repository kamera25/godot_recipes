---
title: "3Dで自動車を作ろう：牽引とドリフト"
weight: 2
draft: false
ghcommentid: 42
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

[キネマティックカー](/godot_recipes/4.x/ja/3d/kinematic_car/car_base/)で高速走行時に「レール上を走っている」ような感覚が気にいりません。ドリフトやトラクション損失を可能にするため、ある程度の「スリップ」特性が欲しいです。

## 解決策

車がドリフト走行している場合、進行方向（向いている向き）と速度ベクトル（移動方向）は必ずしも一致しません。ハンドルを切ると車は旋回しますが、速度ベクトルはすぐに追従してくれません。代わりに `lerp()` 関数を使用して、徐々に目標方向への速度を調整します。

以下の新しい変数を`car_base.gd`に追加してください。

```gdscript
@export var slip_speed = 9.0
@export var traction_slow = 0.75
@export var traction_fast = 0.02

var drifting = false
```

「slip_speed」は、車のトラクションが失われる前に到達すべき速度を指定します。この値は、車の他のパラメーターに合わせて調整が必要となります。

`traction_slow` および `traction_fast` は、`slip_speed` 以下またはそれ以上におけるトラクション特性を表し、値は 0～1 の範囲で設定されます。数値が小さいほど車両は「滑りやすい」感覚が強くなります。これらを 1 に設定すると、「レール上を走る」ように全く滑らない状態になります。

`drifting` はドリフト状態を追跡するためのブール変数です。

次に、`car_base.gd` ファイルの `calculate_steering()` 関数内で、`new_heading` を計算した直後にこのコードを追加してください。

```gdscript
# traction
if not drifting and velocity.length() > slip_speed:
    drifting = true
if drifting and velocity.length() < slip_speed and steer_angle == 0:
    drifting = false
var traction = traction_fast if drifting else traction_slow
```

このコードでは状況に応じて「ドリフト状態」を設定し、その後どのトラクション値を使用するかを決定します。

最後の手順は、速度を新しい進行方向に合わせて補間することです。この行を変更してください。

```gdscript
velocity = new_heading * velocity.length()
```

をこれに：

```gdscript
velocity = lerp(velocity, new_heading * velocity.length(), traction)
```

![alt](/godot_recipes/4.x/img/3d_car_06.gif)

### まとめ

この段階では、車の挙動を幅広く調整できる多数のパラメーターがあります。求める運転スタイルによっては、ここで示した数値とは大きく異なる設定が必要になる場合もあります。

さらに学びたい方のために、フォローアップレシピで扱うトピックをいくつかご紹介します。

* 車両カメラ制御およびカメラ操作
* AI／NPCの制御（ステアリング、障害物回避、走行ライン追従）
* 斜面やスロープ地形への対応機能

## 関連レシピ

- [運動車：基本モデル](/godot_recipes/4.x/ja/3d/kinematic_car/car_base/)
- [2D: 車両のステアリング制御レシピ](/godot_secrets/3.x/2d/car_steering)
- [入力アクション設定](/godot_recipes/4.x/ja/input/input_actions/)
- [3D: CharacterBody3Dの移動機能](/godot_recipes/4.x/ja/3d/kinematic_body/)

#### この動画が気に入ったら？

