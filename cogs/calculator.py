import discord
from discord.ext import commands
from math import *
import time
from humanize import number
from bot import guilds


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="calculate", description="Calculates the given expression.", guilds=guilds)
    async def calc(self, ctx, operation: str):
        try:
            result = eval(operation.replace(' ',''), {'sqrt': sqrt, 'pow': pow})
            await ctx.respond(result)
        except Exception as error:
            await ctx.respond(f'Error occured: `{error}`\nPlease report to `tylersfoot#8888`')

    @commands.slash_command(name="pi", description="Returns the nth digit of pi (up to 1bil)", guilds=guilds)
    async def pi(self, ctx, n):
        await ctx.response.defer(ephemeral=True)
        try:
            n = int(round(float(n)))
            start_time = time.time()
            with open('data/pi-billion.txt', 'r') as file:
                data = file.read()
            digit = data[n+1]
            file.close()
            print(f'\nIndexing took {round((time.time()-start_time), 2)}s to run')
            await ctx.followup.send(f'The {number.ordinal(n)} digit of 𝜋 is {digit}.')
        except Exception as error:
            print(error)
            if str(error) in {'string index out of range', 'cannot fit \'int\' into an index-sized integer'}:
                await ctx.followup.send('Number is too big or small. Enter a number from 1 to 1 billion.')
            if str(error) in {f'could not convert string to float: \'{n}\''}:
                await ctx.followup.send('Please enter a number.')
            else:
                await ctx.followup.send(f'Error occured: `{error}`. Please report this to `tylersfoot#8888`.')


def setup(bot):
    bot.add_cog(Calculator(bot))