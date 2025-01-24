# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
import discord
import traceback
import sys
from discord.ext import commands

class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx, error):
        # triggered when a slash command throws an error
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"You're on cooldown! Try again in {round(error.retry_after, 2)} seconds.", ephemeral=True)
        elif isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have the required permissions to use this command.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("You're missing a required argument.", ephemeral=True)
        else:
            # log unhandled errors
            print("Unhandled exception:", file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.respond("An unexpected error occurred. Please report this to the developers.", ephemeral=True)

def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))