# AI副業OS — 最強コスパAI部隊 基本設計

最終更新: 2026-09-24

## 目的

最高性能のAIを常用するのではなく、

**「成果・収益 ÷ AIコスト」を最大化する。**

### 原則

- 無料AIでできる仕事に有料AIを使わない
- 高性能AIは「難しい判断」に集中させる
- 同じ仕事を複数AIに重複させない
- 失敗した場合だけ上位AIへEscalateする
- AIインフラ構築そのものを目的化しない
- 「30日以内の収益化に寄与するか？」を優先順位の基準にする

最適化対象は **API単価** ではなく、
**「人間の時間を含めた成果1件あたり総コスト」** とする。

---

## 指揮系統（Command Chain）

```
                         USER
                          │
                          ▼
                 ┌────────────────┐
                 │      CODEX      │   司令塔（Commander）
                 └───────┬────────┘   最終優先度決定・重大Escalationの受け皿
                          │
                          ▼
                 ┌────────────────┐
                 │   GPT / Sol     │   副司令塔（Deputy Commander）
                 └───────┬────────┘   タスク分解・AI割当・シニアレビュー・収益判断
                          │
              タスク分解・AI割当
                          │
                          ▼
        ┌────────────────────────────┐
        │      FREE / CHEAP LAYER    │   第1実行部隊
        │                            │
        │ OpenRouter Free / Qwen /   │
        │ Kimi / Gemini free tier /  │
        │ DeepSeek（低額時のみ）/     │
        │ MiniMax / Local Qwen 等     │
        └────────────┬───────────────┘
                     │
              成功 ──┴──→ 完了（必要時のみGPT/Solレビュー）
                     │
                   失敗
                     ▼
        ┌────────────────────────────┐
        │       CLAUDE CODE          │   実行部長（第2実行部隊）
        │                            │
        │ ・実装 / GitHub作業         │
        │ ・デバッグ / テスト          │
        │ ・複数ファイル修正           │
        │ ・無料AI失敗案件の回収       │
        └────────────┬───────────────┘
                     │
              成功 ──┴──→ GPT/Solレビュー
                     │
              難しい設計問題
                     ▼
        ┌────────────────────────────┐
        │         GPT / SOL          │   シニアレビュー層
        │                            │
        │ ・品質確認 / 仕様判断        │
        │ ・収益性判断 / セキュリティ   │
        │ ・設計レビュー / Escalation  │
        │   判断                      │
        └────────────┬───────────────┘
                     │
              通常 ──┴──→ 完了
                     │
             本当に難しい問題のみ
                     ▼
        ┌────────────────────────────┐
        │          ASTRA             │   Principal / Architect
        │                            │
        │ ・初期アーキテクチャ         │
        │ ・重大な技術選定             │
        │ ・解決困難な設計問題         │
        │ ・大規模な方向転換判断       │
        └────────────────────────────┘
```

---

## 標準実行フロー

```
TASK
 ↓
収益化への寄与を判定
 ↓
GPT/Sol Medium等で小さなTaskへ分解
 ↓
最安で処理可能なAIを選択
 ↓
FREE / CHEAP AI
 ↓
成功？ ─ YES → 結果保存 → 必要時のみGPT/Solレビュー
 │
 NO
 ↓
Claude Code（実行部長）
 ↓
成功？ ─ YES → GPT/Solレビュー → 完了
 │
 NO / 設計問題
 ↓
GPT / Sol
 ↓
設計レベルの問題？
 │
 NO → 修正指示 → Claude Code / Cheap AI
 │
 YES
 ↓
Astra
 ↓
設計判断
 ↓
Claude Code / Cheap AIへ実装を戻す
```

---

## AIの役割分担

### Codex — 司令塔（Commander）

組織全体のタスク進捗を統括する最上位レイヤー。

担当:
- 全体タスクの最終優先順位決定
- GPT（副司令塔）への大方針の指示
- Astra判断を経た重大な方向転換の最終承認

禁止:
- Routineな実装・レビュー業務への介入（下位層に委譲する）

### GPT / Sol — 副司令塔（Deputy Commander）

Engineering Manager 兼 Senior Reviewer。Codexの指示を実行可能なタスクへ分解し、AIを割り当てる。

担当（Sol Medium: Task Planner）:
- 大きな要求を小さなTaskへ分解
- 実装仕様作成
- AI割当判断
- Claude Codeへの指示作成

担当（Sol: Senior Reviewer / Business Decision）:
- 最終レビュー
- バグ / 仕様逸脱チェック
- 収益性判断
- 品質Gate
- Escalation判断（Astraへ上げるか否か）

原則として大量実装はしない。Routine作業（Sheets更新、GitHub転記、要約、通常Debug）には使わない。

### 無料・低額AI（Free / Cheap Layer） — 第1実行部隊

大量に使う「作業員」。OpenRouter Free / Qwen / Kimi / Gemini free tier / DeepSeek（低額時のみ）/ MiniMax / Local Qwen 等。

担当:
- 調査の一次処理、要約、翻訳、分類
- SNS台本、字幕、記事ドラフト
- データ整形、Sheets更新、GitHub Issue更新、ログ整理
- 軽微なコード修正、定型作業

可能な限りここで完了させる。

### Claude Code — 実行部長（第2実行部隊）

無料・低額AIの次の階層。**下位AIで処理可能なTaskは可能な限り下位層へ委譲し、自分自身がすべての仕事を処理することを目的としない。**

担当:
- 実際のコード実装、Repo横断修正、GitHub作業
- Debug、Test、Refactoring
- 無料AIが失敗した実装の回収
- ある程度複雑な自動化

重要:
- 最初からClaude Codeを使わない。まず無料/低額AIへ投げ、能力不足の場合のみEscalateする。
- 上位（GPT/Sol、Astra）へEscalateするのは、実装能力ではなく **設計・仕様判断** が必要になった場合を原則とする。
- 役割は「下位AIでは難しい実装・Debug・GitHub作業を高品質に完了させる第2実行階層」。

### Astra — Principal Engineer / Architect

担当:
- 初期Architecture
- 重大な技術選定
- 難しい設計問題
- 大規模な方向転換

禁止:
- Routine coding、Sheets更新、GitHub転記、要約、通常Debug、単純実装

Astraは「コードを書く人」ではなく「最上位の設計者」として扱う。

---

## コスト原則

優先順位:

```
FREE
 ↓
ULTRA LOW COST
 ↓
CLAUDE CODE
 ↓
GPT / SOL
 ↓
ASTRA
```

ただし「安いAIを使うための環境構築」に時間を浪費してはいけない。無料AI接続に時間が掛かる場合は、Claude Code等へ即座にEscalateする。

最適化対象は **API単価** ではなく **「人間の時間を含めた成果1件あたり総コスト」** とする。

---

## 管理・学習ループ

各Taskについて記録する項目:

Task ID / Project / Priority / Revenue Impact / Assigned AI / Actual AI / AI Tier / Cost / Execution Time / Success or Failure / Quality / Escalation / Revenue Result

```
GitHub = AI向けTask / Code / Result
↓
Google Sheets = 人間向けDashboard
↓
AIごとの実績を集計
↓
成功率 × コスト × 速度 × 収益貢献を評価
↓
成績の良いAIへTaskを多く割り当てる
```

---

## 最終的に目指す状態

```
仕事
 ↓
AI Router
 ↓
最安AIへ自動配車
 ↓
無料AIで80〜90%処理
 ↓
難しい実装だけClaude Code
 ↓
判断だけGPT / Sol
 ↓
極めて難しい設計だけAstra
 ↓
結果をGitHub / Sheetsへ自動記録
 ↓
売上・費用・成功率を学習
 ↓
次回のAI配車を改善
```

最重要KPI: AIコスト最小化ではなく、

**「収益 ÷（AI費用 + GPU費用 + 人間の作業時間）」最大化。**
