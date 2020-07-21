import discord
from discord.ext import commands

from datetime import datetime
from utils import default

"""Bot events and commands"""

class Bot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bot startup logging
    @commands.Cog.listener()
    async def on_ready(self):
        time_now = datetime.now()
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f'for {self.bot.command_prefix}help'))
        print(f"Logged in as {self.bot.user} on {len(self.bot.guilds)} servers on {default.date(time_now)}.")

    # Show the bot's latency
    @commands.command(brief='Show the bot\'s latency.', description='Show the bot\'s latency.')
    @commands.guild_only()
    async def ping(self, ctx):
        return await ctx.send(f"**Latency:** {round(self.bot.latency * 1000)}ms")

    # Show information about the bot
    @commands.command(brief='Show information about the bot.', description='Show information about the bot.')
    @commands.guild_only()
    async def info(self, ctx):
        return await ctx.send(f">>> __**{self.bot.user.name}**__\nPowered by discord.py\nSource code: https://github.com/Dakskihedron/kitakami")

def setup(bot):
    bot.add_cog(Bot(bot))