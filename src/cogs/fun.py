import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
    """Commands that do fun stuff."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='coin')
    @commands.guild_only()
    async def coin_flip(self, ctx):
        """Flip a coin and land on heads or tails."""
        sides = ['Heads', 'Tails']
        await ctx.reply(f"{random.choice(sides)}.")

    @commands.command()
    @commands.guild_only()
    async def choose(self, ctx, *, choices: str):
        """Pick one out of multiple choices.

        choices: str, str
        The choices to pick from. List choices using commas."""
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
        Number of sides on the dice. Must be a whole number."""
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
            "It is certain",
            "It is decidedly so",
            "Without a doubt",
            "Yes - definitely",
            "You may rely on it",
            "As I see it, yes",
            "Most likely",
            "Outlook good",
            "Yes",
            "Signs point to yes",
            "Reply hazy, try again",
            "Ask again later",
            "Better not tell you now",
            "Cannot predict now",
            "Concentrate and ask again",
            "Don't count on it",
            "My reply is no",
            "My sources say no",
            "Outlook not so good",
            "Very doubtful"
        ]
        await ctx.reply(f"{random.choice(responses)}.")


def setup(bot):
    bot.add_cog(Fun(bot))
