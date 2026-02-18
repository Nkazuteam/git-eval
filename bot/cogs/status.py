import discord
from discord import app_commands
from discord.ext import commands

from bot.services import score as score_service
from bot.config import RANK_NAMES, RANK_THRESHOLDS, RANKS


class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="status", description="現在のランク・累積スコアを確認します")
    async def status(self, interaction: discord.Interaction):
        discord_id = str(interaction.user.id)
        user = score_service.get_user(discord_id)

        if not user:
            await interaction.response.send_message(
                "未登録です。`/register <github-username>` で登録してください。",
                ephemeral=True,
            )
            return

        rank = user["rank"]
        total_score = user["score"]
        github = user["github_username"]
        rank_label = f"{rank} ({RANK_NAMES[rank]})"

        remaining = score_service.score_for_next_rank(rank, total_score)

        # Progress bar
        rank_idx = RANKS.index(rank)
        if rank_idx < len(RANKS) - 1:
            next_rank = RANKS[rank_idx + 1]
            floor = RANK_THRESHOLDS[rank]
            ceiling = RANK_THRESHOLDS[next_rank]
            progress = (total_score - floor) / (ceiling - floor) if ceiling > floor else 1.0
            bar_len = 20
            filled = int(progress * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            next_info = f"次ランク ({next_rank}) まで: **{remaining}** pt\n`{bar}` {progress:.0%}"
        else:
            next_info = "最高ランクに到達しています!"

        embed = discord.Embed(
            title=f"{interaction.user.display_name} のステータス",
            color=discord.Color.blue(),
        )
        embed.add_field(name="GitHub", value=f"`{github}`", inline=True)
        embed.add_field(name="ランク", value=f"**{rank_label}**", inline=True)
        embed.add_field(name="累積スコア", value=f"**{total_score}** pt", inline=True)
        embed.add_field(name="進捗", value=next_info, inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))
