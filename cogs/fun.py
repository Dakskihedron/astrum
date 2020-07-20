import discord
from discord.ext import commands

import random
from utils import default

"""Fun commands"""

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Coinflip
    @commands.command(brief='Flip a coin.', description='Flip a coin')
    @commands.guild_only()
    async def coinflip(self, ctx):
        sides = ['heads', 'tails']
        random.shuffle(sides)
        landed_side = random.choice(sides)
        return await ctx.send(f"{ctx.author.mention} {landed_side}.")

    # Decide
    @commands.command(usage='[choice|choice|...]', brief='Makes a choice for you.', description='Makes a choice for you\nSeparate choices with `|`.')
    @commands.guild_only()
    async def decide(self, ctx, *, choices : str):
        choice_list = choices.split('|')
        random.shuffle(choice_list)
        answer = random.choice(choice_list)
        return await ctx.send(f"{ctx.author.mention} {answer}")

    # Dice
    @commands.command(brief='Roll a random number.', description='Roll a random number.')
    @commands.guild_only()
    async def dice(self, ctx, number : float):
        if (number).is_integer():
            return await ctx.send(f"{ctx.author.mention} {random.randrange(1, number)}")
        else:
            return await ctx.send(f"{ctx.author.mention} the provided number must be a whole number.")

    @dice.error
    async def dice_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            return await ctx.send(f"{ctx.author.mention} the provided number must be larger than one.")

    # Magic eight ball
    @commands.command(name='8ball', usage='[question]', brief='Seek advice or fortune-telling.', description='Seek advice or fortune-telling.')
    @commands.guild_only()
    async def eightball(self, ctx, question):
        random.shuffle(default.eightball_responses)
        answer = random.choice(default.eightball_responses)
        return await ctx.send(f"{ctx.author.mention} {answer}.")

    @eightball.error
    async def eightball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"{ctx.author.mention} you didn't ask a question.")

def setup(bot):
    bot.add_cog(Fun(bot))