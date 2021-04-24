import discord
from discord.ext import commands

from main import initial_extensions

class Admin(commands.Cog):
    """Commands restricted to specific users."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='load')
    @commands.guild_only()
    @commands.is_owner()
    async def load_cog(self, ctx, *, cog : str):
        """Load a specified cog.

        cog: cogs.[str]
        The name of the cog you want to load."""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        else:
            return await ctx.send(f"**SUCCESS:** Loaded `{cog}`")

    @commands.command(name='unload')
    @commands.guild_only()
    @commands.is_owner()
    async def unload_cog(self, ctx, *, cog : str):
        """Unload a specified cog.

        cog: cogs.[str]
        The name of the cog you want to unload."""
        if cog == 'cogs.admin':
            return await ctx.send(f"**ERROR:** 'cogs.admin' cannot be unloaded.")
        else:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
            else:
                return await ctx.send(f"**SUCCESS:** Unloaded `{cog}`")

    @commands.command(name='reload')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_cog(self, ctx, *, cog : str):
        """Reload a specified cog.

        cog: cogs.[str]
        The name of the cog you want to reload."""
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        else:
            return await ctx.send(f"**SUCCESS:** Reloaded `{cog}`")
    
    @load_cog.error
    @unload_cog.error
    @reload_cog.error
    async def cog_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("You did not specify a cog.")

    @commands.command(name='reloadall')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_all_cogs(self, ctx):
        """Reload all cogs."""
        for extension in initial_extensions:
            try:
                self.bot.reload_extension(extension)
                print(f"Successfully reloaded extension {extension}")
            except Exception as e:
                return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        return await ctx.send("**Successfully reloaded all cogs.**")

def setup(bot):
    bot.add_cog(Admin(bot))