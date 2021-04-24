import discord
from discord.ext import commands

"""Role commands"""

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Changes the name of the user's highest role
    @commands.command(name='rolename', usage='[new role name]', brief='Changes the name of your highest role.', description='Changes the name of your highest role.')
    @commands.guild_only()
    async def change_role_name(self, ctx, *, new_name):
        current_name = ctx.author.top_role.name
        if ctx.author.top_role.position == 0:
            return await ctx.send(f"{ctx.author.mention} your role cannot be edited.")
        else:
            old_name = current_name
            await ctx.author.top_role.edit(name = new_name)
            return await ctx.send(f"{ctx.author.mention} changed your role name from `{old_name}` to `{new_name}`.")

    @change_role_name.error
    async def change_role_name_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send(f"{ctx.author.mention} the name cannot exceed 100 characters.")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention} you didn't provide a name.")

    # Changes the colour of the user's highest role
    @commands.command(name='rolecolour', usage='[new role colour]', brief='Changes the colour of your highest role.', description='Changes the colour of your highest role.')
    @commands.guild_only()
    async def change_role_colour(self, ctx, new_colour):
        current_colour = ctx.author.top_role.colour
        if ctx.author.top_role.position == 0:
            return await ctx.send(f"{ctx.author.mention} your role cannot be edited.")
        else:
            old_colour = current_colour
            colour = new_colour.replace('#', '')
            await ctx.author.top_role.edit(colour = discord.Colour(int(colour, 16)))
            return await ctx.send(f"{ctx.author.mention} changed your role colour from `{old_colour}` to `#{colour}`.")

    @change_role_colour.error
    async def change_role_colour_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send(f"{ctx.author.mention} you didn't provide a valid six character colour hex code.")
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention} you didn't provide a colour hex code")

def setup(bot):
    bot.add_cog(Roles(bot))