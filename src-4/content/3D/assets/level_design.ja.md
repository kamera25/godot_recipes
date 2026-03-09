---
title: "Designing a Level"
weight: 15
draft: true
---

## 問題文

## 解決策

私たちのレベル設計には、以下のいくつかの選択肢を検討する必要があります：

### オプション

#### グリッドマップ

組み込みの `{{< gd-icon GridMap >}}GridMap` ノードを使用すると、エディター上でメッシュをグリッド状に配置できます。この概念は2D用の `{{< gd-icon TileMap >}}TileMap` ノードと似ていますが、機能性はやや限られています。

このオプションには以下のような欠点があります：

1. Godot のグリッドマップ機能は比較的基本的なもので（特に2D版と比較すると）、長い間更新されていません。
1. 配置は固定グリッドレイアウトに限定されるため、メッシュの配置自由度が限られています。

## モデルを直接配置する

また、エディターでグリッドスナップを有効化し、直接 **ファイルシステム** タブからシーンをドラッグ＆ドロップして配置することも可能です。この方法は `GridMap` よりも柔軟性に優れていますが、オブジェクトの配置手順がやや煩雑になるという側面があります。

#### 外部ツール

第三の選択肢として、専用ツールでレベルを設計した後、Godotにインポートする方法があります。[Blender](https://blender.org/)はこの目的で非常に人気の高い選択です。すでに独自の3Dアセットを作成している場合、おそらくモデリング作業にはBlenderを使用していることでしょう。

Blenderを使用することで、使い慣れたモデリングツールでレベルを作成し、その後 `GLTF` 形式でGodot向けにエクスポートすることが可能です。さらに[インポート時のヒント機能](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_scenes.html#import-hints)を活用すれば、Godotが自動的に衝突判定用シェイプやライトなどをインポートしたレベル内に生成してくれます。

Godotの組み込み[Blenderサポート](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_scenes.html#importing-blend-files-directly-within-godot)を活用すれば、さらに簡単に連携できます。`.blend`ファイルに変更を加えると、その変更が即座にGodotプロジェクトに反映されます。

### 操作可能なオブジェクト

#### ドア

Find the `wall_doorway_scaffold.glb` file in the **FileSystem** and double-click to check the import settings and see that you've created a static collision for both meshes (the door frame and the door). Right-click to create a "New Inherited Scene".

以下の手順で進めます：

1. アニメーション用に「AnimationPlayer」ノードを追加します。このノードを使ってドアの開閉アニメーションを実装します。最終的に以下のようなノードツリー構造になります：

**SS**

The "wall_doorway_scaffold_door" is the mesh that we want to rotate.
We want to be able to open the door in either direction, so we're going to create two animations. Both of them rotate the door's **Y** rotation by `90°`, but "open+" opens in the **+Z** direction and "open-" does the opposite. This way, when the player interacts with the door, we can open it away from them, no matter which side they're on.

Add the {{< gd-icon StaticBody3D >}}`StaticBody3D` child of the door to a group called "interactable". This is the object the player is going to detect. If it's in that group, the player will call `interact()` on it.

ドアシーンにスクリプトを追加：

```gdscript
extends Node3D

var open = false

func interact(dir):
    if open:
        return
    if dir.dot(global_transform.basis.z) < 0:
        $AnimationPlayer.play("open+")
    else:
        $AnimationPlayer.play("open-")
    open = true
```

#### 胸

Find the `chest.glb` file in the **FileSystem** and double-click to check the import settings and see that you've created a static collision for both meshes (the chest body and lid). Right-click to create a "New Inherited Scene".

追加する {{< gd-icon AnimationPlayer >}} `AnimationPlayer` と胸蓋が開くアニメーションを作成します。

Similar to the door, add the static body to the "interactable" group and an `interact()` function in its script:

```gdscript
extends Node3D

func interact(_dir):
    $AnimationPlayer.play("open")
```
