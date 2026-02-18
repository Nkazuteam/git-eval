import discord
from discord import app_commands
from discord.ext import commands

from bot.services import score as score_service
from bot.services.role import update_role, _role_name
from bot.config import RANK_NAMES


class Register(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="register", description="GitHub アカウントを紐付けて Git-Eval に登録します")
    @app_commands.describe(github_username="GitHub ユーザー名")
    async def register(self, interaction: discord.Interaction, github_username: str):
        discord_id = str(interaction.user.id)
        existing = score_service.get_user(discord_id)

        if existing:
            # Confirm overwrite
            old_name = existing["github_username"]
            view = ConfirmOverwrite(discord_id, github_username, interaction)
            await interaction.response.send_message(
                f"既に `{old_name}` で登録されています。`{github_username}` に上書きしますか？\n"
                f"(ランク・スコアはリセットされます)",
                view=view,
                ephemeral=True,
            )
            return

        user_data = score_service.register_user(discord_id, github_username)
        rank = user_data["rank"]

        # Assign initial role
        guild = interaction.guild
        if guild:
            role_name = _role_name(rank)
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                role = await guild.create_role(name=role_name)
            await interaction.user.add_roles(role)

        rank_label = f"{rank} ({RANK_NAMES[rank]})"
        embed = discord.Embed(
            title="登録完了",
            description=(
                f"GitHub: `{github_username}`\n"
                f"ランク: **{rank_label}**\n"
                f"スコア: 0\n\n"
                f"`/guide` で現在ランクの評価基準を確認できます。"
            ),
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ConfirmOverwrite(discord.ui.View):
    def __init__(self, discord_id: str, github_username: str, interaction: discord.Interaction):
        super().__init__(timeout=30)
        self.discord_id = discord_id
        self.github_username = github_username

    @discord.ui.button(label="上書きする", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_data = score_service.register_user(self.discord_id, self.github_username)
        rank = user_data["rank"]

        guild = interaction.guild
        if guild:
            # Remove all old rank roles, add new one
            for r in interaction.user.roles:
                if r.name.startswith("Git-Eval:"):
                    await interaction.user.remove_roles(r)
            role_name = _role_name(rank)
            role = discord.utils.get(guild.roles, name=role_name)
            if not role:
                role = await guild.create_role(name=role_name)
            await interaction.user.add_roles(role)

        rank_label = f"{rank} ({RANK_NAMES[rank]})"
        await interaction.response.edit_message(
            content=f"上書き完了: GitHub `{self.github_username}` / ランク **{rank_label}** / スコア 0",
            view=None,
        )

    @discord.ui.button(label="キャンセル", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="キャンセルしました。", view=None)


async def setup(bot: commands.Bot):
    await bot.add_cog(Register(bot))
