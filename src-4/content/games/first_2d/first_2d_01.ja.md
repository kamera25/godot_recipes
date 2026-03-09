---
title: "Project Setup"
weight: 1
draft: false
pre: "01. "
---

この最初のゲームプロジェクトでは、初めてGodot Engineでゲームを作成する手順をご案内します。事前の経験は必要ありませんが、少なくとも[『Godot 101：入門ガイド』](/godot_recipes/4.x/g1intr/start/)セクションに目を通していることが望ましいです。ここでは、エディタインターフェースやGodot UIの操作方法について学ぶことができます。

{{% notice style="note" title="Why start with 2D?"%}}
In a nutshell, 3D games are much more complex than 2D ones. However, many of the underlying game engine features you'll need to know are the same. You should stick to 2D until you have a good understanding of Godot's workflow. At that point, the jump to 3D will feel much easier.
{{% /notice %}}

Open Godot and start a new project. You can name it anything you'd like - we're going with "Classic Shmup", since this is a traditional shoot-em-up style game.

## アートワークのダウンロード方法

ゲームで使用するアートワークは、itch.ioからダウンロードできます：
[Grafxkid氏によるミニピクセルパック](https://grafxkid.itch.io/mini-pixel-pack-3)

アートワークパックを解凍し、プロジェクトにコピーするには、フォルダを[ファイルシステム]タブにドラッグアンドドロップしてください。

![alt](/godot_recipes/4.x/img/2d_101_01.png)

## プロジェクト設定

Next, we need to set up some project-wide settings. Open **Project Settings** and check the "Advanced Settings" toggle in the upper-right.

* **表示/ウィンドウ** セクションにおいて：

    * **ウィンドウ幅の上書き** & **ウィンドウ高さの上書き** を `480`, `640` に設定。
    * **伸縮モード** を `canvas_items` に指定。

これらの設定により、ゲームが適切なサイズで表示されるようになります。ピクセルアートを使用しているため、画像自体は極端に小さく、古い機種向けの解像度である「240×320」でも問題なく表示されます。ただし現代のモニターではこのサイズは画面に対してかなり小さいため、他の設定で比例的に拡大表示することが可能です。1080pモニターをお使いの場合は、オーバーライド値を「720×96ą」に変更することもできます。また、ゲーム実行中にウィンドウサイズを変更することもできるようになります。

* **キャンバステクスチャ**セクションの**レンダリング/テクスチャ**設定で、**デフォルトテクスチャフィルタ**を「ニアレスト」に設定してください。これにより、美しいピクセルアートが鮮明なまま保たれ、左側ではなく右側のようなきれいな表示になります：

![alt](/godot_recipes/4.x/img/2d_101_02.png)

* Click the **Input Map** tab at the top of the **Project Settings** window. This is where we can set up the inputs we want to use in the game. In the "Add New Action" box, type the following, hitting `<enter>` after each to add it to the list of actions: `right`, `left`, `up`, `down`, `shoot`. To assign key(s) to each named input, click the **+** button to its right and press the key on your keyboard. When you're done, you should have something like this:

<img src=\ alt=\>

他のキー設定を使いたい場合は、自由に変更してください。

## 次のステップ

設定は完了しました。いよいよ開始できます！次のセクションでは、プレイヤーが操作する宇宙船を作成します。

| {{% button href="/godot_recipes/4.x/games/first_2d/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_02/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
