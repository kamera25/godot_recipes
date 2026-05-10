---
title: "Tween"
weight:
draft: true
ghcommentid:
tags: []
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## {{< gd-icon Tween >}}`Tween` アニメーション処理

{{< gd-icon Tween >}}`Tween`ノードは、時間経過に伴うプロパティのアニメーション化や補間処理が必要な場合に非常に便利です。アニメ制作において「トゥイニング」という用語をご存知かもしれませんが、これはキーフレーム間の中間値を生成するプロセスを指す専門用語です。

### 補間オプション

* `interpolate_property()`

* `interpolate_method()` 関数

### 移行タイプ

`trans_type` パラメーターを使用することで、補間に使用する遷移タイプを選択できます。これは、各フレームにおけるプロパティ値を計算するための数学的公式を指定するものです。異なるタイプのトランジションは、それぞれ特徴的な移動パターンを生成します。以下に示すように、各アイコンの`position`値は同一の範囲と時間範囲でTween処理されます。

![alt](/godot_recipes/4.x/img/tween_01.gif)

{{% notice note %}}
{{% /notice %}}

## 関連レシピ

- []()

<!-- #### Videoが気に入ったら？ -->

{{< youtube  >}} -->