---
title: "レイキャストを使用した射撃"
weight: 3
draft: false
tags: []
---

## 課題

FPSゲームで射撃機能を実装しますが、個別の発射物を手動で動かすのは非現実的です。

## 解決策

ゲームの物理演算エンジンは、非常に高速で移動するオブジェクトを処理しようとすると破綻しがちです。解決策としては、射手の位置からレイキャストを行い、最初に衝突する物体を検出する方法が有効です。

Godotにおけるレイキャスティングには、主に2つの方法があります。{{< gd-icon RayCast3D >}}`RayCast3D`ノードを使用する方法と、物理エンジンを直接操作して空間内に直線状の光線（レイ）を投射する方法です。どちらも同じ目的を達成できますが、それぞれに異なる利点があります。ノードベースのアプローチは、継続的な衝突検出が必要な場合に特に有効です - 例えば、床に触れているかどうかを確認するための下向きのレイを継続的にチェックする場合などに最適です。

第二の方法、つまり物理状態を問い合わせる方法を採用しましょう。これは、「発射」キーを押した瞬間に、何かに当たったかどうかを知りたいからです。

{{% notice note %}}
このレシピでは、すでに動作するFPSキャラクターコントローラーと移動可能なワールドが用意されていることを前提としています。もし用意されていない場合は、先に[FPSキャラクターの作り方](/godot_recipes/4.x/ja/3d/basic_fps)のチュートリアルを参照してください。
{{% /notice %}}

ヒットした内容を確認するには、`FPSPlayer`シーンに{{<  gd-icon CanvasLayer >}}`CanvasLayer`ノードと{{<  gd-icon Label >}}`Label`ノードを追加してください。

We'll add an input check in the `_input()` function, which we're already using to handle mouse input.

```gdscript
    if event.is_action_pressed("shoot"):
        shoot()
```

次に、`shoot()` メソッドを定義します。この関数が呼び出されるたびに、以下の処理を実行する `PhysicsRayQueryParameters3D` オブジェクトを作成します。
1. レイの始点（カメラ位置）を定義
2. レイの終点（カメラから前方100メートル投影された位置）を定義

このパラメータはワールドの `direct_space_state` を通じて物理エンジンに渡されます。衝突情報を含むDictonaryが返された場合、そのデータに基づいてラベルを更新し、当たったオブジェクトの種類を表示できるようにします。

```gdscript
func shoot():
    var space = get_world_3d().direct_space_state
    var query = PhysicsRayQueryParameters3D.create($Camera3D.global_position,
            $Camera3D.global_position - $Camera3D.global_transform.basis.z * 100)
    var collision = space.intersect_ray(query)
    if collision:
        $CanvasLayer/Label.text = collision.collider.name
    else:
        $CanvasLayer/Label.text = ""
```


## 関連レシピ

- [FPSキャラクターの作り方](/godot_recipes/4.x/ja/3d/basic_fps)

## <i class="fas fa-code-branch"></i> このプロジェクトをダウンロードする

プロジェクトコードはこちらよりダウンロードできます。 [https://github.com/godotrecipes/3d_shoot_castrays](https://github.com/godotrecipes/3d_shoot_castrays)
