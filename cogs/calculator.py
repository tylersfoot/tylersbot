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
        await ctx.response.defer(ephemeral=False)
        try:
            allowed_chars = "0123456789+-*/^().e "
            if not all(char in allowed_chars for char in expression):
                await ctx.respond("Expression contains invalid characters.", ephemeral=True)
                return
            
            result = parse_expr(expression, evaluate=True)
            await ctx.respond(f"The result is: `{result}`")
        except SympifyError:
            await ctx.respond("Invalid mathematical expression! Please use a valid format.", ephemeral=True)
        except Exception as error:
            if "Exceeds the limit" in str(error):
                await ctx.respond("Expression is too large to calculate.", ephemeral=True)
            else:
                raise error

def setup(bot):
    
    bot.add_cog(Calculator(bot))
