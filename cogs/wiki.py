import discord
from discord.ext import commands
import wikipedia
import asyncio
from random import randint
import traceback


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['wikipediasearch', 'wikiresults', 'wikipediaresults', 'wikis', 'wikipedias'])
    async def wikisearch(self, ctx, *, request):

        try:
            wikicontent = wikipedia.search(request, results=10, suggestion=False)  # Wikipedia search request
            # print('--------------------------------')
            # print(wikicontent)
            wikilinks = []
            # for i in wikicontent:
            #     try:
            #         wikilinks.append(wikipedia.page(i, auto_suggest=False, redirect=True, preload=False).url)
            #     except wikipedia.DisambiguationError as e:
            #         try:
            #             wikilinks.append(wikipedia.page(e.options[0]).url)
            #         except:
            #             wikilinks.append('https://en.wikipedia.org/wiki/Special:Search?search=' + i.replace(' ', '_'))
            for i in wikicontent:
                wikilinks.append('https://en.wikipedia.org/wiki/Special:Search?search=' + i.replace(' ', '_'))

            # print('--------------------------------')
            # print(wikilinks)
            embed = discord.Embed(
                title="Wikipedia search results:",
                color=int(str(ctx.author.color)[1:], 16),
            )
            if not wikicontent:
                wikicontent = f'Sorry, there are no search results for "{request}".'
            wikiresults = []
            for i in range(len(wikicontent)):
                wikiresults.append(f'[{wikicontent[i]}]({wikilinks[i]})')

            embed.description = "\n".join(wikiresults)
            embed.set_thumbnail(
                url='https://www.wikipedia.org/static/images/project-logos/enwiki.png'
            )
            await ctx.send(embed=embed)

        # Handle random errors
        except Exception as error:
            await ctx.send(f'Sorry, an error occurred: \n[{error}]\n - Please report to tylersfoot.')
            print(traceback.format_exc())

    @commands.command(aliases=['wikipedia', 'wikiarticle', 'wikia', 'wikiaa'])
    async def wiki(self, ctx, *, request):

        # Checks if the request is valid
        try:
            pagecontent = wikipedia.page(request, auto_suggest=False, redirect=True, preload=False)
            pagetext = wikipedia.summary(request, auto_suggest=False, redirect=True, sentences=5)

            # Tries to set first image in article to embed thumbnail
            try:
                thumbnail = pagecontent.images[0]
            except Exception as error:
                # If there are no images, it will set it to the default wikipedia picture
                try:
                    print(f'Couldn\'t load {thumbnail}, {error}')
                    thumbnail = 'https://www.wikipedia.org/static/images/project-logos/enwiki.png'
                except:
                    print(f'Couldn\'t load thumbnail, {error}')
                    thumbnail = 'https://www.wikipedia.org/static/images/project-logos/enwiki.png'

            embed = discord.Embed(
                title=pagecontent.title,
                color=int(str(ctx.author.color)[1:], 16),
                description=f'{pagetext}\n\n[Read further]({pagecontent.url})'
            )
            embed.set_thumbnail(
                url=thumbnail
            )
            await ctx.send(embed=embed)

        except wikipedia.PageError:
            await ctx.send(f'Sorry, there are no results for "{request}".')

        except Exception as error:
            await ctx.send(f'Sorry, an error occurred: \n[{str(error)[:1900]}]\n - Please report to tylersfoot.')
            print(traceback.format_exc())

    @commands.command(aliases=['wikipediarandom', 'wikipediarand', 'wikirand', 'wiki_random', 'wiki_rand'])
    async def wikirandom(self, ctx):
        # Gets a random wikipedia article

        try:
            tries = 0
            # Tries to get a random article 10 times
            for i in range(10):
                tries += 1
                try:
                    random_article = wikipedia.random(pages=1)
                    pagecontent = wikipedia.page(random_article)
                    break
                except Exception as e:
                    continue

            pagetext = wikipedia.summary(random_article, sentences=5)

            # Tries to set first image in article to embed thumbnail
            try:
                thumbnail = pagecontent.images[0]
            except Exception as error:
                # If there are no images, it will set it to the default wikipedia picture
                try:
                    print(f'Couldn\'t load {thumbnail}, {error}')
                    thumbnail = 'https://www.wikipedia.org/static/images/project-logos/enwiki.png'
                except:
                    print(f'Couldn\'t load thumbnail, {error}')
                    thumbnail = 'https://www.wikipedia.org/static/images/project-logos/enwiki.png'

            embed = discord.Embed(title=random_article,
                                  color=int(str(ctx.author.color)[1:], 16),
                                  description=f'{pagetext}\n\n[Read further]({pagecontent.url})'
                                  )
            embed.set_thumbnail(url=thumbnail)
            embed.set_footer(text=f'Requested by {ctx.author.name} | {tries} attempts', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except Exception as error:
            await ctx.send(f'Sorry, an error occurred: \n[{error}]\n - Please report to tylersfoot.')
            print(traceback.format_exc())


def setup(bot):
    bot.add_cog(Wiki(bot))
