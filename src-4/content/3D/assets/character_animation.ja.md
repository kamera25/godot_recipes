---
title: "Character Animation"
weight: 5
draft: false
---

## 問題文

以下の状況に対応する：ユーザーが作成したかサードパーティからダウンロードした不正なアニメーション付き3DキャラクターをGodotでセットアップしたい。

## 解決策

このレシピでは、既にキャラクターモデルとアニメーションをインポート済みであることを前提としています。まだの方は、[アセットのインポート方法](/4.x/3d/assets/importing_assets/)を参照してください。参考までに、私たちは[セクション説明欄](/godot_recipes/4.x/3d/assets/)でリンクされているアートパックを使用しています。

### キャラクターの準備

以下の理由でキャラクターには `CharacterBody3D` を選択しました。そのため、シーンはこのような外観になるはずです（メッシュリストが非常に長いため、`Rig`ノードは折りたたみ状態にしています）：

![alt](/godot_recipes/4.x/img/3dcharacter_imported_scene.png)

最初に目につくのは、キャラクターが武器と盾でいっぱいになっていることです！ 作者は親切にも、すべての装備品が正しく取り付けられ、適切な向きになるようにしてくれています。リストをスクロールして、表示したくないアイテムを隠すことができます。

![alt](/godot_recipes/4.x/img/3dcharacter_default_pose.png)

### アニメーションツリーについて

利用可能なアニメーションが多数ある場合、それらをすべてコードで管理するのは急速に複雑化します。プレイヤーが行っている動作に応じて、どのタイミングでどのアニメーションを再生するかを判断するには、どれほど多くの`if`文が必要になるか考えてみてください。アニメーションがわずかであれば問題ありませんが、数が増えるとすぐに手に負えなくなり、実用的ではなくなってしまいます。

Also, consider when the character is standing still: it should be playing the "Idle" animation. When the player presses "forward", the character should move and switch to playing the "Walking" animation. This sudden transition is going to look jarring, so we'd prefer if the two animations can be "blended" into a smoother transition.

これらの複雑なアニメーション問題を解決するには、`AnimationTree`ノードを使用する必要があります。このノードは{{< gd-icon AnimationPlayer >}}`AnimationPlayer`を制御するために設計されており、アニメーションの遷移やブレンド方法を管理する機能を備えています。

シーンに `AnimationTree` コンポーネントを追加します。［インスペクター］で［ツリールート］を新規作成された `AnimationNodeStateMachine` に設定し、［Animプレイヤー］ではキャラクターのアニメーションノードを選択します（{{< gd-icon AnimationPlayer >}}`AnimationPlayer`）。最後に［有効化］チェックボックスをオンにしてください。

![alt](/godot_recipes/4.x/img/animtree_settings.png)

{{% notice style="note" title="" %}}
You may notice that when the {{< gd-icon AnimationTree >}}`AnimationTree` is active, you can't choose animations in the {{< gd-icon AnimationPlayer >}}`AnimationPlayer`. If you need to make any changes or test the animations, uncheck the tree's **Active** property while doing so.
{{% /notice %}}

### 待機/歩行/走行サイクルについて

このモデルには数多くのアニメーションが付随しています。ここでは特に待機→歩行/走行の遷移、ジャンプ、攻撃モーションに焦点を当てます。他のアニメーションも必要に応じて同様の方法で扱えます。

In the {{< gd-icon AnimationPlayer >}}`AnimationPlayer`, find the "Idle", "Running_A", "Walking_Backwards", and "Running_Strafe_Left"/"Running_Strafe_Right" animations. Make sure they're all set to loop - you can test them by pressing the "Play" button: (▶). If any of them are not, reimport the character after setting them (see [Importing Assets](/4.x/3d/assets/importing_assets/)).

「AnimationTree」ノードを選択すると、ウィンドウ下部にパネルが開きます：

![alt](/godot_recipes/4.x/img/animtree_empty.png)

As an example, right-click in the empty space and choose **Add Animation → Idle**, then add the "1H_Melee_Attack_Chop" animation as well.

Select the **Connect Nodes** button and draw a connection from `Start` to `Idle`. You should immediately see the "Idle" animation playing.

しかし、このままではうまくいきません。2つのアニメーション間で急速に点滅を繰り返すだけで、両方が「即時遷移」に設定されているため、スムーズな移行ができないからです。

To change the transition conditions, change to **Select** mode using the icon and then click on one of the connections. In the Inspector, you'll see the connection properties. For the connection from idle to attack, we want **Advance/Mode** to be "Enabled" (not "Auto"). This means it happens only when told to. Notice that the icon on the connection line changes color.

For the connection from attack to idle, set **Switch Mode** to "At End" and **Advance Mode** to "Auto".

これで、攻撃ノードの ▶ ボタンをクリックすると再生が始まり、完了するとすぐにアイドル状態に戻ります。

この設定により、異なるアニメーションの実装方法とそれらの間の遷移方法について理解できたかと思います。ただし、さらに一歩進んだ内容を扱うため、ゴミ箱アイコンを使用して2つのアニメーションを削除し、代わりに「ブレンドスペース」を設定してみましょう。

### ブレンドスペース

以下の手順で設定を進めてください：
1. 空欄に右クリックして新規 `BlendSpace2D` を作成します
2. BlendSpaceの名前をクリックし、`IWR`（idle-walk-run）に改名します
3. `Start`から遷移を追加し、ブレンドスペースが自動的に再生されるようにします

鉛筆アイコンをクリックするとブレンドスペースを編集できます。

![alt](/godot_recipes/4.x/img/blendspace_empty.png)

この2次元空間はキャラクターの水平方向移動ベクトルを表します。静止状態の場合は座標が`(0, 0)`となるため、まず**ポイントを作成**ボタンをクリックしてから、グリッド中央をクリックして**アニメーション追加 → 待機姿勢**を設定してください。

At the center-top, add the "Running_A" animation, and center-bottom, "Walking_Backwards". At the two horizontal ends, add the strafe animations.

<img src=\ alt=\
>

次に、十字ボタンをクリックしてブレンド位置を設定し、グリッド上でドラッグして移動させてください。アニメーションが極値間でスムーズに遷移するのが確認できるはずです。

<video width="500" controls src="/godot_recipes/4.x/img/blendtree_testing.webm"></video>

When you're done experimenting with the blendspace, click "Root" in the **Path** at the top of the panel to return to the root of the tree.

### 状態機械の設定

The `IWR` looping animations can be thought of as the "heart" of the animation tree. The character will spend most of its time playing these animations. Any other animations will branch off from it (like we did earlier with the attack).

以下の画像では、他の複数のアニメーションで同じ手法を採用しています。遷移プロパティは、前述の例と同様に設定されている点にご注目ください。

<img src=\ alt=\>

また、アニメーションの名前をクリックすることで変更することも可能です。中には非常に長い名前のものもありますので。

The one animation that's different is jumping. The jump animation is split into three parts: "start"and "land", which are played when the character starts jumping, and when the jump ends. The "idle" portion of the jump is a looping animation that plays as long as the character is in the air - if they fall a long way, for example.

以下の手順で3つのジャンプアニメーションを追加し、適切にリンクしてください：

![alt](/godot_recipes/4.x/img/anim_tree_jumping.png)

We need to be able to go straight from `IWR` to `Jump_Idle` in the event of falling off a ledge, but if pressing "jump", we'll go through `Jump_Start` first.

In addition, we've left the transition from `IWR` to `Jump_Start` as "Auto". Instead of changing it to "Enabled", we've added a **Condition** of `jumping` to the transition:

![alt](/godot_recipes/4.x/img/animtree_condition.png)

同様に、「`Jump_Idle`」から「`Jump_Land`」への状態遷移には「`grounded`」（着地状態）という条件があります。

これらの条件をコードで設定し、遷移を実行することになります。

最後に、注意深く観察すると、`Jump_Land`から`IWR`へのトランジションが滑らかでないことに気づくかもしれません。これは、2つのアニメーションの最終フレームと最初のフレームが完全には一致していないためです。この問題を解決するには、両者間のトランジションを選択し、小さな**Xfade時間**を`0.1`に設定することで、スムーズに移行させることができます。

## まとめ

3Dキャラクターのアニメーション設定が完了し、使用準備が整いました。`{{< gd-icon AnimationTree >}}` `AnimationTree` を設定したことで、キャラクターのモーションコード内でアニメーションを選択し、スムーズに遷移させることが格段に容易になりました。

[セクションの説明](/godot_recipes/4.x/3d/assets/) を参照すると、3D作業のさらなる事例や、ダウンロード可能なGodotプロジェクトなどの例を確認できます。

#### 関連動画

{{< youtube YrNQCB34PAc >}}
https://youtu.be/YrNQCB34PAc