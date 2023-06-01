import datetime
import discord
from discord.ext import commands
from math import *
import time
from humanize import number
from bot import guilds
import mpmath
import traceback
import asyncio
''' !!!!WARNING!!!!
This uses eval(), which can be used to execute code. Just be careful when using this.
'''

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.slash_command(name="calculate", description="Calculates the given expression.")
    async def calc(self, ctx, expression: str):
        # create task to run the calculation in background
        task = asyncio.create_task(eval(expression))
        await ctx.response.defer(ephemeral=False)
        try:
            # list of operators
            operators = ['+', '-', '*', '/', '^', 'sqrt']

            # loop through the list of operators
            for operator in operators:
                # replace the operator symbol with the corresponding python operator (e.g. '^' becomes '**')
                expression = str(expression)
                expression = expression.replace(operator, {
                    '+': '+',
                    '-': '-',
                    '*': '*',
                    'x': '*',
                    '/': '/',
                    '^': '**',
                    'sqrt': 'sqrt',
                    ' ': '',
                    '(': '(',
                    ')': ')'
                }[operator])

            # wait for the evaluation to complete or for the timeout to expire
            result = await asyncio.wait_for(task, timeout=10)

            await ctx.respond(result)
            
            # cancel the timer
            signal.alarm(0)
        except asyncio.TimeoutError:
            task.cancel()
            await ctx.respond('Calculation took too long, please try again with a simpler expression')
        except Exception as e:
            try:
                await ctx.respond(f'Sorry, an error occurred: \n`{e}`\n - Please report to a developer')
            except:
                await ctx.send(f'Sorry, an error occurred: \n`{e}`\n - Please report to a developer')

def setup(bot):
    bot.add_cog(Calculator(bot))
