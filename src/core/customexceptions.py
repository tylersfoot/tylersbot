from discord.ext import commands


class NotDeveloperError(commands.CommandError):
    # raised when a non-developer tries to use a developer command
    pass


class WikiDisambiguationError(commands.CommandError):
    # raised when a Wikipedia search returns a disambiguation page
    def __init__(self, request):
        self.request = request


class WikiPageError(commands.CommandError):
    # raised when a Wikipedia search returns no results
    def __init__(self, request):
        self.request = request


class OsuAccountNotLinkedError(commands.CommandError):
    # raised when an osu! account is not in the db
    pass


class BotMissingPermissionsError(commands.CommandError):
    # raised when the bot is missing permissions
    def __init__(self, missing_permissions):
        self.missing_permissions = missing_permissions
