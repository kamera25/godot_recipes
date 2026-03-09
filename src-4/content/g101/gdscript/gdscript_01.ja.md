---
title: "Getting started"
weight: 1
draft: false
ghcommentid: 90
pre: "01. "
---

## 概要

スクリプトをノードやその他のオブジェクトに割り当てることが、ゲームの動作やメカニクスを構築する方法です。例えば、{{< gd-icon Sprite2D >}}`Sprite2D`ノードは自動的に画像を表示しますが、画面上で移動させるには、速度や移動方向などを制御するスクリプトを追加する必要があります。

これはインスペクターを使用する場合と同様と考えてください。GDScriptはGodotノードに関するあらゆる知識を持ち、それらへのアクセス方法を知っているだけでなく、動的に変更することも可能です。

[Godot公式ウェブサイトのGDScriptドキュメント](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html)は、言語の基本を理解するための最適なリソースです。時間を取ってしっかり読み込むことを強くお勧めします。

**GDScript は Python ですか？**

You'll often read comments to the effect that "GDScript is based on Python". That's somewhat misleading; GDScript uses a _syntax_ that's modeled on Python's, but it's a distinct language that's optimized for and integrated into the Godot engine. That said, if you already know some Python, you'll find GDScript looks very familiar.

{{% notice warning %}}
多くのチュートリアル（およびGodot自体）では、ある程度のプログラミング経験があることを前提としています。これまで一度もコードを書いたことがない場合、Godotを学ぶのは困難に感じるかもしれません。ゲームエンジンを習得するだけでも大きな挑戦ですが、同時にコーディングも学ぶとなると、負担はさらに大きくなります。もしこのセクションのコードで苦戦しているなら、初心者向けプログラミング講座（Pythonがおすすめです）を履修することで、基本的な概念をしっかりと理解できるはずです。
{{% /notice %}}

## スクリプトの構成要素

GDScriptファイルの最初の行は`extends <クラス名>`で始めなければなりません。ここで`<クラス名>`は、既存の組み込みクラスまたはユーザーが定義したカスタムクラスのいずれかを指定します。たとえば、{{< gd-icon CharacterBody2D >}}`CharacterBody2D`ノードにスクリプトをアタッチする場合、スクリプトの冒頭は`extends CharacterBody2D`となります。これは、お使いのスクリプトが組み込みの`CharacterBody2D`オブジェクトの持つ機能をすべて引き継ぎ、さらにユーザー定義の追加機能で拡張していることを意味します。

In the rest of the script, you can define any number of variables (aka "class properties") and functions (aka "class methods").

## スクリプトの作成方法

最初のスクリプトを作成しましょう。覚えておくべきは、どのノードにもスクリプトをアタッチできるということです。

Open the editor and add a {{< gd-icon Sprite2D >}}`Sprite2D` node to empty scene. Right-click on the new node, and choose "Attach Script". You can also click the button next to the search box.

![alt](/godot_recipes/4.x/img/gds_01_attach.png?width=250)

Next you need to decide where you want the script saved and what to call it. If you've named the node, the script will automatically be named to match it (so unless you've changed anything this script will likely be called "sprite2d.gd").

スクリプトエディタウィンドウが開きます。ここに、新しく作成した空のスプライト用スクリプトが表示されます。Godotは自動的にいくつかのコード行と、各コードの機能を説明するコメントを自動生成しています。

```gdscript
extends Sprite2D

# Called when the node enters the scene tree for the first time.
func _ready():
    pass # Replace with function body.

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta):
    pass
```

```gd
スクリプトが {{< gd-icon Sprite2D >}}`Sprite2D` に追加されたため、最初の行は `extends Sprite2D` に自動的に設定されます。このスクリプトは {{< gd-icon Sprite2D >}}`Sprite2D` クラスを継承しているため、{{< gd-icon Sprite2D >}}`Sprite2D`ノードが提供するすべてのプロパティとメソッドにアクセスして操作することが可能になります。

{{% notice title="Properties and methods" style="note" %}}
*Properties* and *methods* are two terms which specifically mean *variables* and *functions* that are defined in an object. Programmers tend to use the terms interchangeably.
{{% /notice %}}

After that is where you're going to define all the variables you will use in the script, the "member variables". You define variables with the 'var' keyword - as you can see by the comment examples.

どうぞコメントを削除して、次の部分について話しましょう。

Now we see a function called `_ready()`. In GDScript you define a function with the keyword "func". The `_ready()` function is a special one that Godot looks for and runs whenever a node is added to the tree, for example when we hit "Play".

Let's say that when the game starts, we want to make sure the sprite goes to a particular location. In the Inspector, we want to set the **Position** property. Notice that it's in the section called "Node2D" - that means this is a property that *any* {{< gd-icon Node2D >}}`Node2D` type node will have, not just {{< gd-icon Sprite2D >}}`Sprite2D`s.

コード内でプロパティを設定するにはどうすればよいでしょうか？1つの方法として、インスペクターでそのプロパティの上にマウスカーソルを合わせると、その名前を確認できます。

[画像: alt=\ /godot_recipes/4.x/img/gds_01_01.png]

Godot has a great built-in help/reference tool. Click on "Classes" at the top of the Script window and search for Node2D and you'll see a help page showing you all the properties and methods the class has available. Looking down a bit you can see `position` in the "Member Variables" section - that's the one we want. It also tells us the property is of the type "Vector2".

![alt](/godot_recipes/4.x/img/gds_01_02.png)

スクリプトに戻ってそのプロパティを使用しましょう：

```gdscript
func _ready():
    position = Vector2(100, 150)
```

エディターが入力に応じて即座に提案を表示しているのに注目してください。Godotは多くの場面でベクトルを使用しており、この点については後ほど詳しく説明します。まずは「Vector2」と入力してみましょう。ヒントが表示されるので、`x` と `y` には2つの浮動小数点数を指定する必要があることがわかります。

Now we have a script that says "When this sprite starts, set its position to `(100, 150)`". We can try this out by pressing the "Play Scene" button.

![alt](/godot_recipes/4.x/img/gds_01_03.png)

{{% notice style="tip" title="Learning tip" %}}
When first learning to code, beginners often ask "How do you memorize all these commands?" Just like any other skill, it's not a matter of memorization, it's about practice. As you use things more, the things you do frequently will "stick" and become automatic. Until then, it's a great idea to keep the reference docs handy. Use the search function whenever you see something you don't recognize. If you have multiple monitors, keep a copy of the [web docs](https://docs.godotengine.org/en/latest/) open on the side for quick reference.
{{% /notice %}}


## まとめ

GDScriptで最初のスクリプトを作成しましたね！次に進む前に、このステップで行った内容をすべて理解しておいてください。次回部分では、スプライトを画面上で移動させるためのコードをさらに追加します。