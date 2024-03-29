import discord
from discord.ext import commands
from datetime import datetime
import aiohttp
import json
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
        self.config = None

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

    @commands.Cog.listener()
    async def on_ready(self):
        print("Loading config file...")
        try:
            with open('././config.json') as config:
                self.config = json.load(config)
            print("Config file successfully loaded.")
            if 'blacklist' in self.config:
                print("Danbooru blacklist found.")
            else:
                raise FileNotFoundError()
        except FileNotFoundError:
            print(
                "Config file or Danbooru blacklist missing. "
                "Disabling 'danbooru' command."
                )
            self.bot.remove_command('danbooru')

    @commands.command()
    @commands.guild_only()
    async def apod(self, ctx, date=None):
        """Show the Astronomical Picture of the Day.

        date: yyyy-mm-dd
        Optional date for a specific picture.
        """
        url = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api_key}'

        if date is not None:
            url += f'&date={date}'

        data, status = await self.get_data(url)

        if data and status:
            return await ctx.reply(f"{status}: {data['msg']}")

        if data['media_type'] == 'image':
            embed = discord.Embed(
                title=f"{data['title']}",
                colour=discord.Colour.blurple()
            )
            embed.set_image(url=data['url'])

            if 'copyright' in data:
                embed.set_footer(
                    text=f"Image Credit & Copyright: {data['copyright']}"
                    )
            else:
                embed.set_footer(text='Public Domain')
            return await ctx.send(embed=embed)

        if data['media_type'] == 'video' and 'youtube' in data['url']:
            url = re.search(
                'https://www.youtube.com/embed/(.*)?rel=0', data['url']
                )
            return await ctx.send(f"https://youtu.be/{url.group(1)}")

        await ctx.send(data['url'])

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def danbooru(self, ctx, *, tags=''):
        """Show a random image from Danbooru.

        tag: str
        Optional tag(s) for narrowing image search.
        """

        for tag in self.config['blacklist']:
            if tag in tags.lower():
                return await ctx.reply("The specified tag(s) are blacklisted.")

        url = (
            f'https://danbooru.donmai.us/'
            f'posts.json?limit=200&tags={tags}')
        data, status = await self.get_data(url)

        if data and status:
            return await ctx.reply(f"{status}: {data['message']}")

        if len(data) == 0:
            return await ctx.reply(
                "The specified tag(s) returned no results."
                )

        post = random.choice(data)
        msg = await ctx.send(post['file_url'])
        self.image_cache[ctx.author.id] = msg.id

    @commands.command()
    @commands.is_nsfw()
    @commands.guild_only()
    async def undo(self, ctx):
        """Remove your recently requested image."""
        try:
            request = self.image_cache[ctx.author.id]
        except KeyError:
            return await ctx.reply("No image to remove.")

        msg = await ctx.channel.fetch_message(request)
        await msg.delete()
        self.image_cache.pop(ctx.author.id)

    @commands.command()
    @commands.guild_only()
    async def weather(self, ctx, *, location):
        """Retrieve weather data for a location from OpenWeatherMap.

        location: str
        The location to retrieve weather data for.
        """
        url = (
            f'https://api.openweathermap.org/'
            f'data/2.5/weather?q={location}'
            f'&appid={owm_api_key}&units=metric'
            )
        data, status = await self.get_data(url)

        if data and status:
            return await ctx.reply(f"{status}: {data['message']}")

        sys = data['sys']
        weather = data['weather'][0]
        main = data['main']
        wind = data['wind']

        if 'country' not in sys:
            title = f"{data['name']}"
        else:
            title = f"{data['name']}, {sys['country']}"

        embed = discord.Embed(
            title=title,
            colour=discord.Colour.blurple(),
            description=(
                f"**{round(main['temp'])}\u00b0C**"
                f"\u2002{weather['main']} ({weather['description']})"
                )
            )

        embed.set_thumbnail(
            url=(
                f'http://openweathermap.org/'
                f"img/wn/{weather['icon']}@2x.png"
                )
            )

        if 'rain' not in data:
            rain = '0'
        else:
            rain = data['rain']['1h']

        compass_dir = [
            'N', 'NNE', 'NE', 'ENE',
            'E', 'ESE', 'SE', 'SSE',
            'S', 'SSW', 'SW', 'WSW',
            'W', 'WNW', 'NW', 'NNW',
            'N',
            ]
        wind_dir = compass_dir[round((wind['deg'] % 360) / 22.5)]

        embed.add_field(
            name='Temperatures',
            value=f"""
            Min Temp: {round(main['temp_min'])}\u00b0C
            Max Temp: {round(main['temp_max'])}\u00b0C
            """,
            inline=False
        )

        embed.add_field(
            name='Atmospherics',
            value=f"""
            Percipitation: {rain} mm
            Humidity: {main['humidity']}%
            Wind Speed: {round(wind['speed'], 1)} m/s {wind_dir}
            Atmos Pres: {main['pressure']} hPa
            """,
            inline=False
        )

        embed.add_field(
            name='Times',
            value=f"""
            Sunrise: {datetime.fromtimestamp(sys['sunrise'])
            .strftime('%I:%M %p')}
            Sunset: {datetime.fromtimestamp(sys['sunset'])
            .strftime('%I:%M %p')}
            """,
            inline=False
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(APIs(bot))
