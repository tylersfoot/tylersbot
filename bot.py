import datetime
from datetime import datetime
import discord
import json
import os
import time
from itertools import cycle
from discord.ext import commands, tasks
from dotenv import load_dotenv
import globalvariables as gv

startupTime = time.time()


def update_guild_count():
    gv.guilds = []
    for guild in bot.guilds:
        gv.guilds.append(guild.id)


def get_prefix(client, message):
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

# def get_prefix(arg1, message):
#     with open('data/prefixes.json', 'r') as f:
#         prefixes = json.load(f)
#     return prefixes.get(str(message.guild.id), "t.")


def get_servercount():
    with open('data/prefixes.json', 'r') as f:
        prefixes = json.load(f)
        f.close()
    return len(prefixes)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')


    class CustomHelpCommand(commands.HelpCommand):
        def __init__(self):
            super().__init__(command_attrs={
                'cooldown': commands.Cooldown(1, 3, commands.BucketType.member)
            })

        async def send_bot_help(self, mapping):
            for cog in mapping:
                await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in mapping[cog]]}')
            return await super().send_bot_help(mapping)

        async def send_cog_help(self, cog):
            await self.get_destination().send(f'{cog.qualified_name}: {[command.name for command in cog.get_commands()]}')

        async def send_group_help(self, group):
            await self.get_destination().send(f'{group.name}: {[command.name for index, command in enumerate(group.commands)]}')

        async def send_command_help(self, command):
            await self.get_destination().send(command.name)


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
        f"t.help | {get_servercount()} servers",
        "t.help | made by tylersfoot",
        "t.help | migrated to pycord"
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
        update_guild_count()
        reloads = ''
        print('Loading all cogs...')
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                if reloads == '':
                    reloads = file
                else:
                    reloads += ', ' + file
                try:
                    bot.load_extension(f'cogs.{file[:-3]}')
                except Exception as e:
                    print(f'Cog {file} could not load. Error: {e}')
                else:
                    pass
        print(f'Reloaded {reloads}')
        try:
            await bot.sync_commands()
            print(bot.commands)
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


    @tasks.loop(seconds=10)
    async def change_status():
        await bot.change_presence(activity=discord.Game(next(status)))


    @bot.command(aliases=['runtime'])
    async def uptime(ctx):
        global startupTime
        currentTime = time.time()
        difference = int(round(currentTime - startupTime))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text=f"{bot.user.name} | {bot.user.id}")
        await ctx.send(embed=embed)
        # except discord.HTTPException:
        #     await ctx.send("Current uptime: " + text)

    @bot.command()
    async def load(ctx, extension):
        if ctx.message.author.id == 460161554915000355:
            await bot.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension}.py')
        else:
            await ctx.send('Sorry, you are not tylersfoot.')

    @bot.command()
    async def unload(ctx, extension):
        if ctx.message.author.id == 460161554915000355:
            await bot.unload_extension(f'cogs.{extension}')
            await ctx.send(f'Unloaded {extension}.py')
        else:
            await ctx.send('Sorry, you are not tylersfoot.')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')


    @bot.slash_command(name="reload", description="Reloads cogs..",
                       guild_ids=gv.guilds, aliases=['refresh', 'update'])
    async def reload(ctx, extension: discord.Option(str)):
        reloads = ''
        if ctx.author.id == 460161554915000355:
            if extension == 'info':
                extension = 'information'
            if extension == 'mod':
                extension = 'moderation'
            if extension == 'chat':
                extension = 'chatbot'
            if extension == 'roles':
                extension = 'selfroles'
            if extension in ['cogs', 'extensions', 'all', 'a']:
                await ctx.respond('Reloading all cogs...')
                for file in os.listdir('./cogs'):
                    if file.endswith('.py'):
                        if reloads == '':
                            reloads = file
                        else:
                            reloads += ', ' + file
                        try:
                            bot.unload_extension(f'cogs.{file[:-3]}')
                        except Exception as e:
                            print(f'Cog {file} could not unload. Error: {e}')
                            pass
                        else:
                            pass
                        bot.load_extension(f'cogs.{file[:-3]}')
                await ctx.respond(f'Reloaded {reloads}')
                print(f'Reloaded {reloads}')
            else:
                try:
                    bot.unload_extension(f'cogs.{extension}')
                    bot.load_extension(f'cogs.{extension}')
                    await ctx.respond(f'Reloaded {extension}.py')
                    print(f'Reloaded {extension}.py')
                except Exception as e:
                    await ctx.respond(f'Error reloading {extension}.py')
                    print(f'Error reloading {extension}.py: {e}')
        else:
            await ctx.respond('Sorry, you are not tylersfoot.')


    @bot.command()
    async def prefix(ctx):
        print('f')
        await ctx.send(f'My prefix here is {get_prefix(bot, ctx.message)}')


    @bot.command()
    async def gc(ctx):
        await ctx.send(f'{gv.guilds}')

    @bot.command()
    async def sync(ctx):
        await bot.sync_commands()
        await ctx.send('done')


    # @bot.user_command(name="Account Creation Date", guild_ids=guilds)  # create a user command for the supplied guilds
    # async def account_creation_date(ctx, member: discord.Member):  # user commands return the member
    #     await ctx.respond(f"{member.name}'s account was created on {member.created_at}")


    @bot.slash_command(name="ping", description="Sends the bot's latency.", guild_ids=gv.guilds)
    async def ping(ctx):
        await ctx.respond(f'Pong! {round(bot.latency * 1000)}ms')


    @bot.slash_command(name="update_guilds", description="Updates the bot's guild count.", guild_ids=gv.guilds)
    async def update_guilds(ctx):
        update_guild_count()
        print(f'Updated with {len(gv.guilds)} guilds: {gv.guilds}')
        await ctx.respond(f'Updated {len(gv.guilds)} guilds: {gv.guilds}')


    @bot.event
    async def on_member_join(member):
        print(f'{member} has joined the server.')


    @bot.event
    async def on_member_remove(member):
        print(f'{member} has left the server.')


    bot.run(token)
