import discord
from discord.ext import commands

import os
import random
import requests
import re

# Get API tokens from environment variables
nasa_api_key = os.getenv('NASA_API_KEY')

class APIs(commands.Cog):
    """Commands related to APIs."""
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = dict()

    @commands.command()
    @commands.guild_only()
    async def apod(self, ctx, date=None):
        """Show the Astronomical Picture of the Day.

        date: yyyy-mm-dd
        The date for a specific picture. Leave blank for today's picture."""
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}'
        if date != None:
            url = url + f'&date={date}'
        try:
            r = requests.get(url)
            r.raise_for_status()
            data = r.json()
            if data['media_type'] == 'image':
                embed = discord.Embed(
                    title = f"{data['title']}",
                    colour = discord.Colour.blurple()
                )
                embed.set_image(url=data['url'])
                if 'copyright' in data:
                    embed.set_footer(text=f"Image Credit & Copyright: {data['copyright']}")
                else:
                    embed.set_footer(text="Public Domain")
                return await ctx.send(embed=embed)
            elif data['media_type'] == 'video':
                url = re.search('https://www.youtube.com/embed/(.*)?rel=0', data['url'])
                return await ctx.send(f'https://youtu.be/{url.group(1)}')
            else:
                return await ctx.send(data['url'])
        except requests.exceptions.RequestException:
            data = requests.get(url).json()
            await ctx.reply(f"{r.status_code}: {data['msg']}")

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def danbooru(self, ctx, tags=''):
        """Show an image from Danbooru.

        tag: str
        Optional tag(s) for searching specific images."""
        blacklist = [
            "loli",
            "lolicon",
            "shota",
            "shotacon",
            "cub",
            "child",
            "beastiality",
            "incest",
            "rape"
        ]
        for x in blacklist:
            if x in tags.lower():
                return await ctx.reply("The specified tag(s) are blacklisted.")
        else:
            url = f'https://danbooru.donmai.us/posts.json?limit=200&tags={tags}'
            try:
                r = requests.get(url)
                r.raise_for_status()
                data = r.json()
                if len(data) == 0:
                    return await ctx.reply("The specified tag(s) returned no results.")
                else:
                    post = random.choice(data)
                    msg = await ctx.send(post['file_url'])
                    self.image_cache[ctx.author.id] = msg.id
                    return
            except requests.exceptions.RequestException:
                data = requests.get(url).json()
                await ctx.reply(f"{r.status_code}: {data['message']}")

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def undo(self, ctx):
        """Remove your recently requested image."""
        request = self.image_cache[ctx.author.id]
        try:
            msg = await ctx.channel.fetch_message(request)
        except:
            return await ctx.reply("There is no image to remove.")
        else:
            await msg.delete()
            del request

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.reply("Command can only be used in a NSFW channel.")

def setup(bot):
    bot.add_cog(APIs(bot))