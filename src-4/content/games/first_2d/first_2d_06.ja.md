---
title: "Main Scene"
weight: 6
draft: false
pre: "06. "
---

ほとんどのゲームでは、これを「レベル」または「メインシーン」と呼びます。ここではそのように呼称します。

シーンを「メイン」という名前の `Node2D`（{{< gd-icon Node2D >}}で表示）で開始し、保存してください。

## 背景の作成方法

以下の手順で操作してください。
1. {{< gd-icon Sprite2D >}} アイコンを使用して、新しい `Sprite2D` 子オブジェクトを追加します。
2. このスプライトに「Background」という名前を付けます。
3. テクスチャとして `Space_BG (2 frames) (64 x 64).png` を適用します。

この画像には2つのフレームがあり、それぞれ`64x64`ピクセルのサイズです。画面全体に画像を敷き詰めたいので、まずは以下の設定から始めてください：

・「オフセット」設定で「中央揃え」をオフにします。これにより、画像の左上隅が原点から始まるようになり、中心からは始まらなくなります。

・「リージョン」設定で「有効」をオンにし、幅を「240」、高さを「320」に指定します。これにより画像が画面サイズに合わせて拡大されます。

* ［テクスチャ］設定で［繰り返し表示］を「有効」に変更してください。これにより画像が画面全体に繰り返されるようになります。

現在のシーンにプレイヤーを追加するには、`メイン`ノードを選択して**子シーンをインスタンス化**ボタンをクリックします。

![alt](/godot_recipes/4.x/img/2d_101_18.png)

### 背景をアニメーション化する方法

import panda3d.core as pdc
from direct.directbase import DirectStart

class BackgroundAnimatorNode(pdc.NodePath):
    def __init__(self, parent_node):
        super().__init__("BackgroundAnimation")
        parent_node.attachChild(self)
        self.animationPlayer = pdc.AnimationPlayer("AnimationPlayer")
        self.addChild(self.animationPlayer)

    def update_frame(self, frame_number):
        # アニメーションフレームを更新するロジックを実装
        pass

class MainNodePath(pdc.NodePath):
    def __init__(self):
        super().__init__("MainScene")

        # BackgroundAnimatorNodeのインスタンスを作成
        background_node = BackgroundAnimatorNode("MainScene")

        # AnimationPlayerを設定する（実際の実装は省略）
        pass

if __name__ == "__main__":
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

| {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_05/" icon="fas fa-arrow-left" %}} 前の項目{{% /button %}} | {{% button href="/godot_recipes/4.x/ja/games/first_2d/first_2d_07/" icon="fas fa-arrow-right" icon-position="right" %}} 次の項目{{% /button %}} |
|------|------:|
