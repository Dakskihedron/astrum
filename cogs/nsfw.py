import discord
from discord.ext import commands

import random
import requests
from bs4 import BeautifulSoup
from utils import default

"""NSFW commands"""

class NSFW(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = dict()

    # Gets random post from rule34.xxx based on specified tag(s)
    @commands.command(aliases=['r34'],usage='[tag]', brief='Show a random image from rule34.xxx with the specified tag(s).', description='Show a random image from rule34.xxx with the specified tag(s). Multiple tags can be appended with + e.g. tag1+tag2. Leave blank to get a random image.')
    @commands.guild_only()
    @commands.is_nsfw()
    async def rule34(self, ctx, tag: str = None):
        embed = discord.Embed()
        if not tag:
            r = requests.get('https://rule34.xxx/index.php?page=post&s=random').url
            post = requests.get(f'http://rule34.xxx/index.php?page=dapi&s=post&q=index&id={r[(r.find("id=") + 3):]}')
            if post.status_code == 200:
                soup = BeautifulSoup(post.text, 'lxml')
                embed.description = f'[Post Link](https://rule34.xxx/index.php?page=post&s=view&id={soup.find("post")["id"]})'
                embed.set_image(url=soup.find("post")["file_url"])
                msg = await ctx.send(embed=embed)
                self.image_cache[ctx.author.id] = msg.id            
                return
            else:
                return await ctx.send(f"{ctx.author.mention} couldn't process the request. Error code: {post.status.code}")
        else:
            for x in default.nsfw_blacklist:
                if x in tag.lower():
                    return await ctx.send(f"{ctx.author.mention} one of the tags you specified is blacklisted.")
                else:
                    r = requests.get(f'https://rule34.xxx/index.php?page=dapi&s=post&q=index&tags={tag.lower()}')
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text, 'lxml')
                        post_count = int(soup.find('posts')['count'])
                        if post_count == 0:
                            return await ctx.send(f"{ctx.author.mention} there are no posts for the specified tag.")
                        else:
                            page_count = int(round(post_count/100))
                            page = random.randint(0, page_count)
                            post = soup.find('posts').find_all('post')
                            if post_count < 100:
                                image = post[random.randint(0, post_count-1)]
                            elif page == page_count:
                                image = post[random.randint(0, post_count%100 - 1)]
                            else:
                                image = post[random.randint(0, 99)]
                            embed.description = f'[Post Link](https://rule34.xxx/index.php?page=post&s=view&id={image["id"]})'
                            embed.set_image(url=image['file_url'])
                        msg = await ctx.send(embed=embed)
                        self.image_cache[ctx.author.id] = msg.id
                        return
                    else:
                        return await ctx.send(f"{ctx.author.mention} couldn't process the request. Error code: {r.status.code}")

    # Deletes the recently requested image
    @commands.command(aliases=['hateit'], brief='Delete the image you recently requested.', description='Delete the image you recently requested.')
    @commands.guild_only()
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

    @rule34.error
    @deletethis.error
    async def error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.send(f"{ctx.author.mention} that command requires you to be in an NSFW channel.")

def setup(bot):
    bot.add_cog(NSFW(bot))