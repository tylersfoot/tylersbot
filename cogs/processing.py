import discord
from discord.ext import commands
import random
import pyqrcode
import os


class Processing(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['qrcode', 'qr-code'])
    async def qr(self, ctx, *, link):

        uid = str(random.randint(1, 1000000))
        try:
            url = pyqrcode.create(link)
        except ValueError:
            await ctx.send('Text too big to be converted to QR code.')
            return
        else:
            pass

        url.png(f'./data/temp/{uid}.png', scale=5)

        embed = discord.Embed(
            title=f"Here is your processed QR code!",
            color=random.randint(0, 0xFFFFFF)
        )

        file = discord.File(f'./data/temp/{uid}.png', filename=f'qr-{uid}.png')
        embed.set_image(url=f'attachment://qr-{uid}.png')

        embed.timestamp = ctx.message.created_at
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.send(file=file, embed=embed)

    # @commands.command(aliases=['wikipedia', 'wikisearch'])
    # async def wiki(self, ctx, *, query):
    #
    #     try:
    #         wiki.summary(query, sentences=1, auto_suggest=False)
    #     except wiki.exceptions.DisambiguationError as e:
    #         query = e.options[0]
    #         return
    #     except wiki.exceptions.PageError:
    #         await ctx.send('Page not found.')
    #         return
    #     else:
    #         pass
    #
    #     p = wiki.page(query)
    #
    #     embed = discord.Embed(
    #         title=f"{p.title}",
    #         description=f'{wiki.summary(query, sentences=10)}',
    #         url=f'{p.url}',
    #         color=random.randint(0, 0xFFFFFF)
    #     )
    #     embed.set_thumbnail(url=f'{p.images[0]}')
    #     embed.timestamp = ctx.message.created_at
    #     embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
    #     await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Processing(client))
