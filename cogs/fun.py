import discord
from discord.ext import commands
import random
from bot import guilds
import datetime


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="8ball", description="Decide your fate!")
    async def eightball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(
            title=f"Question: {question}",
            description=f'Answer: {random.choice(responses)}',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.respond(embed=embed)

    @commands.slash_command(name="say", description="Tell the bot to say something.")
    async def say(self, ctx, *, arg=None):
        if arg is None:
            await ctx.respond('Say what?')
        else:
            await ctx.respond(arg)

    @commands.slash_command(name="coinflip", description="Flips a coin.")
    async def coinflip(self, ctx):
        coin = ['Heads', 'Tails']
        await ctx.respond(f'Flipped a coin and got {random.choice(coin)}!')

    @commands.slash_command(name="punch", description="Punches a user.")
    async def punch(self, ctx, arg):

        await ctx.respond(f'Punched {arg}!')

    @commands.slash_command(name="doublepunch", description="Punches two users.")
    async def doublepunch(self, ctx, member1: discord.Member = None, member2: discord.Member = None):
        if member1 is None:
            member1 = self.client.user.mention
        if member2 is None:
            member2 = self.client.user.mention
        await ctx.respond(f'Double punched {member1} and {member2}! Ouch!')

    @commands.slash_command(name="roundhousekick", description="Roundhouse kicks multiple users.")
    async def roundhousekick(self, ctx, *args):
        everyone = ', '.join(args)
        await ctx.respond(f'Roundhouse kicked {everyone}! Impressive!')
        

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        easter egg type thing. adds a reaction and replies with a message at a 0.1% change every message is sent.
        feel free to remove this or change it if it gets annoying. also the emojis wont work since you're probably
        not in my server.
        '''
        if message.author.bot:
            return
        if random.random() < 0.001:
            await message.add_reaction('<a:deadcat:1063260777278083224>')
            embed = discord.Embed(
                title=f"ATTENTION!!!!",
                description=f'thanks for your attention <:kirbysmile:1063259570232885310>',
                color=int(str(message.author.color)[1:], 16)
            )
            embed.set_image(url='https://media.discordapp.net/attachments/962179885231652966/1063261025232760992/attention-thanks-for-your-attention-trolling-poster-3593367102.jpeg')
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f'this message has a 0.1% chance of appearing!', icon_url=message.author.avatar.url)
            await message.channel.send(embed=embed)
        # example of doing something if any message sent has 'example' in it
        if 'example' in message.content.lower():
            await message.add_reaction('\U0001F480') # skull emoji


def setup(bot):
    bot.add_cog(Fun(bot))
