import discord
from discord.ext import commands
from craiyon import Craiyon
import aiofiles
import aiofiles.os
import time
import random
from PIL import Image
from bot import guilds
import datetime
import traceback


def merge(im1, im2):
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im


async def image_open(path):
    return Image.open(path)


def merge_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (im1.width, 0))
    return dst


def merge_v(im1, im2):
    dst = Image.new('RGB', (im1.width, im1.height + im2.height))
    dst.paste(im1, (0, 0))
    dst.paste(im2, (0, im1.height))
    return dst


class Imagegen(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="img", description="Generates images based off the prompt using AI.", guilds=guilds)
    async def imggen(self, ctx, *, prompt):
        uid = str(random.randint(1, 1000000000000))
        try:
            # message = await ctx.respond('Generating images... please wait around 40-60 seconds <a:loading1:1048082138282606642>', ephemeral=True)
            message = await ctx.respond('Generating images... please wait around 40-60 seconds <a:loading1:1048082138282606642>')
            # await ctx.response.defer(ephemeral=True)
            start_time = time.perf_counter()

            generator = Craiyon()  # Instantiates the api wrapper
            result = await generator.async_generate(prompt)
            await result.async_save_images('./data/temp/')  # Saves the generated images to 'data/temp/
            for i in range(1, 10):
                await aiofiles.os.rename(f'./data/temp/image-{i}.jpg', f'./data/temp/img-{uid}-{i}.jpg')

            imdict = {f"im{i}": await image_open(f"./data/temp/img-{uid}-{i}.jpg") for i in range(1, 10)}
            # make top row
            merge_h(imdict[f"im{1}"], imdict[f"im{2}"]).save(f"./data/temp/img-{uid}-merged1.jpg")
            merged1 = await image_open(f"./data/temp/img-{uid}-merged1.jpg")
            merge_h(merged1, imdict[f"im{3}"]).save(f"./data/temp/img-{uid}-merged1.jpg")
            merged1 = await image_open(f"./data/temp/img-{uid}-merged1.jpg")
            # make middle row
            merge_h(imdict[f"im{4}"], imdict[f"im{5}"]).save(f"./data/temp/img-{uid}-merged2.jpg")
            merged2 = await image_open(f"./data/temp/img-{uid}-merged2.jpg")
            merge_h(merged2, imdict[f"im{6}"]).save(f"./data/temp/img-{uid}-merged2.jpg")
            merged2 = await image_open(f"./data/temp/img-{uid}-merged2.jpg")
            # make bottom row
            merge_h(imdict[f"im{7}"], imdict[f"im{8}"]).save(f"./data/temp/img-{uid}-merged3.jpg")
            merged3 = await image_open(f"./data/temp/img-{uid}-merged3.jpg")
            merge_h(merged3, imdict[f"im{9}"]).save(f"./data/temp/img-{uid}-merged3.jpg")
            merged3 = await image_open(f"./data/temp/img-{uid}-merged3.jpg")
            # merge rows
            merge_v(merged1, merged2).save(f"./data/temp/img-{uid}-merged4.jpg")
            merged4 = await image_open(f"./data/temp/img-{uid}-merged4.jpg")
            merge_v(merged4, merged3).save(f"./data/temp/img-{uid}-merged5.jpg")

            filesize = await aiofiles.os.path.getsize(f"./data/temp/img-{uid}-merged5.jpg")

            embed = discord.Embed(
                title=f"Here are your AI generated images!",
                description=f'Prompt: "{prompt}"',
                color=int(str(ctx.author.color)[1:], 16)
            )
            file = discord.File(f'./data/temp/img-{uid}-merged5.jpg', filename=f'ai-{uid}.jpg')
            embed.set_image(url=f'attachment://ai-{uid}.jpg')

            embed.timestamp = datetime.datetime.now()
            total_time = time.perf_counter() - start_time
            embed.set_footer(text=f'Requested by {ctx.author.name} ~ generated in {total_time:.1f}s ~ {(filesize/(1024*1024)):.2f}MB ~ Craiyon AI', icon_url=ctx.author.avatar.url)
            await ctx.followup.send(file=file, embed=embed)
            file.close()
            for i in range(1, 10):
                await aiofiles.os.remove(f'./data/temp/img-{uid}-{i}.jpg')
                try:
                    await aiofiles.os.remove(f'./data/temp/img-{uid}-merged{i}.jpg')
                except:
                    pass
        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            e = f"{e} (line {tb[-1].lineno})"
            try:
                await ctx.respond(f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')
            except:
                await ctx.send(f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')


def setup(bot):
    bot.add_cog(Imagegen(bot))
