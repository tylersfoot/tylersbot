import discord
from discord.ext import commands
import random
import pyqrcode
import os


class Qrcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['qrcode', 'qr-code'])
    async def qr(self, ctx, *, message):
        # Generates a qr code from the message text

        # -------------------------------- #
        def grab_box(input, rows, columns, x, y):
            # grabs an x by y box of characters
            output = []
            for i in range(rows):
                output.append(''.join(input[x + i][y:y + columns]))
            return output
        # -------------------------------- #
        def check(input):
            # checks for the amongus
            rows = len(input)
            cols = len(input[0])
            for i in range(rows - 5 + 1):
                for j in range(cols - 4 + 1):
                    if grab_box(input, 5, 4, i, j) == ['0111', '1100', '1111', '0111', '0101']:
                        return True, j, i
            return False, 0, 0
        # -------------------------------- #

        uid = str(random.randint(1, 1000000))
        try:
            code = pyqrcode.create(message)
        except ValueError:
            await ctx.send(f'Text too big to be converted to QR code.')
            return
        else:
            pass
        text = code.text()
        code.png(f'./data/temp/{uid}.png', scale=5)

        qrtext = text.splitlines()
        for i in range(len(qrtext)):
            qrtext[i] = list(qrtext[i])

        embed = discord.Embed(
            title=f"Here is your processed QR code!",
            color=int(str(ctx.author.color)[1:], 16)
        )
        if check(qrtext)[0]:
            embed.description = f'AMONG US FOUND IN QR CODE AT {check(qrtext)[1]}, {check(qrtext)[2]}!!!!'
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


def setup(bot):
    bot.add_cog(Qrcode(bot))
