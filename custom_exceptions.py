from discord.ext import commands

class NotDeveloperError(commands.CommandError):
    # raised when a non-developer tries to use a developer command
    pass
