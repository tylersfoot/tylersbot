import discord
from discord.ext import commands
from sympy import parse_expr
from sympy.core.sympify import SympifyError
import asyncio
from concurrent.futures import ThreadPoolExecutor


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executor = ThreadPoolExecutor()

    async def evaluate_expression(self, expression: str):
        # Define local and global dictionaries for safe evaluation
        local_dict = {}
        global_dict = {}

        # This function evaluates the expression in a separate thread
        expression = expression.replace(" ", "").replace("^", "**").replace("×", "*").replace("÷", "/")

        # Run the blocking `parse_expr` function in a thread
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, parse_expr, expression, local_dict, global_dict, True)

    # @commands.slash_command(
    #     name="calculate",
    #     description="Calculates the given mathematical expression.",
    #     integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install},
    # )
    # async def calc(self, ctx, expression: str):
    #     await ctx.response.defer(ephemeral=False)

    #     try:
    #         # Use asyncio to set a timeout for the evaluation
    #         result = await asyncio.wait_for(self.evaluate_expression(expression), timeout=5)
    #         await ctx.respond(f"The result is: `{result}`")
    #     except asyncio.TimeoutError:
    #         await ctx.respond("The calculation took too long and was canceled.", ephemeral=True)
    #     # except SympifyError:
    #     #     await ctx.respond("Invalid mathematical expression! Please use a valid format.", ephemeral=True)
    #     # except SyntaxError:
    #     #     await ctx.respond("Invalid mathematical expression! Please use a valid format.", ephemeral=True)
    #     # except TypeError:
    #     #     await ctx.respond("Invalid mathematical expression! Please use a valid format.", ephemeral=True)
    #     except Exception as error:
    #         if "Exceeds the limit" in str(error):
    #             await ctx.respond("Expression is too large to calculate.", ephemeral=True)
    #         else:
    #             raise error


def setup(bot):
    bot.add_cog(Calculator(bot))
