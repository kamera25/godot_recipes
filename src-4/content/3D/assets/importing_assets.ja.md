---
title: "Importing Assets"
weight: 1
draft: false
---

## 問題文

以下の3Dアセットセットをダウンロード（または作成）しました：リギング済みでアニメーション化されたキャラクターを含むファイル群で、これをGodotにインポートしたいと考えています。

## 解決策

本例では、[セクションの説明](/godot_recipes/4.x/3d/assets/) に記載されているアートパックをダウンロードして解凍済みであることを前提とします。

プロジェクトにファイルをコピーする前に、以下の点に注意してください：資産にはOBJ、FBX、GLTFといった複数の異なるファイル形式が存在します。また、変更を希望する場合に備えてサンプルや個別テクスチャなどの追加ファイルも用意されています。これらすべては不要であり、GodotではGLTF形式が最も推奨されるインポートフォーマットです。したがって、必ず`gltf`フォルダまたは`.gltf`ファイル（もしくは同等のバイナリ形式である`.glb`）のみをプロジェクトディレクトリにドラッグ＆ドロップしてください。

Here, I've taken the `gltf` folder from the "Dungeon" pack and the `characters` folder from the "Adventurers" pack and dragged them into my project.

{{% notice style="note" title="" %}}
There are a lot of files in the Dungeon pack - Godot may take a little time to read them all!
{{% /notice %}}

## キャラクターのインポート方法

ファイルシステムタブで`knight.glb`ファイルを選択し、左上の**インポート**タブをクリックしてください。

<img src=\ alt=\>

こちらには基本的なインポート設定が表示されますが、より詳細なオプションも利用可能です。**詳細設定**ボタンをクリックすると、新しいウィンドウが開きます：

![alt](/godot_recipes/4.x/img/3d_import_adv.png)

左側に表示されるのは、GLTFシーンに含まれる全てのデータです - テクスチャやアニメーションも含まれます。キャラクターに付属する各種武器オプションや、豊富なアニメーションリストに注目してください。

中央に選択した文字のプレビューが表示され、右側には選択した項目の設定を調整できるオプションメニューがあります。

```
プレイヤーが `CharacterBody3D`としてコード化されるため、ここでノードタイプを指定できます。`シーンルート`をクリックし、右側のパネルで**ルートタイプ**を `CharacterBody3D`に設定してください。

### アニメーション機能

Scroll down to the list of animations. You'll see that there are many, but while some we'll only want to play once, such as attacks, others like "Idle" and "Running", we'd like to be looping. For any animation like this, select the animation name and set the **Loop Mode** to "Linear". Do this for all of the "Walking", "Running", and "Idle" variations. When you're done, click the **Reimport** button at the bottom.

![alt](/godot_recipes/4.x/img/3d_import_loop.png)

{{% notice style="info" title="Setting Loop Automatically" %}}
If you are making your own characters, you can skip this step by ensuring that your animations' names end with `"-loop"`. For details on this and other *import hints*, see [Import Hints](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_scenes.html#import-hints) in the Godot documentation.
{{% /notice %}}

ファイルシステム内の「knight.glb」を右クリックし、［新規継承シーン］を選択してください。

このシーンではすべてのモデルと［アニメーションプレーヤー］{{< gd-icon AnimationPlayer >}} `AnimationPlayer` が表示され、ここではアニメーションを実際にテストすることができます。

## ワールドアイテムのインポート

Importing objects for the environment will be a similar process. As an example, let's use one of the dungeon walls. There are a lot of files in the dungeon pack, so type "wall" in the file filter to help find it:

![alt](/godot_recipes/4.x/img/3d_import_wall.png)

幸いなことに、Godotではインポート時に自動的にこれらの処理を行ってくれます。

In the import window, select the mesh object. On the right side, check the **Physics** box, and set the **Shape Type** to "Simple Convex" (feel free to check out the other options too).

<img src=\ alt=\>

をクリックします。ゲームでこのアセットを使用する際、Godotは自動的に対応する衝突形状を持った{{< gd-icon StaticBody3D >}}`StaticBody3D`を作成します。

{{% notice style="info" title="Automating Collision Shapes" %}}
As above, there is an import hint for collision shapes as well. In your Blender project, appending `-col` (or some other variations) will let the importer know to do this step automatically. See the *import hints* link for details.
{{% /notice %}}

## インポート処理の自動化

自作アセットを作成する際にはインポートヒントを追加する方法が推奨されますが、今回のように既存のアセットパックをダウンロードする場合には適用できません。

特定タイプのノードすべてに適用可能な*インポートスクリプト*を作成することが可能です。例えば、前述した静的衝突判定オブジェクトの自動生成を自動化できます。

以下のスクリプト例では、インポートされたオブジェクトのすべてのノードをループ処理し、各メッシュに対して静的衝突判定を作成します。

```gdscript
@tool
extends EditorScenePostImport

func _post_import(scene):
    iterate(scene)
    return scene

func iterate(node):
    if node != null:
        if node is MeshInstance3D:
            node.create_trimesh_collision()
        for child in node.get_children():
            iterate(child)
```

**インポート** タブでは、この設定を**インポートスクリプト**として指定できます。その後、**再インポート**をクリックすると、衝突が作成されます。

## まとめ

以上で、Godotへの3Dアセットインポートに関する概要説明を終了します。

以下のセクションを参照してください：[セクション説明](/godot_recipes/4.x/3d/assets/)、インポートした3Dアセットを扱う際の具体例が記載されています。

#### 関連動画

{{< youtube XRUWhE4OnOY >}}
