import discord
from discord.ext import commands

import random
from utils import default

class Fun(commands.Cog):
    """Commands that do fun stuff."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['coin'])
    @commands.guild_only()
    async def coinflip(self, ctx):
        """Flip a coin and land on heads or tails."""
        sides = ['Heads', 'Tails']
        side = random.choice(sides)
        return await ctx.send(f"{side}.")

    @commands.command(aliases=['choice', 'decision'])
    @commands.guild_only()
    async def choose(self, ctx, choices: str):
        """Pick one out of multiple choices.

        choices: str|str
        The choices to pick from. Multiple choices can be appended. Separate all choices with vertical bars."""
        choice_list = choices.split('|')
        random.shuffle(choice_list)
        answer = random.choice(choice_list)
        return await ctx.send(answer)

    @choose.error
    async def choose_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You did not provide any choices.")

    @commands.command()
    @commands.guild_only()
    async def dice(self, ctx, number: float):
        """Roll a number between 1 and the specified number.

        number: int
        The highest number rollable. Must be a whole number."""
        if (number).is_integer():
            return await ctx.send(random.randint(1, number))
        else:
            return await ctx.send("The number must be a whole number.")

    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("The number must be larger than one.")

    @commands.command(name='8ball')
    @commands.guild_only()
    async def eightball(self, ctx):
        """Seek advice or fortune-telling."""
        random.shuffle(default.eightball_responses)
        answer = random.choice(default.eightball_responses)
        return await ctx.send(f"{answer}.")

def setup(bot):
    bot.add_cog(Fun(bot))