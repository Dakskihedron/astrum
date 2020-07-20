import discord
from discord.ext import commands

import os
import dotenv
from dotenv import load_dotenv
load_dotenv()

# Get environment variables
token = os.getenv('DISCORD_TOKEN')
prefix = os.getenv('DISCORD_PREFIX')

bot = commands.Bot(
    command_prefix = prefix,
    help_command = commands.DefaultHelpCommand(command_attrs=dict(brief='Shows this message.'), no_category='Utility')
)

def is_guild_owner():
    def predicate(ctx):
        return ctx.guild is not None and ctx.guild.owner_id == ctx.author.id
    return commands.check(predicate)

# Reload all cogs (owner only)
@bot.command(name='reloadall', brief='Reload all cogs.', description='Reload all cogs.')
@commands.guild_only()
@commands.check_any(commands.is_owner(), is_guild_owner())
async def reload_all(ctx):
    for file in os.listdir('cogs'):
        if file.endswith('.py'):
            name = file[:-3]
            bot.reload_extension(f'cogs.{name}')
            print(f"Reloaded the {name} cog.")
    return await ctx.send("Successfully reloaded all cogs.")

# Load extensions/cogs
bot.load_extension('cogs.bot')
bot.load_extension('cogs.fun')
bot.load_extension('cogs.misc')
bot.load_extension('cogs.roles')

bot.run(token)