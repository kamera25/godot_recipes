---
title: "ハート容器：3つの方法"
weight: 5
draft: false
---

## 課題

ハート型のコンテナバー（または他のアイコンベースのバー）を表示する必要があります。

## 解決策

プレイヤーの体力を表示する一般的な方法として、一連のアイコン（通常はハートマーク）を使用する手法があります。プレイヤーがダメージを受けると、これらが徐々に消失していきます。

本レシピでは、以下の3つの方法でこの情報を表示する方法をご紹介します。「簡易表示」「空欄表示」、そして「部分表示」です。

![alt](/godot_recipes/4.x/img/heart_bar_02.png)

この画像はプレイヤーが「3」の体力を持っている時、バーに表示される内容を表しています。

* **シンプル表示**：ハートのみを表示します。
* **空の状態表示**：空き容量があるハートコンテナを表示します。
* **部分充填表示**：プレイヤーが部分的に満たされたコンテナを持つことを許可します。

### バーの設定手順

使用している心臓画像のサイズは53×45ピクセルです。以下から入手できます：

[ケンニードットネット：プラットフォーマーアートデラックス](https://kenney.nl/assets/platformer-art-deluxe)

Ideally, your heart bar will be easy to drop into your overall HUD/UI. It therefore makes sense to make it a separate scene. We'll start with an {{< gd-icon HBoxContainer >}}`HBoxContainer` which will keep things aligned. Set the **Theme Overrides/Constants/Separation** to `5`.

{{< gd-icon TextureRect >}}`TextureRect` 子要素を追加します。ハートテクスチャを **テクスチャ** プロパティにドラッグし、**[伸縮モード]** を「固定」に設定してください。ノード名を「1」に指定したら、"Ctrl+D"を押して必要な数（この例では5つ）のハート用に同じノードを複製します。最終的なノード構成は以下のようになります。

![alt](/godot_recipes/4.x/img/heart_bar_03.png)

### スクリプトの追加方法

以下のスクリプトは3種類すべてのバー構成に対応できるよう設計されています。ゲームで実際に使用するモードは1つで済むはずなので、他のモードに関連するコードは削除しても構いません。

まず、必要なテクスチャを読み込み、3つのバーモードを定義します。

```gdscript
extends HBoxContainer

enum modes {SIMPLE, EMPTY, PARTIAL}

var heart_full = preload("res://assets/hud_heartFull.png")
var heart_empty = preload("res://assets/hud_heartEmpty.png")
var heart_half = preload("res://assets/hud_heartHalf.png")

@export var mode : modes

func update_health(value):
    match mode:
        MODES.simple:
            update_simple(value)
        MODES.empty:
            update_empty(value)
        MODES.partial:
            update_partial(value)
```

バーに対して `update_health()` を呼び出すと、選択されたモードに基づいて渡された値が表示されます。

{{% notice note %}}
入力値に対する境界チェックは行いません。ゲームで健康度を実装する方法には様々な方法があるため、これについては開発者の裁量に委ねられています。
{{% /notice %}}

まず、`update_simple()` メソッドについて説明します。この処理では、ハートコンテナを順にループしながら、各 `{{< gd-icon TextureRect >}}TextureRect` の表示状態を設定します。

```gdscript
func update_simple(value):
    for i in get_child_count():
        get_child(i).visible = value > i
```

`update_empty()` は非常に似ていますが、アイコンを隠す代わりに、そのテクスチャを空のコンテナー用に変更します。

```gdscript
func update_empty(value):
    for i in get_child_count():
        if value > i:
            get_child(i).texture = heart_full
        else:
            get_child(i).texture = heart_empty
```

最後に、部分的に充填された容器については、第三のテクスチャと可能な値の数が2倍になります。

```gdscript
func update_partial(value):
    for i in get_child_count():
        if value > i * 2 + 1:
            get_child(i).texture = heart_full
        elif value > i * 2:
            get_child(i).texture = heart_half
        else:
            get_child(i).texture = heart_empty
```

以下に各バーモードの使用例を示します。

![alt](/godot_recipes/4.x/img/heart_bar_04.gif)

## まとめ

このハートバーの設定を独自のHUD作成の基礎として活用してください。この手法をさらに拡張すれば、多種多様な情報表示をサポートすることができます。

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらでダウンロードできます。 [https://github.com/godotrecipes/heart_bars](https://github.com/godotrecipes/heart_bars)

<!-- {{% notice note %}}
プロジェクトファイルはこちらからダウンロードできます: [heart_bars.zip](/godot_recipes/3.x/files/heart_bars.zip)
{{% /notice %}} -->

## 関連レシピ

- [UI：コンテナー](/godot_recipes/3.x/ui/containers/) -->