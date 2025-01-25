import discord
import requests
import json
from discord.ext import commands
from dotenv import load_dotenv
import os
from discord.commands import option
from database import db_osu_insert_user, db_osu_get_user
from custom_exceptions import OsuAccountNotLinkedError
from logger import *


API_URL = 'https://osu.ppy.sh/api/v2'
TOKEN_URL = "https://osu.ppy.sh/oauth/token"

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
        log_error(f"Token not found in osu!api response")
        return None
    
    return token


def clean_mode(mode: str, type: str):
    match type:
        case 'display': # for osu!{mode}
            match mode:
                case 'Standard': return 'std'
                case 'Taiko':    return 'taiko'
                case 'Catch':    return 'catch'
                case 'Mania':    return 'mania'
                case _:          return 'std'
        case 'api': # for api requests
            match mode:
                case 'Standard': return 'osu'
                case 'Taiko':    return 'taiko'
                case 'Catch':    return 'ctb'
                case 'Mania':    return 'mania'
                case _:          return 'osu'
        case 'website': # for website links
            match mode:
                case 'Standard': return 'osu'
                case 'Taiko':    return 'taiko'
                case 'Catch':    return 'fruits'
                case 'Mania':    return 'mania'
                case _:          return 'osu'
        case _: return 'osu'
        
def username_to_id(username: str):
    try:
        token = get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(f'{API_URL}/users/{username}', headers=headers)
        response.raise_for_status()
        return response.json().get('id')
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching user ID: {e}")
        return None


def id_to_username(userid: int):
    try:
        token = get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

        response = requests.get(f'{API_URL}/users/{userid}', headers=headers)
        response.raise_for_status()
        return response.json().get('username')
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching username: {e}")
        return None


class Osu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    osu_group = discord.SlashCommandGroup(
        name = "osu", 
        description = "osu! related commands",
        integration_types = {discord.IntegrationType.guild_install, discord.IntegrationType.user_install}
    )


    @osu_group.command(name="top", description="Gets osu! play data.")
    @option("mode", type=str, description="Pick a gamemode", choices=["Standard", "Taiko", "Catch", "Mania"])
    async def osu_play(self, ctx, mode: str, index: int = 1, user: str = ''):
        # validate parameters
        index = max(1, index)
        if index > 100:
            await ctx.respond("The index must be between 1 and 100.", ephemeral=True)
            return

        # get user ID from database
        if user == '':
            user = db_osu_get_user(ctx.author.id)
            if user is None:
                raise OsuAccountNotLinkedError
        # if its a username
        elif not user.isdigit():
            user = username_to_id(user)
            if user is None:
                await ctx.respond(f"Could not find an osu! account with the username `{user}`.", ephemeral=True)
                return

        # make the API request
        token = get_token()
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        params = {'mode': clean_mode(mode, 'api'), 'limit': index}

        try:
            response = requests.get(f'{API_URL}/users/{user}/scores/best', params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            await ctx.respond(f"Failed to fetch data: {e}", ephemeral=True)
            return

        # extract play data
        play = data[index - 1]
        rank = rank_emojis.get(play.get('rank'), "Unknown rank")
        mods = 'NM' if not play.get('mods') else ' '.join(play.get('mods'))

        embed = discord.Embed(
            title=f"#{index} Top osu!{clean_mode(mode, 'display')} Play for {play['user']['username']}",
            description=f"",
            color=int(str(ctx.author.color)[1:], 16) if ctx.author.color else discord.Color.blurple()
        )
        embed.set_thumbnail(url=play.get('beatmapset', {}).get('covers', {}).get('list@2x', ''))
        embed.timestamp = discord.utils.utcnow()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        embed.add_field(
            name=f"{play['beatmapset']['title']} [{play['beatmap']['version']}] [{play['beatmap']['difficulty_rating']}★]",
            # name=f"[{play['beatmapset']['title']} [{play['beatmap']['version']}] [{play['beatmap']['difficulty_rating']}★]](https://osu.ppy.sh/beatmapsets/{play['beatmapset']['id']}#{clean_mode(mode, 'website')}/{play['beatmap']['id']})",
            value=f"""
            ▸ {rank} ▸ {play['pp']}pp ▸ {round(play['accuracy'] * 100, 2)}% ▸ +{mods}
            ▸ {"{:,}".format(play['score'])} ▸ {play['max_combo']}x ▸ [{play['statistics']['count_300']}/{play['statistics']['count_100']}/{play['statistics']['count_50']}/{play['statistics']['count_miss']}]
            ▸ Score set on: {play['created_at'][:10]}
            """,
            inline=False
        )
        await ctx.respond(embed=embed)


    # @osu_group.command(name="osu play", description="Gets osu! play data.", integration_types={discord.IntegrationType.guild_install, discord.IntegrationType.user_install})
    # @option("mode", type=str, description="Pick a gamemode", choices=["Standard", "Taiko", "Catch", "Mania"])
    # async def osutop(self, ctx, mode, userid: str = 'def'):
    #     token = get_token()
    #     headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'Bearer {token}'}
    #     if userid == 'def':
    #         with open('data/osuaccounts.json', 'r') as f:
    #             accounts = json.load(f)
    #             userid = accounts[str(ctx.author.id)]
    #             f.close()
    #     if mode == 'def':
    #         params = {'limit': 5}
    #     else:
    #         params = {'mode': mode, 'limit': 5}
    #     response = requests.get(f'{API_URL}/users/{userid}/scores/best', params=params, headers=headers)
    #     user = response.json()[0].get('user', {}).get('username')
    #     if mode == 'def':
    #         mode = response.json()[0].get('beatmap', {}).get('mode')
    #     modevis = 'Standard'
    #     if mode == 'taiko':
    #         modevis = 'Taiko'
    #     elif mode == 'ctb':
    #         modevis = 'Catch the Beat'
    #     elif mode == 'mania':
    #         modevis = 'Mania'
    #     embed = discord.Embed(
    #         title=f'Top 5 osu! {modevis} plays for {user}',
    #         description='',
    #         color=int(str(ctx.author.color)[1:], 16)
    #     )
    #     embed.set_thumbnail(url=ctx.author.avatar.url)
    #     embed.timestamp = ctx.message.created_at
    #     embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
    #     for i in range(0, 5):
    #         cover = response.json()[i].get('beatmapset', {}).get('covers', {}).get('list@2x')
    #         title = response.json()[i].get('beatmapset', {}).get('title')
    #         artist = response.json()[i].get('beatmapset', {}).get('artist')
    #         difficulty = response.json()[i].get('beatmap', {}).get('version')
    #         mods = response.json()[i].get('mods')
    #         combo = response.json()[i].get('max_combo')
    #         score = response.json()[i].get('score')
    #         pp = round(response.json()[i].get('pp'), 2)
    #         stars = response.json()[i].get('beatmap', {}).get('difficulty_rating')
    #         rank = response.json()[i].get('rank')
    #         accuracy = round(response.json()[i].get('accuracy') * 100, 2)
    #         statistics = response.json()[i].get('statistics')
    #         modslist = ''
    #         if rank == 'SS':
    #             rank = '<:osurankSS:971559056537960509>'
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
    #         embed.add_field(
    #             name=f'{i + 1}. {title} [{difficulty}] +{mods} [{stars}★]',
    #             value=f'''▸ {rank} ▸ {pp}pp ▸ {accuracy}%
    #         ▸ {"{:,}".format(score)} ▸ {combo}x ▸ [{statistics.get("count_300")}/{statistics.get("count_100")}/{statistics.get("count_50")}/{statistics.get("count_miss")}]
    #         ▸ Score set on: {response.json()[i].get('created_at')[:10]}''',
    #             inline=False
    #         )
    #     await ctx.send(embed=embed)
    
        
    @osu_group.command(name="link", description="Link your osu! account with your Discord account.")
    async def osu_link(self, ctx, username: str):
        id = username_to_id(username)
        if not id:
            await ctx.respond(f"Could not find an osu! account with the username `{username}`.", ephemeral=True)
            return
        
        db_osu_insert_user(ctx.author.id, id)

        await ctx.respond(f"Successfully linked your osu! account `{username}` to your Discord account.")


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
