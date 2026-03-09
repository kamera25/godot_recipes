---
title: "Main Scene"
weight: 6
draft: false
pre: "06. "
---

Before we can make enemies, powerups, or any other game objects, we need a place where they can all exist together with the player. In most games, this would be called a "level" or "main" scene, and that's what we'll call it here.

Start the scene with a {{< gd-icon Node2D >}}`Node2D` called "Main" and save it.

## 背景の作成方法

Add a {{< gd-icon Sprite2D >}}`Sprite2D` child. Name this sprite "Background" and add the `Space_BG (2 frames) (64 x 64).png` as its texture.

この画像には2つのフレームがあり、それぞれ`64x64`ピクセルのサイズです。画面全体に画像を敷き詰めたいので、まずは以下の設定から始めてください：

* Under **Offset** set **Centered** to "off". This makes the image's top left corner start at the origin rather than its center.

* Under **Region**, turn **Enabled** "on", and then set the **Rect** to a width of `240` and a height of `320`. This makes the image stretch to the size of the screen.

* ［テクスチャ］設定で［繰り返し表示］を「有効」に変更してください。これにより画像が画面全体に繰り返されるようになります。

現在のシーンにプレイヤーを追加するには、`メイン`ノードを選択して**子シーンをインスタンス化**ボタンをクリックします。

![alt](/godot_recipes/4.x/img/2d_101_18.png)

### 背景をアニメーション化する方法

```python
import panda3d.core as pdc
from direct.directbase import DirectStart

class BackgroundAnimatorNode(pdc.NodePath):
    def __init__(self, parent_node):
        super().__init__(\)
        parent_node.attachChild(self)
        self.animationPlayer = pdc.AnimationPlayer(\)
        self.addChild(self.animationPlayer)

    def update_frame(self, frame_number):
        # アニメーションフレームを更新するロジックを実装
        pass

class MainNodePath(pdc.NodePath):
    def __init__(self):
        super().__init__(\)

        # BackgroundAnimatorNodeのインスタンスを作成
        background_node = BackgroundAnimatorNode(\)

        # AnimationPlayerを設定する（実際の実装は省略）
        pass

if __name__ == \:
    DirectStart()
```

エディタウィンドウの下部には**アニメーション**パネルが表示されます。ここには多くの情報が配置されていますので、その構成を確認していきましょう：

![alt](/godot_recipes/4.x/img/2d_101_19.png)

クリックしてください。次に［新規アニメーション］を選択します。新しいアニメーションには名前を「scroll」と付けてください。［長さ］の値は「2」に設定し、［ループ再生］と［自動再生］ボタンを有効にします。

アニメーション機能は、制御したいプロパティを表す「トラック」を追加することで動作します。プレイヤーのタイムライン上では、「キーフレーム」を追加して特定の時点でそのプロパティに設定したい値を指定します。

アニメーションにキーフレームを追加するには、インスペクタの各プロパティ横に表示された鍵アイコンをクリックします。スライダ（タイムライン上の青いマーカー）が時間「0」に位置していることを確認したら、まず「背景」を選択し、**領域/矩形**の横にある鍵ボタンをクリックします。新規トラックを作成するか確認されるので、指示に従ってください。すると、追加されたキーフレームを表す小さなドットとともに、新しいトラックがアニメーションパネルに追加されます。スライダを時間「2」まで移動させ、最後に**領域/矩形**プロパティの **y** 値を「64」に設定します。別のキーフレームを追加するには、該当するキーをクリックします。

アニメーションの再生ボタンを押すと、プレーヤーの背後で背景がゆっくりとスクロール表示されるはずです。

## 次のステップ

メインシーンが完成し、敵キャラクターを追加する準備が整いました。次のステップでは、弾丸と同じ方法で単一の敵用シーンを作成し、その後複数回インスタンス化します。

| {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_05/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_07/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
