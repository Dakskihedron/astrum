import discord
from discord.ext import commands

from utils import default

class Info(commands.Cog):
    """Commands to do with information."""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """Show the bot's response time and latency."""
        m = await ctx.send("**Pinging...**")
        embed = discord.Embed(colour = discord.Colour.blurple())
        embed.add_field(name='Response', value=f"{(m.created_at - ctx.message.created_at).total_seconds() * 1000} ms", inline=False)
        embed.add_field(name='Latency', value=f"{self.bot.latency * 1000:.2f} ms", inline=False)
        await m.edit(content=None, embed=embed)

    @commands.command()
    @commands.guild_only()
    async def source(self, ctx):
        """Link to bot's source code on GitHub."""
        return await ctx.send(default.github_link)

def setup(bot):
    bot.add_cog(Info(bot))