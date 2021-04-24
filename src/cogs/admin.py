import discord
from discord.ext import commands

from main import initial_extensions

"""Admin commands"""

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Load cog
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def load(self, ctx, *, cog : str):
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        else:
            return await ctx.send(f"**SUCCESS:** Loaded '{cog}'.")

    # Unload cog
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def unload(self, ctx, *, cog : str):
        if cog == 'cogs.admin':
            return await ctx.send(f"**ERROR:** 'cogs.admin' cannot be unloaded.")
        else:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
            else:
                return await ctx.send(f"**SUCCESS:** Unloaded '{cog}'.")

    # Reload cog
    @commands.command(name='reload', hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog : str):
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        else:
            return await ctx.send(f"**SUCCESS:** Reloaded '{cog}'.")

    # Reload all cogs
    @commands.command(hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def reloadall(self, ctx):
        for extension in initial_extensions:
            try:
                self.bot.reload_extension(extension)
            except Exception as e:
                return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
            else:
                return await ctx.send(f"**SUCCESS:** Reloaded all cogs.")

def setup(bot):
    bot.add_cog(Admin(bot))