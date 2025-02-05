# https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#exceptions
import discord
import traceback
import sys
from discord.ext import commands
from customexceptions import *
from logger import *


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()    
    async def on_application_command_error(self, ctx, error):
        # triggered when a slash command throws an error
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.respond(f"You're on cooldown! Try again in {round(error.retry_after, 2)} seconds.", ephemeral=True)
        elif isinstance(error, commands.MissingPermissions):
            missing = ', '.join(error.missing_permissions)
            await ctx.respond(f"You don't have the required permissions to use this command. Missing permission `{missing}`", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.respond("You're missing a required argument.", ephemeral=True)
        elif isinstance(error, NotDeveloperError):
            await ctx.respond("Only developers can use this command! You.. shouldn't even be able to see this :P", ephemeral=True)
        elif isinstance(error, WikiDisambiguationError):
            await ctx.respond(f"There are too many search results \"{error.request}\". Please be more specific.", ephemeral=True)
        elif isinstance(error, WikiPageError):
            await ctx.respond(f"Sorry, there are no results for \"{error.request}\".", ephemeral=True)
        elif isinstance(error, OsuAccountNotLinkedError):
            await ctx.respond(f"Please link your osu! account with `/osu link`!", ephemeral=True)
        elif isinstance(error, BotMissingPermissionsError):
            missing = ', '.join(error.missing_permissions)
            await ctx.respond(f"I am missing the permission(s) `{missing}`!", ephemeral=True)
        elif "Must be 2000 or fewer in length" in str(error):
            await ctx.respond("The bot's response was too long for Discord!", ephemeral=True)

        else:
            # log unhandled errors
            log_error(f"Unhandled exception: {error}")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
            await ctx.respond("An unexpected error occurred. Please report this to the developers.", ephemeral=True)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))