---
title: "衝突レイヤーとマスク"
weight: 3
draft: false
---

## 解決策

衝突レイヤーとマスクは、Godot 4においてどのオブジェクト同士が相互作用するかを制御する上で不可欠な要素です。

#### 胸

*  **衝突判定レイヤー**：オブジェクトが **存在する** レイヤを指定します。
*  **衝突検知マスク**：オブジェクトが **衝突を検出する** 対象のレイヤを指定します。

### サンプルプロジェクト例

※ ノード | 層 | マスク | 相互作用 ※
| :--- | :--- | :--- | :--- |
| **プレイヤー** | 1 | 2, 3 | 敵とコインをスキャン |
| **敵キャラ** | 2 | 1 | プレイヤーをスキャン |
| **コイン** | 3 | (なし) | 特にスキャンする必要がない |

### セットアップ方法

Godot 4では、プロジェクト設定の［レイヤー名］＞［2D物理演算］でレイヤーに名前を付けられます。これにより、インスペクターでの管理が大幅に効率化されます。

### ノードの選択方法

Godot 4では、ビット操作を容易にするため、`get_collision_layer_value(layer_number)`と`set_collision_layer_value(layer_number, value)`を使用することをおすすめします。

```gdscript
# Enable layer 2
set_collision_layer_value(2, true)

# Check if masking layer 3
if get_collision_mask_value(3):
    print("Scanning layer 3")
```

[!NOTE]
**Godot 3から4への移行ポイントまとめ**:
- レイヤー用インスペクターUIが改善されました
- `set_collision_layer_value()`などの新ヘルパーメソッドにより、複雑なビット演算処理(例: `1 << (layer - 1)`)が不要になりました
