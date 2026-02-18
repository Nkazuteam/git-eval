import discord

from bot.config import RANKS, RANK_NAMES, NOTIFICATION_CHANNEL_ID


def _role_name(rank: str) -> str:
    return f"Git-Eval: {rank} ({RANK_NAMES[rank]})"


async def update_role(guild: discord.Guild, member: discord.Member, old_rank: str, new_rank: str) -> bool:
    """Update member's rank role. Returns True if rank actually changed."""
    if old_rank == new_rank:
        return False

    old_role_name = _role_name(old_rank)
    new_role_name = _role_name(new_rank)

    # Remove old rank role
    old_role = discord.utils.get(guild.roles, name=old_role_name)
    if old_role and old_role in member.roles:
        await member.remove_roles(old_role)

    # Add new rank role (create if missing)
    new_role = discord.utils.get(guild.roles, name=new_role_name)
    if not new_role:
        new_role = await guild.create_role(name=new_role_name)
    await member.add_roles(new_role)

    return True


async def send_promotion_notification(
    guild: discord.Guild, member: discord.Member, new_rank: str
) -> None:
    if not NOTIFICATION_CHANNEL_ID:
        return
    channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.TextChannel):
        return

    rank_label = f"{new_rank} ({RANK_NAMES[new_rank]})"
    embed = discord.Embed(
        title="Rank Up!",
        description=f"{member.mention} さんが **{rank_label}** ランクに昇格しました!",
        color=discord.Color.gold(),
    )
    await channel.send(embed=embed)
