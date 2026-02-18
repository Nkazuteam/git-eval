import logging

import discord

from bot.config import RANKS, RANK_NAMES, NOTIFICATION_CHANNEL_ID

logger = logging.getLogger(__name__)


def _role_name(rank: str) -> str:
    return f"Git-Eval: {rank} ({RANK_NAMES[rank]})"


async def ensure_role(guild: discord.Guild, member: discord.Member, rank: str) -> None:
    """Ensure member has the correct rank role (add if missing)."""
    role_name = _role_name(rank)
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        role = await guild.create_role(name=role_name)
        logger.info("Created role: %s", role_name)
    if role not in member.roles:
        await member.add_roles(role)
        logger.info("Ensured role %s for %s", role_name, member)


async def update_role(guild: discord.Guild, member: discord.Member, old_rank: str, new_rank: str) -> bool:
    """Update member's rank role. Returns True if rank actually changed."""
    if old_rank == new_rank:
        # Even if rank didn't change, ensure member has the role
        await ensure_role(guild, member, new_rank)
        return False

    old_role_name = _role_name(old_rank)
    new_role_name = _role_name(new_rank)

    # Remove old rank role
    old_role = discord.utils.get(guild.roles, name=old_role_name)
    if old_role and old_role in member.roles:
        await member.remove_roles(old_role)
        logger.info("Removed role %s from %s", old_role_name, member)

    # Add new rank role (create if missing)
    new_role = discord.utils.get(guild.roles, name=new_role_name)
    if not new_role:
        new_role = await guild.create_role(name=new_role_name)
        logger.info("Created role: %s", new_role_name)
    await member.add_roles(new_role)
    logger.info("Assigned role %s to %s", new_role_name, member)

    return True


async def send_promotion_notification(
    guild: discord.Guild, member: discord.Member, new_rank: str
) -> None:
    if not NOTIFICATION_CHANNEL_ID:
        logger.warning("NOTIFICATION_CHANNEL_ID not set, skipping notification")
        return
    channel = guild.get_channel(NOTIFICATION_CHANNEL_ID)
    if not channel or not isinstance(channel, discord.TextChannel):
        logger.warning("Channel %s not found or not a text channel", NOTIFICATION_CHANNEL_ID)
        return
    logger.info("Sending promotion notification to #%s", channel.name)

    rank_label = f"{new_rank} ({RANK_NAMES[new_rank]})"
    embed = discord.Embed(
        title="Rank Up!",
        description=f"{member.mention} さんが **{rank_label}** ランクに昇格しました!",
        color=discord.Color.gold(),
    )
    await channel.send(embed=embed)
