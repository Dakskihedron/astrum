import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
import cogs.utils.default as default

import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('BOT_PREFIX')

intents = discord.Intents.default()

bot = commands.Bot(
    intents = intents,
    command_prefix = prefix,
    activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=f'for {prefix}help'
    )
)

@bot.event
async def on_ready():
    print(f"{bot.user} logged in on {len(bot.guilds)} servers on {default.date(datetime.now())}")

if __name__ == '__main__':
    for ext in os.listdir('src/cogs'):
        if ext.endswith('.py'):
            ext = ext[:-3]
            try:
                bot.load_extension(f'cogs.{ext}')
                print(f"Successfully loaded extension '{ext}'")
            except Exception as e:
                print(f"Failed to load extension '{ext}'\n{type(e).__name__}: {e}")

bot.run(token)