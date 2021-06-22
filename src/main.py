import discord
from discord.ext import commands
import os
import platform
import logging
import cogs.utils.default as default
from dotenv import load_dotenv
from datetime import datetime

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log',
    encoding='utf-8',
    mode='w'
    )
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
    )
logger.addHandler(handler)

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('BOT_PREFIX')

intents = discord.Intents.default()
bot = commands.Bot(
    intents=intents,
    command_prefix=prefix,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'for {prefix}help'
        )
)


@bot.event
async def on_ready():
    print(
        f"{'=' * 51}\n"
        f"Current local time: {default.date(datetime.now())}\n"
        f"Running Discord.py version: {discord.__version__}\n"
        f"Running Python version: {platform.python_version()}\n"
        f"Logged in as {bot.user} on {len(bot.guilds)} servers\n"
        f"{'=' * 51}"
        )

if __name__ == '__main__':
    print("Loading extensions...")
    for ext in os.listdir('src/cogs'):
        if ext.endswith('.py'):
            ext = ext[:-3]
            try:
                bot.load_extension(f'cogs.{ext}')
                print(f"Successfully loaded extension '{ext}'")
            except Exception as e:
                print(
                    f"Failed to load extension '{ext}' "
                    f"{type(e).__name__}: {e}"
                    )

bot.run(token)
