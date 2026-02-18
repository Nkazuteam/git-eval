# Git-Eval E ランク: Emerging

基本的なコードが書けることを確認するランクです。

## お題: 動くプログラムを書こう

好きな言語で小さなプログラムを作ってください。何を作るかは自由です。

### やること

1. このリポジトリを clone する
2. 好きな言語でプログラムを書く
3. `git-eval-config.json` に言語と実行コマンドを書く
4. commit して push する

### git-eval-config.json の書き方

```json
{
  "language": "python",
  "run": "python src/main.py"
}
```

言語に応じた例:
- Python: `"run": "python src/main.py"`
- Node.js: `"run": "node src/index.js"`
- Go: `"run": "go run ./..."`
- Rust: `"run": "cargo run"`

### 評価ポイント（100 点満点）

**CI/CD チェック（60 点）**

| チェック項目 | 配点 |
|---|---|
| ソースファイルが存在する | 10 |
| git-eval-config.json が設定されている | 5 |
| プログラムが正常に実行できる | 20 |
| 関数/メソッドを使っている | 10 |
| 条件分岐やループを使っている | 10 |
| CRLF 改行が混入していない | 5 |

**LLM 評価（40 点）**

| チェック項目 | 配点 |
|---|---|
| コードが意図通りに動いているか | 20 |
| 基本的な書き方（変数名、構造） | 20 |

### 提出方法

push するだけ！

### GitHub Secrets の設定

| Secret 名 | 値 |
|---|---|
| `GIT_EVAL_URL` | 管理者から通知された Webhook URL |
| `GIT_EVAL_SECRET` | 管理者から通知された Secret キー |
| `ANTHROPIC_API_KEY` | Claude API キー（LLM 評価に必要） |
