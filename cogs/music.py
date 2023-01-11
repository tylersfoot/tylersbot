import discord
from discord.ext import commands
import youtube_dl
import asyncio
from bot import guilds
import datetime

playing = False
paused = False


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_bot = None

    async def musicstop(self):
        global playing, paused
        try:
            if playing:
                self.voice_bot.stop()
                self.voice_bot.resume()
                playing = False
                paused = False
                return 'Stopped.'
            else:
                return 'Nothing currently playing.'
        except Exception as e:
            return e

    @commands.slash_command(name="join", description="Joins the voice channel you are in.")
    async def join(self, ctx):
        try:
            if ctx.author.voice is None:
                await ctx.respond(f'You are not in a voice channel!')
            else:
                voice_channel = ctx.author.voice.channel
                if self.voice_bot is None:
                    self.voice_bot = await voice_channel.connect()
                    await ctx.respond(f'Joined `{voice_channel}`.')
                elif ctx.author.voice.channel == self.voice_bot.channel:
                    await ctx.respond(f'I am already connected to `{voice_channel}`!')
                else:
                    await self.voice_bot.move_to(voice_channel)
                    await ctx.respond(f'Moved to `{voice_channel}`.')
        except Exception as e:
            await ctx.respond(f'Sorry, an error occurred: \n`{str(e)[:1900]}`\n - Please report to `tylersfoot#8888`.')

    @commands.slash_command(name="disconnect", description="Disconnects from the current voice channel.")
    async def disconnect(self, ctx):
        try:
            global playing, paused
            if self.voice_bot is None:
                await ctx.respond('I am not in a voice channel!')
            else:
                voice_channel = ctx.author.voice.channel
                try:
                    self.voice_bot.resume()
                    self.voice_bot.stop()
                except:
                    pass
                playing = False
                paused = False
                await self.voice_bot.disconnect()
                self.voice_bot = None
                await ctx.respond(f'Disconnected from `{voice_channel}`.')
        except Exception as e:
            await ctx.respond(f'Sorry, an error occurred: \n`{str(e)[:1900]}`\n - Please report to `tylersfoot#8888`.')

    @commands.slash_command(name="play", description="Plays a song (youtube link)")
    async def play(self, ctx, *, url):
        global playing, paused
        if ctx.author.voice is None:
            await ctx.respond(f'You are not in a voice channel!')
        else:
            voice_channel = ctx.author.voice.channel
            if self.voice_bot is None:
                self.voice_bot = await voice_channel.connect()
                await ctx.respond(f'Joined `{voice_channel}` and loading... <a:loading1:1048082138282606642>')
            elif ctx.author.voice.channel != self.voice_bot.channel:
                await self.voice_bot.move_to(voice_channel)
                await ctx.respond(f'Moved to `{voice_channel}` and loading... <a:loading1:1048082138282606642>')
            else:
                await ctx.respond(f'Loading... <a:loading1:1048082138282606642>')
            await self.musicstop()
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
            try:
                with youtube_dl.YoutubeDL(ytdlopts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    # gets the thumbnail
                    video_thumbnail_url = info['thumbnail']
                    # gets the duration of the video
                    if info.get('duration'):
                        duration = int(info.get("duration", 0))
                        minutes, seconds = divmod(duration, 60)
                        formatted_duration = f"{minutes}:{seconds:02d}"

                    url2 = info['formats'][0]['url']
                    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            except KeyError:
                await ctx.edit(f'Invalid YouTube link provided. If you believe this is a mistake, please report to `tylersfoot#8888`.')
            await asyncio.sleep(0.2)
            self.voice_bot.play(source)
            playing = True
            embed = discord.Embed(
                title=f"Now Playing",
                description=f"[{info['title']}]({info['webpage_url']})",
                color=int(str(ctx.author.color)[1:], 16)
            )
            embed.add_field(name="Views", value=format(info['view_count'], ','))
            embed.add_field(name="Uploader", value=info['uploader'])
            embed.add_field(name="Duration", value=formatted_duration)
            embed.set_thumbnail(url=video_thumbnail_url)
            embed.set_footer(
                text=f'Requested by {ctx.author.name}#{ctx.author.discriminator}',
                icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await ctx.edit(content=None, embed=embed)


    @commands.slash_command(name="stop", description="Stops playing audio.")
    async def stop(self, ctx):
        result = await self.musicstop()
        await ctx.respond(result)


    @commands.slash_command(name="pause", description="Pauses the audio.")
    async def pause(self, ctx):
        global playing, paused
        if playing and not paused:
            self.voice_bot.pause()
            paused = True
            await ctx.respond("Paused.")
        elif playing and paused:
            await ctx.respond("Already paused.")
        else:
            await ctx.respond("Nothing currently playing.")

    @commands.slash_command(name="resume", description="Resumes playing audio.")
    async def resume(self, ctx):
        global playing, paused
        if playing and paused:
            self.voice_bot.resume()
            await ctx.respond("Resumed.")
        elif playing and not paused:
            await ctx.respond("Already paused.")
        else:
            await ctx.respond("Nothing currently playing.")

    # @commands.Cog.listener()
    # async def on_voice_state_update(self, member, before, after):
    #
    #     if not member.id == self.bot.user.id:
    #         return
    #
    #     elif before.channel is None:
    #         voice = after.channel.guild.voice_bot
    #         time = 0
    #         while True:
    #             await asyncio.sleep(1)
    #             time = time + 1
    #             if voice.is_playing() and not voice.is_paused():
    #                 time = 0
    #             if time == 300:
    #                 await voice.disconnect()
    #             if not voice.is_connected():
    #                 break


def setup(bot):
    bot.add_cog(Music(bot))
