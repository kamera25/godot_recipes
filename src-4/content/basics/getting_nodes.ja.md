---
title: "Understanding node paths"
weight: 2
draft: false
ghcommentid: 11
---

## 問題文

これはGodotヘルプチャンネルで最も頻繁に報告される問題の一つです：無効なノード参照です。ほとんどの場合、以下のようなエラーメッセージとして表示されます：

> '位置' インデックスは無効です（基底オブジェクト：'null インスタンス'）。

## 解決策

It's that last part, the "null instance", that's the source of this problem, and the main source of confusion for Godot beginners.

この問題を回避するには、「ノードパス」の概念を理解することが重要です。

### ノードパスの理解

シーンツリーはノードで構成されており、これらは親子関係によって接続されています。ノードパスとは、このツリー構造を辿りながらあるノードから別のノードへ移動する際に通る経路のことです。

As an example, let's take a simple "Player" scene:

![alt](/godot_recipes/4.x/img/node_paths_01.png)

このシーンのスクリプトは `Player` ノードに実装されています。もしスクリプトが `AnimatedSprite` ノードに対して `play()` メソッドを呼び出す必要がある場合、そのノードへの参照が必要です：

```gdscript
get_node("AnimatedSprite").play()
```

The argument of the `get_node()` function is a string representing the *path* to the desired node. In this case, it's a child of the node the script is on. If the path you give it is invalid, you'll get the dreaded `null instance` error (as well as "Node not found").

ノード参照を `get_node()` で取得する状況は非常に頻繁にあるため、GDScript にはそのためのショートカットが用意されています：

```gdscript
$AnimatedSprite.play()
```

{{% notice info %}}
`get_node()` 関数は、対象ノードへの **参照** を返します。
{{% /notice %} 】

より複雑なシーンツリーを見てみましょう：

<img src=\ alt=\
>

もしメインスクリプトがスコアラベルにアクセスする必要がある場合、以下のパスを使用してアクセス可能です：

```gdscript
get_node("HUD/ScoreLabel").text = "0"
# or using the shortcut:
$HUD/ScoreLabel.text = "0"
```

{{% notice tip %}}
When using `$` notation, the Godot editor will autocomplete paths for you. You can also right-click on a node in the Scene tab and choose "Copy Node Path".
{{% /notice %}}

What if the node you want to access is higher in the tree? You can use `get_parent()` or `".."` to reference the parent node. In the above example tree, to get the `Player` node from the `ScoreLabel`:

```gdscript
get_node("../../Player")
```

Let's break that down. The path `"../../Player"` means "get the node that's up one level (`HUD`), then one more level (`Main`), then its child `Player`".

{{% notice tip %}}
Does this seem familiar? Node paths work exactly like directory paths in your operating system. The `/` character indicates the parent-child relationship, and `..` means "up one level".
{{% /notice %}}

### 相対パスと絶対パスの違い

上記の例はすべて相対パスを使用しています。これは現在のノードを起点として、目的地までの経路をたどる形式です。ノードへのパスは絶対パス形式で指定することも可能で、この場合シーンのルートノードを基点とします。

例如，玩家節點的絕對路徑如下：

```gdscript
get_node("/root/Main/Player")
```

`/root` は `get_tree().root` を介してもアクセス可能ですが、これはシーンのルートノードではありません。これはデフォルトで常に SceneTree に存在するビューポートノードです。

### 警告事項

上記の例は問題なく動作しますが、後々問題を引き起こす可能性のあるいくつかの注意点があります。以下のような状況を想像してみてください：`Player`ノードには`health`プロパティがあり、これをUI内のどこかにある`HealthBar`ノードに表示したいとします。プレイヤースクリプトには次のように記述するかもしれません：

```gdscript
func take_damage(amount):
    health -= amount
    get_node("../Main/UI/HealthBar").text = str(health)
```

初期段階では問題なく機能するかもしれませんが、これは非常に「脆弱」な方式であり、簡単に破綻する可能性があることを意味します。この種の構成には主に2つの重大な問題があります：

1. プレイヤーシーン単体でのテストは不可能です。プレイヤーシーンを単独で実行した場合や、UIを持たないテストシーンで使用した場合、`get_node()` 行が原因でクラッシュが発生します。
2. UIの変更はできません。UIのレイアウトを変更するか設計を見直すことにした場合は、パスが無効になるため、必ず修正する必要があります。

この理由から、シーンツリーの\方向へノードパスを指定する操作は可能な限り避けるべきです。前述の状況では、プレイヤーの体力が変化した時にシグナルを発行するように変更すれば、UIコンポーネントはその信号を受け取って自身の状態を更新できます。この方法なら、ゲームコードに影響を与えることなくノードを自由に再配置・分離することが可能になります。

## まとめ

ノードパスの使い方をマスターすれば、必要なノードを簡単に参照できるようになります。そして、「nullインスタンス」エラーメッセージに悩まされることもなくなります。

<!-- ## 関連するレシピ

- [Using KinematicBody2D](/godot_recipes/3.x/physics/godot3_kinematic2d/) -->