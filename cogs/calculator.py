import discord
from discord.ext import commands
from sympy import parse_expr
from sympy.core.sympify import SympifyError
import multiprocessing
import asyncio


def calc_worker(expression, queue):
    try:
        # do the parsing (and any heavy calculation) in this process
        result = parse_expr(expression)
        queue.put(('success', result))
    except Exception as e:
        queue.put(('error', str(e)))


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(
        name="calculate",
        description="Calculates the given mathematical expression.",
        integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install},
    )
    async def calc(self, ctx, expression: str):
        await ctx.response.defer(ephemeral=False)
        # clean up the expression
        expression2 = expression.replace(" ", "").replace("^", "**").replace("×", "*").replace("÷", "/")
        
        # start a new process for the heavy calculation
        queue = multiprocessing.Queue()
        process = multiprocessing.Process(target=calc_worker, args=(expression2, queue))
        process.start()
        
        # poll every 0.1 sec until either the process finishes or 5 sec have passed
        start_time = asyncio.get_running_loop().time()
        while process.is_alive() and (asyncio.get_running_loop().time() - start_time) < 5:
            await asyncio.sleep(0.1)

        if process.is_alive():
            # if it's still running after 5 seconds, terminate it without blocking the loop
            await asyncio.to_thread(process.terminate)
            await asyncio.to_thread(process.join)
            await ctx.respond("The calculation took too long to process!", ephemeral=True)
            return
        else:
            # if finished, ensure we join quickly (again, offloaded to a thread)
            await asyncio.to_thread(process.join)

        # get the result from the queue
        status, result = queue.get_nowait()

        if status == 'success':
            await ctx.respond(f"expression: `{expression}`\nresult: `{result}`")
        else:
            # handle known error messages
            if "Exceeds the limit" in result:
                await ctx.respond(f"the expression `{expression}` is too large to calculate.", ephemeral=True)
            else:
                await ctx.respond(f"`{expression}` is not a valid mathematical expression!", ephemeral=True)



def setup(bot):
    bot.add_cog(Calculator(bot))
