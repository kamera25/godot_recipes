---
title: "Designing the Player Scene"
weight: 2
draft: false
pre: "02. "
---

最後のセクションでは、プロジェクトを設定し、ゲームアートをダウンロードしました。これでコーディングを開始する準備が整いました。まずはプレイヤー操作可能な宇宙船から着手しましょう。

## 船シーンの設定

Godot ワークフローにおいて共通的な作業の一つにシーンの作成があります。前述したように、Godotにおける「シーン」とは、単なる複数の「ノード」の集合体に過ぎません。ほとんどのGodotプロジェクトでは、各ゲームオブジェクトは個別のシーンとして構成され、目的に応じた機能を提供するノードと、必要に応じて動作をカスタマイズするスクリプトが組み込まれています。

### ノードの選択方法

最初のステップは、どのタイプのノードから始めるかを決めることです。シーンに追加する最初のノードは「ルートノード」と呼ばれます。通常、シーンのルートノードはゲームオブジェクトの主要な動作を定義するものでなければなりません。その後、追加機能を実現するために「子ノード」を取り付けていきます。

さて、ゲームに登場する船はどんなデザインにすべきでしょうか？要件を整理し、それらを満たすために活用できそうなノードを検討してみましょう。

その船には以下が必要です：

* _2D空間での移動_。これには基本的な{{< gd-icon Node2D >}}`Node2D`ノードで十分です。なぜならこのノードには`position`、`rotation`などの2D関連プロパティが備わっているからです。ただし、外観に関する要素はありません。

* _画像を表示_。{{< gd-icon Sprite2D >}}`Sprite2D`はこの目的のためのノードです。これも{{< gd-icon Node2D >}}`Node2D`であるため、自由に移動させることができます。

* _衝突検出機能_：画面内で敵キャラが射撃したり移動したりするため、自機がダメージを受けたタイミングを正確に把握する必要があります。固い物体同士の相互作用（跳ね返りや運動量伝達など）を考慮する必要はなく、単に接触を検知できれば十分です。この用途には{{< gd-icon Area2D >}}`Area2D`コンポーネントが最適です。他オブジェクトとの接触検出機能を備え、位置関連プロパティを持っていますが、独自の視覚表現は持ちません。

このリストを見ると、`Area2D`が主要な機能を提供していることがわかります。ここに`Sprite2D`をアタッチして宇宙船の画像を表示すれば、必要なものはすべて揃います。

## シーンの構築方法

```markdown
**シーン** タブで、**＋** ボタンまたは**その他のノードを追加** ボタンをクリックして最初のノードを作成します。{{< gd-icon Area2D >}}`Area2D` と入力し、リストから選択してください。ノードが **シーン** タブに追加されたら、その名前をクリックして `Player` に改名し、`<Ctrl+S>` キーを押してシーンを保存します。
```

### 船舶情報の表示

`プレイヤー`ノードを選択した状態で、もう1つのノードを追加します：{{< gd-icon Sprite2D >}}`Sprite2D`。整理しやすくするため、このノードの名前を`船`に変更しましょう。

「ファイルシステム」タブから、アートパック内の `Player_ship (16x16).png` ファイルをドラッグし、インスペクターの「テクスチャ」プロパティにドロップしてください。

<img src=\ width=\>

最初に気づくのは、どうやら船が3隻あるように見える点です！アートパックに含まれている画像には、左右へ移動するバージョンも含まれています。これを利用してみましょう - ［インスペクター］の［アニメーション］セクションで、**Hフレーム数**を`3`に設定します。これで**フレーム**プロパティを変更すると、これら3つの異なるバージョン間を切り替えられるようになります。今のところは`1`のままにしておいてください。

<img src=\ alt=\>

### 衝突形状の追加方法

また、{{< gd-icon Area2D >}}`Area2D`ノードの横にある黄色の警告三角アイコンにもお気づきかもしれません。このアイコンをクリックすると、このエリアに形状が定義されていないという警告メッセージが表示されます。適切に対応するためには、`Player`ノードの下に{{< gd-icon CollisionShape2D >}}`CollisionShape2D`ノードを追加する必要があります。これにより、オブジェクト同士が衝突判定を行うための正確な境界を設定できます。

このノードの［インスペクター］ウィンドウで「形状」プロパティを確認すると、現在は `<empty>` と表示されています。このボックスをクリックすると、様々な形状を選択できるドロップダウンメニューが表示されます。ここでは {{< gd-icon RectangleShape2D >}} を選択して「新規長方形シェイプ2D」を追加すると、船の上に水色の正方形が表示されるはずです。

図形のサイズを調整するには、オレンジ色の円をドラッグするか、［インスペクター］ウィンドウの「形状」プロパティ内で直接クリックして、手動で幅と高さを入力することができます。

![alt](/godot_recipes/4.x/img/2d_101_05.png)

### 排気システム

The ship will look much more dynamic with a little animation. Included in the art pack are some animations of exhaust flames named "Boosters". There are three: one for each version of the ship (left, forward, and right).

To display these, select the `Ship` node and add a child {{< gd-icon AnimatedSprite2D >}}`AnimatedSprite2D` node and name it "Boosters".

```plain
インスペクターの[アニメーション]セクションにある[スプライトフレーム]プロパティは現在空になっています。これをクリックすると新しい[スプライトフレーム]が作成されますので、その後でエディタウィンドウ下部のアニメーションパネルを開くために[スプライトフレーム]項目をクリックしてください。

![alt](/godot_recipes/4.x/img/2d_101_06.png?width=800)

Double-click the "default" animation to rename it to "forward". Then, to add the animation images, click the **Add frames from sprite sheet** button:

![alt](/godot_recipes/4.x/img/2d_101_07.png?width=800)

```markdown
「Boosters (16 x 16).png」画像を選択すると、「フレーム選択」ウィンドウが表示され、必要なフレームを選択できるようになります。

![alt](/godot_recipes/4.x/img/2d_101_08.png?width=800)

このアニメーションにはフレームが2つしかありませんが、グリッドが正しくありません。画像サイズに合わせて **サイズ** の値を変更してください：`16 x 16`。その後、両方のフレームをクリックして選択し、**フレームを追加(2個)** ボタンをクリックしてください。

<img src=\ alt=\>

2つのフレームを追加したら、**再生**ボタンを押してアニメーションを実行してください。また、**ロード時に自動再生**ボタンを切り替えれば、自動的にアニメーションが開始されるようになります。

<img src=\ alt=\>

処理が少し遅いので、フレームレートを「10 FPS」に変更してください。

追加アニメーションを2つ作成するには、**[アニメーションを追加]** ボタンをクリックして、それぞれ「左」と「右」と命名してください。

![alt](/godot_recipes/4.x/img/2d_101_11.png)

Repeat the process, adding the left and right "Booster" sprite sheets.

### 銃のクールダウン時間

The last node we'll need to complete the player setup is a {{< gd-icon Timer >}}`Timer` to control how fast the player can shoot. Add the `Timer` as a child of `Player` and name it `GunCooldown`. Set its **One Shot** property to "On". This means that when the timer ends, it won't automatically restart. In the player's code, we'll start the timer when the player shoots, and they won't be able to shoot again until the timer runs out.

### 次のステップ

プレイヤーシーンの設定はこれで完了です。ゲーム内でプレイヤーが操作する艦船に必要な機能を実装するため、ノードを追加しました。次のセクションでは、プレイヤーが艦船を制御し、射撃を行い、物体と衝突したことを検知するためのコードを追加してゆきます。

| {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_01/" icon="fas fa-arrow-left" %}}Prev{{% /button %}} | {{% button href="/godot_recipes/4.x/games/first_2d/first_2d_03/" icon="fas fa-arrow-right" icon-position="right" %}}Next{{% /button %}} |
|------|------:|
