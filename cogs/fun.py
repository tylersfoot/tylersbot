import discord
from discord.ext import commands
import random
import datetime


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    fun_group = discord.SlashCommandGroup(
        name = "fun", 
        description = "Fun commands",
        integration_types = {discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )


    @fun_group.command(name="8ball", description="Decide your fate!")
    async def fun_eightball(self, ctx, question: str):
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


    @fun_group.command(name="say", description="Tell the bot to say something.")
    async def fun_say(self, ctx, message: str):
        await ctx.respond(message)


    @fun_group.command(name="coinflip", description="Flips a coin.")
    async def fun_coinflip(self, ctx):
        coin = ['Heads', 'Tails']
        await ctx.respond(f'Flipped a coin and got {random.choice(coin)}!')


    @fun_group.command(name="punch", description="Punches a user.")
    async def fun_punch(self, ctx, user: discord.Member):
        await ctx.respond(f'Punched {user.mention}!')


    @fun_group.command(name="doublepunch", description="Punches two users.")
    async def fun_doublepunch(self, ctx, user1: discord.Member, user2: discord.Member):
        await ctx.respond(f'Double punched {user1.mention} and {user2.mention}! Ouch!')
        
    
    # @commands.slash_command(name="roundhousekick", description="Roundhouse kicks multiple users.")
    # async def roundhousekick(self, ctx, members: commands.Greedy[discord.Member]):
    #     if not members:
    #         await ctx.respond("You need to specify at least one user!", ephemeral=True)
    #         return

    #     everyone = ', '.join(member.mention for member in members)
    #     await ctx.respond(f'Roundhouse kicked {everyone}! Impressive!')
        

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        easter egg type thing. adds a reaction and replies with a message at a 0.01% change every message is sent.
        feel free to remove this or change it if it gets annoying. also the emojis wont work since you're probably
        not in my server.
        '''
        if message.author.bot:
            return
        if random.random() < 0.0001:
            await message.add_reaction('<a:deadcat:1063260777278083224>')
            embed = discord.Embed(
                title=f"ATTENTION!!!!",
                description=f'thanks for your attention <:kirbysmile:1063259570232885310>',
                color=int(str(message.author.color)[1:], 16)
            )
            embed.set_image(url='https://media.discordapp.net/attachments/962179885231652966/1063261025232760992/attention-thanks-for-your-attention-trolling-poster-3593367102.jpeg')
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f'this message has a 0.01% chance of appearing!', icon_url=message.author.avatar.url)
            await message.channel.send(embed=embed)
            
        # example of doing something if any message sent has a certain substring in it
        if 'fnf' in message.content.lower():
            await message.add_reaction('\U0001F480') # skull emoji


def setup(bot):
    bot.add_cog(Fun(bot))
