from discord.ext import commands


class Events(commands.Cog):
    """Event listeners."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply(
                "Missing required arguments. "
                f"Refer to `{ctx.prefix}help {ctx.command}` "
                "for additional information."
            )

        elif isinstance(error, commands.BadArgument):
            if ctx.command.has_error_handler():
                return
            else:
                await ctx.reply(
                    "Bad argument. "
                    f"Refer to `{ctx.prefix}help {ctx.command}` "
                    "for additional information."
                )

        elif isinstance(error, commands.NSFWChannelRequired):
            await ctx.reply("Command requires NSFW channel.")


def setup(bot):
    bot.add_cog(Events(bot))
