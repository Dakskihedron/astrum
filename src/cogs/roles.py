import discord
from discord.ext import commands


class Roles(commands.Cog):
    """Commands for editing your role - assuming each member has their own custom role."""
    def __init__(self, bot):
        self.bot = bot

    def has_role(ctx):
        return (len(ctx.author.roles[1:]) > 0)

    @commands.command(name='rolename')
    @commands.guild_only()
    @commands.check(has_role)
    async def change_role_name(self, ctx, *, name: str):
        """Change the name of your highest role.

        name: str
        The name you want to change to. Cannot exceed 100 characters."""
        old_name = ctx.author.top_role.name
        await ctx.author.top_role.edit(name=name)
        await ctx.reply(f"Changed name of role from `{old_name}` to `{name}`")

    @change_role_name.error
    async def change_role_name_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("The name cannot exceed 100 characters.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing name.")

    @commands.command(name='rolecolour')
    @commands.guild_only()
    @commands.check(has_role)
    async def change_role_colour(self, ctx, colour):
        """Change the colour of your highest role.

        colour: hex
        The hexadecimal code of the colour you want to change to."""
        old_colour = ctx.author.top_role.colour
        colour = colour.replace('#', '')
        await ctx.author.top_role.edit(colour=discord.Colour(int(colour, 16)))
        await ctx.reply(f"Changed colour of role from `{old_colour}` to `#{colour}`")

    @change_role_colour.error
    async def change_role_colour_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Invalid hex code.")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("Missing hex code of colour.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("No valid role assigned.")


def setup(bot):
    bot.add_cog(Roles(bot))
