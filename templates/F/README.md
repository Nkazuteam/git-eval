# Git-Eval F ランク: Foundation

「開発を始められる状態」を自分で作れるかを見るランクです。

## お題: プロジェクトをゼロから初期化しよう

好きな言語でプロジェクトを初期化し、正しい設定ファイルを整えてください。

### やること

1. このリポジトリを clone する
2. 好きな言語/フレームワークでプロジェクトを初期化する
   - 例: `npm init`, `cargo init`, `python -m venv .venv` + `pyproject.toml` 等
3. `.gitignore` を適切に設定する
4. `src/` 等のディレクトリ構成を作る
5. commit して push する

### 評価ポイント（100 点満点）

| チェック項目 | 配点 |
|---|---|
| `.gitignore` が存在し中身がある | 20 |
| `.gitattributes` が存在する | 15 |
| プロジェクト設定ファイルがある | 25 |
| `src/` 等のソースディレクトリがある | 15 |
| `README.md` が更新されている | 10 |
| 不要ファイル（node_modules 等）がない | 15 |

### 即アウト条件（0 点）

- **`.env` ファイルが push されている**
- **CRLF 改行のファイルが含まれている**

これらが検出された場合、他のチェックに関係なく 0 点になります。

### 提出方法

push するだけ！

### GitHub Secrets の設定

リポジトリの Settings → Secrets and variables → Actions に以下を追加:

| Secret 名 | 値 |
|---|---|
| `GIT_EVAL_URL` | 管理者から通知された Webhook URL |
| `GIT_EVAL_SECRET` | 管理者から通知された Secret キー |
