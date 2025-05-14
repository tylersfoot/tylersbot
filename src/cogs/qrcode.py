import discord
from discord.ext import commands
import random
import pyqrcode
import os
import datetime
from pathlib import Path
from core.logger import log_error
from core.paths import TEMP_PATH


class Qrcode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="qr",
        description="Generates a qr code from the given text/link.",
        integration_types={
            discord.IntegrationType.guild_install,
            discord.IntegrationType.user_install,
        },
    )
    async def qr(self, ctx, *, message: str):
        def grab_box(input, rows, columns, x, y):
            # grabs an x by y box of characters
            return ["".join(input[x + i][y : y + columns]) for i in range(rows)]

        def check(input):
            # checks for the amongus
            rows = len(input)
            cols = len(input[0])
            for i in range(rows - 5 + 1):
                for j in range(cols - 4 + 1):
                    if grab_box(input, 5, 4, i, j) == [
                        "0111",
                        "1100",
                        "1111",
                        "0111",
                        "0101",
                    ]:
                        return True, j, i
            return False, 0, 0

        await ctx.response.defer()
        # temporary file path
        temp_dir = Path(TEMP_PATH)
        temp_dir.mkdir(parents=True, exist_ok=True)
        uid = str(random.randint(1, 1000000000000))
        file_path = temp_dir / f"qr-{uid}.png"

        try:
            code = pyqrcode.create(message)
        except ValueError:
            await ctx.respond(
                "The text is too large to be converted into a QR code.", ephemeral=True
            )
            return

        # generate QR code
        code.png(file_path, scale=5)
        qrtext = [list(line) for line in code.text().splitlines()]
        among_us_detected, x, y = check(qrtext)

        embed = discord.Embed(
            title="Here is your processed QR code!",
            description=f"**<a:siren:1332271399557140542> AMONG US FOUND IN QR CODE AT ({x}, {y})** <a:siren:1332271399557140542>\n\nConverted text: {message}"
            if among_us_detected
            else f"Converted text: {message}",
            color=int(str(ctx.author.color)[1:], 16),
        )
        embed.set_image(url=f"attachment://qr-{uid}.png")
        embed.set_footer(
            text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url
        )
        embed.timestamp = datetime.datetime.now()

        file = discord.File(file_path, filename=f"qr-{uid}.png")
        await ctx.respond(file=file, embed=embed)

        try:
            os.remove(file_path)
        except OSError as e:
            log_error(f"Error removing temporary file: {e}")


def setup(bot):
    bot.add_cog(Qrcode(bot))
