---
title: "レベルの設計"
weight: 15
draft: true
---

## 課題

## 解決策

レベル設計には、以下のいくつかの選択肢を検討が必要です。

### オプション

#### グリッドマップ

組み込みの `{{< gd-icon GridMap >}}GridMap` ノードを使用すると、エディター上でメッシュをグリッド状に配置できます。この概念は2D用の `{{< gd-icon TileMap >}}TileMap` ノードと似ていますが、機能性はやや限られています。

このオプションには以下のような欠点があります。

1. Godot のグリッドマップ機能は比較的基本的なもので（特に2D版と比較すると）、長い間更新されていません。
1. 配置は固定グリッドレイアウトに限定されるため、メッシュの配置自由度が限られています。

## モデルを直接配置する

また、エディターでグリッドスナップを有効化し、直接 **ファイルシステム** タブからシーンをドラッグ＆ドロップして配置することもできます。この方法は `GridMap` よりも柔軟性に優れていますが、オブジェクトの配置手順がやや煩雑になるという側面があります。

#### 外部ツール

第三の選択肢として、専用ツールでレベルを設計した後、Godotにインポートする方法があります。[Blender](https://blender.org/)はこの目的で非常に人気の高い選択です。すでに独自の3Dアセットを作成している場合、おそらくモデリング作業にはBlenderを使用していることでしょう。

Blenderを使用することで、使い慣れたモデリングツールでレベルを作成し、その後 `GLTF` 形式でGodot向けにエクスポートできます。さらに[インポート時のヒント機能](https://docs.godotengine.org/ja/stable/tutorials/assets_pipeline/importing_scenes.html#import-hints)を活用すれば、Godotが自動的に衝突判定用シェイプやライトなどをインポートしたレベル内に生成してくれます。

Godotの組み込み[Blenderサポート](https://docs.godotengine.org/ja/stable/tutorials/assets_pipeline/importing_scenes.html#importing-blend-files-directly-within-godot)を活用すれば、さらに簡単に連携できます。`.blend`ファイルに変更を加えると、その変更が即座にGodotプロジェクトに反映されます。

### 操作可能なオブジェクト

#### ドア

「壁とドアの足場」（wall_doorway_scaffold.glb）ファイルを**ファイルシステム**内で見つけ、ダブルクリックしてインポート設定を確認し、両方のメッシュ（ドアフレームとドア）に対して静止衝突オブジェクトが適切に作成されていることを確認してください。右クリックして「新規継承シーン」を作成します。

以下の手順で進めます。

1. アニメーション用に「AnimationPlayer」ノードを追加します。このノードを使ってドアの開閉アニメーションを実装します。最終的に以下のようなノードツリー構造になります。

**SS**

「wall_doorway_scaffold_door」は、回転させたいメッシュです。
ドアを両方向に開閉できるようにするため、2つのアニメーションを作成します。どちらのアニメーションもドアの**Y軸**周りの回転を`90°`変更しますが、「open+」は**+Z方向**に、「open-」はその逆方向に開きます。これにより、プレイヤーがドアに触れたとき、どの側に立っていても外側に開くようになります。

ドアの子要素である {{< gd-icon StaticBody3D >}}`StaticBody3D` を「インタラクタブル」というグループに追加します。これはプレイヤーが検出する対象となるオブジェクトです。このグループに属することで、プレイヤーは `interact()` メソッドを呼び出すことが可能になります。

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

「ファイルシステム」内で `chest.glb` ファイルを見つけ、ダブルクリックしてインポート設定を確認し、両方のメッシュ（チェスト本体と蓋）に対して静的衝突判定が正しく設定されていることを確認してください。右クリックで「新規継承シーン」を作成します。

追加する {{< gd-icon AnimationPlayer >}} `AnimationPlayer` と胸蓋が開くアニメーションを作成します。

ドアと同様に、静的ボディを「インタラクション可能」グループに追加し、スクリプト内に `interact()` 関数を実装します。

```gdscript
extends Node3D

func interact(_dir):
    $AnimationPlayer.play("open")
```
