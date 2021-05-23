import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime

# Get environment variables
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

def date(target):
    return target.strftime("%a, %d %b %Y @ %I:%M:%S %p")

# On ready log
@bot.event
async def on_ready():
    print(f"{bot.user} logged in on {len(bot.guilds)} servers on {date(datetime.now())}")

# Load the following extensions
initial_extensions = (
    "cogs.bot_owner",
    "cogs.apis",
    "cogs.fun",
    "cogs.info",
    "cogs.misc",
    "cogs.roles"
)

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
        print(f"Successfully loaded extension {extension}")
    except Exception as e:
        print(f"Failed to load extension {extension}")

bot.run(token)