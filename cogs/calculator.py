import discord
from discord.ext import commands
from sympy import parse_expr
from sympy.core.sympify import SympifyError


class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.slash_command(name="calculate", description="Calculates the given mathematical expression.",
                            integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def calc(self, ctx, expression: str):
        await ctx.response.defer(ephemeral=False)  # defers the response
        try:
            # allow only valid characters (numbers, operators, and basic math symbols)
            allowed_chars = "0123456789+-*/^().e "
            if not all(char in allowed_chars for char in expression):
                raise ValueError("Expression contains invalid characters.")

            # safely parse and evaluate the expression
            result = parse_expr(expression, evaluate=True)
            await ctx.respond(f"The result is: `{result}`")
        except SympifyError:
            await ctx.respond("Invalid mathematical expression! Please use a valid format.")
        except ValueError as e:
            await ctx.respond(str(e))
        except Exception as e:
            await ctx.respond(f"An unexpected error occurred: `{e}`")


def setup(bot):
    bot.add_cog(Calculator(bot))
