import discord
from discord.ext import commands
from bot import get_servercount
import datetime
import random
import time

for guild in bot.guilds:
    guilds.append(guild.id)

start_time = time.time()


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.user_command(name="Account Creation Date", guild_ids=guilds)  # create a user command for the supplied guilds
    async def account_creation_date(self, ctx, member: discord.Member):  # user commands return the member
        await ctx.respond(f"{member.name}'s account was created on {member.created_at}")

    @commands.command()
    async def servercount(self, ctx):
        await ctx.send(f'I am in {get_servercount()} servers! (Count refreshes every time bot is restarted)')

    @commands.command(aliases=['invlink', 'invite', 'botinvite', 'botinv'])
    async def invitelink(self, ctx):
        await ctx.send(f'''Bot invite link: https://discordapp.com/oauth2/authorize?bot_id={self.bot.user.id}&scope=bot&permissions=8
        Bot server invite link: https://discord.gg/DKpCvsJ4fp''')

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        icon_url = member.avatar.url
        avatarEmbed = discord.Embed(
            title=f"{member.name}\'s Avatar",
            color=int(str(ctx.author.color)[1:], 16)
        )
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
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
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
        if message.author == self.bot.user:
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


def setup(bot):
    bot.add_cog(Information(bot))
