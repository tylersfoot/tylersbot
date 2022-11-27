import os
import json
import requests
import discord
from discord.ext import commands

# this is my Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/tylersfoot/'


class Chatbot(commands.Cog):
    def __init__(self, client):
        model_name = 'DialoGPT-medium-rick'
        self.client = client
        super().__init__()
        self.api_endpoint = API_URL + model_name
        # retrieve the secret API token from the system environment
        # huggingface_token = os.environ['HUGGINGFACE_TOKEN']
        huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }


    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        self.query({'inputs': {'text': 'Hello!'}})

    # tempchan = null
    # for channel in ctx.guild.channels:
    #     if channel.name == "henry-logs":
    #         await ctx.send(
    #             "Henry Logs channel is already setup. If you have access to it, it should be available in the channel list")
    #         tempchan = channel
    #         break;
    # if tempchan == null:
    #     await ctx.send(
    #         "Henry logs channel is not found! If you have such access please create channel named **EXACTLY**")
    #     await ctx.send("```henry-logs```")

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ctx = await client.get_context(message)
        if message.author == self.client.user:
            return
        if str(message.channel) == 'chatbot':
            # form query payload with the content of the message
            payload = {'inputs': {'text': message.content}}

            # while the bot is waiting on a response from the model
            # set the its status as typing for user-friendliness
            async with message.channel.typing():
                response = self.query(payload)
            bot_response = response.get('generated_text', None)

            # we may get ill-formed response if the model hasn't fully loaded
            # or has timed out
            if not bot_response:
                if 'error' in response:
                    print(response['error'])
                    bot_response = '`{}`'.format(response['error'])
                else:
                    bot_response = 'Hmm... something is not right with the chatbot.'

            # send the model's response to the Discord channel
            await message.channel.send(bot_response, reference=message)
        return


async def setup(client):
    await client.add_cog(Chatbot(client))