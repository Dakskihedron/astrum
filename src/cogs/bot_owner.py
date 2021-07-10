from discord.ext import commands
import os


class BotOwner(commands.Cog):
    """Commands related to cogs. Only usable by the bot owner."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='cogs')
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
        The name of the cog to load.
        """
        try:
            self.bot.load_extension(f'cogs.{cog}')
        except Exception as e:
            return await ctx.reply(f"```diff\n- {type(e).__name__}: {e}\n```")
        await ctx.reply(
            f"```diff\n+ Extension '{cog}' successfully loaded.\n```"
            )

    @commands.command(name='unload')
    @commands.guild_only()
    @commands.is_owner()
    async def unload_cog(self, ctx, cog: str):
        """Unload a specified cog.

        cog: str
        The name of the cog to unload.
        """
        if cog == 'bot_owner':
            return await ctx.reply(
                "```diff\n- Extension 'bot_owner' cannot be unloaded.\n```"
                )
        else:
            try:
                self.bot.unload_extension(f'cogs.{cog}')
            except Exception as e:
                return await ctx.reply(
                    f"```diff\n- {type(e).__name__}: {e}\n```"
                    )
            await ctx.reply(
                f"```diff\n+ Extension '{cog}' successfully unloaded.\n```"
                )

    @commands.command(name='reload')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_cog(self, ctx, cog: str):
        """Reload a specified cog.

        cog: str
        The name of the cog to reload.
        """
        try:
            self.bot.reload_extension(f'cogs.{cog}')
        except Exception as e:
            return await ctx.reply(f"```diff\n- {type(e).__name__}: {e}\n```")
        await ctx.reply(
            f"```diff\n+ Extension '{cog}' successfully reloaded.\n```"
            )

    @commands.command(name='restart')
    @commands.guild_only()
    @commands.is_owner()
    async def reload_all_cogs(self, ctx):
        """Reload all cogs."""
        nl = '\n'
        log = []
        for cog in os.listdir('./src/cogs'):
            if cog.endswith('.py'):
                cog = cog[:-3]
                try:
                    self.bot.reload_extension(f'cogs.{cog}')
                    log.append(f"+ Extension '{cog}' successfully reloaded.")
                except Exception as e:
                    log.append(
                        f"- Extension '{cog}' failed to reload. "
                        f"{type(e).__name__}: {e}"
                        )
        await ctx.send(f"```diff\n{nl.join(log)}\n```")


def setup(bot):
    bot.add_cog(BotOwner(bot))
