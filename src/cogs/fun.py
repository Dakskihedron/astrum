import discord
from discord.ext import commands
import random
import asyncio
import cogs.utils.functions as functions


class Fun(commands.Cog):
    """Commands that do fun stuff."""
    def __init__(self, bot):
        self.bot = bot
        self.playing_list = []

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
        else:
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
        if ctx.author.id not in self.playing_list:
            self.playing_list.append(ctx.author.id)
        else:
            return await ctx.reply("Game already running.")
        data, status = await functions.get_data(
            'https://random-word-api.herokuapp.com/word?number=1'
            )
        if data and status:
            return await ctx.reply(f"{status}: {data}")
        else:
            word = data[0]
        guesses = 8
        char_list = []
        word_guessed = list(len(word) * '_')
        embed = discord.Embed(colour=discord.Colour.blurple())
        embed.set_author(name=f'Guesses Left: {guesses}')
        embed.add_field(
            name=f"`{' '.join(word_guessed)}`",
            value='\u200b'
            )
        embed.set_footer(text=f'End game with {ctx.prefix}end')
        await ctx.reply(embed=embed)

        def check(message):
            return message.author == ctx.message.author

        while guesses != 0:
            try:
                char = await self.bot.wait_for(
                    'message',
                    timeout=30,
                    check=check
                    )
                char = char.content.lower()
            except asyncio.TimeoutError:
                self.playing_list.pop(self.playing_list.index(ctx.author.id))
                return await ctx.reply(
                    "Game timed out. "
                    f"The word was {word}."
                    )
            if char == f'{ctx.prefix}end':
                break
            elif char in char_list or char in word_guessed:
                await ctx.reply("Duplicate letter.")
            elif char in word:
                for index, x in enumerate(word):
                    if x == char:
                        word_guessed[index] = char
                    embed.set_field_at(
                        index=0,
                        name=f"`{' '.join(word_guessed)}`",
                        value=' '.join(char_list) or '\u200b'
                        )
                await ctx.reply(embed=embed)
                if ''.join(word_guessed) == word:
                    self.playing_list.pop(
                        self.playing_list.index(ctx.author.id)
                        )
                    return await ctx.reply("You figured out the word!")
            elif not char == f'{ctx.prefix}hangman':
                guesses -= 1
                if guesses == 0:
                    break
                char_list.append(char)
                embed.set_author(name=f'Guesses Left: {guesses}')
                embed.set_field_at(
                    index=0,
                    name=f"`{' '.join(word_guessed)}`",
                    value=' '.join(char_list)
                    )
                await ctx.reply(embed=embed)
        self.playing_list.pop(self.playing_list.index(ctx.author.id))
        return await ctx.reply(
            f"Game ended. The word was {word}."
            )


def setup(bot):
    bot.add_cog(Fun(bot))
