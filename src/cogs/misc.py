import discord
from discord.ext import commands

from utils import default

"""Miscellaneous commands"""

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Shows information about a user
    @commands.command(name='userinfo', usage='[user]', brief='Shows information about a user.', description='Shows information about a user. Leave blank to show information about yourself.')
    @commands.guild_only()
    async def user_info(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            title = f'**{user}**',
            colour = user.colour
        )
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Current display name', value=user.display_name, inline=False)
        embed.add_field(name='Discord join date', value=default.date(user.created_at), inline=False)
        embed.add_field(name='Server join date', value=default.date(user.joined_at), inline=False)
        embed.add_field(name='Highest role in server', value=user.top_role.mention, inline=False)

        return await ctx.send(embed=embed)

    @user_info.error
    async def user_info_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"{ctx.author.mention} you didn't provide a valid user.")

    # Gets a user's avatar
    @commands.command(usage='[user]', brief='Gets a user\'s avatar.', description='Gets a user\'s avatar. Leave blank to get your own avatar.')
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        avatar = user.avatar_url
        return await ctx.send(avatar)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"{ctx.author.mention} you didn't provide a valid user.")

def setup(bot):
    bot.add_cog(Misc(bot))