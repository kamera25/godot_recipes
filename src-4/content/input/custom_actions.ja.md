---
title: "実行中に入力アクションを追加する"
weight: 3
draft: false
---

## 課題

実行時にインプットマップにアクションを追加が必要です。

## 解決策

Typically, you'll add actions to the 入力Map via _Project Settings_, as shown in [Recipe: 入力アクション](/godot_recipes/4.x/input/input_actions/). However, you may find yourself needing to add one or more actions directly in a script. The [入力Map singleton](https://docs.godotengine.org/en/latest/classes/class_inputmap.html) has methods to help you do this.

以下に、スペースキーを使用して「攻撃」という新しいアクションを追加する例を示します。

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
`入力Map.add_action()` メソッドは、同じアクションが既に存在する場合にエラーを発生させます。新しいアクションを追加する前に、まず `入力Map.has_action()` で確認することをオススメします。
{{% /notice %}}

### 実際の使用例

たとえば、[レシピ: プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)で作成したプラットフォームキャラクターを別のプロジェクトで再利用したい場合を考えてみましょう。シーンファイル、スクリプト、およびアセットをすべて単一フォルダに保存していれば、そのフォルダ全体を新規プロジェクトにコピーするだけで済みます。ただし、入力が正常に機能するようにするには、インタラクションマップも編集が必要です。

代わりに、以下のコードをプレイヤースクリプトに追加すれば、必要な入力アクションが自動的に追加されるようになります。

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

- [入力アクション設定](/godot_recipes/4.x/ja/input/input_actions/)
- [プラットフォーマーキャラクタの作成](/godot_recipes/4.x/ja/2d/platform_character/)

<!-- #### Videoをいいねしましたか？ -->
