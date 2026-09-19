# Project scripts

このディレクトリには、サイト本文の編集・翻訳・品質確認に使う Python スクリプトをまとめています。

## 入口となるシェルスクリプト

- `./scripts/i18n.sh update` — Markdown の内容を `output.po` に反映
- `./scripts/i18n.sh apply` — `output.po` の翻訳を日本語 Markdown に適用
- `./scripts/i18n.sh merge-html` — `docs_extracted.po` の新しい項目を `output.po` に追加
- `./scripts/checks.sh` — PO、Python、GDScript、生成 HTML のチェックをまとめて実行
- `./scripts/maintenance.sh fix-links` — PO 内の旧リンクを補正
- `./scripts/maintenance.sh split-translation` — 翻訳文の手順分割を実行

各スクリプトはプロジェクトルートから呼び出されるため、実行場所に依存しません。

## 配置

- `i18n/`: Markdown/HTML と PO の抽出・適用
- `checks/`: 翻訳、リンク、GDScript の検査
- `maintenance/`: 個別の保守処理
- `tests/`: Python のユニットテスト
