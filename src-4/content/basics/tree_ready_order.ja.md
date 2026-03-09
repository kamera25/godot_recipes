---
title: "Understanding tree order"
weight: 1
draft: false
ghcommentid: 9
---

## 問題文

神がシーンツリー内のノードをどのように処理するかを理解しておく必要があります。

## 解決策

"Tree order" is mentioned often in the Godot docs and in tutorials. However, it is not always obvious to a beginner what is meant by this. Generally speaking, the order in which nodes are handled in the tree is in *top-down* fashion, starting at the root and going down each branch in turn.

シーンツリーの順序管理は、Godot初心者にとって非常に混乱しやすい要素です。この例では、各処理がどのような順番で実行されるかを具体的に解説します。

以下にサンプルノード設定例をご紹介します：

![alt](/godot_recipes/4.x/img/tree_order_01.png)

各ノードには以下のスクリプトが添付されています：

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

結果について議論する前に、まず各コールバック関数が何を表しているのかを整理しましょう：

* `_init()` メソッドはオブジェクトが最初に作成された際に呼び出されます。この時点でオブジェクトのインスタンスがコンピュータのメモリ上に確保されます。

* ノードが初めてツリーに挿入される際に呼び出されます（インスタンス化時や `add_child()` を使用した場合など）。

* `_ready()` メソッドは、ノードとそのすべての子ノードがツリーに追加され、準備が完了した時点で呼び出されます。

* `_process()` は毎フレーム（通常は 1 秒間に約 60 回）ツリー内の各ノードで呼び出されます。

單獨在單一節點上運行此程序，按照你所料的順序如下：

```
TestRoot init
TestRoot enter tree
TestRoot ready
TestRoot process
```

※子供の情報を追加すると複雑になるため、以下に詳しく説明します：

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

ご覧の通り、これらのノードはすべてツリー順に従って上から下へ、枝を先に印刷しています - ただし`_ready()`コードは例外です。

以下は[ノードリファレンス](https://docs.godotengine.org/en/3.2/classes/class_node.html#class-node-method-ready)からの引用です：

> Called when the node is "ready", i.e. when both the node and its children have entered the scene tree. If the node has children, their `_ready` callbacks get triggered first, and the parent node will receive the ready notification afterwards.

このことから、ノード構造を設定する際に重要な経験則が導き出せます：

{{% notice tip %}}
親ノードは子ノードを管理するべきで、逆であってはなりません。
{{% /notice %}}

この要件を満たすためには、親ノード内のコードが子ノードのすべてのデータに完全にアクセス可能である必要があります。そのため、`_ready()` メソッドはツリー構造を**逆順**で処理する必要があります。

この原則は `_ready()` メソッド内で他のノードにアクセスしようとする際にも適用されます。ツリーを親ノード（あるいはさらに上層の祖先ノード）に移動する必要がある場合は、子ノードではなくその親ノード内で該当コードを実行する方が適切です。

## 関連レシピ

- [ノードパスの理解](/godot_recipes/3.x/basics/getting_nodes/)