import discord
from discord.ext import commands
import datetime


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    info_group = discord.SlashCommandGroup(
        name = "info", 
        description = "Informational commands",
        integration_types = {discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )


    @info_group.command(name="suggestion", description="Sends a suggestion to the developers.")
    async def info_suggestion(self, ctx, text: str):
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


    @info_group.command(name="bugreport", description="Sends a bug report to the developers. Add as much information as possible!")
    async def info_bugreport(self, ctx, text: str):
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


    @info_group.command(name="guild_count", description="Gets the bot's guild count.")
    async def info_guildcount(self, ctx):
        guildcount = len(self.bot.guilds)
        if guildcount == 1:
            await ctx.respond(f'I am in 1 guild!')
        else:
            await ctx.respond(f'I am in {guildcount} guilds!')


    @info_group.command(name="invite", description="Sends invite links related to the bot.")
    async def info_invite(self, ctx):
        await ctx.respond(f'''Guild Invite: https://discord.gg/DKpCvsJ4fp
Bot Invite: https://discord.com/oauth2/authorize?client_id={self.bot.user.id}
GitHub Link: https://github.com/tylersfoot/tylersbot''')


    @info_group.command(name="avatar", description="Grabs the avatar of the specified user.",
                            integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def info_avatar(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}\'s Avatar",
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_image(url=f"{member.avatar.url}")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)
        
        
    @commands.user_command(name="Avatar", description="Grabs the avatar of the specified user.",
                           integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def info_avatar_user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(
            title=f"{member.name}\'s Avatar",
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_image(url=f"{member.avatar.url}")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)


    @info_group.command(name="guild_info", description="Sends information about the current guild.")
    async def info_guildinfo(self, ctx):
        fa = False
        if ctx.guild.mfa_level == 1:
            fa = True
        embed = discord.Embed(
            title="Guild information",
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
            value=f'<t:{int(ctx.guild.created_at.timestamp())}:D>',
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
        
                
    @info_group.command(name="account_creation_date", description="Returns when an account was created.")
    async def info_account_creation_date(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            
        timestamp = int(member.created_at.timestamp())
        await ctx.respond(f"{member.name}'s account was created on <t:{timestamp}:D>.")
    
    
    @commands.user_command(name="Account Creation Date", description="Returns when an account was created.",
                           integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    async def info_account_creation_date_user(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
            
        timestamp = int(member.created_at.timestamp())
        await ctx.respond(f"{member.name}'s account was created on <t:{timestamp}:D>.")


def setup(bot):
    bot.add_cog(Information(bot))
