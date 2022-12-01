import discord
from discord.ext import commands
from craiyon import Craiyon
import asyncio
import time
import os
import random
import PIL
from PIL import Image


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


class Imagegen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['imggen', 'imagegen', 'aiimage', 'aiimg', 'aiimagegen', 'aiimggen'])
    async def img(self, ctx, *, prompt):
        try:
            startTime = time.time()
            uid = str(random.randint(1, 1000000000000))

            await ctx.reply('Generating images... please wait around 1-2 minutes.')
            generator = Craiyon()  # Instantiates the api wrapper
            async with ctx.typing():
                result = generator.generate(prompt)
                result.save_images('./data/temp/')  # Saves the generated images to 'data/temp/
            for i in range(1, 10):
                os.rename(f'./data/temp/image-{i}.png', f'./data/temp/img-{uid}-{i}.png')

            imdict = {}
            for i in range(1, 10):
                imdict["im{0}".format(i)] = Image.open(f"./data/temp/img-{uid}-{i}.png")
                # im = Image.open(f"./data/temp/img-{uid}-1.png")
                # print(im.format, im.size, im.mode)
            # im = Image.close(f"./data/temp/img-{uid}-1.png")
            merge(imdict[f"im{1}"], imdict[f"im{2}"]).save(f"./data/temp/img-{uid}-merged.png")
            for i in range(3, 10):
                merged = Image.open(f"./data/temp/img-{uid}-merged.png")
                merge(imdict[f"im{i}"], merged).save(f"./data/temp/img-{uid}-merged.png")

            embed = discord.Embed(
                title=f"Here are your ai generated images!",
                description=f'Prompt: "{prompt}"',
                color=int(str(ctx.author.color)[1:], 16)
            )
            file = discord.File(f'./data/temp/img-{uid}-merged.png', filename=f'img-{uid}-merged.png')
            embed.set_image(url=f'attachment://img-{uid}-merged.png')

            embed.timestamp = ctx.message.created_at
            embed.set_footer(text=f'Requested by {ctx.author.name} - took {(time.time() - startTime):.1f}s to generate', icon_url=ctx.author.avatar.url)
            await ctx.reply(file=file, embed=embed)
            for i in range(1, 10):
                os.remove(f'./data/temp/img-{uid}-{i}.png')
            os.remove(f'./data/temp/img-{uid}-merged.png')
        except Exception as e:
            await ctx.reply(f'An error occured: [{e}] \nPlease report this to tylersfoot#8888')


def setup(bot):
    bot.add_cog(Imagegen(bot))
