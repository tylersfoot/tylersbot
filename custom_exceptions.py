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