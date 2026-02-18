"""Run once to clear all slash commands (guild + global), then exit."""
import asyncio
import discord
from discord.ext import commands
from bot.config import DISCORD_TOKEN, GUILD_ID

print(f"Connecting... (GUILD_ID={GUILD_ID})")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        guild = discord.Object(id=GUILD_ID)

        # Clear guild commands
        bot.tree.clear_commands(guild=guild)
        await bot.tree.sync(guild=guild)
        print("Cleared guild commands.")

        # Clear global commands
        bot.tree.clear_commands(guild=None)
        await bot.tree.sync()
        print("Cleared global commands.")

        print("Done.")
    except Exception as e:
        print(f"Error: {e}")
    await bot.close()


asyncio.run(bot.start(DISCORD_TOKEN))
