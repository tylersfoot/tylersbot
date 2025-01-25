import discord
from discord.ext import commands
import datetime


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    mod_group = discord.SlashCommandGroup(
        name = "mod", 
        description = "Moderation commands",
        integration_types = {discord.IntegrationType.guild_install}
    )

        
    @mod_group.command(name="purge", description="Purges messages from the channel.")
    async def mod_purge(self, ctx, amount: int):
        if not ctx.author.guild_permissions.manage_messages:
            raise commands.MissingPermissions(['manage_messages'])
        
        amount = min(amount, 50)  # limit to 50 messages for safety
        await ctx.channel.purge(limit=amount)
        await ctx.respond( f'Deleted {amount} messages.')
        
        
    @mod_group.command(name="kick", description="Kicks a user from the server.")
    async def mod_kick(self, ctx, member: discord.Member, reason: str = None, notify: bool = True):
        if not ctx.author.guild_permissions.kick_members:
            raise commands.MissingPermissions(['kick_members'])

        if reason is None:
            reason = "No reason provided."
        dmsent = True
        
        if notify:
            # DM embed
            embed = discord.Embed(
                title=f"You were kicked from: **{ctx.guild.name}**",
                description=f"**Reason:** {reason}.",
                color=discord.Color.red()
            )
            embed.timestamp = datetime.datetime.now()

            # attempt to DM the user
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                dmsent = False

        await ctx.guild.kick(member, reason=reason)
        if dmsent:
            await ctx.respond(f"Kicked {member.mention} from the server.")
        else:
            await ctx.respond(f"Kicked {member.mention} from the server, but could not send a DM to notify them.")
        
        
    @mod_group.command(name="ban", description="Bans a user from the server.")
    async def mod_ban(self, ctx, member: discord.Member, reason: str = None, notify: bool = True):
        if not ctx.author.guild_permissions.ban_members:
            raise commands.MissingPermissions(['ban_members'])

        if reason is None:
            reason = "No reason provided."
        dmsent = True
        
        if notify:
            # DM embed
            embed = discord.Embed(
                title=f"You were banned from: **{ctx.guild.name}**",
                description=f"**Reason:** {reason}.",
                color=discord.Color.red()
            )
            embed.timestamp = datetime.datetime.now()

            # attempt to DM the user
            try:
                await member.send(embed=embed)
            except discord.Forbidden:
                dmsent = False

        await ctx.guild.ban(member, reason=reason)
        if dmsent:
            await ctx.respond(f"Banned {member.mention} from the server.")
        else:
            await ctx.respond(f"Banned {member.mention} from the server, but could not send a DM to notify them.")    
            
            
    @mod_group.command(name="unban", description="Unbans a user from the server.")
    async def mod_unban(self, ctx, user_id: str, reason: str = None, notify: bool = True):
        if not ctx.author.guild_permissions.ban_members:
            raise commands.MissingPermissions(['ban_members'])
        try:
            user = await self.bot.fetch_user(user_id)
        except:
            await ctx.respond("User not found.", ephemeral=True)
            return
        
        if reason is None:
            reason = "No reason provided."
        dmsent = True

        if notify:
            embed = discord.Embed(
                title=f"You were unbanned from: **{ctx.guild.name}**",
                description=f"**Reason:** {reason}.",
                color=discord.Color.green()
            )
            embed.timestamp = datetime.datetime.now()

            try:
                await user.send(embed=embed)
            except discord.Forbidden:
                dmsent = False

        await ctx.guild.unban(user, reason=reason)
        if dmsent:
            await ctx.respond(f"Unbanned {user.mention} from the server.")
        else:
            await ctx.respond(f"Unbanned {user.mention} from the server, but could not send a DM to notify them.")
        

            
    @mod_group.command(name="slowmode", description="Sets the slowmode for the channel.")
    async def mod_slowmode(self, ctx, duration: str):
        if not ctx.author.guild_permissions.manage_guild:
            raise commands.MissingPermissions(['manage_guild'])

        # parse the duration string
        multiplier = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'y': 31536000}
        if duration.lower() in ['off', 'none', '0']:
            await ctx.channel.edit(slowmode_delay=0)
            await ctx.respond("Slowmode disabled.", ephemeral=True)
            return

        try:
            amount = int(duration[:-1])
            unit = duration[-1].lower()
            if unit not in multiplier:
                raise ValueError

            total_seconds = amount * multiplier[unit]
            if total_seconds > 21600:  # 6-hour limit
                await ctx.respond("Slowmode cannot be more than 6 hours.", ephemeral=True)
                return
            if total_seconds < 0:
                await ctx.respond("Slowmode cannot be negative.", ephemeral=True)

            await ctx.channel.edit(slowmode_delay=total_seconds)
            await ctx.respond(f"Slowmode set to {amount}{unit}.")
        except (ValueError, IndexError):
            await ctx.respond("Invalid duration format. Use a number followed by a unit (`10s`, `5m`, `1h`).", ephemeral=True)    
            
            
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        description = message.content or "Message had no content."

        embed = discord.Embed(
            title=f"{message.author}\'s Message",
            description=description
        )
        embed.timestamp = datetime.datetime.now()
        
        channel = await self.bot.fetch_channel(1050002784671518790)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
