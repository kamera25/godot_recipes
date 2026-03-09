---
title: "Adding Input Actions in code"
weight: 3
draft: false
---

## 問題文

実行時に入力マップにアクションを追加する必要があります。

## 解決策

通常、入力アクションは[プロジェクト設定]から追加します（詳細は[レシピ：入力アクション]参照）。ただし、スクリプト内で直接アクションを追加する必要がある場合もあります。このような場合には、［InputMapシングルトン］(https://docs.godotengine.org/en/latest/classes/class_inputmap.html)が提供するメソッドが便利です。

以下に、スペースキーを使用して「攻撃」という新しいアクションを追加する例を示します：

```gdscript
func _ready():
    InputMap.add_action("attack")
    var ev = InputEventKey.new()
    ev.keycode = KEY_SPACE
    InputMap.action_add_event("attack", ev)
```

左マウスボタンも同じ操作に追加したい場合は：

```gdscript
ev = InputEventMouseButton.new()
ev.button_index = MOUSE_BUTTON_LEFT
InputMap.action_add_event("attack", ev)
```

{{% notice note %}}
`InputMap.add_action()` メソッドは、同じアクションが既に存在する場合にエラーを発生させます。新しいアクションを追加する前に、まず `InputMap.has_action()` で確認することをお勧めします。
{{% /notice %}}

### 実際の使用例

たとえば、[レシピ: プラットフォームキャラクター](/godot_recipes/4.x/2d/platform_character/)で作成したプラットフォームキャラクターを別のプロジェクトで再利用したい場合を考えてみましょう。シーンファイル、スクリプト、およびアセットをすべて単一フォルダに保存していれば、そのフォルダ全体を新規プロジェクトにコピーするだけで済みます。ただし、入力が正常に機能するようにするには、インタラクションマップも編集する必要があります。

代わりに、以下のコードをプレイヤースクリプトに追加すれば、必要な入力アクションが自動的に追加されるようになります：

```gdscript
var controls = {"walk_right": [KEY_RIGHT, KEY_D],
                "walk_left": [KEY_LEFT, KEY_A],
                "jump": [KEY_UP, KEY_W, KEY_SPACE]}

func _ready():
    add_inputs()

func add_inputs():
    var ev
    for action in controls:
        if not InputMap.has_action(action):
            InputMap.add_action(action)
        for key in controls[action]:
            ev = InputEventKey.new()
            ev.keycode = key
            InputMap.action_add_event(action, ev)
```

## 関連レシピ

- [入力アクション設定](/godot_recipes/4.x/input/input_actions/)
- [プラットフォーマーキャラクタの作成](/godot_recipes/4.x/2d/platform_character/)

<!-- #### この動画が気に入ったら？
 -->
