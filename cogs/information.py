import discord
from discord.ext import commands
import datetime


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    @commands.slash_command(name="suggestion", description="Sends a suggestion to the developers.")
    async def suggestion(self, ctx, text: str):
        embed = discord.Embed(
            title=f"{ctx.author}\'s Suggestion",
            description=f'{text}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.timestamp = datetime.datetime.now()
        # posts in suggestions/reports channel
        channel = await self.bot.fetch_channel(1049496433100853350)
        await ctx.respond('Suggestion sent!', ephemeral=True)
        await channel.send(embed=embed)


    @commands.slash_command(name="bugreport", description="Sends a bug report to the developers. Add as much information as possible!")
    async def bugreport(self, ctx, text: str):
        embed = discord.Embed(
            title=f"{ctx.author}\'s Bug Report",
            description=f'{text}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.timestamp = datetime.datetime.now()
        # posts in suggestions/reports channel
        channel = await self.bot.fetch_channel(1049496433100853350)
        await ctx.respond('Report sent!', ephemeral=True)
        await channel.send(embed=embed)


    @commands.slash_command(name="server_count", description="Gets the bot's server count.")
    async def servercount(self, ctx):
        servercount = len(self.bot.guilds)
        if servercount == 1:
            await ctx.respond(f'I am in 1 server!')
        else:
            await ctx.respond(f'I am in {servercount} servers!')


    @commands.slash_command(name="invite_link", description="Sends the invite link for the development server.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def invitelink(self, ctx):
        await ctx.respond(f'''tylersfoot development server invite: https://discord.gg/DKpCvsJ4fp''')


    @commands.slash_command(name="avatar", description="Grabs the avatar of the specified user.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
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
        
        
    @commands.user_command(name="Avatar", description="Grabs the avatar of the specified user.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def avatar_user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}\'s Avatar",
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_image(url=f"{member.avatar.url}")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)


    @commands.slash_command(name="server_info", description="Sends information about the current server.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
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
            value=f'Tier {ctx.guild.premium_tier} with {ctx.guild.premium_subscription_count} boosts',
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
        
                
    @commands.slash_command(name="account_creation_date", description="Returns when an account was created.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def account_creation_date(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        creation_date = member.created_at.strftime("%B %d, %Y")
        await ctx.respond(f"{member.name}'s account was created on {creation_date}.")
    
    
    @commands.user_command(name="Account Creation Date", description="Returns when an account was created.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def account_creation_date_user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        creation_date = member.created_at.strftime("%B %d, %Y")
        await ctx.respond(f"{member.name}'s account was created on {creation_date}.")


def setup(bot):
    bot.add_cog(Information(bot))
