import discord
from discord import app_commands
from discord.ext import commands

from bot.services import score as score_service
from bot.config import RANK_NAMES, TEMPLATE_REPO_URL

GUIDE_TEXTS: dict[str, str] = {
    "G": (
        "**【G ランク: Generalist】― ターミナルと Git の基礎 【AI 利用禁止】**\n\n"
        "覚えれば効率が爆上がりするものを、自分の手で叩いて身につけるランクです。\n"
        "このランクだけは AI 禁止。自力で覚えることに意味があります。\n\n"
        "■ やること\n"
        f"1. テンプレートリポジトリを clone する\n"
        f"   `git clone {TEMPLATE_REPO_URL}`\n"
        "2. ターミナルで clone したフォルダに `cd` で移動する\n"
        "3. `mkdir` でフォルダを作り、その中にファイルを作成する\n"
        "4. `git add` → `git commit` で変更を記録する\n"
        "5. ブランチを切る: `git switch -c my-first-branch`\n"
        "6. ブランチ上でファイルを編集して commit する\n"
        "7. GitHub に `git push` する\n"
        "8. GitHub 上で PR を作成してマージする\n\n"
        "■ 評価ポイント\n"
        "- ターミナル基礎: `cd`, `ls`, `mkdir`, `cp`, `mv`, `rm` 等\n"
        "- パスの理解: 絶対パス・相対パスの違い\n"
        "- Git 基礎: `init`, `add`, `commit`, `push`, `pull`, `clone`\n"
        "- ブランチ操作: `branch` / `switch -c`\n"
        "- GitHub 操作: リポジトリ作成、PR、マージ\n\n"
        "■ 評価方法\n"
        "CI/CD のみで機械的にチェック（LLM 不要）"
    ),
    "F": (
        "**【F ランク: Foundation】― 開発環境とプロジェクトの型を知る**\n\n"
        "ターミナルと Git が使える前提で、「開発を始められる状態」を自分で作れるかを見ます。\n\n"
        "■ 評価ポイント\n"
        "- 環境構築: 言語・ランタイムのインストール、パッケージマネージャ\n"
        "- プロジェクト初期化: `npm init`, `cargo init` 等\n"
        "- ディレクトリ構成: 一般的なプロジェクト構造の理解\n"
        "- .gitignore: 不要ファイルの除外\n"
        "- .env: 環境変数ファイルの扱い\n"
        "- .gitattributes: 改行コードの管理\n\n"
        "■ 即アウト条件（0 点）\n"
        "- .env ファイルが push されている\n"
        "- CRLF 改行のファイルが含まれている"
    ),
    "E": (
        "**【E ランク: Emerging】― 基本的なコードが書ける**\n\n"
        "手を動かしてコードを書き始める段階です。\n\n"
        "■ 評価ポイント\n"
        "- 文法: 基本的な構文エラーがない\n"
        "- 実行: プログラムが動作する\n"
        "- 入出力: 標準入出力やファイル操作\n"
        "- 基本構造: 変数、関数、条件分岐、ループ\n\n"
        "■ 評価方法\n"
        "CI/CD 中心（ビルド通過・実行成功の確認）+ LLM で基本チェック"
    ),
    "D": (
        "**【D ランク: Developer】― チーム開発を意識した Git 運用**\n\n"
        "個人で書けるだけでなく、チームで開発する作法が身についているかを見ます。\n\n"
        "■ 評価ポイント\n"
        "- コミット: 意味のあるコミットメッセージ\n"
        "- ブランチ戦略: 機能ごとにブランチを切る\n"
        "- PR: わかりやすい PR の説明\n"
        "- コードの分割: 1 コミット・1 PR の粒度が適切\n\n"
        "■ 評価方法\n"
        "CI/CD でコミット履歴・ブランチ構成をチェック + LLM でメッセージ品質を評価"
    ),
    "C": (
        "**【C ランク: Competent】― 動くだけでなく「ちゃんと動く」ものを作れる**\n\n"
        "コードが動くのは当たり前。テストやリンターを通す習慣があるかを見ます。\n\n"
        "■ 評価ポイント\n"
        "- ビルド: コンパイル / ビルドが通る\n"
        "- テスト: 最低限のテストがある\n"
        "- リンター: 静的解析を通せる\n"
        "- 再現性: 他の人が clone して動かせる\n\n"
        "■ 評価方法\n"
        "CI/CD の比重が高い + LLM で可読性を軽くチェック"
    ),
    "B": (
        "**【B ランク: Builder】― 読みやすく保守しやすいコードが書ける**\n\n"
        "■ 評価ポイント\n"
        "- 可読性: 命名・構造がわかりやすい\n"
        "- 設計: 適切な関心の分離\n"
        "- エラーハンドリング: 異常系の考慮\n"
        "- ドキュメント: README・コメントが過不足ない\n\n"
        "■ 推奨\n"
        "DECISION.md の添付を推奨します（設計判断の説明）\n\n"
        "■ 評価方法\n"
        "LLM の比重が上がる + CI/CD はカバレッジ・複雑度"
    ),
    "A": (
        "**【A ランク: Architect】― 設計判断ができる**\n\n"
        "■ 評価ポイント\n"
        "- アーキテクチャ: 全体設計の妥当性\n"
        "- イディオム: 言語らしい書き方\n"
        "- トレードオフ: 技術選択の根拠が明確\n"
        "- セキュリティ: 脆弱性への配慮\n"
        "- 判断の説明: なぜその技術を選んだかを言語化\n\n"
        "■ 推奨\n"
        "DECISION.md の添付を推奨します\n\n"
        "■ 評価方法\n"
        "LLM 中心の評価"
    ),
    "S": (
        "**【S ランク: Specialist】― 技術選定にうるさいレベル**\n\n"
        "■ 評価ポイント\n"
        "- 技術選定: 目的に対して最適な手段を選べている\n"
        "- 目的と手段の一致: オーバースペックや不足がない\n"
        "- 創意工夫: 独自のアプローチ・最適化\n"
        "- 総合力: 上記すべてを高水準で満たす\n\n"
        "■ 注意\n"
        "目的と手段の逆転には厳しく減点します\n"
        "DECISION.md の添付を強く推奨します\n\n"
        "■ 評価方法\n"
        "LLM による深い評価が必須"
    ),
}


class Guide(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="guide", description="現在ランクの評価基準・即アウト条件を表示します")
    async def guide(self, interaction: discord.Interaction):
        discord_id = str(interaction.user.id)
        user = score_service.get_user(discord_id)

        if not user:
            await interaction.response.send_message(
                "未登録です。`/register <github-username>` で登録してください。",
                ephemeral=True,
            )
            return

        rank = user["rank"]
        text = GUIDE_TEXTS.get(rank, "ガイドが見つかりません。")

        embed = discord.Embed(
            title=f"ランクガイド ― {rank} ({RANK_NAMES[rank]})",
            description=text,
            color=discord.Color.purple(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guide(bot))
