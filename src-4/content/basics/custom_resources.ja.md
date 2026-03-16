---
title: "カスタムリソースを使用"
weight: 10
draft: false
ghcommentid: 85
---

## 課題

ゲーム内でデータを処理する方法や、柔軟なデータオブジェクトを作成する方法を探しているようです。

## 解決策

Godotの`Resource`クラスは、データを格納・操作するための強力なツールです。Godotで扱う最も一般的なオブジェクトの多くは[Resource](https://docs.godotengine.org/ja/stable/classes/class_resource.html#class-resource)タイプを拡張しています。アニメーション、衝突形状、画像など。リソースは単なるデータ保持だけでなく、そのデータを操作することもできます（Unityの *ScriptableObject* に似ています。）。

Godot に標準で用意されているすべての `リソース`タイプに加え、独自のカスタムリソースを作成してゲーム固有のデータを管理することもできます。これはデータの抽象化とカプセル化を実現する利点があり、ゲーム内の他のあらゆるオブジェクトから利用できる汎用的なコンポーネントを作成できます。

### 例：プレイヤーの移動

この例では、プラットフォーマーゲームにおけるプレイヤーの体力管理を取り上げます。多くのゲームプレイシステムはプレイヤーの健康状態と連動しています。例えば：

* プレイヤーが障害物に衝突するとダメージを受ける場合があります
* 敵キャラクターがプレイヤーに触れたり攻撃したりすることでダメージを与えられます
* オブジェクトを拾う、または特定の場所に立つことでプレイヤーが回復できます
* ゲーム画面には体力ゲージを表示し、発生する変化を適切に表示が必要です

さらに、他の相互作用も存在する可能性があります。プレイヤーが体力を減らすとゲームのサウンドトラックが変化する、あるいは敵の行動パターンがプレイヤーのステータスに応じて変化する、といった具合です。

{{% notice note %}}
これは意図的に簡略化した例です。実際の運用では、ここで使用している機能よりも多くの機能が必要になる場合や、ゲームのアーキテクチャに合わせてこの例を修正する必要があるでしょう。
{{% /notice %}}

まず最初に、新しいカスタムリソース「PlayerHealth」を定義が必要です。このリソースは健康状態に関連するプロパティを管理が必要です。さらに、体力値の変化（回復やダメージを受けるなど）を処理するための機能とシグナルを提供します。

スクリプトタブで、ファイル >新規スクリプト を選択します。「リソース」を継承するように設定し、ファイル名を "PlayerHealth.gd" とします。

これを部分ごとに分解して考えましょう。

上部には `extends` 行とリソースに割り当てる `class_name` があります。このページ名はエディタ内の様々な場所で表示されます。

```gdscript
extends Resource
class_name PlayerHealth
```

次に、ゲームオブジェクトがプレイヤーのHP値変化を監視するために購読できるシグナルがあります。また、HP値がゼロに達するなどの追加イベント用のシグナルも実装できます。

```gdscript
signal health_changed
```

使用するプロパティです。

```gdscript
export (int) var max_value

var current_value = 0
```

この関数を使用すると、HPを最大値に初期化できます。ゲームの再起動時や新しいレベルを開始する際に実行するとよいでしょう。

```gdscript
func reset():
    current_value = max_value
```

この機能はプレイヤーにダメージが与えられた際に毎回呼び出されるべきです。

```gdscript
func take_damage(amount):
    current_value = max(0, current_value - amount)
    emit_signal("health_changed", current_value)
```

この機能はプレイヤーの回復が必要な時に随時呼び出されるべきです

```gdscript
func heal(amount):
    current_value = min(max_value, current_value + amount)
    emit_signal("health_changed", current_value)
```

以下が完全なスクリプトです：

```gdscript
extends Resource
class_name PlayerHealth

signal health_empty
signal health_changed

export (int) var max_value

var current_value = 0

func reset():
    current_value = max_value

func take_damage(amount):
    current_value = max(0, current_value - amount)
    emit_signal("health_changed", current_value)

func heal(amount):
    current_value = min(max_value, current_value + amount)
    emit_signal("health_changed", current_value)
```

#### 新規リソースの作成

一度「PlayerHealth」クラスを定義すれば、新しいインスタンスを作成できます。インスペクター上部の「新規リソース作成」ボタンをクリックしてください。

![alt](/godot_recipes/3.x/img/custom_resource_01.png)

「新規リソース作成」ダイアログでは、様々な種類のリソースが一覧表示されます。検索機能を使って、作成した `PlayerHealth` タイプを見つけてください。

![alt](/godot_recipes/3.x/img/custom_resource_02.png)

これで、希望する`max_value`を設定し、新しいリソースを`.tres`ファイルとして保存できます。

![alt](/godot_recipes/3.x/img/custom_resource_03.png)

#### リソースの使用方法

リソースの作成と保存が完了したら、いよいよ使用準備が整います。このシナリオでは、以下のオブジェクトが存在します。

* プレイヤー： `KinematicBody2D`（{{< gd-icon KinematicBody2D >}}）オブジェクト
* UI要素：健康状態を表示する `ProgressTexture`（{{< gd-icon TextureProgressBar >}}）を含むコンポーネント
* 回復エリア：その範囲内に入った対象を回復する `Area2D`（{{< gd-icon Area2D >}}）ノード
* スパイクゾーン：接触するとダメージを与えるタイルマップのタイルセット

ゲームの全コードを掲載するのではなく、体力リソースに関連する部分だけを取り上げます。

プレイヤー側では、インスペクター経由でリソースを割り当てるために変数を `エクスポート` しています。移動処理コードの一部として、プレイヤーがスパイクに接触した際には `hurt()` 関数を呼び出すようになっています。

```gdscript
export (Resource) var health

func _ready():
    health.reset()

func hurt(amount):
    # Called when running into obstacles
    health.take_damage(amount)
```

回復ゾーン（`Area2D`オブジェクト）は、内部に位置し`health`プロパティを持つすべてのオブジェクトに影響を与えます。

```gdscript
func _physics_process(delta):
    for body in get_overlapping_bodies():
        if "health" in body:
            body.health.heal(heal_rate * delta)
```

最後に、UIにHPステータスを表示するために、同じHPリソースを接続し、その`health_changed`シグナルに接続します。

```gdscript
export (Resource) var player_health

func _ready():
    if player_health:
        player_health.connect("health_changed", self, "_on_player_health_changed")

func _on_player_health_changed(value):
    healthbar.value = float(value) / player_health.max_value * 100
```

動作例をご覧ください。

![alt](/godot_recipes/3.x/img/custom_resource_04.gif)

{{% notice note %}}
プロジェクトファイルをこちらからダウンロードしてください: [custom_resources.zip](/godot_recipes/3.x/files/custom_resources.zip)
{{% /notice %}}

## 関連レシピ

- [プラットフォームキャラクター](/godot_recipes/4.x/ja/2d/platform_character/)
- [オブジェクトのHPバー](/godot_recipes/4.x/ja/ui/unit_healthbar/)