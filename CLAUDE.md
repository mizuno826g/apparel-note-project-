# Apparel Note Project — 共通ルール

## プロジェクト概要

アパレル・ファッション系のトレンドリサーチ → 記事執筆 → ファクトチェック → 画像生成 → 公開
までを複数のAIエージェントが連携して実行するパイプライン。

---

## エージェント構成

| エージェント | ディレクトリ | 役割 |
|------------|------------|------|
| 01_trend-researcher | `01_trend-researcher/` | トレンド調査・情報収集 |
| 02_writer | `02_writer/` | 記事執筆 |
| 03_fact-checker | `03_fact-checker/` | ファクトチェック・精度検証 |
| 04_image-creator | `04_image-creator/` | 画像プロンプト生成・画像指示 |
| 05_orchestrator | `05_orchestrator/` | 全エージェントの進行管理 |

---

## データフロー

```
01_trend-researcher
  → shared/01_research_report.md

02_writer (01_research_report.md を読み込んで執筆)
  → shared/02_article_draft.md

03_fact-checker (02_article_draft.md を検証)
  → shared/03_factcheck_report.md

04_image-creator (02_article_draft.md + 03_factcheck_report.md を参照)
  → shared/04_image_report.md

05_orchestrator
  → output/ 以下に最終成果物を格納
```

---

## shared/ ディレクトリ ルール

- **書き込み権限：** 担当エージェントのみが自分の出力ファイルに書き込む
- **読み込み：** すべてのエージェントが参照可能
- **フォーマット：** Markdown（`.md`）形式で統一
- **上書き禁止：** 既存ファイルを削除せず、バージョンが必要な場合は末尾に `_v2` 等を付与

---

## output/ ディレクトリ ルール

- `output/articles/` — 完成記事（Markdown）
- `output/images/` — 画像プロンプト・生成画像の管理ファイル
- `output/reports/` — 各工程のサマリーレポート

---

## 共通トーン & マナー

- **対象読者：** ファッションに関心のある20〜40代
- **文体：** 読みやすく、専門性と親しみやすさを両立
- **事実ベース：** 推測・憶測での記述は禁止。情報は出典を明記
- **コピーライト：** 他者コンテンツの無断転載禁止。要約・引用は出典を示す

---

## 各エージェントへの共通指示

1. 作業開始前に `shared/` 内の前工程ファイルを必ず読み込むこと
2. 出力ファイルへの書き込みが完了したら、05_orchestrator に完了を報告すること
3. 不明点・エラーは作業を止めず `output/reports/` にログを残すこと
