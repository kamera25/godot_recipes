---
title: "Saving/loading data"
weight: 4
draft: false
ghcommentid: 13
---

## 問題文

ゲームセッション間でローカルデータを保存・読み込みする必要があります。

## 解決策

ゴドットのファイル入出力（IO）システムは `FileAccess` オブジェクトを基盤として構築されています。ファイルをオープンするには `open()` メソッドを呼び出す必要があります。

```gdscript
var file = FileAccess.open("user://myfile.name", File.READ)
```

{{% notice warning %}}
ユーザーデータは `user://` パスにのみ保存する必要があります。エディタから直接実行している場合には `res://` も使用可能ですが、プロジェクトをエクスポートすると、`res://` パスは読み取り専用になります。
{{% /notice %}}

The second argument after the file path is the "Mode Flag", which can be one of the following:

* FileAccess.READ - 読み取り専用でファイルを開く
* FileAccess.WRITE - 書き込み専用でファイルを開く（存在しない場合は新規作成、存在する場合も先頭から再書き込み）
* FileAccess.READ_WRITE - 読み書き両用モードでファイルを開く（既存ファイルは切り捨てない）
* FileAccess.WRITE_READ - 読み書き両用モードでファイルを開く（存在しない場合は新規作成、存在する場合も先頭から再書き込み）

### データの保存方法

データの保存には、その専用データ型（`store_float()`、`store_string()`など）を使用する方法と、汎用的な`store_var()`メソッドを使用する方法があります。後者はGodot組み込みのシリアライゼーション機能を利用してデータをエンコードするため、オブジェクトなどの複雑なデータ構造も扱えます（詳細は後述します）。

まずは簡単な例から始めましょう。プレイヤーのハイスコアを保存する場合を考えます。必要に応じて呼び出せる関数を作成できます：

```gdscript
var save_path = "user://score.save"

func save_score():
    var file = FileAccess.open(save_path, FileAccess.WRITE)
    file.store_var(highscore)
```

我们正在保存得分，但游戏开始时需要能够加载它：

```gdscript
func load_score():
    if FileAccess.file_exists(save_path):
        print("file found")
        var file = FileAccess.open(save_path, FileAccess.READ)
        highscore = file.get_var()
    else:
        print("file not found")
        highscore = 0
```

ファイルを読み込もうとする前に、まずその存在を確認することを忘れないでください。存在しない可能性があるためです。もし存在しない場合は、デフォルト値を使用することが可能です。

必要に応じて任意の数の値に対して何度でも `store_var()` および `get_var()` を使用できます。

### リソース節約について

上記の手法は、保存するデータが少数の値で済む場合には非常に有効です。より複雑なケースでは、Godotと同様にリソース形式でデータを保存することが可能です。Godotは全てのデータを`.tres`ファイル（アニメーション、タイルセット、シェーダーなど）として管理していますが、あなたも同様の方法でデータを保存できます！

リソースの保存と読み込みには、Godot クラスの `ResourceSaver` と `ResourceLoader` を使用してください。

例を挙げると、キャラクターのステータス情報がすべて以下のようにリソースに格納されているとします：

```gdscript
extends Resource
class_name PlayerData

var level = 1
var experience = 100

var strength = 5
var intelligence = 3
var charisma = 2
```

以下のように保存・読み込みが可能です：


```gdscript
func load_character_data():
    if ResourceLoader.exists(save_path):
        return load(save_path)
    return null

func save_character_data(data):
    ResourceSaver.save(data, save_path)
```

リソースにはサブリソースを含められるため、プレイヤーのインベントリ用リソースも必要に応じて一緒に読み込むことができます。このように拡張可能です。

### JSONについてはどうでしょうか？

I see it very often (and some readers may be asking it already): "What if I want to use JSON to save my data?" This is my response:

> SaveファイルにJSONを使用するのは止めてください！

Godotには[JSONサポート](https://docs.godotengine.org/en/latest/classes/class_json.html)が組み込まれていますが、ゲームデータの保存用途としては設計されていません。JSONは「データ交換」形式であり、異なるデータフォーマットやプログラミング言語を使用するシステム間でデータを相互にやり取りできるようにすることを目的としています。

これはつまり、JSONにはゲームデータ保存時に不利となる制約があることを意味します。JSONは多くのデータ型をサポートしていないため（整数と浮動小数点数の区別ができないなど）、データを保存したり読み込んだりするためには、変換や検証に多大な労力を要します。非常に手間がかかり、時間もかかる作業です。

時間を無駄にしないでください。Godotの組み込みシリアル化機能を使用すれば、ノードやリソース、さらにはシーンそのものといったネイティブなGodotオブジェクトを一切手間をかけずに保存できます。これにより、コード量が減り、エラーも減少します。

Godot 自体がシーンやリソースの保存にJSONを使用していないのには理由があります。

### まとめ

この記事で「`FileAccess`」の基本的な機能をざっとご紹介しました。利用可能な「`FileAccess`」メソッドの全一覧については、[公式ドキュメントの`FileAccess`ページ](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html)をご覧ください。