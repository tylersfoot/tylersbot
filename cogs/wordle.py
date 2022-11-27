from discord.ext import commands
import discord
import random

cy = '\U0001F7E8'
cg = '\U0001F7E9'
cw = '\U0001F533'
cb = '\U00002B1B'
board = [['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw], ['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw],
         ['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw], ['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw],
         ['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw], ['--', '--', '--', '--', '--'], [cw, cw, cw, cw, cw]]


class Wordle(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wordlestart(self, ctx):
        global cw, cb, cy, cg, board
        b = board
        # await ctx.send("Wordle is starting... what is your guess? (wordle [guess])")
        await ctx.send("in progress lol")
        embed = discord.Embed(
            title="Wordle",
            description="",
            color=random.randint(0, 0xFFFFFF)
        )
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name=f'------------------',
            value=f'''{b[0][0]}{b[0][1]}{b[0][2]}{b[0][3]}{b[0][4]}
{b[1][0]}{b[1][1]}{b[1][2]}{b[1][3]}{b[1][4]}''',
            inline=False
        )
        embed.add_field(
            name=f'------------------',
            value=f'''{b[2][0]}{b[2][1]}{b[2][2]}{b[2][3]}{b[2][4]}
{b[3][0]}{b[3][1]}{b[3][2]}{b[3][3]}{b[3][4]}''',
            inline=False
        )
        embed.add_field(
            name=f'------------------',
            value=f'''{b[4][0]}{b[4][1]}{b[4][2]}{b[4][3]}{b[4][4]}
{b[5][0]}{b[5][1]}{b[5][2]}{b[5][3]}{b[5][4]}''',
            inline=False
        )
        embed.add_field(
            name=f'------------------',
            value=f'''{b[6][0]}{b[6][1]}{b[6][2]}{b[6][3]}{b[6][4]}
{b[7][0]}{b[7][1]}{b[7][2]}{b[7][3]}{b[7][4]}''',
            inline=False
        )
        embed.add_field(
            name=f'------------------',
            value=f'''{b[8][0]}{b[8][1]}{b[8][2]}{b[8][3]}{b[8][4]}
{b[9][0]}{b[9][1]}{b[9][2]}{b[9][3]}{b[9][4]}''',
            inline=False
        )
        embed.add_field(
            name=f'------------------',
            value=f'''{b[10][0]}{b[10][1]}{b[10][2]}{b[10][3]}{b[10][4]}
{b[11][0]}{b[11][1]}{b[11][2]}{b[11][3]}{b[11][4]}''',
            inline=False
        )
        # await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(Wordle(client))
