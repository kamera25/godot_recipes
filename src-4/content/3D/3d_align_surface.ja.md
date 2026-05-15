---
title: "CharacterBody3D: 表面に位置合わせ"
weight: 15
draft: false
---

## 課題

キャラクターの体は地面や地形と平行になるように調整が必要となります。

## 解決策

このレシピは[キャラクターボディ3D：移動制御](/godot_recipes/4.x/ja/3d/characterbody3d_examples/) レシピで解説されている基本の{{< gd-icon CharacterBody3D >}}`CharacterBody3D`コントローラーを拡張する内容となっています。まずはそちらを先にお読みください。

まず、シーンに地形を追加しました。こちらのリンクからダウンロードできます。[https://fertile-soil-productions.itch.io/modular-terrain-pack](https://fertile-soil-productions.itch.io/modular-terrain-pack)。ローポリモデルですが、お好みの地形を自由に使用・作成していただいて構いません。

ご覧の通り、移動自体は地形に沿って機能していますが、戦車が斜面に対して向きを変えないため、まるで「浮いて」いるかのように見えます。

<video controls src="/godot_recipes/4.x/img/3d_kinematic_04.webm"></video>

その代わりに、戦車の履帯が地面と平行になるように車体を傾ける必要があります。勾配が変わっても姿勢を維持しなければなりません。そのためには、どの方向が「上」かを把握しておく必要があるのです。

### 表面法線ベクトル

*法線ベクトル*（「ノーマルベクトル」または単に「単位ベクトル」）とは、面に垂直な方向を示す単位ベクトルのことです。これは表面がどの向きを向いているのかを定義します。メッシュの場合、各面には必ず外側を指す法線ベクトルが割り当てられます。

![alt](/godot_recipes/4.x/img/3d_kinematic_05.png)

![alt](/godot_recipes/4.x/img/3d_kinematic_06.gif)

Godot では、衝突が発生した際、接触時の法線ベクトルを取得できます。これは衝突する物体の **接触点における** 法線方向になります。

表面法線を取得した後、タンクの**Y**軸をそれに平行に合わせます。ただし、`Transform3D.looking_at()` 関数は使用できません。このメソッドでは **-Z** 軸（前方方向）が法線方向に揃ってしまうためです。

これを実現するには、以下の関数を使用します。

```gdscript
func align_with_y(xform, new_y):
    xform.basis.y = new_y
    xform.basis.x = -xform.basis.z.cross(new_y)
    xform.basis = xform.basis.orthonormalized()
    return xform
```

与えられた変換行列と新しい**Y**方向ベクトルに基づき、この関数は、指定された法線ベクトルに対して`basis.y`成分が一致するよう、適切に回転調整された変換行列を返します。

{{% notice note %}}
クロス積やその他のベクトル数学に慣れていない方のために、Godot公式ドキュメントに[ベクトル数学入門ガイド](https://docs.godotengine.org/ja/latest/tutorials/math/vector_math.html)が用意されています。
{{% /notice %}}

タンクの移動コードを更新して、表面が衝突した際にこの関数を呼び出せるようにします。

```gdscript
func _physics_process(delta):
    velocity += gravity * delta
    get_input(delta)
    move_and_slide()
    for i in get_slide_count():
        var c = get_slide_collision(i)
        global_transform = align_with_y(global_transform, c.get_normal())
```

この動作は期待通りになりません。

<video controls src="/godot_recipes/4.x/img/3d_kinematic_07.webm"></video>

問題は、タンクの衝突判定形状が地形面のうち複数箇所と干渉している可能性があることです。さらに、`move_and_slide()` 関数では1フレーム内で複数箇所で衝突が発生する場合があり、これが画面表示のカクつき（ジャダー）を引き起こしています。この問題を解決するためには、単一の面を選択し、一貫してその面で判定する必要があります。

タンクに {{< gd-icon RayCast3D >}}`RayCast3D` 子要素を追加し、 **ターゲット位置** を `(0, -1, 0)` に設定します。

このレイキャストが戦車の中心真下から下方向に発射されているため、衝突する個別の面、すなわち戦車直下の表面に整列させます。

```gdscript
func _physics_process(delta):
    velocity += gravity * delta
    get_input(delta)
    move_and_slide(v)
    var n = $RayCast3D.get_collision_normal()
    global_transform = align_with_y(global_transform, n)
```

これはかなり改善されましたが、タンクがエッジを越えるたびに瞬時に整列するため、まだ少し不自然に見えます。

<video controls src="/godot_recipes/4.x/img/3d_kinematic_08.webm"></video>

この最終問題は、即座にスナップするのではなく、新しい変換に補間することで解決できます。

```gdscript
func _physics_process(delta):
    velocity += gravity * delta
    get_input(delta)
    velocity = move_and_slide_with_snap(velocity, Vector3.DOWN*2, Vector3.UP, true)
    var n = $RayCast.get_collision_normal()
    var xform = align_with_y(global_transform, n)
    global_transform = global_transform.interpolate_with(xform, 12 * delta)
```

結果は非常に滑らかでより魅力的なものになります。

<video controls src="/godot_recipes/4.x/img/3d_kinematic_09.webm"></video>

以下の手順でさらに精度の高い結果を得られます。前面と背面にそれぞれレイキャストを1回ずつ実行します。そこから平均的な法線ベクトルを算出します。

```gdscript
var n = ($FrontRay.get_collision_normal() + $RearRay.get_collision_normal()) / 2.0
```

補間量は自由に調整してみてください。この環境で`12`が最適でしたが、環境によってはさらに高い値や低い値が適している場合もあります。

## <i class="fas fa-code-branch"></i> プロジェクトのダウンロード

プロジェクトのサンプルコードをダウンロードする：[https://github.com/godotrecipes/characterbody3d_examples](https://github.com/godotrecipes/characterbody3d_examples)

## 関連レシピ

- [CharacterBody3Dの移動](/godot_recipes/4.x/ja/3d/characterbody3d_examples/)
- [ゲーム数学 補間](/godot_recipes/4.x/ja/math/interpolation/)
- [ゲーム数学 トランスフォーム](/godot_recipes/4.x/ja/math/transforms/)

