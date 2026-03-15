---
title: "AdMobプラグインを更新しています（バージョン 3.2.1）"
weight: 13
draft: true
pre: "13. "
---

## Installation

[パート11](/godot_recipes/3.x/games/circle_jump/circle_jump_11/) でモバイル広告の設定を行って以降、GodotによるAndroidプラグイン処理とAdMob SDKには重要な更新が加えられています。もし現在ゲームが正常に動作している場合、現時点では特に変更を加える必要はないでしょう（まだ）。新規プロジェクトを開発中の場合は、以下の手順に従うことをお勧めします。

以前と同様に、[Shin-NiL Android AdMobプラグイン](https://github.com/Shin-NiL/Godot-Android-Admob-Plugin)を使用しています。「リリース」タブからzipファイルをダウンロードしてください。

最初のステップは、プロジェクトにAndroidカスタムビルドテンプレートをインストールすることです：

![alt](/godot_recipes/3.x/img/admob_3.2_03.png)

プラグインを解凍し、`admob-plugin` フォルダを `res://android/` ディレクトリに、`admob-lib` フォルダを `res://` ディレクトリに配置してください。

以下の2ファイルを編集する必要があります。

* `res://android/build/gradle.properties`

以下の行を追加してください。

```
android.useAndroidX=true
android.enableJetifier=true
```

* `res://android/admob-plugin/AndroidManifest.conf`

AdMobアプリケーションIDを`android:value=""/>`行に貼り付けてください。サンプルのアプリIDは置き換える必要があります。

## 設定

これで `AdMob` ノードを `Main` シーンに追加できます。

![alt](/godot_recipes/3.x/img/admob_3.2_01.png)

クリックしてみると、ノードの設定に使用するエクスポート済みプロパティセットが表示されます。ここで広告ユニットIDを貼り付け、本番広告やテスト広告などを構成していきます。

![alt](/godot_recipes/3.x/img/admob_3.2_02.png)

注: 「AdMob」ノードは接続可能なシグナルを提供しており、広告の読み込み完了、クローズ、ロード失敗時に通知されます。このゲームでは「リワード型」広告は使用していませんが、これらのシグナルを利用すれば適切なタイミングで報酬を付与することができます。


以前のプラグインを使用していた場合、`settings`シングルトン内でプラグインの初期化と広告の表示/非表示処理を実装していました。しかし、`AdMob`ノードがこの機能を管理できるようになったため、このコードは不要になりました。代わりに、`Main`内の該当呼び出し箇所を`AdMob`ノードへの呼び出しに置き換えます。

```gdscript
onready var admob = $Admob
```

これまでsettings.hide_ad_banner()などを呼び出していた箇所は、すべて以下の新しい同等関数で置き換え可能です

```gdscript
admob.show_interstitial()

admob.show_banner()
```