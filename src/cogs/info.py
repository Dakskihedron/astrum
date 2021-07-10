import discord
from discord.ext import commands
import platform


class Info(commands.Cog):
    """Commands to do with information."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def meta(self, ctx):
        """Return technical info."""
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            description=f"```\nRunning Discord.py v{discord.__version__}\n"
            f"Running Python {platform.python_version()}\n"
            f"Running on {len(self.bot.guilds)} server(s)\n```"
            )
        await ctx.reply(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def ping(self, ctx):
        """Return response time and latency."""
        m = await ctx.send('Pinging...')
        time = m.created_at - ctx.message.created_at
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            description="```\n"
            f"Response: {time.total_seconds() * 1000} ms\n"
            f"Latency: {self.bot.latency * 1000:.2f} ms\n```"
        )
        await m.edit(content=None, embed=embed)

    @commands.command()
    @commands.guild_only()
    async def source(self, ctx):
        """Return link to source code on GitHub."""
        await ctx.send("https://github.com/Dakskihedron/astrum")


def setup(bot):
    bot.add_cog(Info(bot))
