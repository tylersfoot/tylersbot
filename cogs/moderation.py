import asyncio
import discord
import json
import random
from asyncio import sleep
from discord.ext import commands
import datetime

snipe_message_author = {}
snipe_message_content = {}


class DurationConverter(commands.Converter):
    async def convert(self, ctx, argument):
        if argument in ['off', 'none', '0']:
            return 0, 's'
        amount = argument[:-1]
        unit = argument[-1]

        if amount.isdigit() and unit in ['s', 'm', 'h', 'd', 'w', 'y']:
            return int(amount), unit

        await ctx.send('Invalid duration.')


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(
            title=f"{message.author}\'s Message",
            description=f'{message.content}'
        )
        embed.timestamp = datetime.datetime.now()
        # posts in suggestions/reports channel
        channel = await self.bot.fetch_channel(1050002784671518790)
        await channel.send(embed=embed)
        # snipe_message_author[message.channel.id] = message.author
        # snipe_message_content[message.channel.id] = message.content
        # await sleep(60)
        # del snipe_message_author[message.channel.id]
        # del snipe_message_content[message.channel.id]

    # @commands.command()
    # async def snipe(self, ctx):
    #     channel = ctx.channel
    #     try:
    #         snipeEmbed = discord.Embed(title=f"Last deleted message in #{channel.name}",
    #                                    description=snipe_message_content[channel.id],
    #                                    color=random.randint(0, 0xFFFFFF))
    #         snipeEmbed.set_footer(text=f"Deleted by {snipe_message_author[channel.id]}")
    #         await ctx.send(embed=snipeEmbed)
    #     except:
    #         await ctx.send(f"There are no deleted messages in #{channel.name}")

    @commands.command(aliases=['clear'])
    async def purge(self, ctx, amount: int):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_messages:
            await ctx.channel.purge(limit=amount + 1)
            await ctx.send(f'Deleted {amount} messages')
        else:
            raise commands.MissingPermissions(['manage_messages'])

    @commands.command()
    async def kick(self, ctx, member: commands.MemberConverter, *, reason=None):
        if ctx.message.author.permissions_in(ctx.message.channel).kick_members:
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f'Kicked {member}')
        else:
            raise commands.MissingPermissions(['kick_members'])

    @commands.command()
    async def ban(self, ctx, member: commands.MemberConverter, *, reason=None):
        if ctx.message.author.permissions_in(ctx.message.channel).ban_members:
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f'Banned {member}')
        else:
            raise commands.MissingPermissions(['ban_members'])

    @commands.command()
    async def tempban(self, ctx, member: commands.MemberConverter, duration: DurationConverter, *, reason=None):

        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}
        amount, unit = duration

        if ctx.message.author.permissions_in(ctx.message.channel).ban_members:

            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f'Banned {member} for {amount}{unit}')
            await asyncio.sleep(amount * multiplier[unit])
            await ctx.guild.unban(member)

        else:
            raise commands.MissingPermissions(['ban_members'])

    @commands.command()
    async def unban(self, ctx, member: commands.MemberConverter, *, reason=None):
        if ctx.message.author.permissions_in(ctx.message.channel).ban_members:
            await ctx.guild.unban(member, reason=reason)
            await ctx.send(f'Unbanned {member}')
        else:
            raise commands.MissingPermissions(['ban_members'])

    @commands.command(aliases=['setprefix', 'prefixset', 'prefixchange'])
    async def changeprefix(self, ctx, prefix):
        if ctx.message.author.permissions_in(ctx.message.channel).manage_guild:
            with open('data/prefixes.json', 'r') as f:
                prefixes = json.load(f)
                f.close()

            prefixes[str(ctx.guild.id)] = prefix

            with open('data/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
                f.close()
            await ctx.send(f'Prefix changed to {prefix}')
            await ctx.guild.me.edit(nick=f'[{prefix}] tylersbot')
        else:
            raise commands.MissingPermissions(['manage_guild'])

    @commands.command()
    async def slowmode(self, ctx, duration: DurationConverter):
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}
        amount, unit = duration
        if ctx.message.author.permissions_in(ctx.message.channel).manage_guild:
            if amount*multiplier[unit] > 21600:
                await ctx.send('Slowmode cannot be more than 6 hours')
            else:
                await ctx.channel.edit(slowmode_delay=amount * multiplier[unit])
                await ctx.send(f'Slowmode set to {amount}{unit}')
        else:
            raise commands.MissingPermissions(['manage_guild'])


def setup(bot):
    bot.add_cog(Moderation(bot))
