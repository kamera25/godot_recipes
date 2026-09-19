# Godotレシピ SEO改善計画

対象: https://kamera25.github.io/godot_recipes/4.x/ja/ と共通テンプレート。
実装担当: Luna。公開・検索順位の測定は今回のローカル修正とは別に実施する。

## 調査結果と優先順位

1. **ページごとの説明文を用意する。** 修正前の生成HTML304件では、日本語152件、英語152件がそれぞれ同一のmeta descriptionだった。明示した説明文を優先し、記事では本文から短い説明を生成する。OGPにも同じ説明を使用する。
2. **日本語トップで学べる内容を明示する。** 「ホーム」というタイトルを改善し、Godot 4、日本語チュートリアル、学習内容を自然に伝える。「Godot 4.0が最新安定版」という古い記述と、Godot 3案内の誤った外部リンクを直す。非公式翻訳であること、原著者、学習カテゴリへの導線も明確にする。
3. **URLの表記を統一する。** 修正前はcanonicalが末尾スラッシュ、hreflangとサイトマップがindex.html付きだった。既存のURL構造を維持し、テーマのdisableExplicitIndexURLs設定で整合させる。
4. **構造化データを安全に生成する。** テンプレートでJSON文字列を手組みせず、構造化した値をJSONとして出力する。言語、パンくず、原著者の扱い、画像の存在を確認する。修正前の圧縮ビルドではJSONの解析は成功しており、公開データが一律に壊れているという診断ではない。

## 完了条件

- Hugo 0.157.0で本番相当のビルドが成功する。
- 生成HTMLの構造化データをJSONとして解析できる。
- 日本語・英語のトップ、カテゴリ、記事でタイトルと説明文が出力される。
- canonical、言語切り替え情報、サイトマップが同じURL表記を使用する。
- 日本語トップからの内部リンクが生成先に存在する。
- URL変更、大規模な本文翻訳、架空の日付や評価の追加を行わない。

## 公開後の確認

Search Consoleでサイトマップ `https://kamera25.github.io/godot_recipes/4.x/sitemap.xml` の取得状況と、主要日本語ページのインデックス状況を確認する。改善前後の表示回数、クリック率、検索語句を比較する。今回Search Consoleのデータにはアクセスしていないため、流入や順位の改善量は未測定。

GitHub Pagesのプロジェクト配下にrobots.txtを追加しても、ホスト直下のrobots.txtの代わりにはならないため、それだけを目的とした追加は行わない。

## 参考資料

- [Google: ページ固有の説明文とスニペット](https://developers.google.com/search/docs/appearance/snippet)
- [Google: サイトマップの作成と送信](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google: 言語別ページの指定](https://developers.google.com/search/docs/specialty/international/localized-versions)
