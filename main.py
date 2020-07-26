import discord
from discord.ext import commands

import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from utils import default

# Get environment variables
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('DISCORD_PREFIX')

bot = commands.Bot(
    command_prefix = prefix,
    help_command = commands.DefaultHelpCommand(command_attrs=dict(brief='Shows this message.'), no_category='Bot')
)

# Bot 'ready' event logging
@bot.event
async def on_ready():
    time_now = datetime.now()
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'for {bot.command_prefix}help'))
    print(f"Logged in as {bot.user} on {len(bot.guilds)} servers on {default.date(time_now)}.")

# Show bot latency
@bot.command(brief='Show the bot\'s latency.', description='Show the bot\'s latency.')
@commands.guild_only()
async def ping(ctx):
    return await ctx.send(f"**Latency:** {round(bot.latency * 1000)}ms")

# Show information about the bot
@bot.command(brief='Show information about the bot.', description='Show information about the bot.')
@commands.guild_only()
async def info(ctx):
    embed = discord.Embed(
        title = f'**{bot.user.name}**',
        description = f"**Powered by discord.py.**\nBot developer: Dakskihedron\nSource code: [GitHub]({default.github_link})"
    )
    embed.set_thumbnail(url=bot.user.avatar_url)
    return await ctx.send(embed=embed)

# Load extensions
initial_extensions = (
    "cogs.admin",
    "cogs.fun",
    "cogs.misc",
    "cogs.nsfw",
    "cogs.roles"
)

for extension in initial_extensions:
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f"Failed to load extension {extension}.")

bot.run(token)