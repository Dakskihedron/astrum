import discord
from discord.ext import commands
import cogs.utils.functions as functions


class Misc(commands.Cog):
    """Commands that don't go anywhere else."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='user')
    @commands.guild_only()
    async def user_info(self, ctx, user: discord.Member = None):
        """Return information about a user.

        user: mention or userid
        The user to show information about. Leave blank for youself.
        """
        user = user or ctx.author
        name = str(user)

        if user.nick:
            name = f'{user.nick} ({user.name})'
        else:
            name = user.name

        roles = ', '.join(role.mention for role in user.roles[1:])

        embed = discord.Embed(
            title=name,
            colour=user.colour if roles else discord.Colour.blurple()
        )

        embed.set_thumbnail(url=user.avatar_url)

        embed.add_field(
            name='User Information',
            value=f"""
            Username: {user}
            ID: {user.id}
            Created: {functions.date(user.created_at)}
            """,
            inline=False
        )

        embed.add_field(
            name='Member Information',
            value=f"""
            Joined: {functions.date(user.joined_at)}
            Roles: {roles or None}
            """,
            inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(aliases=['icon'])
    @commands.guild_only()
    async def avatar(self, ctx, user: discord.Member = None):
        """Return a user's avatar.

        user: mention or userid
        The user to return the avatar of. Leave blank for yourself.
        """
        user = user or ctx.author
        await ctx.send(user.avatar_url)

    @user_info.error
    @avatar.error
    async def user_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.reply("User could not be found.")


def setup(bot):
    bot.add_cog(Misc(bot))
