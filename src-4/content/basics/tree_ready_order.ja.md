---
title: "ツリー順序を理解しよう"
weight: 1
draft: false
ghcommentid: 9
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 課題

Godotがシーンツリー内のノードをどのように処理するかを理解しておく必要があります。

## 解決策

「ツリー順序」はGodotの公式ドキュメントやチュートリアルで頻出する概念ですが、初心者にはその意味が直感的に理解しにくいものです。基本的に、ノードがツリー内で処理される順番は **上から下へ** で、ルートノードを起点として、各ブランチごとに順番に下層へと降りていくのが原則です。

シーンツリーの順序管理は、Godot初心者にとって非常に混乱しやすい要素です。この例では、各処理がどのような順番で実行されるかを具体的に解説します。

以下にサンプルノード設定例をご紹介します。

![alt](/godot_recipes/4.x/img/tree_order_01.png)

各ノードには以下のスクリプトがアタッチされています。

```gdscript
extends Node

func _init():
    # Note: a Node doesn't have a "name" yet here.
    print("TestRoot init")

func _enter_tree():
    print(name + " enter tree")

func _ready():
    print(name + " ready")

# This ensures we only print *once* in process().
var test = true
func _process(delta):
    if test:
        print(name + " process")
    test = false
```

結果について議論する前に、まず各コールバック関数が何を表しているのかを整理します。

* `_init()` はオブジェクトが最初に作成された際に呼び出されます。この時点でオブジェクトのインスタンスがコンピュータのメモリ上に確保されます。

* `_enter_tree()` はノードが初めてツリーに追加される際に呼び出されます（インスタンス化時や `add_child()` を使用した場合など）。

* `_ready()` メソッドは、ノードとそのすべての子ノードがツリーに追加され、準備が完了した時点で呼び出されます。

* `_process()` は毎フレーム（通常は 1 秒間に約 60 回）ツリー内の各ノードで呼び出されます。

これを単一ノードで単独に実行した場合、予想通りの順序になります。

```
TestRoot init
TestRoot enter tree
TestRoot ready
TestRoot process
```

子ノードも含めるとより複雑になります。以下が実行時の出力です。

```
TestRoot init
TestChild1 init
TestChild3 init
TestChild2 init

TestRoot enter tree
TestChild1 enter tree
TestChild3 enter tree
TestChild2 enter tree

TestChild3 ready
TestChild1 ready
TestChild2 ready
TestRoot ready

TestRoot process
TestChild1 process
TestChild3 process
TestChild2 process
```

ご覧の通り、これらのノードはすべてツリー順に従って上から下へ、ブランチを先に表示しています。ただし`_ready()`コードは例外です。

以下は[ノードリファレンス](https://docs.godotengine.org/ja/4.x/classes/class_node.html)からの引用です。

> ノードが「準備完了」状態になった際に呼び出されます。すべての子ノードがシーンツリーに組み込まれた時点で自ノードがトリガーされます。子要素がある場合、まず子ノードの `_ready` コールバックが実行され、その後に親ノードへ通知されます。

よって、ノードを組み立てる時の重要な指針が導き出せます。

{{% notice tip %}}
親ノードは子ノードを管理するべきで、子ノードが親ノードを管理すべきではありません。
{{% /notice %}}

この要件を満たすためには、親ノード内のコードが子ノードのすべてのデータに完全にアクセス可能である必要があります。そのため、`_ready()` メソッドはツリー構造を**逆順**で処理する必要があります。

この原則は `_ready()` メソッド内で他のノードにアクセスしようとする際にも適用されます。ツリーを親ノード（あるいはさらに上層の祖先ノード）に移動する必要がある場合は、子ノードではなくその親ノード内で該当コードを実行する方が適切です。

## 関連レシピ

- [ノードパスの理解](/godot_recipes/4.x/ja/basics/getting_nodes/)