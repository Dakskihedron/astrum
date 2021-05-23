import discord
from discord.ext import commands

import os
import dotenv
import requests
import re

# Get API tokens from environment variables
nasa_api_key = os.getenv('NASA_API_KEY')

class APIs(commands.Cog):
    """Commands related to APIs."""
    def __init__(self, bot):
        self.bot = bot

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
        except requests.exceptions.RequestException as e:
            data = requests.get(url).json()
            return await ctx.reply(f"{r.status_code}: {data['msg']}")

def setup(bot):
    bot.add_cog(APIs(bot))