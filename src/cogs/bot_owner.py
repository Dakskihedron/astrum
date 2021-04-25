import discord
from discord.ext import commands

from main import initial_extensions

class BotOwner(commands.Cog):
    """Commands related to cogs. Only usable by the bot owner."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listcogs')
    @commands.guild_only()
    @commands.is_owner()
    async def list_cogs(self, ctx):
        """List all cogs."""
        nl = '\n'
        ext_list = []
        for extension in initial_extensions:
            ext_list.append(extension.replace('cogs.', ''))
        return await ctx.send(f"```\n{nl.join(ext_list)}\n```")
        
    @commands.command(name='load')
    @commands.guild_only()
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        """Load a specified cog.

        cog: str
        The name of the cog you want to load."""
        cog = f'cogs.{cog}'
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            return await ctx.send(f"**ERROR:** {type(e).__name__} - {e}")
        else:
            return await ctx.send(f"**SUCCESS:** Loaded `{cog}`")

    @commands.command(name='unload')
    @commands.guild_only()
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        """Unload a specified cog.

        cog: str
        The name of the cog you want to unload."""
        cog = f'cogs.{cog}'
        if cog == 'cogs.bot_owner':
            return await ctx.send(f"**ERROR:** `cogs.bot_owner` cannot be unloaded.")
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
    async def reload_cog(self, ctx, cog: str):
        """Reload a specified cog.

        cog: str
        The name of the cog you want to reload."""
        cog = f'cogs.{cog}'
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
    bot.add_cog(BotOwner(bot))