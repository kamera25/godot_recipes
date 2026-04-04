---
title: "ラベル"
weight: 1
draft: false
ghcommentid: 55
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
{{% /notice %}}

## 課題

画面にテキストを表示したい。

## 解決策

スクリーンにテキストを表示する機会が増えるでしょう。例えば、タイトル表示やカウントダウンタイマー、スコアカウンターなどがその一例です。これらのほとんどは、Godotの {{< gd-icon Label >}}`Label` ノードを使えば簡単に実装できます。

### フォント操作について

はじめに、フォントファイルが必要になります。Godotのフォントサポートについては別のレシピで詳しく解説しますが、ここではTTFまたはOTF形式のフォントファイルを前提とします。ビットマップフォントを使用する場合は、関連するレシピを参照してください。

{{% notice note %}}
この例では、人気のある無料フォント「Roboto」を使用します。このフォントは[Google Fonts](https://fonts.google.com/specimen/Roboto)で入手できます。こちらからもダウンロードできます。 [Roboto_font.zip](/godot_recipes/4.x/ja/files/Roboto_font.zip)
{{% /notice %}}

### ラベルの追加方法

シーンに新しい {{< gd-icon Label >}}`Label`ノードを追加します。インスペクターでは、ほとんどのプロパティが自明な内容になっています（マウスカーソルを合わせると説明が表示されます）：

![alt](/godot_recipes/4.x/img/ui_label_properties.png)

「テキスト」フィールドに任意の文字を入力して、表示スタイルを試してみます。デフォルトフォントが設定されていますが、かなりシンプルな（しかも小さい）デザインになっています。

#### `DynamicFont`の追加方法

フォントを追加するには：インスペクターで「カスタムフォント」セクションまでスクロールダウンし、展開してください。空の「フォント」プロパティで『新規ダイナミックフォント』を選択し、新しく表示された`DynamicFont`をクリックしてさらに展開します。

![alt](/godot_recipes/4.x/img/ui_label_font_properties.png)

フォントファイル（この例では`Roboto-Medium.ttf`を使用しています）を*フォントデータ*プロパティにドラッグするか、「読み込み」を選択して直接ファイルを指定します。調整すべきプロパティは複数ありますが、まずは*サイズ*を少し大きくしてみます。

テキストの表示に与える影響を自由に調整してみてください。例えば、以下の画像では、2番目のラベルに*フィルター*プロパティが有効になっています。

![alt](/godot_recipes/4.x/img/ui_label_font_filter.png)

#### 色の調整

ラベルのフォントカラーは「カスタムカラー」セクションで調整できます。ここでは「フォントカラー」を変更できるほか、影の色を追加することもできます。影のプロパティは「カスタム定数」セクションで設定します。

![alt](/godot_recipes/4.x/img/ui_label_font_colors.png)

### 動的に変化するテキスト表示

シーンに静的テキストのみが必要な場合、ここで完了です。ただし、ラベルを動的に更新する必要がある場合は、コード内で`text`プロパティを使用して実装できます。

{{< gd-icon Timer >}}`Timer`ノードがシーンに含まれている場合、以下のように操作できます。

```gdscript
extends Control

var counter = 0

func _ready():
    $Label.text = str(counter)

func _on_Timer_timeout():
    counter += 1
    $Label.text = str(counter)
```

ラベルの使用例やUIノードとの連携方法については、[関連レシピ](#関連レシピ)セクションをご覧ください。

<!-- {{% notice note %}}
プロジェクトファイルをこちらからダウンロードしてください: [screen_shake.zip](/godot_recipes/4.x/ja/files/screen_shake.zip)
{{% /notice %}} -->

## 関連レシピ

<!-- - [ノイズ](/godot_recipes/4.x/ja/math/noise/) -->


#### この動画が気に入ったら？

<!-- {{< youtube C-Sn55e5wnk >}} -->