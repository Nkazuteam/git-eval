import hashlib
import hmac

import discord
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from bot.config import WEBHOOK_SECRET, GUILD_ID, RANKS
from bot.services import score as score_service
from bot.services.role import update_role, send_promotion_notification

router = APIRouter(prefix="/webhook")


class EvalResult(BaseModel):
    github_username: str
    score: int
    feedback: str
    skip_to_rank: str | None = None


def _verify_signature(body: bytes, signature: str) -> bool:
    expected = hmac.new(
        WEBHOOK_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)


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

    # Apply skip-grade if applicable
    if payload.skip_to_rank and payload.skip_to_rank in RANKS:
        old_rank, new_rank, new_score = score_service.apply_skip_grade(
            discord_id, payload.skip_to_rank
        )
    else:
        old_rank, new_rank, new_score = score_service.add_score(
            discord_id, payload.score
        )

    # Update Discord role and send notification if promoted
    from bot.main import bot
    import logging

    logger = logging.getLogger(__name__)

    guild = bot.get_guild(GUILD_ID)
    promoted = False
    if not guild:
        logger.warning("Guild %s not found", GUILD_ID)
    else:
        # get_member uses cache only; fall back to API fetch
        member = guild.get_member(int(discord_id))
        if not member:
            try:
                member = await guild.fetch_member(int(discord_id))
            except discord.NotFound:
                member = None
                logger.warning("Member %s not found in guild", discord_id)

        if member:
            promoted = await update_role(guild, member, old_rank, new_rank)
            if promoted:
                await send_promotion_notification(guild, member, new_rank)

            # Send DM with feedback
            try:
                embed_title = "評価結果"
                if promoted:
                    embed_title += f" (昇格: {old_rank} → {new_rank}!)"

                embed = discord.Embed(
                    title=embed_title,
                    description=(
                        f"**スコア:** +{payload.score} pt (累積: {new_score} pt)\n"
                        f"**ランク:** {new_rank}\n\n"
                        f"**フィードバック:**\n{payload.feedback}"
                    ),
                    color=discord.Color.green() if promoted else discord.Color.blue(),
                )
                await member.send(embed=embed)
            except discord.Forbidden:
                logger.info("DM blocked by %s", member)
            except Exception as e:
                logger.error("Failed to send DM: %s", e)

    return {
        "status": "ok",
        "discord_id": discord_id,
        "old_rank": old_rank,
        "new_rank": new_rank,
        "score": new_score,
        "promoted": promoted,
    }
