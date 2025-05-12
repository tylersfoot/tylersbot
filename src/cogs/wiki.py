import discord
from discord.ext import commands
import wikipedia
from core.customexceptions import WikiPageError, WikiDisambiguationError
import datetime


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    wiki_group = discord.SlashCommandGroup(
        name = "wiki", 
        description = "Wikipedia related commands",
        integration_types = {discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )


    @wiki_group.command(name="search", description="Searches for a list of Wikipedia articles.")
    async def wiki_search(self, ctx, request: str):
        try:
            wikicontent = wikipedia.search(request, results=10, suggestion=False)  # Wikipedia search request

            wikilinks = []
            for i in wikicontent:
                wikilinks.append("https://en.wikipedia.org/wiki/Special:Search?search=" + i.replace(' ', '_'))

            embed = discord.Embed(
                title="Wikipedia search results:",
                color=int(str(ctx.author.color)[1:], 16),
            )
            if not wikicontent:
                wikicontent = f"Sorry, there are no search results for \"{request}\"."
            wikiresults = []
            for i in range(len(wikicontent)):
                wikiresults.append(f'[{wikicontent[i]}]({wikilinks[i]})')

            embed.description = "\n".join(wikiresults)
            embed.set_thumbnail(
                url="https://www.wikipedia.org/static/images/project-logos/enwiki.png"
            )
            embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed)

        except wikipedia.PageError:
            raise WikiPageError(request)
        except wikipedia.DisambiguationError:
            raise WikiDisambiguationError(request)
        except IndexError:
            raise WikiPageError(request)

    @wiki_group.command(name="article", description="Returns a summary of the Wikipedia article specified.")
    async def wiki_article(self, ctx, request: str):
        try:
            pagecontent = wikipedia.page(request, auto_suggest=False, redirect=True, preload=False)
            pagetext = wikipedia.summary(request, auto_suggest=False, redirect=True, sentences=5)

            # tries to set first image in article to embed thumbnail
            try:
                thumbnail = pagecontent.images[0]
            except Exception as error:
                # if there are no images, it will set it to the default wikipedia picture
                print(f"Couldn\'t load thumbnail, {error}")
                thumbnail = "https://www.wikipedia.org/static/images/project-logos/enwiki.png"

            embed = discord.Embed(
                title=pagecontent.title,
                color=int(str(ctx.author.color)[1:], 16),
                description=f'{pagetext}\n\n[Read further]({pagecontent.url})'
            )
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed)

        except wikipedia.PageError:
            raise WikiPageError(request)
        except wikipedia.DisambiguationError:
            raise WikiDisambiguationError(request)


    @wiki_group.command(name="random", description="Returns the summary of a random Wikipedia article.")
    async def wiki_random(self, ctx):
        try:
            tries = 0
            # tries to get a random article 10 times
            for i in range(10):
                tries += 1
                try:
                    random_article = wikipedia.random(pages=1)
                    pagecontent = wikipedia.page(random_article)
                    break
                except Exception as e:
                    continue

            pagetext = wikipedia.summary(random_article, sentences=5)

            # tries to set first image in article to embed thumbnail
            try:
                thumbnail = pagecontent.images[0]
            except Exception as error:
                # if there are no images, it will set it to the default wikipedia picture
                try:
                    print(f"Couldn't load {thumbnail}, {error}")
                    thumbnail = "https://www.wikipedia.org/static/images/project-logos/enwiki.png"
                except:
                    print(f"Couldn't load thumbnail, {error}")
                    thumbnail = "https://www.wikipedia.org/static/images/project-logos/enwiki.png"

            embed = discord.Embed(title=random_article,
                                  color=int(str(ctx.author.color)[1:], 16),
                                  description=f'{pagetext}\n\n[Read further]({pagecontent.url})'
                                  )
            embed.set_thumbnail(url=thumbnail)
            if tries > 1:
                embed.set_footer(text=f"Requested by {ctx.author.name} | {tries} attempts", icon_url=ctx.author.avatar.url)
            else:
                embed.set_footer(text=f"Requested by {ctx.author.name} | {tries} attempt", icon_url=ctx.author.avatar.url)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed)
        except wikipedia.PageError:
            raise WikiPageError("random") 
        except wikipedia.DisambiguationError:
            raise WikiDisambiguationError("random")


def setup(bot):
    bot.add_cog(Wiki(bot))
