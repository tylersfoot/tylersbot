import datetime
import discord
import json
import os
import time
from itertools import cycle
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiofiles.os
import sys

startupTime = time.time()
# not really sure why this is here? im pretty sure this gets overwritten in update_guild_count()
guilds = [806659671129456640, 894275390959407134, 926920084860076082, 962179884627669062, 970926942511566851, 971048611184017448]
# people who can call dev commands
developers = [460161554915000355]


async def clear_temp():
    direct = './data/temp/'
    count = 0
    for f in await aiofiles.os.listdir(direct):
        await aiofiles.os.remove(os.path.join(direct, f))
        count += 1
    return count


def update_guild_count():
    global guilds
    guilds = []
    for guild in bot.guilds:
        guilds.append(guild.id)
    with open('data/globalvariables.json', 'w') as f:
        guildsjson = json.dumps(guilds)
        f.write(guildsjson)
        f.close()


def get_prefix(client, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def get_servercount():
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        f.close()
    return len(prefixes)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    activity = discord.Activity(
        type=discord.ActivityType.playing,
        name="Bot Started!"
    )

    bot = commands.Bot(
        command_prefix=get_prefix,
        help_command=commands.MinimalHelpCommand(),
        intents=discord.Intents.all(),
        activity=activity,
        status=discord.Status.online
    )
    status = cycle([
        f".help | {get_servercount()} servers",
        ".help | made by tylersfoot",
        ".help | another status",
        ".help | yippee"
    ])
    

    @bot.event
    async def on_ready():
        change_status.start()
        print(f'''
    #--------------------------#
    |  Logged in as {bot.user.name}  |
    |  id:{bot.user.id}   |
    #--------------------------#
    ''')

        update_guild_count() # update guild count
        await clear_temp() # clear temp folder
        cogs = ''
        print('Loading all cogs...')
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                if cogs == '':
                    cogs = file
                else:
                    cogs += ', ' + file
                try:
                    bot.load_extension(f'cogs.{file[:-3]}')
                except Exception as e:
                    print(f'Cog {file} could not load. Error: {e}')
                else:
                    pass
        print(f'Loaded {cogs}')
        try:
            await bot.sync_commands()
            # print(bot.commands)
            print(f'Synced commands')
        except Exception as e:
            print(f'Error syncing commands: {e}')


    @bot.event
    async def on_guild_join(guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            f.close()

        prefixes[str(guild.id)] = 't.'
        await guild.me.edit(nick=f'[t.] tylersbot')

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            f.close()


    @bot.event
    async def on_guild_remove(guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            f.close()

        prefixes.pop(str(guild.id))

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            f.close()

    # changes status every 10 seconds; change in `status` list
    @tasks.loop(seconds=10)
    async def change_status():
        await bot.change_presence(activity=discord.Game(next(status)))

    
    @bot.slash_command(name="uptime", description="Sends the bot's uptime since last restart.")
    async def uptime(ctx):
        global startupTime
        currentTime = time.time()
        difference = int(round(currentTime - startupTime))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(
            title=f"Tylersbot Uptime",
            description=text,
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)


    @bot.slash_command(name="unload", description="[DEV CMD] Unloads cogs.")
    async def unload(ctx, extension: str):
        cogs = ''
        if ctx.author.id in developers:
            if extension == 'info':
                extension = 'information'
            if extension == 'mod':
                extension = 'moderation'
            if extension == 'chat':
                extension = 'chatbot'
            if extension == 'roles':
                extension = 'selfroles'
            if extension == 'qr':
                extension = 'qrcode'
            if extension in ['cogs', 'extensions', 'all', 'a']:
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
                            print(f'Cog {file} could not unload. Error: {e}')
                            pass
                        else:
                            pass
                await ctx.respond(f'Unloaded {cogs}')
                print(f'Unloaded {cogs}')
            else:
                try:
                    bot.unload_extension(f'cogs.{extension}')
                    await ctx.respond(f'Unloaded {extension}.py')
                    print(f'Unloaded {extension}.py')
                except Exception as e:
                    await ctx.respond(f'Error unloading {extension}.py: {e}')
                    print(f'Error unloading {extension}.py: {e}')
        else:
            await ctx.respond('You must be a developer to use this command.')


    @bot.slash_command(name="reload", description="[DEV CMD] Loads/reloads cogs.")
    async def reload(ctx, extension: str):
        await ctx.response.defer(ephemeral=False)
        cogs = ''
        if ctx.author.id in developers:
            if extension == 'info':
                extension = 'information'
            if extension == 'mod':
                extension = 'moderation'
            if extension == 'chat':
                extension = 'chatbot'
            if extension == 'roles':
                extension = 'selfroles'
            if extension in ['cogs', 'extensions', 'all', 'a']:
                for file in os.listdir('./cogs'):
                    if file.endswith('.py'):
                        if cogs == '':
                            cogs = file
                        else:
                            cogs += ', ' + file
                        try:
                            bot.unload_extension(f'cogs.{file[:-3]}')
                        except Exception as e:
                            print(f'Cog {file} could not unload. Error: {e}')
                            pass
                        else:
                            pass
                        bot.load_extension(f'cogs.{file[:-3]}')
                await ctx.respond(f'Reloaded {cogs}')
                print(f'Reloaded {cogs}')
            else:
                try:
                    try:
                        bot.unload_extension(f'cogs.{extension}')
                    except Exception as e:
                        print(f'Cog {extension} could not unload. Error: {e}')
                        pass
                    else:
                        pass
                    bot.load_extension(f'cogs.{extension}')
                    await ctx.respond(f'Reloaded {extension}.py')
                    print(f'Reloaded {extension}.py')
                except Exception as e:
                    await ctx.respond(f'Error reloading {extension}.py: {e}')
                    print(f'Error reloading {extension}.py: {e}')
        else:
            await ctx.respond('You must be a developer to use this command.')


    @bot.command()
    async def prefix(ctx):
        print('f')
        await ctx.send(f'My prefix here is {get_prefix(bot, ctx.message)}')


    @bot.slash_command(name="sync", description="[DEV CMD] Syncs slash commands.")
    async def sync(ctx):
        if ctx.author.id in developers:
            await ctx.response.defer(ephemeral=True)
            await bot.sync_commands()
            await ctx.followup.send('Synced commands.')
        else:
            await ctx.respond('You must be a developer to use this command.')


    @bot.slash_command(name="stopbot", description="[DEV CMD] Stops/terminates the bot.")
    async def stopbot(ctx):
        if ctx.author.id in developers:
            await ctx.respond('Stopping bot...')
            await bot.close()
            sys.exit()
        else:
            await ctx.respond('You must be a developer to use this command.')


    @bot.slash_command(name="clear_temp", description="[DEV CMD] Clears temp folder.")
    async def cleartemp(ctx):
        if ctx.author.id in developers:
            await ctx.response.defer(ephemeral=True)
            count = await clear_temp()
            await ctx.followup.send(f'Cleared {count} files from the temp folder.')
        else:
            await ctx.respond('You must be a developer to use this command.')


    @bot.slash_command(name="ping", description="Sends the bot's latency/ping.")
    async def ping(ctx):
        await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')


    @bot.slash_command(name="update_guilds", description="Updates the bot's guild count.")
    async def update_guilds(ctx):
        update_guild_count()
        print(f'Updated with {len(guilds)} guilds: {guilds}')
        await ctx.respond(f'Updated {len(guilds)} guilds: {guilds}')


    @bot.event
    async def on_member_join(member):
        print(f'{member} has joined the server.')


    @bot.event
    async def on_member_remove(member):
        print(f'{member} has left the server.')


    bot.run(token)
