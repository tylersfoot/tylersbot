import discord
from discord.ext import commands
from math import *
import time
from humanize import number


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def calc(self, ctx, operation: str):
        try:
            result = eval(operation.replace(' ',''), {'sqrt': sqrt, 'pow': pow})
            await ctx.reply(result)
        except Exception as error:
            await ctx.reply(f'Error occured: `{error}`')

    @commands.command()
    async def pi(self, ctx, n):
        async with ctx.typing():
            try:
                n = int(round(float(n)))
                start_time = time.time()
                with open('data/pi-billion.txt', 'r') as file:
                    data = file.read()
                digit = data[n+1]
                file.close()
                print(f'\nIndexing took {round((time.time()-start_time), 2)}s to run')
                await ctx.reply(f'The {number.ordinal(n)} digit of 𝜋 is {digit}.')
            except Exception as error:
                print(error)
                if str(error) in {'string index out of range', 'cannot fit \'int\' into an index-sized integer'}:
                    await ctx.reply('Number is too big or small. Enter a number from 1 to 1 billion.')
                if str(error) in {f'could not convert string to float: \'{n}\''}:
                    await ctx.reply('Please enter a number.')
                else:
                    await ctx.reply(f'Error occured: `{error}`. Please report this to `tylersfoot`.')


def setup(bot):
    bot.add_cog(Calculator(bot))