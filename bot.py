import datetime
from datetime import datetime, timedelta
import discord
import json
import os
from os import listdir, system
import time
from itertools import cycle
import asyncio
from discord.ext import commands, tasks
from dotenv import load_dotenv
import aiohttp
from pretty_help import PrettyHelp

startupTime = time.time()


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

    client = commands.Bot(
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


    @client.event
    async def on_ready():
        change_status.start()
        print(f'''
    ------
    Logged in as
    {client.user.name}
    id:{client.user.id}
    ------
    ''')


    @client.event
    async def on_guild_join(guild):
        with open('data/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            f.close()

        prefixes[str(guild.id)] = 't.'
        await guild.me.edit(nick=f'[t.] tylersbot')

        with open('data/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            f.close()


    @client.event
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
        await client.change_presence(activity=discord.Game(next(status)))


    @client.command(aliases=['runtime'])
    async def uptime(ctx):
        global startupTime
        currentTime = time.time()
        difference = int(round(currentTime - startupTime))
        text = str(datetime.timedelta(seconds=difference))
        embed = discord.Embed(colour=0xc8dc6c)
        embed.add_field(name="Uptime", value=text)
        embed.set_footer(text=f"{client.user.name} | {client.user.id}")
        await ctx.send(embed=embed)
        # except discord.HTTPException:
        #     await ctx.send("Current uptime: " + text)

    @client.command()
    async def load(ctx, extension):
        if ctx.message.author.id == 460161554915000355:
            await client.load_extension(f'cogs.{extension}')
            await ctx.send(f'Loaded {extension}.py')
        else:
            await ctx.send('Sorry, you are not tylersfoot.')

    @client.command()
    async def unload(ctx, extension):
        if ctx.message.author.id == 460161554915000355:
            await client.unload_extension(f'cogs.{extension}')
            await ctx.send(f'Unloaded {extension}.py')
        else:
            await ctx.send('Sorry, you are not tylersfoot.')
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await client.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded {filename}')

    @client.command(aliases=['refresh', 'update'])
    async def reload(ctx, extension):
        global reloads
        reloads = ''
        if ctx.message.author.id == 460161554915000355:
            if extension == 'info':
                extension = 'information'
            if extension == 'mod':
                extension = 'moderation'
            if extension == 'chat':
                extension = 'chatbot'
            if extension == 'roles':
                extension = 'selfroles'
            if extension in ['cogs', 'extensions', 'all']:
                await ctx.send('Reloading all cogs...')
                for file in os.listdir('./cogs'):
                    if file.endswith('.py'):
                        if reloads == '':
                            reloads = file
                        else:
                            reloads += ', ' + file
                        try:
                            await client.unload_extension(f'cogs.{file[:-3]}')
                        except commands.ExtensionNotLoaded:
                            pass
                        else:
                            pass
                        await client.load_extension(f'cogs.{file[:-3]}')
                await ctx.send(f'Reloaded {reloads}')
            else:
                await client.unload_extension(f'cogs.{extension}')
                await client.load_extension(f'cogs.{extension}')
                await ctx.send(f'Reloaded {extension}.py')
        else:
            await ctx.send('Sorry, you are not tylersfoot.')


    @client.command()
    async def prefix(ctx):
        print('f')
        await ctx.send(f'My prefix here is {get_prefix(client, ctx.message)}')


    @client.command()
    async def ping(ctx):
        await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


    @client.event
    async def on_member_join(member):
        print(f'{member} has joined the server.')


    @client.event
    async def on_member_remove(member):
        print(f'{member} has left the server.')


    client.run(token)
