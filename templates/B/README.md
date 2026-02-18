# Git-Eval B ランク: Builder

読みやすく保守しやすいコードが書けるかを見るランクです。

## お題: 品質の高いコードを書こう

CI/CD チェックに加え、LLM（Claude）がコードの可読性・設計・エラーハンドリングを評価します。

### やること

1. このリポジトリを clone する（または既存プロジェクトに YAML を追加）
2. `git-eval-config.json` を設定する
3. 可読性を意識してコードを書く
4. テスト・リンターを通す
5. （推奨）`DECISION.md` で設計判断を説明する
6. commit して push する

### git-eval-config.json の書き方

```json
{
  "language": "python",
  "build": "pip install -r requirements.txt",
  "test": "pytest --cov=src",
  "lint": "flake8 src/"
}
```

### DECISION.md の例

```markdown
## 技術選定
- Python + FastAPI を選択。理由: 非同期処理が必要で、型ヒントの恩恵が大きいため。

## 設計判断
- Repository パターンを採用し、DB アクセスを抽象化。
- エラーは例外ではなく Result 型で返す方針。
```

### 評価ポイント（100 点満点）

| チェック項目 | 配点 | 評価方法 |
|---|---|---|
| テストが通る | 10 | CI/CD |
| リンターが通る | 10 | CI/CD |
| テストカバレッジ | 10 | CI/CD |
| コードの可読性 | 20 | LLM |
| 関心の分離・設計 | 20 | LLM |
| エラーハンドリング | 15 | LLM |
| ドキュメントの質 | 15 | LLM |

### GitHub Secrets の設定

| Secret 名 | 値 |
|---|---|
| `GIT_EVAL_URL` | 管理者から通知された Webhook URL |
| `GIT_EVAL_SECRET` | 管理者から通知された Secret キー |
| `ANTHROPIC_API_KEY` | Claude API キー（LLM 評価に必要） |
