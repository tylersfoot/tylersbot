import discord
from discord.ext import commands
from revChatGPT.revChatGPT import Chatbot as CB
from bot import guilds
from dotenv import load_dotenv
import os


class Chatbot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="chatlogin", description="Logs into the chatbot")
    async def chatlogin(self, ctx):
        global chatbot
        await ctx.respond('Logging in... <a:loading1:1048082138282606642>')
        try:
            load_dotenv()
            email = os.getenv('CHATBOT_EMAIL')
            password = os.getenv('CHATBOT_PASSWORD')
            chatbot = CB({
                "email": email,
                "password": password
            })
            await ctx.edit(content='Logged in!')
        except Exception as e:
            await ctx.edit(content=f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')

    @commands.slash_command(name="chatrefresh", description="Refreshes the current chatbot thread (deletes previous context)")
    async def chatrefresh(self, ctx):
        global chatbot
        await ctx.respond('Refreshing thread... <a:loading1:1048082138282606642>')
        try:
            chatbot.reset_chat()
            await ctx.edit(content='Refreshed the chatbot thread!')
        except Exception as e:
            await ctx.edit(content=f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')

    @commands.slash_command(name="chat", description="Send a message to the chatbot!")
    async def chat(self, ctx, *, prompt: str):
        global chatbot
        await ctx.respond('Sending the message to the chatbot... <a:loading1:1048082138282606642>')
        try:
            await ctx.edit(content='Waiting for a response from the chatbot... <a:loading1:1048082138282606642>')
            response = chatbot.get_chat_response(prompt)
            # send the username of the person who sent the message
            message = f'{ctx.author.mention}: {prompt}\n\n`Chatbot:` {response["message"]}'
            message = message[:2000]
            await ctx.edit(content=message)
        except NameError:
            await ctx.edit(content=f'Please run the `/chatlogin` command!')
        except Exception as e:
            await ctx.edit(content=f'Sorry, an error occurred: \n`{e}`\n - Please report to `tylersfoot#8888`')


def setup(bot):
    bot.add_cog(Chatbot(bot))
