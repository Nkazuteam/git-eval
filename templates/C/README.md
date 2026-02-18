# Git-Eval C ランク: Competent

動くだけでなく「ちゃんと動く」ものを作れるかを見るランクです。

## お題: テストとリンターを導入しよう

自分のプロジェクトにテストとリンターを追加し、CI で自動チェックできる状態にしてください。

### やること

1. このリポジトリを clone する（または既存プロジェクトに YAML を追加）
2. `git-eval-config.json` を設定する
3. テストを書く
4. リンターを設定する
5. commit して push する

### git-eval-config.json の書き方

```json
{
  "language": "python",
  "build": "pip install -r requirements.txt",
  "test": "pytest",
  "lint": "flake8 src/"
}
```

### 評価ポイント（100 点満点）

**CI/CD チェック（60 点）**

| チェック項目 | 配点 |
|---|---|
| ビルド/セットアップが成功する | 15 |
| テストファイルが存在する | 10 |
| テストが通る | 15 |
| リンター設定が存在する | 10 |
| リンターが通る | 10 |

**LLM 評価（40 点）**

| チェック項目 | 配点 |
|---|---|
| コードの基本的な可読性 | 20 |
| 再現性（他の人が動かせるか） | 20 |

### 提出方法

push するだけ！

### GitHub Secrets の設定

| Secret 名 | 値 |
|---|---|
| `GIT_EVAL_URL` | 管理者から通知された Webhook URL |
| `GIT_EVAL_SECRET` | 管理者から通知された Secret キー |
| `ANTHROPIC_API_KEY` | Claude API キー（LLM 評価に必要） |
