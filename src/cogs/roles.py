import discord
from discord.ext import commands


class Roles(commands.Cog):
    """Commands for individual user role editing."""
    def __init__(self, bot):
        self.bot = bot

    def has_role(ctx):
        return (len(ctx.author.roles[1:]) > 0)

    @commands.command()
    @commands.guild_only()
    @commands.check(has_role)
    async def rname(self, ctx, *, name: str):
        """Change the name of your highest role.

        name: str
        The name to change to. Cannot exceed 100 characters.
        """
        old_name = ctx.author.top_role.name
        await ctx.author.top_role.edit(name=name)
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            description="```diff\nRole name changed:\n"
            f"- {old_name}\n+ {name}\n```"
        )
        await ctx.reply(embed=embed)

    @rname.error
    async def rname_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Name cannot exceed 100 characters.")

    @commands.command()
    @commands.guild_only()
    @commands.check(has_role)
    async def rcolour(self, ctx, colour):
        """Change the colour of your highest role.

        colour: hex
        The hexadecimal code of the colour to change to.
        """
        old_colour = ctx.author.top_role.colour
        colour = colour.replace('#', '')
        await ctx.author.top_role.edit(colour=discord.Colour(int(colour, 16)))
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            description="```diff\nRole colour changed:\n"
            f"- {old_colour}\n+ #{colour}\n```"
        )
        await ctx.reply(embed=embed)

    @rcolour.error
    async def rcolour_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("Invalid hex code.")

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.reply("No valid role assigned.")


def setup(bot):
    bot.add_cog(Roles(bot))
