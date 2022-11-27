import discord
from discord.ext import commands
from bot import get_servercount
import datetime
import random
import time

start_time = time.time()


class Information(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def servercount(self, ctx):
        await ctx.send(f'I am in {get_servercount()} servers! (Count refreshes every time bot is restarted)')

    @commands.command(aliases=['invlink', 'invite', 'botinvite', 'botinv'])
    async def invitelink(self, ctx):
        await ctx.send(f'''Bot invite link: https://discordapp.com/oauth2/authorize?client_id={self.client.user.id}&scope=bot&permissions=8
        Bot server invite link: https://discord.gg/DKpCvsJ4fp''')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        icon_url = member.avatar_url
        avatarEmbed = discord.Embed(title=f"{member.name}\'s Avatar", color=random.randint(0, 0xFFFFFF))
        avatarEmbed.set_image(url=f"{icon_url}")
        avatarEmbed.timestamp = ctx.message.created_at
        await ctx.send(embed=avatarEmbed)

    @commands.command()
    async def serverinfo(self, ctx):
        fa = False
        if ctx.guild.mfa_level == 1:
            fa = True
        embed = discord.Embed(
            title="Server information",
            description=f'{ctx.guild} ({ctx.guild.id})'
                        f'\nDescription: {ctx.guild.description}',
            color=random.randint(0, 0xFFFFFF)
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        embed.timestamp = ctx.message.created_at
        embed.add_field(
            name="Verification",
            value=f'Level: {ctx.guild.verification_level}'
                  f'\nRequires 2FA: {fa}',
            inline=True
        )
        embed.add_field(
            name="Owner",
            value=f'{ctx.guild.owner}'
                  f'\nID: {ctx.guild.owner.id}',
            inline=True
        )
        embed.add_field(
            name="Created on",
            value=f'{ctx.guild.created_at.__format__("%d %b %Y")}',
            inline=True
        )
        embed.add_field(
            name="Boosts",
            value=f'Tier {ctx.guild.premium_tier} with {ctx.guild.premium_subscription_count} boosts'
                  f'\nbruh boosters',
            inline=True
        )
        embed.add_field(
            name="Members",
            value=f'Online: {sum(member.status != discord.Status.offline and not member.bot for member in ctx.guild.members)}/{sum(not member.bot for member in ctx.guild.members)}'
                  f'\nBots: {sum(member.bot and member.status != discord.Status.offline for member in ctx.guild.members)}/{sum(member.bot for member in ctx.guild.members)}',
            inline=True
        )
        embed.add_field(
            name="Roles",
            value=f'Roles: {len(ctx.guild.roles)}'
                  f'\nHighest role: {ctx.guild.roles[-1].mention}',
            inline=True
        )
        await ctx.send(embed=embed)


'''
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content == 'Hello' or message.content == 'hello':
            await message.channel.send('Hi!')

        if message.content == 'react' or message.content == 'React':
            await message.add_reaction('\U0001F9D0')

        if message.content == '.help':
            await message.channel.send(
                f'Stuff you can do:\n'
                f'- Say \'hello\'\n'
                f'- Say \'react\'\n'
                f'- Edit a message'
                f'- React to a message'
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await before.channel.send(
            f'{before.author} edited a message.\n'
            f'Before: {before.content}\n'
            f'After: {after.content}'
        )
        
    @commands.command()
    async def eastereggs(self, ctx):
        await ctx.send('say fnf, play weezer')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(
            f'{user} reacted with {reaction.emoji}.'
        )
'''


async def setup(client):
    await client.add_cog(Information(client))
