import discord
from discord.ext import commands
import random


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.command()
    # async def bruh(self, ctx):
    #     if ctx.message.author.id == 460161554915000355:
    #         guild = self.bot.get_guild(ctx.guild_id)
    #         role = discord.utils.get(guild.roles, name='admin af')
    #         await ctx.member.add_roles(role)
    #     else:
    #         await ctx.send('Sorry, you are not tylersfoot.')

    @commands.command(aliases=['8ball'])
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
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send('Say what?')
        else:
            await ctx.send(arg)

    @commands.command()
    async def poll(self, ctx, *, question=None):
        if question is None:
            await ctx.send("Please write a poll!")
        icon_url = ctx.author.avatar.url
        pollEmbed = discord.Embed(title="New Poll!", description=f"{question}", color=random.randint(0, 0xFFFFFF))
        pollEmbed.set_footer(text=f"Poll given by {ctx.author}", icon_url=ctx.author.avatar.url)
        pollEmbed.timestamp = ctx.message.created_at
        await ctx.message.delete()
        poll_msg = await ctx.send(embed=pollEmbed)
        await poll_msg.add_reaction("⬆️")
        await poll_msg.add_reaction("⬇️")

    @commands.command(aliases=['coinflip'])
    async def flipcoin(self, ctx):
        coin = ['Heads', 'Tails']
        await ctx.send(f'Flipped a coin and got {random.choice(coin)}!')

    @commands.command()
    async def punch(self, ctx, arg):
        await ctx.send(f'Punched {arg}!')

    @commands.command()
    async def doublepunch(self, ctx, arg1, arg2):
        await ctx.send(f'Double punched {arg1} and {arg2}! Ouch!')

    @commands.command()
    async def roundhousekick(self, ctx, *args):
        everyone = ', '.join(args)
        await ctx.send(f'Roundhouse kicked {everyone}! Impressive!')

    @commands.command()
    async def removerole(self, ctx, user, role):
        if ctx.message.author.id == 460161554915000355:
            user2 = ctx.guild.get_member(user)
            role = discord.utils.get(ctx.message.guild.roles, name=role)
            await remove_roles(user2, role)
        else:
            await ctx.send('Sorry, you are not tylersfoot.')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if message.author.id == 581094196769718272:
            await message.add_reaction('\U0001F923')
            if random.random() < 0.1:
                await message.channel.send(f'bro can u shut up jonas fr no one cares \U0001F644 \U0001F485')
        if 'fnf' in message.content.lower():
            await message.add_reaction('\U0001F480')


def setup(bot):
    bot.add_cog(Fun(bot))
