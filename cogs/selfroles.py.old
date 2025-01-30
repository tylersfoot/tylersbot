import discord
from discord.ext import commands


class Selfroles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_message_id = 962196125937463298

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # Gives role based on reaction
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)

        if payload.emoji.name == '🗿':
            role = discord.utils.get(guild.roles, name='stone')
            await payload.member.add_roles(role)
        elif payload.emoji.name == '💰':
            role = discord.utils.get(guild.roles, name='money')
            await payload.member.add_roles(role)
        elif payload.emoji.name == '🔥':
            role = discord.utils.get(guild.roles, name='fire')
            await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        # Removes role based on reaction
        if payload.message_id != self.role_message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if payload.emoji.name == '🗿':
            role = discord.utils.get(guild.roles, name='stone')
            await member.remove_roles(role)
        elif payload.emoji.name == '💰':
            role = discord.utils.get(guild.roles, name='money')
            await member.remove_roles(role)
        elif payload.emoji.name == '🔥':
            role = discord.utils.get(guild.roles, name='fire')
            await member.remove_roles(role)


async def setup(bot):
    await bot.add_cog(Selfroles(bot))
