---
title: "Godot 4 ゲーム開発チュートリアル＆レシピ"
description: "Godot 4のゲーム開発チュートリアル、実装レシピ、GDScriptのサンプルコードを日本語で解説。2D・3D・入力・物理・UIを初心者から学べます。"
date: 2019-04-09T22:57:31-07:00
draft: false
---

# <i class='fas fa-utensils'></i>&nbsp;Godotレシピ

> Godotのノードは、いわば料理の具材。君なら、どんな一品を作ってみる？

このサイトでは、ゲームシステムを構築するための解決策と実例を提供しています。

{{% notice style="tip" title="Godotのバージョン"%}}
このサイトにはGodot 4.x向けのチュートリアルとサンプルが含まれています。一部の記事はGodot 3からの更新作業中であるため、旧バージョンの記述が残っている場合があります。<br>
オリジナルの英語版Godot 3.xレシピについては、KidsCanCodeの[Godot Recipes](https://kidscancode.org/godot_recipes/3.x/)をご覧ください：<br>
{{% button href="https://kidscancode.org/godot_recipes/3.x/" style="primary" icon="utensils" %}}Godot 3レシピ集（原文・英語）{{% /button %}}
{{% /notice %}}

ゲーム開発を学ぶ準備はできていますか？趣味として、あるいは夢のキャリアへの最初の一歩として、今ほど良いタイミングはありません。現代のプログラミング言語とツールを駆使すれば、高品質なゲームを簡単に作成できます。また世界中に向けて配信できます。その中の一つがGodotゲームエンジンです。初心者でもゲーム開発技術を楽しく、親しみやすい方法で学ぶことができます。一方、経験豊富な開発者にとっては、自らのビジョンを形にするための強力なツールです。カスタマイズも可能で、オープンソースとして利用できます。

![Godot logo](/godot_recipes/4.x/img/godot3_logo.png?width=400px)

このサイトでは、Godotゲームエンジンの初心者向けガイドをはじめ、さまざまなゲーム開発のヒントやテクニックを幅広く紹介しています。サイドバーのコンテンツを自由に閲覧して、興味のある分野を見てみてください。

Godotを初めて使う方はまずは [Godotとは？](/godot_recipes/4.x/ja/g101/start/101_01/) から始めてください。

### おすすめの学習順序

初めてゲームを作るなら、[Godotとは？](/godot_recipes/4.x/ja/g101/start/101_01/) → [GDScript入門](/godot_recipes/4.x/ja/g101/gdscript/) → [はじめての2Dゲーム](/godot_recipes/4.x/ja/games/first_2d/) の順に進むと、エディター操作・スクリプト・ゲーム制作をつなげて学べます。その後は、[2D](/godot_recipes/4.x/ja/2d/) のキャラクター操作や衝突判定、[入力](/godot_recipes/4.x/ja/input/) と [カメラ](/godot_recipes/4.x/ja/2d/touchscreen_camera/) を組み合わせて、自分のゲームへ発展させてください。

[はじめてのGodot](/godot_recipes/4.x/ja/g101/)、[2D](/godot_recipes/4.x/ja/2d/)、[3D](/godot_recipes/4.x/ja/3d/)、[入力](/godot_recipes/4.x/ja/input/)、[物理](/godot_recipes/4.x/ja/physics/)、[UI](/godot_recipes/4.x/ja/ui/) の各セクションを参照して、適切なトピックを見つけてください。

### このサイトの利用方法

#### 初心者の方へ

ゲーム開発が初めての場合は、まず [はじめてのGodot(基礎編)](/godot_recipes/4.x/ja/basics/) のセクションから始めてください。ここではGodotアプリケーションの概要を学びます。次に、プロジェクトを段階的に作成していきます。学ぶべきことは多岐にわたりますが、最初はすべてを理解する必要はありません。最初は複雑に感じられる概念も含まれるため、繰り返し学習することが不可欠です。Godotの各種機能を実際に操作すればするほど、その使い方に慣れ、次第に「簡単」だと感じられるようになります。

{{% notice info %}}
このサイトは、プログラミングに関する基本的な経験があることを前提としています。もし完全に未経験で Godot をさわり始める場合は先に、[初心者向けの学習ガイド](https://docs.godotengine.org/ja/stable/getting_started/step_by_step/index.html)をご覧ください。
{{% /notice %}}

#### 経験豊富な開発者へ

経験豊富な開発者の方や、他のゲームエンジンに精通している方は、左側のメニューから興味ある分野をご覧ください。「Godot流(Godot Way)」の手法で各種タスクを実行する方法を詳細に解説しています。有用なガイドやチュートリアルを多数用意しています。すべての記事について、サンプルコードと実践的なプロジェクト例も提供しています。
