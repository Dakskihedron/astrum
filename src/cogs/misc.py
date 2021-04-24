import discord
from discord.ext import commands

from utils import default

class Misc(commands.Cog):
    """Commands that don't go anywhere else."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo')
    @commands.guild_only()
    async def user_info(self, ctx, user: discord.Member = None):
        """Show information about a user.

        user: discord.Member
        The user you want to show information about. Leave blank for youself."""
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
            return await ctx.send("User could not be found.")

    @commands.command()
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member = None):
        """Return a user's avatar.

        user: discord.Member
        The user you want to return the avatar of. Leave blank for yourself."""
        user = user or ctx.author
        avatar = user.avatar_url
        return await ctx.send(avatar)

    @avatar.error
    async def avatar_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            return await ctx.send("User could not be found.")

def setup(bot):
    bot.add_cog(Misc(bot))