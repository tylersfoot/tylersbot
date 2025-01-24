import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord.commands import option

API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = "https://osu.ppy.sh/oauth/token"


def get_token():
    load_dotenv()
    
    data = {
        'client_id': os.getenv('OSU_CLIENT_ID'),
        'client_secret': os.getenv('OSU_CLIENT_SECRET'),
        'grant_type': 'client_credentials',
        'scope': 'public'
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(TOKEN_URL, data=data, headers=headers)
    response.raise_for_status()
    token = response.json().get('access_token')
    
    if not token:
        print("Error: Token not found in response.")
        print(response.json())
        return None
    
    return token

class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.slash_command(name="osu play", description="idk something osu", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    # async def osuplay(self, ctx, count: int = 1, mode: str = 'osu', userid: str = 'def'):
    #     token = get_token()
    #     headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
    #     if userid == 'def':
    #         with open('data/osuaccounts.json', 'r') as f:
    #             accounts = json.load(f)
    #             userid = accounts[str(ctx.author.id)]
    #             f.close()
    #     if count > 100 or count < 1:
    #         await ctx.respond('Play must be between 1 and 100.')
    #     else:
    #         params = {'mode': mode, 'limit': count}
    #         modevis = 'Standard'
    #         if mode == 'taiko':
    #             modevis = 'Taiko'
    #         elif mode == 'ctb':
    #             modevis = 'Catch the Beat'
    #         elif mode == 'mania':
    #             modevis = 'Mania'

    #         count = count - 1
    #         response = requests.get(f'{API_URL}/users/{userid}/scores/best', params=params, headers=headers)
    #         cover = response.json()[count].get('beatmapset', {}).get('covers', {}).get('list@2x')
    #         user = response.json()[count].get('user', {}).get('username')
    #         title = response.json()[count].get('beatmapset', {}).get('title')
    #         artist = response.json()[count].get('beatmapset', {}).get('artist')
    #         difficulty = response.json()[count].get('beatmap', {}).get('version')
    #         mods = response.json()[count].get('mods')
    #         combo = response.json()[count].get('max_combo')
    #         score = response.json()[count].get('score')
    #         pp = round(response.json()[count].get('pp'), 2)
    #         stars = response.json()[count].get('beatmap', {}).get('difficulty_rating')
    #         rank = response.json()[count].get('rank')
    #         accuracy = round(response.json()[count].get('accuracy') * 100, 2)
    #         statistics = response.json()[count].get('statistics')
    #         modslist = ''
    #         if rank == 'X':
    #             rank = '<:osurankX:971559056537960509>'
    #         elif rank == 'SH':
    #             rank = '<:osurankSH:971562051371683902>'
    #         elif rank == 'XH':
    #             rank = '<:osurankXH:971561995809746954>'
    #         elif rank == 'S':
    #             rank = '<:osurankS:971558974690312213>'
    #         elif rank == 'A':
    #             rank = '<:osurankA:971559105187680266>'
    #         elif rank == 'B':
    #             rank = '<:osurankB:971559146967146586>'
    #         elif rank == 'C':
    #             rank = '<:osurankC:971559185546346536>'
    #         elif rank == 'D':
    #             rank = '<:osurankD:971559256421711933>'
    #         else:
    #             await ctx.send(f'rank??? {rank}')
    #         if not mods:
    #             mods = 'NM'
    #         else:
    #             mods = " ".join(mods)
    #             for x in range(len(mods)):
    #                 modslist = modslist + mods[x] + ' '
    #         embed = discord.Embed(
    #             title=f'Number {count + 1} top osu! {modevis} play for {user}',
    #             description='',
    #             color=int(str(ctx.author.color)[1:], 16)
    #         )
    #         embed.set_thumbnail(url=cover)
    #         embed.timestamp = ctx.message.created_at
    #         embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
    #         embed.add_field(
    #             name=f'{title} [{difficulty}] +{mods} [{stars}★]',
    #             value=f'''▸ {rank} ▸ {pp}pp ▸ {accuracy}%
    #         ▸ {"{:,}".format(score)} ▸ {combo}x ▸ [{statistics.get("count_300")}/{statistics.get("count_100")}/{statistics.get("count_50")}/{statistics.get("count_miss")}]
    #         ▸ Score set on: {response.json()[count].get('created_at')[:10]}''',
    #             inline=False
    #         )
    #         await ctx.respond(embed=embed)
    
    async def mode_autocomplete(ctx: discord.AutocompleteContext):
        return ["Standard", "Taiko", "Catch", "Mania"]


    @commands.slash_command(name="osuplay", description="Gets osu! play data.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    @option("mode", type=str, description="Pick a gamemode", choices=["Standard", "Taiko", "Catch", "Mania"])
    async def osuplay(
        self, ctx,
        mode: str,
        index: int = 1, userid: str = 'def'
    ):
        # validate parameters
        index = max(1, index)
        if index > 100:
            await ctx.respond("The index must be between 1 and 100.", ephemeral=True)
            return
        if mode == 'Standard':
            mode = 'osu'
        elif mode == 'Taiko':
            mode = 'taiko'
        elif mode == 'Catch':
            mode = 'ctb'
        elif mode == 'Mania':
            mode = 'mania'
        else:
            mode = 'osu'

        # get user ID from file if default
        if userid == 'def':
            try:
                with open('data/osuaccounts.json', 'r') as f:
                    accounts = json.load(f)
                    userid = accounts.get(str(ctx.author.id))
                    if userid is None:
                        raise KeyError("User ID not found in osuaccounts.json")
            except FileNotFoundError:
                await ctx.respond("osuaccounts.json file not found. Please register your account.", ephemeral=True)
                return
            except KeyError as e:
                await ctx.respond(str(e), ephemeral=True)
                return

        # make the API request
        token = get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        params = {'mode': mode, 'limit': index}

        try:
            response = requests.get(f'{API_URL}/users/{userid}/scores/best', params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            await ctx.respond(f"Failed to fetch data: {e}", ephemeral=True)
            return

        # extract play data
        play = data[index - 1]
        rank_emojis = {
            "X": "<:osurankX:971559056537960509>",
            "SH": "<:osurankSH:971562051371683902>",
            "XH": "<:osurankXH:971561995809746954>",
            "S": "<:osurankS:971558974690312213>",
            "A": "<:osurankA:971559105187680266>",
            "B": "<:osurankB:971559146967146586>",
            "C": "<:osurankC:971559185546346536>",
            "D": "<:osurankD:971559256421711933>",
        }
        rank = rank_emojis.get(play.get('rank'), "Unknown rank")
        mods = 'NM' if not play.get('mods') else ' '.join(play.get('mods'))
        
        modedisplay = 'Standard'
        if mode == 'taiko':
            modedisplay = 'Taiko'
        elif mode == 'ctb':
            modedisplay = 'Catch'
        elif mode == 'mania':
            modedisplay = 'Mania'

        embed = discord.Embed(
            title=f"#{index} Top osu!{modedisplay} Play for {play['user']['username']}",
            description=f"",
            color=int(str(ctx.author.color)[1:], 16) if ctx.author.color else discord.Color.blurple()
        )
        embed.set_thumbnail(url=play.get('beatmapset', {}).get('covers', {}).get('list@2x', ''))
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.add_field(
            name=f"{play['beatmapset']['title']} [{play['beatmap']['version']}] [{play['beatmap']['difficulty_rating']}★]",
            value=f"""
            ▸ {rank} ▸ {play['pp']}pp ▸ {round(play['accuracy'] * 100, 2)}% ▸ +{mods}
            ▸ {"{:,}".format(play['score'])} ▸ {play['max_combo']}x
            ▸ [{play['statistics']['count_300']}/{play['statistics']['count_100']}/{play['statistics']['count_50']}/{play['statistics']['count_miss']}]
            ▸ Score set on: {play['created_at'][:10]}
            """,
            inline=False
        )
        await ctx.respond(embed=embed)


    @commands.command()
    async def osutop(self, ctx, mode='def', userid='def'):
        token = get_token()
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        if userid == 'def':
            with open('data/osuaccounts.json', 'r') as f:
                accounts = json.load(f)
                userid = accounts[str(ctx.author.id)]
                f.close()
        if mode == 'def':
            params = {'limit': 5}
        else:
            params = {'mode': mode, 'limit': 5}
        response = requests.get(f'{API_URL}/users/{userid}/scores/best', params=params, headers=headers)
        user = response.json()[0].get('user', {}).get('username')
        if mode == 'def':
            mode = response.json()[0].get('beatmap', {}).get('mode')
        modevis = 'Standard'
        if mode == 'taiko':
            modevis = 'Taiko'
        elif mode == 'ctb':
            modevis = 'Catch the Beat'
        elif mode == 'mania':
            modevis = 'Mania'
        embed = discord.Embed(
            title=f'Top 5 osu! {modevis} plays for {user}',
            description='',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_thumbnail(url=ctx.author.avatar.url)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        for i in range(0, 5):
            cover = response.json()[i].get('beatmapset', {}).get('covers', {}).get('list@2x')
            title = response.json()[i].get('beatmapset', {}).get('title')
            artist = response.json()[i].get('beatmapset', {}).get('artist')
            difficulty = response.json()[i].get('beatmap', {}).get('version')
            mods = response.json()[i].get('mods')
            combo = response.json()[i].get('max_combo')
            score = response.json()[i].get('score')
            pp = round(response.json()[i].get('pp'), 2)
            stars = response.json()[i].get('beatmap', {}).get('difficulty_rating')
            rank = response.json()[i].get('rank')
            accuracy = round(response.json()[i].get('accuracy') * 100, 2)
            statistics = response.json()[i].get('statistics')
            modslist = ''
            if rank == 'SS':
                rank = '<:osurankSS:971559056537960509>'
            elif rank == 'S':
                rank = '<:osurankS:971558974690312213>'
            elif rank == 'A':
                rank = '<:osurankA:971559105187680266>'
            elif rank == 'B':
                rank = '<:osurankB:971559146967146586>'
            elif rank == 'C':
                rank = '<:osurankC:971559185546346536>'
            elif rank == 'D':
                rank = '<:osurankD:971559256421711933>'
            else:
                await ctx.send(f'rank??? {rank}')
            if not mods:
                mods = 'NM'
            else:
                mods = " ".join(mods)
                for x in range(len(mods)):
                    modslist = modslist + mods[x] + ' '
            embed.add_field(
                name=f'{i + 1}. {title} [{difficulty}] +{mods} [{stars}★]',
                value=f'''▸ {rank} ▸ {pp}pp ▸ {accuracy}%
            ▸ {"{:,}".format(score)} ▸ {combo}x ▸ [{statistics.get("count_300")}/{statistics.get("count_100")}/{statistics.get("count_50")}/{statistics.get("count_miss")}]
            ▸ Score set on: {response.json()[i].get('created_at')[:10]}''',
                inline=False
            )
        await ctx.send(embed=embed)

    @commands.command(aliases=['osuaccountset', 'osusetprofile', 'osuprofileset', 'osusetuser', 'osusetusername',
                               'osusetacc', 'osuaccset', 'osuuserset', 'osuusernameset'])
    async def osusetaccount(self, ctx, *, username):
        token = get_token()
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        with open('data/osuaccounts.json', 'r') as f:
            accounts = json.load(f)
            f.close()
        response = requests.get(f'{API_URL}/users/{username}', headers=headers)
        accID = response.json().get('id')

        accounts[str(ctx.author.id)] = str(accID)

        with open('data/osuaccounts.json', 'w') as f:
            json.dump(accounts, f, indent=4)
            f.close()
        await ctx.send(f'Account set to {username}')

    @commands.command(aliases=['osuaccount', 'osugetaccount', 'osuaccountget', 'osuacc', 'osuaccget', 'osugetacc',
                               'osuaccountinfo', 'osuaccinfo', 'osuprofileget', 'osuprofileinfo', 'osugetprofile'])
    async def osuprofile(self, ctx, mode='def', *, userid='me'):
        token = get_token()
        await ctx.send('In the future, this will be a command that shows you your osu profile!')

    @commands.command(aliases=['rs', 'osurs', 'osurecentplay', 'osurecentscore', 'osurecentscoreset'])
    async def osurecent(self, ctx, mode='def', *, userid='def'):
        token = get_token()
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
        if userid == 'def':
            with open('data/osuaccounts.json', 'r') as f:
                accounts = json.load(f)
                userid = accounts[str(ctx.author.id)]
                f.close()
        if mode == 'def':
            params = {'limit': 1}
        else:
            params = {'mode': mode, 'limit': 1}
        response = requests.get(f'{API_URL}/users/{userid}/scores/recent', params=params, headers=headers)
        if response.status_code == 404:
            await ctx.send(f'User not found')
            return
        if str(response.json()) == '[]':
            await ctx.send('No recent scores found for that user/mode.')
            return
        if mode == 'def':
            mode = response.json()[0].get('beatmap', {}).get('mode')
        modevis = 'Standard'
        if mode == 'taiko':
            modevis = 'Taiko'
        elif mode == 'ctb':
            modevis = 'Catch the Beat'
        elif mode == 'mania':
            modevis = 'Mania'
        user = response.json()[0].get('user', {}).get('username')
        await ctx.send(f'**Recent osu! {modevis} Play for {user}:**')
        cover = response.json()[0].get('beatmapset', {}).get('covers', {}).get('list@2x')
        title = response.json()[0].get('beatmapset', {}).get('title')
        artist = response.json()[0].get('beatmapset', {}).get('artist')
        difficulty = response.json()[0].get('beatmap', {}).get('version')
        mods = response.json()[0].get('mods')
        combo = response.json()[0].get('max_combo')
        score = response.json()[0].get('score')
        pp = round(response.json()[0].get('pp'), 2)
        stars = response.json()[0].get('beatmap', {}).get('difficulty_rating')
        rank = response.json()[0].get('rank')
        accuracy = round(response.json()[0].get('accuracy') * 100, 2)
        statistics = response.json()[0].get('statistics')
        modslist = ''
        if rank == 'SS':
            rank = '<:osurankSS:971559056537960509>'
        elif rank == 'S':
            rank = '<:osurankS:971558974690312213>'
        elif rank == 'A':
            rank = '<:osurankA:971559105187680266>'
        elif rank == 'B':
            rank = '<:osurankB:971559146967146586>'
        elif rank == 'C':
            rank = '<:osurankC:971559185546346536>'
        elif rank == 'D':
            rank = '<:osurankD:971559256421711933>'
        else:
            await ctx.send(f'rank??? {rank}')
        if not mods:
            mods = 'NM'
        else:
            mods = " ".join(mods)
            for x in range(len(mods)):
                modslist = modslist + mods[x] + ' '
        embed = discord.Embed(
            title=f'{title} [{difficulty}] +{mods} [{stars}★]',
            description=f'''▸ {rank} ▸ {pp}pp ▸ {accuracy}%
                    ▸ {"{:,}".format(score)} ▸ {combo}x ▸ [{statistics.get("count_300")}/{statistics.get("count_100")}/{statistics.get("count_50")}/{statistics.get("count_miss")}]
                    ▸ Score set on: {response.json()[0].get('created_at')[:10]}''',
            color=int(str(ctx.author.color)[1:], 16)
        )
        embed.set_thumbnail(url=cover)
        embed.timestamp = ctx.message.created_at
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Osu(bot))
