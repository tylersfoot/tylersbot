import datetime
import discord
from discord.ext import commands
from math import *
import time
from humanize import number
from bot import guilds
import mpmath
import traceback


class Sex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="sex", description="!!!!!!!")
    async def sex(self, ctx, user: discord.Member = None):

        if user is None:
            text = f'{ctx.author.display_name} masturbated by themself.'
            desc = 'Lonely ass loser. Mention someone next time.'
        else:
            text = f'{ctx.author.display_name} had sex with {user.display_name}!'
            desc = '(for legal reasons they definitely consented beforehand)'

        embed = discord.Embed(
            title=text,
            description=desc,
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_image(url="https://media.tenor.com/OSipKEoW1YkAAAAd/sex-cat.gif")
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Sex(bot))
