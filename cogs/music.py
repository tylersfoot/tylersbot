import discord
from discord.ext import commands
import youtube_dl
from time import sleep
import asyncio

playing = False
paused = False
weezer = False


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['j', 'joinchannel'])
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_bot is None:
            await ctx.send("Joined")
            await voice_channel.connect()
        elif ctx.author.voice.channel == ctx.voice_bot.channel:
            await ctx.send("Already in that channel")
        else:
            await ctx.send("Moved")
            await ctx.voice_bot.move_to(voice_channel)

    @commands.command()
    async def weezer(self, ctx):
        global weezer
        if weezer:
            weezer = False
            await ctx.send("Weezer songs now allowed")
        else:
            weezer = True
            await ctx.send("Weezer songs now not allowed")

    @commands.command(aliases=['leave', 'l', 'leavechannel', 'dc', 'dis'])
    async def disconnect(self, ctx):
        global playing, paused
        if ctx.voice_bot is not None:
            ctx.voice_bot.resume()
            ctx.voice_bot.stop()
            playing = False
            paused = False
            await ctx.voice_bot.disconnect()
            await ctx.send("Disconnected")
        else:
            await ctx.send("Not in a voice channel")

    @commands.command(aliases=['pl', 'p', 'playsong'])
    async def play(self, ctx, *, url):
        global playing, paused, weezer
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
        else:
            voice_channel = ctx.author.voice.channel
            if ctx.voice_bot is None:
                await ctx.send("Joined")
                await voice_channel.connect()
            elif ctx.author.voice.channel != ctx.voice_bot.channel:
                await ctx.send("Moved")
                await ctx.voice_bot.move_to(voice_channel)
            if ctx.author.voice.channel == ctx.voice_bot.channel:
                await ctx.send("Loading...")
                ctx.voice_bot.stop()
                ctx.voice_bot.resume()
                playing = False
                paused = False
                FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                                  'options': '-vn'}
                ytdlopts = {
                    'format': 'bestaudio/best',
                    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
                    'restrictfilenames': True,
                    'nocheckcertificate': True,
                    'ignoreerrors': False,
                    'logtostderr': False,
                    'quiet': True,
                    'extract_flat': True,
                    'skip_download': True,
                    'default_search': 'auto',
                    'source_address': '0.0.0.0',  # ipv6 addresses cause issues sometimes
                    'force-ipv4': True,
                    'cachedir': False
                }
                vc = ctx.voice_bot

                with youtube_dl.YoutubeDL(ytdlopts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    url2 = info['formats'][0]['url']
                    if ('weezer' in info['title'] or 'Weezer' in info['title']) and weezer:
                        url = 'https://www.youtube.com/watch?v=D1qU745zMKU'
                        info = ydl.extract_info(url, download=False)
                        url2 = info['formats'][0]['url']
                        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                        sleep(0.5)
                        vc.play(source)
                        playing = True
                        idot = '<a:youareanidiot:971852471871877250>'
                        await ctx.send(f"{idot}YOU{idot}ARE{idot}AN{idot}IDIOT{idot}")
                        await ctx.send("https://c.tenor.com/k_zNRKXYlnkAAAAM/idiot-smile.gif")
                        await ctx.send(f"{idot}YOU{idot}ARE{idot}AN{idot}IDIOT{idot}")
                        return
                    else:
                        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                        sleep(1)
                        vc.play(source)
                        playing = True
                        await ctx.send(f"Playing {info['title']}")

    @commands.command(aliases=['s'])
    async def stop(self, ctx):
        global playing, paused
        if playing:
            ctx.voice_bot.stop()
            ctx.voice_bot.resume()
            playing = False
            paused = False
            await ctx.send("Stopped")
        else:
            ctx.send("Nothing playing")

    @commands.command(aliases=['pau', 'pausesong'])
    async def pause(self, ctx):
        global playing, paused
        if playing and not paused:
            ctx.voice_bot.pause()
            paused = True
            await ctx.send("Paused")
        elif playing and paused:
            await ctx.send("Already paused")
        else:
            await ctx.send("Nothing playing")

    @commands.command(aliases=['r', 'res', 'resumesong'])
    async def resume(self, ctx):
        global playing, paused
        if playing and paused:
            ctx.voice_bot.resume()
            await ctx.send("Resumed")
        elif playing and not paused:
            await ctx.send("Already playing")
        else:
            await ctx.send("Nothing playing")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if not member.id == self.bot.user.id:
            return

        elif before.channel is None:
            voice = after.channel.guild.voice_bot
            time = 0
            while True:
                await asyncio.sleep(1)
                time = time + 1
                if voice.is_playing() and not voice.is_paused():
                    time = 0
                if time == 300:
                    await voice.disconnect()
                if not voice.is_connected():
                    break


def setup(bot):
    bot.add_cog(Music(bot))
