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
            await ctx.respond('Calculation took too long, please try again with a simpler expression.')
        except Exception as e:
            try:
                await ctx.respond(f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')
            except:
                await ctx.send(f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')

    # @commands.slash_command(name="pi", description="Returns the nth digit of pi.", guilds=guilds)
    # async def pi(self, ctx, n: int):
    #     await ctx.response.defer(ephemeral=False)
    #     try:
    #         startTime = time.time()
    #         # Set the precision of the mpmath library to the desired number of digits
    #         mpmath.mp.dps = n + 1
    #
    #         # Calculate the value of pi to n + 1 decimal places
    #         pi = mpmath.pi
    #
    #         # Retrieve the nth digit of pi
    #         digit = int(str(pi)[n + 1])
    #
    #         # Convert the value of digit to a string
    #         digit = str(digit)
    #
    #         # Return the nth digit of pi
    #         embed = discord.Embed(
    #             title=f"The {number.ordinal(n)} digit of pi is {digit}.",
    #             color=int(str(ctx.author.color)[1:], 16)
    #         )
    #         embed.timestamp = datetime.datetime.now()
    #         embed.set_footer(
    #             text=f'Requested by {ctx.author.name} ~ generated in {(time.time() - startTime):.1f}s',
    #             icon_url=ctx.author.avatar.url)
    #         await ctx.followup.send(embed=embed)
    #     except Exception as e:
    #         if str(e) in {'string index out of range', 'cannot fit \'int\' into an index-sized integer'}:
    #             await ctx.respond('Number is too big or small. Enter a number from 1 to 1 billion.')
    #         if str(e) in {f'could not convert string to float: \'{n}\''}:
    #             await ctx.respond('Please enter a number.')
    #         else:
    #             # Extract the line number from the traceback information
    #             tb = traceback.extract_tb(e.__traceback__)
    #             line_number = tb[-1].lineno
    #
    #             # Add the line number to the error message
    #             e = f"{e} (line {line_number})"
    #             await ctx.respond(f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')


def setup(bot):
    bot.add_cog(Calculator(bot))
