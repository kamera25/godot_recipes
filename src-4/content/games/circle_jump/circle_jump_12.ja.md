---
title: "設定を保存しよう"
weight: 12
draft: false
pre: "12. "
---

## 設定の保存について

ゲームに追加した3つの切り替え可能プロパティは正常に動作していますが、アプリケーションを終了すると設定が保存されません。次回起動時にも同じ設定値が保持されるよう、これらを設定が必要です。

まず、設定ファイル `res://settings.gd` で定義を行います。

```gdscript
var settings_file = "user://settings.save"
```

次に、保存したい3つのゲーム設定について、保存／読み込み機能を追加していきます。

```gdscript
func save_settings():
    var f = File.new()
    f.open(settings_file, File.WRITE)
    f.store_var(enable_sound)
    f.store_var(enable_music)
    f.store_var(enable_ads)
    f.close()

func load_settings():
    var f = File.new()
    if f.file_exists(settings_file):
        f.open(settings_file, File.READ)
        enable_sound = f.get_var()
        enable_music = f.get_var()
        self.enable_ads = f.get_var()
        f.close()
```

`load_settings()` を呼び出すタイミングを次のように変更してください。
- `set_enable_ads()` の終了時に `_ready()` 内で呼び出す
- `save_settings()` の終了時にも同じく `_ready()` 内で呼び出す
さらに、`Screens.gd` ファイルでは、サウンド/音楽設定が変更された際に状態を保持する必要があるため、match 文内の各ケース部分に `settings.save_settings()` を追加が必要です。

別の課題として、ゲーム起動時に設定メニューのアイコンが保存ファイルから読み込んだ状態を反映しない問題があります。これは`register_buttons()`関数で対処できます。すでにこの関数は全てのボタンをループ処理してシグナル接続を行っています。

```gdscript
for button in buttons:
    button.connect("pressed", self, "_on_button_pressed", [button])
    match button.name:
        "Ads":
            if settings.enable_ads:
                button.text = "Disable Ads"
            else:
                button.text = "Enable Ads"
        "Sound":
            button.texture_normal = sound_buttons[settings.enable_sound]
        "Music":
            button.texture_normal = music_buttons[settings.enable_music]
```

## スクリーンについて

このセクションに追加するもう一つの要素は「ゲームについて」画面です。これはプレイヤーがこのゲームの概要を把握し、ライセンス情報とこのページへのリンクを確認するためのものです。本作はチュートリアルゲームであるため、このような情報提供が不可欠です。

{{% notice warning %}}
ライセンス条件を遵守することは非常に重要です。Godotで求められる要件については、以下のページを参照してください。[ライセンス遵守について](https://docs.godotengine.org/ja/4.x/about/complying_with_licenses.html)。なお、使用するアートワークについても、クレジット表記やリンク、その他の謝辞が必要となる場合があることにご注意ください。
{{% /notice %}}

これに到達するために、「タイトル」画面に新規ボタンを追加しました。

![alt](/godot_recipes/3.x/img/cj_12_01.png)

ボタンは他のボタンと同様に設定されています。「ボタン」グループに追加して登録されるようにしてください。`Screens.gd`ファイルで、このボタンの名前を対象とするもう一つの`match`を追加します。

```gdscript
"About":
    change_screen($AboutScreen)
```

以下に「バージョン情報」画面の表示内容を示します。

![alt](/godot_recipes/3.x/img/cj_12_02.png)

「BaseScreen.tscn」を継承し、ここにテキスト編集エリアとホームボタン用のコンテナを追加しました。

「テキストエディター」設定で［_BBCode］を有効にし、［テキスト］プロパティに以下を入力します。

```text
[center][u]Circle Jump[/u]

[img]res://assets/images/godot_logo.png[/img][/center]

Circle Jump is an open source tutorial game made with the Godot Game Engine. You can find the tutorial and the game's source code here:

[url=https://github.com/kidscancode/circle_jump]Circle Jump Source[/url]

Copyright © 2019 KidsCanCode

[url=https://github.com/kidscancode/circle_jump/blob/master/LICENSE]License Information[/url]
```

{{% notice note %}}
BBCodeの書式設定に関する詳細な仕様については、[RichTextLabelにおけるBBCode](https://docs.godotengine.org/ja/4.x/tutorials/ui/bbcode_in_richtextlabel.html)のドキュメントを参照してください。
{{% /notice %}}

URL をクリック可能にするには、`TextEdit` の `meta_clicked` シグナルを接続します。

```gdscript
func _on_TextEdit_meta_clicked(meta):
    OS.shell_open(meta)
```

----------

#### GitHubでプロジェクトをフォローしてください！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画の方がお好みですか？

{{< youtube h5987aIENqs >}}