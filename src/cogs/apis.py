import discord
from discord.ext import commands
import aiohttp
from datetime import datetime
import os
import random
import re

nasa_api_key = os.getenv('NASA_API_KEY')
owm_api_key = os.getenv('OWM_API_KEY')


class APIs(commands.Cog):
    """Commands related to APIs."""
    def __init__(self, bot):
        self.bot = bot
        self.image_cache = {}

    async def get_data(self, url):
        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as r:
                data = await r.json()
                try:
                    r.raise_for_status()
                    return data, None
                except aiohttp.ClientResponseError as e:
                    status = e.status
                    return data, status
                except aiohttp.web.Exception as e:
                    print(e)

    @commands.command()
    @commands.guild_only()
    async def apod(self, ctx, date=None):
        """Show the Astronomical Picture of the Day.

        date: yyyy-mm-dd
        Optional date for a specific picture. Leave blank for today's picture."""
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}'
        if date is not None:
            url += f'&date={date}'
        data, status = await self.get_data(url)
        if data and status:
            return await ctx.reply(f"{status}: {data['msg']}")
        else:
            if data['media_type'] == 'image':
                embed = discord.Embed(
                    title=f"{data['title']}",
                    colour=discord.Colour.blurple()
                )
                embed.set_image(url=data['url'])
                if 'copyright' in data:
                    embed.set_footer(text=f"Image Cred & Copyright: {data['copyright']}")
                else:
                    embed.set_footer(text="Public Domain")
                return await ctx.send(embed=embed)
            elif data['media_type'] == 'video' and 'youtube' in data['url']:
                url = re.search('https://www.youtube.com/embed/(.*)?rel=0', data['url'])
                return await ctx.send(f'https://youtu.be/{url.group(1)}')
            else:
                await ctx.send(data['url'])

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def danbooru(self, ctx, *, tags=''):
        """Show a random image from Danbooru.

        tag: str
        Optional tag(s) for searching specific images. Leave blank for random image."""
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
                data, status = await self.get_data(url)
                if data and status:
                    return await ctx.reply(f"{status}: {data['message']}")
                else:
                    if len(data) == 0:
                        return await ctx.reply("The specified tag(s) returned no results.")
                    post = random.choice(data)
                    msg = await ctx.send(post['file_url'])
                    self.image_cache[ctx.author.id] = msg.id
                    return

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def undo(self, ctx):
        """Remove your recently requested image."""
        try:
            request = self.image_cache[ctx.author.id]
        except KeyError:
            return await ctx.reply("There is no image to remove.")
        else:
            msg = await ctx.channel.fetch_message(request)
            await msg.delete()
            self.image_cache.pop(ctx.author.id)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.NSFWChannelRequired):
            return await ctx.reply("Command can only be used in a NSFW channel.")

    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, *, location):
        """Retrieve weather data for a location from OpenWeatherMap.

        location: str
        The location you want to retrieve weather data for."""
        url = f'https://api.openweathermap.org/data/2.5/weather?q={location}&appid={owm_api_key}&units=metric'
        data, status = await self.get_data(url)
        if data and status:
            return await ctx.reply(f"{status}: {data['message']}")
        else:
            embed = discord.Embed(
                title=f"{data['name']}, {data['sys']['country']}",
                colour=discord.Colour.blurple(),
                description=f"**{round(data['main']['temp'])}\u00b0C**\u2002{data['weather'][0]['main']}: {data['weather'][0]['description']}."
            )
            embed.set_thumbnail(url=f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png")
            if 'rain' not in data:
                rain = '0'
            else:
                rain = data['rain']['1h']
            embed.add_field(name="Precipitation:", value=f"{rain} mm")
            embed.add_field(name="Humidity:", value=f"{data['main']['humidity']}%")
            compass_dir = [
                'N',
                'NNE',
                'NE',
                'ENE',
                'E',
                'ESE',
                'SE',
                'SSE',
                'S',
                'SSW',
                'SW',
                'WSW',
                'W',
                'WNW',
                'NW',
                'NNW',
                'N'
            ]
            wind_dir = compass_dir[round((data['wind']['deg'] % 360) / 22.5)]
            embed.add_field(name="Wind Speed:", value=f"{round(data['wind']['speed'], 1)} m/s {wind_dir}")
            embed.add_field(name="Atmos Pres:", value=f"{data['main']['pressure']} hPa")
            embed.add_field(name="Data Generated:", value=datetime.fromtimestamp(data['dt']).strftime("%#I:%M %p, %a %#d"))
            await ctx.send(embed=embed)

    @weather.error
    async def weather_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("No location was provided.")


def setup(bot):
    bot.add_cog(APIs(bot))
