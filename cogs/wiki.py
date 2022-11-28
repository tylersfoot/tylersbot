import discord
from discord.ext import commands
import wikipedia
import asyncio
from random import randint


class Wiki(commands.Cog):
    def __init__(self, client):
        self.client = client
        global current_language
        current_language = "en"  # Default language

    @commands.command(pass_context=True)
    async def search(self, ctx, *, msg):

        # Load current lang for picture
        global current_language

        # Get user input
        request = msg
        request = " ".join(request)
        error = None

        try:
            wikicontent = wikipedia.search(request, results=20, suggestion=False)  # Wikipedia search request
            print(wikicontent)
            print(" ".join(wikicontent))

            # If there are no results
            if not wikicontent:
                wikicontent = "Sorry, there are no search results for '{}'.".format(request)
                embed = discord.Embed(title="Wikipedia search results:", color=0xe74c3c, description=wikicontent)
                embed.set_thumbnail(
                    url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
                await ctx.send(embed=embed)

            # If there are do:
            else:
                embed = discord.Embed(title="Wikipedia search results:", color=0, description="\n".join(wikicontent))
                embed.set_thumbnail(
                    url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
                await ctx.send(embed=embed)

        # Handle random errors
        except Exception as error:
            error = str(error)
            await ctx.send("Sorry, a random error occurred. Please try again.")
            print(error)

    @commands.command(pass_context=True)
    async def display(self, ctx):

        global current_lang

        msg = ctx.message.content.split(" ")
        request = msg[2:]
        request = " ".join(request)

        # Checks if the request is valid
        try:
            pagecontent = wikipedia.page(request)
            pagetext = wikipedia.summary(request, sentences=5)

            # Try to get random image from the article to display.
            # If there are no pictures, it wil set it to the default wkikipedia picture
            try:
                thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]

            except:
                thumbnail = "https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language)

            embed = discord.Embed(title=request, color=0,
                                  description=pagetext + "\n\n[Read further]({})".format(pagecontent.url))
            embed.set_thumbnail(url=thumbnail)
            await ctx.send(embed=embed)


        except wikipedia.DisambiguationError:
            NotSpecificRequestErrorMessage = """Sorry, your search request wasn't specific enough. Please try '/w search (your request)'. This will display all wikipedia articles with your search request. You can than copy the correct result and put that in /a display."""
            embed = discord.Embed(title="Bad request: ", color=0xe74c3c, description=NotSpecificRequestErrorMessage)
            embed.set_thumbnail(
                url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await ctx.send(embed=embed)

        except wikipedia.PageError:

            NoResultErrorMessage = "Sorry, there are no Wikipedia articles with this title. Please try '/w search (your request)' to look up Wikipedia article name's"
            embed = discord.Embed(title="Not found: ", color=0xe74c3c, description=NoResultErrorMessage)
            embed.set_thumbnail(
                url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await ctx.send(embed=embed)

        except:
            RandomErrorMessage = "Sorry, a random error occured"
            embed = discord.Embed(title="Error", color=0xe74c3c, description=RandomErrorMessage)
            embed.set_thumbnail(
                url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await ctx.send(embed=embed)
            # await bot.say(error)

    @commands.command(pass_context=True)
    async def lang(self, ctx):

        global current_language

        msg = ctx.message.content.split(" ")
        command = msg[2]
        langcodes = wikipedia.languages().keys()

        # Check which command to run
        if command == "list" or command == "List":

            # List of most used languages on wikipedia
            languagelist = "English / English = en\nCebuano / Sinugboanong = ceb\nSwedish / Svenska = sv\nGerman / Deutsch = de\nFrench / Français = fr\nDutch / Nederlands = nl\nRussian / Русский = ru\nItalian / Italiano = it\nSpanish / Español = es\nWaray-Waray / Winaray = war\nPolish / Polski = pl\nVietnamese / Tiếng Việt = vi\n Japanese / 日本語 = ja\n"
            languagelistwiki = "https://meta.wikimedia.org/wiki/List_of_Wikipedias"

            embed = discord.Embed(title="Wikipedia language list:", color=0,
                                  description=languagelist + "\n\nAll supported languages can be found [here]({})".format(
                                      languagelistwiki))
            embed.set_thumbnail(
                url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
            await ctx.send(embed=embed)


        elif command == "set" or command == "Set":

            # Check if the given language(langcode) is valid
            if msg[3] in langcodes:
                current_language = msg[3]
                wikipedia.set_lang(msg[3])

            else:
                embed = discord.Embed(title="Languages not found:", color=0xe74c3c,
                                      description="Sorry, the language '{}' was not found. Please run '/w lang list' to see all language codes.".format(
                                          msg[3]))
                embed.set_thumbnail(
                    url="https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language))
                await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def random(self, ctx):

        global current_language

        # Makes sure you will get an article.
        try:
            random_article = wikipedia.random(pages=1)

        except wikipedia.DisambiguationError:

            try:
                random_article = wikipedia.random(pages=1)
            except wikipedia.DisambiguationError:

                try:
                    random_article = wikipedia.random(pages=1)

                except wikipedia.DisambiguationError:
                    random_article = wikipedia.random(pages=1)

        pagecontent = wikipedia.page(random_article)
        pagetext = wikipedia.summary(random_article, sentences=5)

        # Try to set an random image in the article as the thumbnail
        try:
            thumbnail = pagecontent.images[randint(0, len(pagecontent.images))]

        except Exception as error:
            thumbnail = "https://www.wikipedia.org/static/images/project-logos/{}wiki.png".format(current_language)
            print("Couldn't load {}".format(thumbnail))

        embed = discord.Embed(title=random_article, color=0,
                              description=pagetext + "\n\n[Read further]({})".format(pagecontent.url))
        embed.set_thumbnail(url=thumbnail)
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def helpwiki(self, ctx):

        # Help menu
        msg = ctx.message.content.split(" ")

        try:
            helpselect = msg[2]

            if helpselect == "search":
                await ctx.send("```/w search 'term' - searches wikipedia on given term```")

            elif helpselect == "display":
                await ctx.send("```/w display 'term' - displays the article with the given term```")

            elif helpselect == "lang":
                try:
                    langhelp = msg[3]

                    if langhelp == "list":
                        await ctx.send("```/w lang list - displays wikipedia language options list```")

                    elif langhelp == "set":
                        await ctx.send(
                            "```/w lang set 'language code' - set's the language to the given code.\nCode can be found at /w lang list```")

                    else:
                        await ctx.send("```Oops, this looks like invalid input to me.\nPlease see '/w help lang'```")

                except:
                    await ctx.send("```/w help lang list\n/w help set```")

            elif helpselect == "random":
                await ctx.send("```/w random - displays a random article based on the current language set```")

            elif helpselect == "about":
                await ctx.send("```/w about - display's additional information```")

            else:
                await ctx.send("```Oops, looks like invalid input to me.\nPlease see '/w help'```")

        except:
            await ctx.send("```/w help search\n/w help display\n/w help lang\n/w help random\n/w help about```")


async def setup(client):
    await client.add_cog(Wiki(client))
