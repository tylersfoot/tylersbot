import datetime
import discord
import os
import time
from itertools import cycle
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiofiles.os
import sys
from customexceptions import NotDeveloperError
from database import db_initialize
from logger import *
from config import *

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

startupTime = time.time()


async def clear_temp():
    direct = './data/temp/'
    count = 0
    os.makedirs(direct, exist_ok=True)
    for f in await aiofiles.os.listdir(direct):
        await aiofiles.os.remove(os.path.join(direct, f))
        count += 1
    return count

def coglookup(name: str):
    # cog shortcuts
    if name in ['cogs', 'extensions', 'all', 'a']:
        name = 'all'
    if name in ['info']:
        name = 'information'
    if name in ['mod']:
        name = 'moderation'
    if name in ['chat']:
        name = 'chatbot'
    if name in ['roles', 'role']:
        name = 'selfroles'
    if name in ['qr']:
        name = 'qrcode'
    if name in ['calc', 'calculate']:
        name = 'calculator'
    if name in ['error', 'errors', 'errorhandler', 'custom_error_handler']:
        name = 'commanderrorhandler'
    return name


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    # startup activity
    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="Bot Started!",
        test_guild_ids = DEVELOPER_GUILD_ID
    )

    # define bot object
    bot = commands.Bot(
        help_command=commands.MinimalHelpCommand(),
        intents=discord.Intents.all(),
        activity=activity,
        status=discord.Status.online
    )
    
    
    # on startup
    @bot.event
    async def on_ready():
        change_status.start()
        print(f'''
    #--------------------------#
    |  Logged in as {bot.user.name}
    |  id:{bot.user.id} 
    #--------------------------#
    ''')
        
        logger_initialize(bot)
        db_initialize()
        
        await clear_temp() # clear temp folder
        cogs = ''
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                if cogs == '':
                    cogs = file
                else:
                    cogs += ', ' + file
                try:
                    bot.load_extension(f'cogs.{file[:-3]}')
                except Exception as e:
                    log_error(f'Cog {file} could not load. Error: {e}')
                else:
                    pass
        log_info(f'Loaded {cogs}')
        
        await bot.sync_commands()


    status_cycle = cycle([
        "over {guild_count} servers",
        "over {user_count} users",
        "discord.gg/DKpCvsJ4fp",
        "tylersfoot.dev"
    ])

    @tasks.loop(seconds=15)
    async def change_status():
        guild_count = len(bot.guilds)
        user_count = sum(guild.member_count for guild in bot.guilds)

        next_status = next(status_cycle).format(guild_count=guild_count, user_count=user_count)

        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=next_status))
        
    bot_group = bot.create_group(
        name = "bot", 
        description = "Bot related commands",
        integration_types = {discord.IntegrationType.guild_install}
    )
    
    # dev commands (should only be SEEN by developers - aka ADMINS in DEV SERVER)
    dev_group = bot.create_group(
        name = 'dev',
        description = 'Developer commands',
        guild_ids = [DEVELOPER_GUILD_ID],
        default_member_permissions = discord.Permissions(permissions = 0, administrator = True)
    )
        
        
    @bot_group.command(name="uptime", description="Sends the bot's uptime since last restart.")
    async def bot_uptime(ctx):
        global startupTime
        currentTime = time.time()
        difference = int(round(currentTime - startupTime))

        hours, remainder = divmod(difference, 3600)
        minutes, seconds = divmod(remainder, 60)
        if hours > 0:
            text = f"{hours} Hours, {minutes} Minutes, {seconds} Seconds"
        elif minutes > 0:
            text = f"{minutes} Minutes, {seconds} Seconds"
        else:
            text = f"{seconds} Seconds"

        embed = discord.Embed(
            title="tylersbot Uptime",
            description=text,
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)


    @bot_group.command(name="ping", description="Sends the bot's latency/ping.")
    async def bot_ping(ctx):
        await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')


    @dev_group.command(name="unload", description="Unloads cogs.")
    async def bot_unload(ctx, extension: str):
        if ctx.author.id not in DEVELOPER_USER_IDS:
            raise NotDeveloperError
        
        await ctx.response.defer(ephemeral=True)
        extension = coglookup(extension)
        
        if extension == 'all':
            cogs = ''
            await ctx.respond('Unloading all cogs...')
            for file in os.listdir('./cogs'):
                if file.endswith('.py'):
                    if cogs == '':
                        cogs = file
                    else:
                        cogs += ', ' + file
                    try:
                        bot.unload_extension(f'cogs.{file[:-3]}')
                    except Exception as e:
                        log_error(f'Cog {file} could not unload. Error: {e}')
                        pass
                    else:
                        pass
            await ctx.respond(f'Unloaded cogs `{cogs}`', ephemeral=True)
            log_info(f'Unloaded cogs {cogs}')
        else:
            try:
                bot.unload_extension(f'cogs.{extension}')
                await ctx.respond(f'Unloaded cog `{extension}.py`', ephemeral=True)
                log_info(f'Unloaded cog {extension}.py')
            except Exception as e:
                await ctx.respond(f'Error unloading cog `{extension}.py`: {e}')
                log_error(f'Error unloading cog {extension}.py: {e}')


    @dev_group.command(name="reload", description="Loads/reloads cogs.", guild_ids=[962179884627669062])
    async def bot_reload(ctx, extension: str):
        if ctx.author.id not in DEVELOPER_USER_IDS:
            raise NotDeveloperError
        
        await ctx.response.defer(ephemeral=True)
        extension = coglookup(extension)
        
        if extension == 'all':
            cogs = ''
            for file in os.listdir('./cogs'):
                if file.endswith('.py'):
                    if cogs == '':
                        cogs = file
                    else:
                        cogs += ', ' + file
                    try:
                        bot.unload_extension(f'cogs.{file[:-3]}')
                    except Exception as e:
                        log_error(f'Cog {file} could not unload. Error: {e}')
                        pass
                    else:
                        pass
                    bot.load_extension(f'cogs.{file[:-3]}')
            await ctx.respond(f'Reloaded cogs `{cogs}`', ephemeral=True)
            log_info(f'Reloaded cogs {cogs}')
        else:
            try:
                try:
                    bot.unload_extension(f'cogs.{extension}')
                except Exception as e:
                    log_error(f'Cog {extension} could not unload. Error: {e}')
                    pass
                else:
                    pass
                bot.load_extension(f'cogs.{extension}')
                await ctx.respond(f'Reloaded cog `{extension}.py`', ephemeral=True)
                log_info(f'Reloaded cog {extension}.py')
            except Exception as e:
                await ctx.respond(f'Error reloading cog `{extension}.py`: {e}', ephemeral=True)
                log_error(f'Error reloading cog {extension}.py: {e}')


    @dev_group.command(name="sync", description="Syncs slash commands.")
    async def bot_sync(ctx):
        if ctx.author.id not in DEVELOPER_USER_IDS:
            raise NotDeveloperError
        
        await ctx.response.defer(ephemeral=True)
        await bot.sync_commands()
        log_info('Synced commands')
        await ctx.followup.send('Synced commands', ephemeral=True)


    @dev_group.command(name="stop", description="Stops/terminates the bot.")
    async def bot_stop(ctx):
        if ctx.author.id not in DEVELOPER_USER_IDS:
            raise NotDeveloperError

        await ctx.respond('Stopping bot!', ephemeral=True)
        await bot.close()
        sys.exit()


    @dev_group.command(name="clear_temp", description="Clears temp folder.")
    async def bot_cleartemp(ctx):
        if ctx.author.id not in DEVELOPER_USER_IDS:
            raise NotDeveloperError
        
        await ctx.response.defer(ephemeral=True)
        count = await clear_temp()
        await ctx.followup.send(f'Cleared {count} files from the temp folder.', ephemeral=True)


    @bot.event
    async def on_member_join(member):
        log_info(f"{member} has joined the guild '{member.guild.name}' [{member.guild.id}]")


    @bot.event
    async def on_member_remove(member):
        log_info(f"{member} has left the guild '{member.guild.name}' [{member.guild.id}]")


    bot.run(token)
