import discord
from discord.ext import commands
from bot import get_servercount
import datetime
import random
import time
from bot import guilds

start_time = time.time()


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="suggestion", description="Sends a suggestion to the developers.")
    async def suggestion(self, ctx, text):
        embed = discord.Embed(
            title=f"{ctx.author}\'s Suggestion",
            description=f'{text}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.timestamp = datetime.datetime.now()
        # posts in suggestions/reports channel
        channel = await self.bot.fetch_channel(1049496433100853350)
        await ctx.respond('Suggestion sent!')
        await channel.send(embed=embed)

    @commands.slash_command(name="bugreport", description="Sends a bug report to the developers. Add as much information as possible!")
    async def bugreport(self, ctx, text):
        embed = discord.Embed(
            title=f"{ctx.author}\'s Bug Report",
            description=f'{text}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.timestamp = datetime.datetime.now()
        # posts in suggestions/reports channel
        channel = await self.bot.fetch_channel(1049496433100853350)
        await ctx.respond('Report sent!')
        await channel.send(embed=embed)

    @commands.user_command(name="Account Creation Date")  # create a user command for the supplied guilds
    async def account_creation_date(self, ctx, member: discord.Member):  # user commands return the member
        await ctx.respond(f'{member.name}\'s account was created on {member.created_at.strftime("%B %d, %Y")}')

    @commands.slash_command(name="server_count", description="Gets the bot's server count.")
    async def servercount(self, ctx):
        await ctx.respond(f'I am in {get_servercount()} servers! (Count refreshes every time bot is restarted)')

    @commands.slash_command(name="invite_link", description="Sends the invite link for the tylersbot server.")
    async def invitelink(self, ctx):
        await ctx.respond(f'''tylersbot invite link: https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}scope=applications.commands%20bot&permissions=8
        tylersbot development server invite link: https://discord.gg/DKpCvsJ4fp''')

    @commands.slash_command(name="avatar", description="Sends the avatar of the specified user.")
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}\'s Avatar",
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_image(url=f"{member.avatar.url}")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

    @commands.slash_command(name="server_info", description="Sends information about the current server.")
    async def serverinfo(self, ctx):
        fa = False
        if ctx.guild.mfa_level == 1:
            fa = True
        embed = discord.Embed(
            title="Server information",
            description=f'{ctx.guild} ({ctx.guild.id})\nDescription: {ctx.guild.description}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.timestamp = datetime.datetime.now()
        embed.add_field(
            name="Verification",
            value=f'Level: {ctx.guild.verification_level}\nRequires 2FA: {fa}',
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
            value=f'Roles: {len(ctx.guild.roles)}\nHighest role: {ctx.guild.roles[-1].mention}',
            inline=True
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
