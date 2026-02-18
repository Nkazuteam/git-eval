import hashlib
import hmac
import logging

import discord
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from bot.config import WEBHOOK_SECRET, GUILD_ID, RANKS
from bot.services import score as score_service
from bot.services.role import update_role, send_promotion_notification

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhook")


class EvalResult(BaseModel):
    github_username: str
    score: int
    feedback: str
    rank: str | None = None


def _verify_signature(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


@router.get("/debug")
async def debug_status():
    """Check bot connectivity — for debugging only."""
    from bot.state import bot
    from bot.config import NOTIFICATION_CHANNEL_ID

    info = {
        "bot_ready": bot.is_ready(),
        "bot_user": str(bot.user) if bot.user else None,
        "guild_id": GUILD_ID,
        "notification_channel_id": NOTIFICATION_CHANNEL_ID,
    }

    guild = bot.get_guild(GUILD_ID)
    if guild:
        info["guild_name"] = guild.name
        info["guild_member_count"] = guild.member_count
        info["bot_permissions"] = dict(guild.me.guild_permissions) if guild.me else "bot not in guild"
        channel = guild.get_channel(NOTIFICATION_CHANNEL_ID) if NOTIFICATION_CHANNEL_ID else None
        info["notification_channel"] = channel.name if channel else "NOT FOUND"
        info["roles"] = [r.name for r in guild.roles if r.name.startswith("Git-Eval")]
    else:
        info["guild"] = "NOT FOUND"

    return info


@router.post("/eval")
async def receive_eval(request: Request):
    # Signature verification
    signature = request.headers.get("X-Signature-256", "")
    body = await request.body()
    if not _verify_signature(body, signature):
        raise HTTPException(status_code=401, detail="Invalid signature")

    payload = EvalResult.model_validate_json(body)

    # Find user by GitHub username
    result = score_service.find_by_github(payload.github_username)
    if not result:
        raise HTTPException(status_code=404, detail="User not registered")

    discord_id, user_data = result

    old_rank, new_rank, new_score = score_service.add_score(
        discord_id, payload.score, eval_rank=payload.rank
    )

    # Update Discord role and send notification if promoted
    from bot.state import bot

    guild = bot.get_guild(GUILD_ID)
    promoted = False
    discord_error = None

    try:
        if not guild:
            discord_error = f"Guild {GUILD_ID} not found. bot.guilds={[g.id for g in bot.guilds]}"
            logger.warning(discord_error)
        else:
            # get_member uses cache only; fall back to API fetch
            member = guild.get_member(int(discord_id))
            if not member:
                try:
                    member = await guild.fetch_member(int(discord_id))
                except discord.NotFound:
                    member = None

            if not member:
                discord_error = f"Member {discord_id} not found in guild {guild.name}"
                logger.warning(discord_error)
            else:
                promoted = await update_role(guild, member, old_rank, new_rank)
                if promoted:
                    await send_promotion_notification(guild, member, new_rank)

                # Send DM with feedback
                try:
                    embed_title = "評価結果"
                    if promoted:
                        embed_title += f" (昇格: {old_rank} → {new_rank}!)"

                    feedback_text = payload.feedback.replace("\\n", "\n")
                    embed = discord.Embed(
                        title=embed_title,
                        description=(
                            f"**スコア:** +{payload.score} pt (累積: {new_score} pt)\n"
                            f"**ランク:** {new_rank}\n\n"
                            f"**フィードバック:**\n{feedback_text}"
                        ),
                        color=discord.Color.green() if promoted else discord.Color.blue(),
                    )
                    await member.send(embed=embed)
                except discord.Forbidden:
                    logger.info("DM blocked by %s", member)
    except Exception as e:
        discord_error = f"{type(e).__name__}: {e}"
        logger.error("Discord operation failed: %s", discord_error)

    return {
        "status": "ok",
        "discord_id": discord_id,
        "old_rank": old_rank,
        "new_rank": new_rank,
        "score": new_score,
        "promoted": promoted,
        "discord_error": discord_error,
    }
