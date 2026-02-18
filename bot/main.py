import asyncio
import discord
from discord.ext import commands
import uvicorn
from fastapi import FastAPI

from bot.config import DISCORD_TOKEN, GUILD_ID, RANKS, RANK_NAMES

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
app = FastAPI(title="Git-Eval Webhook API")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "bot_ready": bot.is_ready(),
        "bot_user": str(bot.user) if bot.user else None,
    }


@bot.event
async def on_ready():
    guild_obj = bot.get_guild(GUILD_ID)
    if guild_obj:
        # Ensure all rank roles exist
        existing_roles = {r.name for r in guild_obj.roles}
        for rank in RANKS:
            role_name = f"Git-Eval: {rank} ({RANK_NAMES[rank]})"
            if role_name not in existing_roles:
                await guild_obj.create_role(name=role_name)
                print(f"Created role: {role_name}")

    guild = discord.Object(id=GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)
    print(f"Bot ready: {bot.user} | Guild: {GUILD_ID}")


async def _start_api():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()


async def main():
    await bot.load_extension("bot.cogs.register")
    await bot.load_extension("bot.cogs.status")
    await bot.load_extension("bot.cogs.guide")

    from bot.api.webhook import router
    app.include_router(router)

    async with bot:
        await asyncio.gather(
            bot.start(DISCORD_TOKEN),
            _start_api(),
        )


if __name__ == "__main__":
    asyncio.run(main())
