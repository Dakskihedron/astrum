import discord
from discord.ext import commands

from utils.default import nsfw_blacklist
from core.nsfw_core import get_image

"""NSFW commands"""

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = dict()

    # Process NSFW commands and send embed or error
    async def process_nsfw(self, ctx, site: str, tags: str):
        for x in nsfw_blacklist:
            if x in tags.lower():
                return await ctx.send(f"{ctx.author.mention} one of the tags you specified is blacklisted.")
            else:
                file_url, post_link, error = await get_image(site, tags)
                if file_url and post_link:
                    embed = discord.Embed()
                    embed.description = f'[Post Link]({post_link})'
                    embed.set_image(url=file_url)
                    msg = await ctx.send(embed=embed)
                    self.image_cache[ctx.author.id] = msg.id
                    return
                elif error:
                    return await ctx.send(f"{ctx.author.mention} {error}")

    # Get image from Danbooru
    @commands.command(aliases=['dan'], usage='[tag]', brief='Get an image from Danbooru with the specified tag(s).', description='Get an image from Danbooru with the specified tag(s). Multiple tags can be appended with + e.g. tag1+tag2. Note: Danbooru searches are limited to only two tags. Leave blank for random image.')
    @commands.is_nsfw()
    async def danbooru(self, ctx, tags: str = ''):
        return await self.process_nsfw(ctx, 'danbooru', tags)

    # Get image from Gelbooru
    @commands.command(aliases=['gel'], usage='[tag]', brief='Get an image from Gelbooru with the specified tag(s).', description='Get an image from Gelbooru with the specified tag(s). Multiple tags can be appended with + e.g. tag1+tag2+tag... Leave blank for random image.')
    @commands.is_nsfw()
    async def gelbooru(self, ctx, tags: str = ''):
        return await self.process_nsfw(ctx, 'gelbooru', tags)

    # Get image from rule34.xxx
    @commands.command(aliases=['r34'], usage='[tag]', brief='Get an image from rule34.xxx with the specified tag(s).', description='Get an image from rule34.xxx with the specified tag(s). Multiple tags can be appended with + e.g. tag1+tag2... Leave blank for random image.')
    @commands.is_nsfw()
    async def rule34(self, ctx, tags: str = ''):
        return await self.process_nsfw(ctx, 'rule34', tags)

    # Deletes the recently requested image
    @commands.command(aliases=['del', 'undo'], brief='Delete the image you recently requested.', description='Delete the image you recently requested.')
    @commands.is_nsfw()
    async def deletethis(self, ctx):
        try:
            msg = await ctx.channel.fetch_message(self.image_cache[ctx.author.id])
        except:
            return await ctx.send(f"{ctx.author.mention} there is no image to delete.")
        else:
            await msg.delete()
            del self.image_cache[ctx.author.id]
            return

    @danbooru.error
    @gelbooru.error
    @rule34.error
    @deletethis.error
    async def error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send(f"{ctx.author.mention} that command requires you to be in an NSFW channel.")

def setup(bot):
    bot.add_cog(NSFW(bot))