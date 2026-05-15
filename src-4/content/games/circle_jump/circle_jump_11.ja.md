---
title: "モバイル広告"
weight: 11
draft: false
pre: "11. "
---

{{% notice style="tips" title="ℹ️ 留意事項"%}}
この記事は Godot 3から Godot 4 へ内容の書き換え中です。
Godot4では存在しない変数、関数が含まれている場合があります。もしその場合はリポジトリの[Issues](https://github.com/kamera25/godot_recipes/issues)までご報告ください。
{{% /notice %}}

## 広告について

無料プレイ型モバイルゲームを開発する際、収益化手段としてアプリ内課金と広告の2つの選択肢があります。本記事では、モバイル広告プラットフォーム（AdMob）をゲームに統合する方法について解説します。

広告は必ずしも好まれるものではなく、その導入の有無は個々のゲーム開発者が判断すべき事項です。本チュートリアルではメリット・デメリットの検討には踏み込みません。ここでは「もし広告を実装したい」と考えている方向けに、その方法を丁寧に解説します。

## AdMobの設定する

[AdMob](https://www.admob.com/)に移動してアカウントを作成します。

アドモブマネージャーで新しいアプリを作成します。アプリは「サークルジャンプ」というタイトルです。そして「Android」プラットフォームを指定します（iOSについては後ほど説明します）。

「Circle Jump」アプリでは、「広告ユニット」を3種類作成が必要です。これらはゲーム内で表示可能な各種広告形式です。今回のチュートリアルでは、「バナー広告」と「インタースティシャル広告」が必要になります。各広告ユニットには「Ad Unit ID」という文字列が割り当てられます（これは後でゲーム内で使用します）。

![alt](/godot_recipes/4.x/img/cj_11_01.png)

## Godotモジュールの使用について

Godot はデフォルトでは広告サービスを対応していないため、この機能を追加するにはエンジンモジュールまたはプラグインを使用が必要です。使用するモジュールはこちらから確認できます。 [godot-admob](https://github.com/kloder-games/godot-admob)。
このページには、プラグインが提供するメソッドの一覧が記載されています。

カスタムエンジンモジュールを使用するには、エンジンの再コンパイルが必要です。モバイルプラットフォームの場合、デフォルトでダウンロードしたエクスポートテンプレートは本モジュールに対応した形でコンパイルされていないため、それらも再コンパイルが必要です。

エクスポートテンプレートのコンパイルは難しくありませんが、コンピュータ上にビルド環境を設定しましょう。これには、Godotをビルドするために必要なプログラムやライブラリをダウンロードすることが含まれます。この概念に慣れておらず詳しく知りたい場合は、公式ドキュメントの [コンパイル] セクションを参照しましょう [Compiling](https://docs.godotengine.org/ja/latest/development/compiling/introduction_to_the_buildsystem.html)。

幸いなことに、カスタムエクスポートテンプレートの作成は既に完了しています。[godot-custom-mobile-templates](https://github.com/Shin-NiL/godot-custom-mobile-template) GitHubリポジトリに移動します。「リリース」タブを開き、自分の使用しているGodotバージョンに対応したエクスポートテンプレートをダウンロードします。

{{% notice warning %}}
エクスポートテンプレートのバージョンは**必ず**Godotエディタのバージョンと一致しています。カスタムビルド版のエディタを使用している場合は、同じコードブランチからテンプレートも構築が必要です。
{{% /notice %}}

テンプレートをコンピュータの任意の場所に解凍しましょう（Circle Jumpプロジェクトフォルダには入れないでください）。

## エクスポートの設定

Godot エディターに戻って、エクスポート設定に変更を加えましょう。まず、_プロジェクト -> プロジェクト設定_ を開き、「Android」セクションを見つけてください。_モジュール_ プロパティには、コードで使用するモジュールをリストします。モジュール名は `godot-admob` ページに記載されています。"org/godotengine/godot/GodotAdMob"。使用するモジュールが複数ある場合は、カンマで区切ってください。

_プロジェクト設定 -> エクスポートメニューでは、ダウンロードしたカスタムテンプレートを使用するようにGodotに指示が必要です。これらは［カスタムパッケージ］セクションで設定します。フォルダアイコンをクリックして、テンプレートを解凍したディレクトリに移動します。「デバッグ」と「リリース」両方のテンプレートを必ず追加します。

![alt](/godot_recipes/4.x/img/cj_11_02.png)

## コード例

現在ゲームを実行すると（Android端末上で）、指定したモジュールが読み込まれるようになります。これはエンジンのシングルトン経由でアクセスできます。`settings.gd`ファイルを開いて、以下の内容を追加します。

```gdscript
var admob = null
var real_ads = false
var banner_top = false
# Fill these from your AdMob account:
var ad_banner_id = ""
var ad_interstitial_id = ""
var enable_ads = true
```

これはモジュール用の設定変数です。`real_ads` を `false` に設定すると「テスト広告」モードになります。ゲームリリース準備が整うまでは、これを `true` に変更しないでください。`banner_top` は、バナー広告を画面上部に表示するか下部に表示するかを切り替えるトグルです。

`ad_banner_id` および `ad_interstitial_id` には、AdMobアカウントから取得した広告ユニット値を設定が必要です。

モジュールの初期化が必要です。

```gdscript
func _ready():
    if Engine.has_singleton("AdMob"):
        admob = Engine.get_singleton("AdMob")
        admob.init(real_ads, get_instance_id())
        admob.loadBanner(ad_banner_id, banner_top)
        admob.loadInterstitial(ad_interstitial_id)
```

まずモジュールのシングルトンが存在するかを確認します。存在が確認できれば、モジュールを初期化し、広告ユニットを読み込むことができます。

```gdscript
func show_ad_banner():
    if admob and enable_ads:
        admob.showBanner()

func hide_ad_banner():
    if admob:
        admob.hideBanner()
```

次に、バナーの表示／非表示を制御する機能について説明します。これはメニュー画面でのみ表示し、実際のゲームプレイ中には表示されないようにします。

```gdscript
func show_ad_interstitial():
    if admob and enable_ads:
        admob.showInterstitial()
```

この関数を使用して、ゲーム終了時にインタースティシャル広告を表示します。

```gdscript
func _on_interstitial_close():
    if admob and enable_ads:
        show_ad_banner()
```

このモジュールは、インタースティシャル広告が閉じた時にコードを実行するためのコールバックを探しています。ゲームの終了時でメニューに戻るため、バナーを再表示します。

これから、これらの関数をゲームコードから呼び出しましょう。`Main.gd`を開いて、以下を追加します。

- `new_game()`関数内で`settings.hide_ad_banner()`を追加しましょう
- `_on_Jumper_died()`関数の最後に`settings.show_ad_interstitial()`を追加しましょう

デバイスでゲームを起動すると、テスト広告が表示されるはずです。

![alt](/godot_recipes/4.x/img/cj_11_03.jpg)

## 広告を無効化する

多くのゲームでは、アプリ内課金や特定レベル到達などによって広告を非表示にできる機能が提供されています。今回の場合、「設定」画面に追加ボタンを設ける形で実装します。

まず、`enable_ads`の値を変更できるように、セッター関数を追加します。

```gdscript
var enable_ads = true setget set_enable_ads
```
また、セッター関数を追加します。

```gdscript
func set_enable_ads(value):
    enable_ads = value
    if enable_ads:
        show_ad_banner()
    if !enable_ads:
        hide_ad_banner()
```

この設定により、ボタンを押した際にバナー追加機能が即座に表示／非表示されます。

ボタンを追加するには、3行目のボタン列が必要になります。`BaseScreen`シーンを開き、最初のHBoxContainerを複製します。

[`SettingsScreen`]シーンに「Ads」という名前の`Button`を中央の行に追加します。テキストを「広告を無効にする」に設定し、カスタムフォント（サイズ48が適切です）を適用し、さらにカスタムスタイルをすべて「New StyleBoxEmpty」に設定します。最後に、このボタンを「buttons」グループに追加することを忘れないでください。

`Screens.gd`ファイル内で、ボタン処理用の`match`ステートメントに以下を追加します。

```gdscript
match button.name:
    "Ads":
        settings.enable_ads = !settings.enable_ads
        if settings.enable_ads:
            button.text = "Disable Ads"
        else:
            button.text = "Enable Ads"
```

![alt](/godot_recipes/4.x/img/cj_11_04.png)

デバイスでゲームを実行し、広告の有効化／無効化が行えることを確認します。

----------

#### GitHubでプロジェクトをフォローしましょう！

[https://github.com/kidscancode/circle_jump](https://github.com/kidscancode/circle_jump)

#### 動画で見る

{{< youtube 8SOw_Tmw2OI6qclA >}}
