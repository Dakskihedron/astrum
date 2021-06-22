from discord.ext import commands
import os


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
        for ext in os.listdir('./src/cogs'):
            if ext.endswith('.py'):
                ext_list.append(ext[:-3])
        await ctx.send(f"```\n{nl.join(ext_list)}\n```")

    @commands.command(name='load')
    @commands.guild_only()
    @commands.is_owner()
    async def load_cog(self, ctx, cog: str):
        """Load a specified cog.

        cog: str
        The name of the cog you want to load.
        """
        cog = f'cogs.{cog}'
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            return await ctx.reply(f"{type(e).__name__}: {e}")
        else:
            await ctx.reply(f"Successfully loaded '{cog}'.")

    @commands.command(name='unload')
    @commands.guild_only()
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        """Unload a specified cog.

        cog: str
        The name of the cog you want to unload.
        """
        cog = f'cogs.{cog}'
        if cog == 'cogs.bot_owner':
            return await ctx.reply("'cogs.bot_owner' cannot be unloaded.")
        else:
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                return await ctx.reply(f"{type(e).__name__}: {e}")
            else:
                await ctx.reply(f"Successfully unloaded '{cog}'.")

    @commands.command(name='reload')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        """Reload a specified cog.

        cog: str
        The name of the cog you want to reload.
        """
        cog = f'cogs.{cog}'
        try:
            self.bot.reload_extension(cog)
        except Exception as e:
            return await ctx.reply(f"{type(e).__name__}: {e}")
        else:
            await ctx.reply(f"Successfully reloaded '{cog}'.")

    @commands.command(name='reloadall')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_all_cogs(self, ctx):
        """Reload all cogs."""
        for ext in os.listdir('./src/cogs'):
            if ext.endswith('.py'):
                ext = ext[:-3]
                try:
                    self.bot.reload_extension(f'cogs.{ext}')
                    await ctx.send(f"Successfully reloaded extension '{ext}'.")
                except Exception as e:
                    await ctx.send(
                        f"Failed to reload extension '{ext}.' "
                        f"{type(e).__name__}: {e}"
                        )
        await ctx.send("Job done.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("No cog specified.")


def setup(bot):
    bot.add_cog(BotOwner(bot))
