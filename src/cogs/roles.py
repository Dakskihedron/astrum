import discord
from discord.ext import commands

class Roles(commands.Cog):
    """Commands for editing your role - assuming each member has their own custom role."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='rolename')
    @commands.guild_only()
    async def change_role_name(self, ctx, *, name: str):
        """Change the name of your highest role.

        name: str
        The name you want to change to. Cannot exceed 100 characters."""
        current_name = ctx.author.top_role.name
        if ctx.author.top_role.position == 0:
            return await ctx.send("Your role cannot be edited.")
        else:
            old_name = current_name
            await ctx.author.top_role.edit(name = name)
            return await ctx.send(f"Changed name of role from `{old_name}` to `{name}`")

    @change_role_name.error
    async def change_role_name_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("The name cannot exceed 100 characters.")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("Missing name.")

    @commands.command(name='rolecolour')
    @commands.guild_only()
    async def change_role_colour(self, ctx, colour):
        """Change the colour of your highest role.

        colour: hex
        The hexadecimal code of the colour you want to change to."""
        current_colour = ctx.author.top_role.colour
        if ctx.author.top_role.position == 0:
            return await ctx.send("Your role cannot be edited.")
        else:
            old_colour = current_colour
            colour = colour.replace('#', '')
            await ctx.author.top_role.edit(colour = discord.Colour(int(colour, 16)))
            return await ctx.send(f"Changed colour of role from `{old_colour}` to `#{colour}`")

    @change_role_colour.error
    async def change_role_colour_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send("Invalid hex code.")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send("Missing hex code of colour.")

def setup(bot):
    bot.add_cog(Roles(bot))