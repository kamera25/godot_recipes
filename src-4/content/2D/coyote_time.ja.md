---
title: "Coyote Time"
weight: 5
draft: false
---

## 問題文

Your platformer jumping feels "off". Players don't have good control and sometimes they "miss" jumping off the edge of platforms.

## 解決策

The answer to this problem is to use a technique called "coyote time". This gives the player a greater feeling of control and a little "wiggle room" around the process of jumping from the edges of platforms.

"Coyote time" works like this:

プレイヤーがプラットフォームの端から離れた場合、数フレームの間は依然として地面にいるかのようにジャンプできるようにしています。

{{% notice style="info" title="Origins" %}}
The name "coyote time" comes from the famous cartoon coyote, who wouldn't fall until he looked down:

![alt](/godot_recipes/4.x/img/coyote.png)
 {{% /notice %}}


この機能を既存のプラットフォームキャラクタに追加します。設定方法については[プラットフォームキャラクタレシピ](/godot_recipes/4.x/2d/platform_character/)を参照してください。

タイミング処理に関しては、`CoyoteTimer`という名前の`タイマー`ノードを追加し、設定を**ワンショットモード**にします。

コヨーテの時間管理に必要な新しい変数がいくつかあります：

```gdscript
var coyote_frames = 6  # How many in-air frames to allow jumping
var coyote = false  # Track whether we're in coyote time or not
var last_floor = false  # Last frame's on-floor state
```

フレーム単位で時間を設定しているため、`_ready()`内で`Timer`の長さを設定する際にも次のように変換できます：

```gdscript
$CoyoteTimer.wait_time = coyote_frames / 60.0
```

各フレームで現在の `is_on_floor()` 値を保存し、次のフレームで使用するようにします。したがって、`move_and_slide()` の後に `_physics_process()` 内に以下を設定してください：

```gdscript
    last_floor = is_on_floor()
```

ジャンプ入力を検知した場合、キャラクターが床にいる状態か、またはコヨーテ時間モードかどうかを確認する必要があります：

```gdscript
    if Input.is_action_just_pressed("jump") and (is_on_floor() or coyote):
        velocity.y = jump_speed
        jumping = true
```

コヨーテ状態への移行は、プレイヤーがプラットフォームの端から降りた瞬間に開始されます。これはつまり、前回のフレームでは床の上にいたが、現在は床から離れた位置にいるということを意味します。この条件を確認した上で、ちょうど「オンフロア」から「オフフロア」に移行した場合のみ、タイマーを起動することができます：

```gdscript
    if !is_on_floor() and last_floor and !jumping:
        coyote = true
        $CoyoteTimer.start()
```

「CoyoteTimer」は以下のタイミングでコヨーテ状態の終了を通知します：

```gdscript
func _on_coyote_timer_timeout():
    coyote = false
```

{{% notice style="tip" title="Implementing in 3D" %}}
You can apply the same process to 3d characters.
{{% /notice %}}

## <i class="fas fa-code-branch"></i> Download This Project

[動くプラットフォーム](/godot_recipes/4.x/2d/moving_platforms) プロジェクト内のキャラクターにはコヨーテタイムが実装されています。

プロジェクトコードはこちらからダウンロードできます: [https://github.com/godotrecipes/2d_moving_platforms](https://github.com/godotrecipes/2d_moving_platforms)

## 関連レシピ

* [プラットフォームキャラクタ](/godot_recipes/4.x/2d/platform_character/)
