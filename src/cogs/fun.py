import discord
from discord.ext import commands
import random
import asyncio
import aiohttp


class Fun(commands.Cog):
    """Commands that do fun stuff."""
    def __init__(self, bot):
        self.bot = bot
        self.playing_hangman = set()

    @commands.command(name='coin')
    @commands.guild_only()
    async def coin_flip(self, ctx):
        """Flip a coin and land on heads or tails."""
        sides = [
            'Heads',
            'Tails',
            ]
        await ctx.reply(f"{random.choice(sides)}.")

    @commands.command()
    @commands.guild_only()
    async def choose(self, ctx, *, choices: str):
        """Pick one out of multiple choices.

        choices: str, str
        The choices to pick from. List choices using commas.
        """
        choices = choices.split(',')
        await ctx.reply(random.choice(choices))

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("You did not provide any choices.")

    @commands.command()
    @commands.guild_only()
    async def dice(self, ctx, number: float):
        """Roll a number between 1 and the specified number.

        number: int
        Number of sides on the dice. Must be a whole number.
        """
        if (number).is_integer():
            return await ctx.reply(random.randint(1, number))
        await ctx.reply("The number must be a whole number.")

    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.reply("The number must be larger than one.")

    @commands.command(name='8ball')
    @commands.guild_only()
    async def eight_ball(self, ctx):
        """Seek advice or fortune-telling."""
        responses = [
            'It is certain',
            'It is decidedly so',
            'Without a doubt',
            'Yes - definitely',
            'You may rely on it',
            'As I see it, yes',
            'Most likely',
            'Outlook good',
            'Yes',
            'Signs point to yes',
            'Reply hazy, try again',
            'Ask again later',
            'Better not tell you now',
            'Cannot predict now',
            'Concentrate and ask again',
            'Don\'t count on it',
            'My reply is no',
            'My sources say no',
            'Outlook not so good',
            'Very doubtful',
            ]
        await ctx.reply(f"{random.choice(responses)}.")

    @commands.command()
    @commands.guild_only()
    async def hangman(self, ctx):
        """Start a game of hangman."""
        if ctx.author.id not in self.playing_hangman:
            self.playing_hangman.add(ctx.author.id)
        else:
            return await ctx.reply("Game already running.")

        url = 'https://random-word-api.herokuapp.com/word?number=1'

        timeout = aiohttp.ClientTimeout(total=10)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as r:
                word = (await r.json())[0]

        guess_count = 6
        guess_wrong = []
        guess_correct = list(len(word) * '_')
        guesses = {
            0: '8/8b/Hangman-0.png',
            1: 'd/d6/Hangman-6.png',
            2: '6/6b/Hangman-5.png',
            3: '2/27/Hangman-4.png',
            4: '9/97/Hangman-3.png',
            5: '7/70/Hangman-2.png',
            6: '3/30/Hangman-1.png'
        }

        embed = discord.Embed(colour=discord.Color.blurple())
        embed.set_thumbnail(
            url=f'https://upload.wikimedia.org/wikipedia/commons/{guesses[0]}'
            )
        embed.add_field(name=f"`{' '.join(guess_correct)}`", value='\u200b')
        embed.set_footer(text='Type end to quit game.')
        await ctx.reply(embed=embed)

        def check(message):
            return message.author == ctx.message.author and \
                message.channel == ctx.channel

        while guess_count != 0:
            try:
                guess = await self.bot.wait_for(
                    'message', timeout=30, check=check
                    )
            except asyncio.TimeoutError:
                break

            guess = guess.content.lower()

            if len(guess) > 1:
                if guess == 'end':
                    break
                if guess == ctx.prefix + 'hangman':
                    continue
                await ctx.reply("Enter a letter.")
                continue

            if guess in guess_wrong or guess in guess_correct:
                await ctx.reply("Duplicate letter.")
                continue

            if guess in word:
                for index, x in enumerate(word):
                    if x == guess:
                        guess_correct[index] = guess
                embed.set_field_at(
                    index=0,
                    name=f"`{' '.join(guess_correct)}`",
                    value=' '.join(guess_wrong) or '\u200b'
                    )
                await ctx.reply(embed=embed)
                if ''.join(guess_correct) == word:
                    self.playing_hangman.remove(ctx.author.id)
                    return await ctx.reply("You figured out the word!")
            else:
                embed.set_thumbnail(
                    url='https://upload.wikimedia.org/wikipedia/commons/'
                    f'{guesses[guess_count]}'
                    )
                guess_wrong.append(guess)
                embed.set_field_at(
                    index=0,
                    name=f"`{' '.join(guess_correct)}`",
                    value=' '.join(guess_wrong)
                    )
                await ctx.reply(embed=embed)
                guess_count -= 1
                if guess_count == 0:
                    break
        self.playing_hangman.remove(ctx.author.id)
        await ctx.reply(f"Game ended. The word was {word}.")


def setup(bot):
    bot.add_cog(Fun(bot))
