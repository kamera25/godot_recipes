---
title: "オーディオマネージャー"
weight: 1
draft: false
ghcommentid: 80
---

## 課題

オブジェクトが破壊されたり収集された際に再生するために `オーディオStreamPlayer` をモブ/コインなどに追加しました。ただ、対象のオブジェクトを削除すると、オーディオプレイヤーも同時に削除され、音が途切れる問題が発生します。より簡単に音声を管理できる方法を教えてください。

## 解決策

この問題を解決するため、SceneTreeのどこからでもアクセス可能なノードを使用します。このノードは一連の`オーディオStreamPlayer`ノードと、再生するサウンドストリームのキューを管理します。

スクリプトエディターで新しいスクリプトを作成します。

```gdscript
extends Node

var num_players = 8
var bus = "master"

var available = []  # The available players.
var queue = []  # The queue of sounds to play.


func _ready():
    # Create the pool of AudioStreamPlayer nodes.
    for i in num_players:
        var player = AudioStreamPlayer.new()
        add_child(player)
        available.append(player)
        player.finished.connect(_on_stream_finished.bind(player))
        player.bus = bus


func _on_stream_finished(stream):
    # When finished playing a stream, make the player available again.
    available.append(stream)


func play(sound_path):
    queue.append(sound_path)


func _process(delta):
	# Play a queued sound if any players are available.
    if not queue.empty() and not available.empty():
        available[0].stream = load(queue.pop_front())
        available[0].play()
        available.pop_front()
```

このスクリプトをプロジェクト設定で 自動読み込み に設定してください。「オーディオManager」のように、わかりやすく認識しやすい名前を付けてください。

![alt](/godot_recipes/4.x/img/audio_mgr_01.png)

プロジェクト内で音を再生したい任意の場所で、以下を使用してください。

```gdscript
AudioManager.play("res://path/to/sound")
```

覚えておくと便利ですが、サウンドファイルをテキストエディターに直接ドラッグ＆ドロップすることで、ファイルパスを簡単に貼り付けることができます。

{{% notice note %}}
この音声マネージャーは、[SFXPlayer by TheDuriel](https://github.com/TheDuriel/DurielsGodotUtilities) の協力を得て適応されています
{{% /notice %}}

### サンプルプロジェクト例

以下に、オーディオマネージャーノードの使用例を示すサンプルプロジェクトをダウンロードできます。このプロジェクトでは、音声ファイルを格納したフォルダを読み込み、ボタングリッドを生成します。ボタンをクリックすると、対応するサウンドが再生されます。

![alt](/godot_recipes/4.x/img/audio_mgr_02.png)

上部に、音声マネージャーのリアルタイム統計が表示されます。

<!-- ## 関連するレシピ
 -->


<!-- #### Videoが気に入ったら？ -->

{{< youtube 7axJJYont6Y >}} -->

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトのサンプルコードはこちらからダウンロードできます。[https://github.com/godotrecipes/audio_manager](https://github.com/godotrecipes/audio_manager)
