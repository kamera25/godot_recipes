---
title: "コヨーテタイム"
weight: 5
draft: false
---

## 課題

プラットフォームゲームのジャンプ操作に違和感があります。プレイヤーはコントロールが取りづらく、場合によっては足場に正しく飛び降りられないことがあります。

## 解決策

この問題を解決するには、「コヨーテ・タイム」と呼ばれるテクニックが有効です。これはプレイヤーにより高い操作感覚と、プラットフォームの端を移動するプロセスにおいて若干の「余裕時間」を提供します。また、プレイヤーがより自然にジャンプ操作を行えるようになります。

「コヨーテタイム」の仕組みは以下の通りです。

プレイヤーがプラットフォームの端から離れた場合、数フレームの間は依然として地面にいるかのようにジャンプできます。

{{% notice style="info" title="そもそもなぜコヨーテ？" %}}
「コヨーテタイム」という名称は、地面を見下ろすまで落下しないカートゥーンキャラクターのコヨーテに由来しています。

![alt](/godot_recipes/4.x/img/coyote.png)
 {{% /notice %}}


この機能を既存のプラットフォームキャラクターに追加してください。設定方法については[プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)を参照してください。

タイミング処理に関しては、`CoyoteTimer`という名前の{{< gd-icon Timer >}}`Timer`ノードを追加し、設定を**ワンショットモード**にします。

コヨーテタイム管理に必要な新しい変数がいくつかあります。

```gdscript
var coyote_frames = 6  # How many in-air frames to allow jumping
var coyote = false  # Track whether we're in coyote time or not
var last_floor = false  # Last frame's on-floor state
```

フレーム単位で時間を設定しているため、`_ready()`内で{{< gd-icon Timer >}}`Timer`の長さを設定する際にも次のように変換できます。

```gdscript
$CoyoteTimer.wait_time = coyote_frames / 60.0
```

各フレームで現在の `is_on_floor()` 値を保存し、次のフレームで使用するようにします。したがって、`move_and_slide()` の後に `_physics_process()` 内に以下を設定します。

```gdscript
    last_floor = is_on_floor()
```

ジャンプ入力を検知した場合、キャラクターが床にいる状態か、またはコヨーテ時間モードかどうかを確認します。

```gdscript
    if Input.is_action_just_pressed("jump") and (is_on_floor() or coyote):
        velocity.y = jump_speed
        jumping = true
```

コヨーテ状態への移行は、プレイヤーがプラットフォームの端から降りた瞬間に開始されます。これは、前回のフレームでは床の上にいたが、現在は床から離れた位置にいるということです。この条件を確認した上で、ちょうど「オンフロア」から「オフフロア」に移行した場合のみ、タイマーを起動できます。

```gdscript
    if !is_on_floor() and last_floor and !jumping:
        coyote = true
        $CoyoteTimer.start()
```

「CoyoteTimer」は以下のタイミングでコヨーテ状態の終了を通知します。

```gdscript
func _on_coyote_timer_timeout():
    coyote = false
```

{{% notice style="tips" title="3Dキャラクターへの実装方法" %}}
この手順は3Dキャラクターにも同様の方法で適用できます。
{{% /notice %}}

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

[動くプラットフォーム](/godot_recipes/4.x/ja/2d/moving_platforms) プロジェクト内のキャラクターにはコヨーテタイムが実装されています。

プロジェクトコードはこちらからダウンロードできます。 [https://github.com/godotrecipes/2d_moving_platforms](https://github.com/godotrecipes/2d_moving_platforms)

## 関連レシピ

- [プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)
