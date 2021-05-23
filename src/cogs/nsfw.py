import discord
from discord.ext import commands

from utils.default import nsfw_blacklist
from utils.nsfw_backend import get_image

class NSFW(commands.Cog):
    """Commands related to NSFW content. Only work in channels tagged as NSFW."""
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = dict()

    # Process NSFW commands and send embed or error
    async def process_nsfw(self, ctx, site: str, tags: str):
        for x in nsfw_blacklist:
            if x in tags.lower():
                return await ctx.reply("One of the tags you have specified is blacklisted.")
            else:
                file_url, post_link, error = await get_image(site, tags)
                if file_url and post_link:
                    embed = discord.Embed(colour = discord.Colour.blurple())
                    embed.description = f'[Post Link]({post_link})'
                    embed.set_image(url=file_url)
                    msg = await ctx.send(embed=embed)
                    self.image_cache[ctx.author.id] = msg.id
                    return
                elif error:
                    return await ctx.reply(error)

    @commands.command(aliases=['dan'])
    @commands.is_nsfw()
    async def danbooru(self, ctx, tags: str = ''):
        """Get a random image from Danbooru with the specified tag(s).
        Danbooru searches are limited to two tags.

        tags: str
        The tag(s) you want to search. Multiple tags can be appended using plus signs. Spaces in tags must be replaced with an underscore. Leave blank for a random image."""
        return await self.process_nsfw(ctx, 'danbooru', tags)

    @commands.command(aliases=['gel'])
    @commands.is_nsfw()
    async def gelbooru(self, ctx, tags: str = ''):
        """Get a random image from Gelbooru with the specified tag(s).

        tags: str
        The tag(s) you want to search. Multiple tags can be appended using plus signs. Spaces in tags must be replaced with an underscore. Leave blank for a random image."""
        return await self.process_nsfw(ctx, 'gelbooru', tags)

    @commands.command(aliases=['r34'])
    @commands.is_nsfw()
    async def rule34(self, ctx, tags: str = ''):
        """Get a random image from rule34.xxx with the specified tag(s).

        tags: str
        The tag(s) you want to search. Multiple tags can be appended using plus signs. Spaces in tags must be replaced with an underscore. Leave blank for a random image."""
        return await self.process_nsfw(ctx, 'rule34', tags)

    @commands.command(name='undo', aliases=['delete', 'del'])
    @commands.is_nsfw()
    async def delete_post(self, ctx):
        """Remove the image you recently requested."""
        try:
            msg = await ctx.channel.fetch_message(self.image_cache[ctx.author.id])
        except:
            return await ctx.reply("There is no image to delete.")
        else:
            await msg.delete()
            del self.image_cache[ctx.author.id]
            return

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.reply("Command can only used in a NSFW channel.")

def setup(bot):
    bot.add_cog(NSFW(bot))