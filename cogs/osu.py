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
import datetime


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
                case 'standard': return 'std'
                case 'taiko':    return 'taiko'
                case 'catch':    return 'catch'
                case 'mania':    return 'mania'
                case _:          return 'std'
        case 'api': # for api requests
            match mode:
                case 'standard': return 'osu'
                case 'taiko':    return 'taiko'
                case 'catch':    return 'fruits'
                case 'mania':    return 'mania'
                case _:          return 'osu'
        case 'website': # for website links
            match mode:
                case 'standard': return 'osu'
                case 'taiko':    return 'taiko'
                case 'catch':    return 'fruits'
                case 'mania':    return 'mania'
                case _:          return 'osu'
        case 'clean': # from website to normal again
            match mode:
                case 'osu':    return 'standard'
                case 'taiko':  return 'taiko'
                case 'fruits': return 'catch'
                case 'mania':  return 'mania'
                case _:        return 'standard'
        case _: return 'osu'
        

def clean_statistics(statistics: dict, mode: str):
    # returns the hit statistics for the mode (e.g. [300/100/50/miss])
    match mode:
        case 'standard':
            hit_counts = (f"[{statistics['count_300']}/{statistics['count_100']}/"
                            f"{statistics['count_50']}/{statistics['count_miss']}]")
        case 'taiko':
            hit_counts = (f"[{statistics['count_300']}/{statistics['count_100']}/"
                            f"{statistics['count_miss']}]")
        case 'catch':
            hit_counts = (f"[{statistics['count_300']}/{statistics['count_100']}/"
                            f"{statistics['count_50']}/{statistics['count_katu']}/"
                            f"{statistics['count_miss']}]")
        case 'mania':
            hit_counts = (f"[{statistics['count_300']}/{statistics['count_100']}/"
                            f"{statistics['count_50']}/{statistics['count_geki']}/"
                            f"{statistics['count_katu']}/{statistics['count_miss']}]")
        case _:
            hit_counts = (f"[{statistics['count_300']}/{statistics['count_100']}/"
                            f"{statistics['count_50']}/{statistics['count_geki']}/"
                            f"{statistics['count_katu']}/{statistics['count_miss']}]")
    return hit_counts
            
        
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


    @osu_group.command(name="play", description="Sends a play from the user's top plays.")
    @option("mode", type=str, description="Pick a gamemode", choices=["standard", "taiko", "catch", "mania"])
    async def osu_play(self, ctx, mode: str = '', index: int = 1, user: str = ''):
        # validate parameters
        index = max(min(index, 100), 1)

        # get user ID from database
        if not user:
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

        try:
            # get user data
            if mode:
                response_user = requests.get(f'{API_URL}/users/{user}/{clean_mode(mode, 'api')}', headers=headers)
            else:
                response_user = requests.get(f'{API_URL}/users/{user}', headers=headers)
            response_user.raise_for_status()
            data_user = response_user.json()
            
            # get play data
            if mode:
                params = {'mode': clean_mode(mode, 'api'), 'limit': index}
            else:
                mode = clean_mode(data_user.get('playmode'), 'clean')
                params = {'mode': clean_mode(mode, 'api'), 'limit': index}
            
            response_play = requests.get(f'{API_URL}/users/{user}/scores/best', params=params, headers=headers)
            response_play.raise_for_status()
            data_play = response_play.json()
        except requests.RequestException as error:
            if "Not Found" in str(error):
                await ctx.respond(f"Could not find an osu! account with the username or id `{user}`.", ephemeral=True)
            else:
                await ctx.respond(f"Failed to fetch data: {error}", ephemeral=True)
            return 

        # extract play data
        try:
            data_play = data_play[index - 1]
        except IndexError:
            await ctx.respond(f"Could not find a play at index `{index}`.", ephemeral=True)
            return
        
        play = {
            "rank": rank_emojis.get(data_play.get('rank'), "F"),
            "mods": 'NM' if not data_play.get('mods') else ''.join(data_play.get('mods')),
            "cover": data_play.get('beatmapset', {}).get('covers', {}).get('list@2x'),
            "title": data_play.get('beatmapset', {}).get('title'),
            "artist": data_play.get('beatmapset', {}).get('artist'),
            "difficulty": data_play.get('beatmap', {}).get('version'),
            "combo": data_play.get('max_combo'),
            "score": "{:,}".format(data_play.get('score')),
            "pp": round(data_play.get('pp'), 2) if data_play.get('pp') else 0,
            "stars": data_play.get('beatmap', {}).get('difficulty_rating'),
            "accuracy": round(data_play.get('accuracy') * 100, 2),
            "statistics": clean_statistics(data_play.get('statistics'), mode),
            "date": int(datetime.datetime.fromisoformat(data_play.get('created_at').replace("Z", "+00:00")).timestamp()),
            "map_link": f"https://osu.ppy.sh/beatmapsets/{data_play.get('beatmapset', {}).get('id')}#{clean_mode(mode, 'website')}/{data_play.get('beatmap', {}).get('id')}"
        }
        
        user_data = {
            "username": id_to_username(user),
            "avatar": data_user.get('avatar_url'),
            "country_code": data_user.get('country_code'),
            "pp": data_user.get('statistics').get('pp'),
            "global_rank": data_user.get('statistics').get('global_rank'),
            "country_rank": data_user.get('statistics').get('country_rank'),
        }
            
        embed = discord.Embed(
            title=f"#{index} Top osu!{clean_mode(mode, 'display')} Play for {user_data['username']}",
            description=f"",
            color=int(str(ctx.author.color)[1:], 16) if ctx.author.color else discord.Color.blurple()
        )
        embed.set_author(
            name=f"{user_data['username']}: {user_data['pp']}pp (#{user_data['global_rank']} {user_data['country_code']}{user_data['country_rank']})",
            icon_url=user_data['avatar'],
            url=f"https://osu.ppy.sh/users/{user}/{clean_mode(mode, 'website')}"
        )
        embed.add_field(
            name=f"{play['title']} [{play['difficulty']}] [{play['stars']}★]",
            # name={ title: f"{play['title']} [{play['difficulty']}] [{play['stars']}★]", url: play['map_link'] },
            # name="[balls](https://google.com)",
            value=f"""
            ▸ **{play['rank']} ▸ {play['pp']}pp ▸ {play['accuracy']}% ▸ +{play['mods']}**
            ▸ {play['score']} ▸ {play['combo']}x ▸ {play['statistics']}
            ▸ Score set <t:{play['date']}:R>
            """,
            inline=False
        )
        embed.set_thumbnail(url=play['cover'])
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        
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


    @osu_group.command(name="recent", description="Sends the user's most recent play.")
    @option("mode", type=str, description="Pick a gamemode", choices=["standard", "taiko", "catch", "mania"])
    async def osu_recent(self, ctx, mode: str = '', user: str = ''):
        # get user ID from database
        if not user:
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
        
        try:
            # get user data
            if mode:
                response_user = requests.get(f'{API_URL}/users/{user}/{clean_mode(mode, 'api')}', headers=headers)
            else:
                response_user = requests.get(f'{API_URL}/users/{user}', headers=headers)
            response_user.raise_for_status()
            data_user = response_user.json()
            
            # get play data
            if mode:
                params = {'mode': clean_mode(mode, 'api'), 'limit': 1, 'include_fails': '1'}
            else:
                mode = clean_mode(data_user.get('playmode'), 'clean')
                params = {'mode': clean_mode(mode, 'api'), 'limit': 1, 'include_fails': '1'}
            
            response_play = requests.get(f'{API_URL}/users/{user}/scores/recent', params=params, headers=headers)
            response_play.raise_for_status()
            data_play = response_play.json()
        except requests.RequestException as error:
            if "Not Found" in str(error):
                await ctx.respond(f"Could not find an osu! account with the username or id `{user}`.", ephemeral=True)
            else:
                await ctx.respond(f"Failed to fetch data: {error}", ephemeral=True)
            return 
        
        if str(data_play) == '[]':
            await ctx.respond("No recent scores found for that user/mode.", ephemeral=True)
            return
        
        # extract play data
        data_play = data_play[0]
        
        play = {
            "rank": rank_emojis.get(data_play.get('rank'), "F"),
            "mods": 'NM' if not data_play.get('mods') else ''.join(data_play.get('mods')),
            "cover": data_play.get('beatmapset', {}).get('covers', {}).get('list@2x'),
            "title": data_play.get('beatmapset', {}).get('title'),
            "artist": data_play.get('beatmapset', {}).get('artist'),
            "difficulty": data_play.get('beatmap', {}).get('version'),
            "combo": data_play.get('max_combo'),
            "score": "{:,}".format(data_play.get('score')),
            "pp": round(data_play.get('pp'), 2) if data_play.get('pp') else 0,
            "stars": data_play.get('beatmap', {}).get('difficulty_rating'),
            "accuracy": round(data_play.get('accuracy') * 100, 2),
            "statistics": clean_statistics(data_play.get('statistics'), mode),
            "date": int(datetime.datetime.fromisoformat(data_play.get('created_at').replace("Z", "+00:00")).timestamp()),
            "map_link": f"https://osu.ppy.sh/beatmapsets/{data_play.get('beatmapset', {}).get('id')}#{clean_mode(mode, 'website')}/{data_play.get('beatmap', {}).get('id')}"
        }
        
        user_data = {
            "username": id_to_username(user),
            "avatar": data_user.get('avatar_url'),
            "country_code": data_user.get('country_code'),
            "pp": data_user.get('statistics').get('pp'),
            "global_rank": data_user.get('statistics').get('global_rank'),
            "country_rank": data_user.get('statistics').get('country_rank'),
        }

        embed = discord.Embed(
            title=f"{play['artist']} - {play['title']} [{play['difficulty']}] [{play['stars']}★]",
            url=play['map_link'],
            description=f"""
            ▸ **{play['rank']} ▸ {play['pp']}pp ▸ {play['accuracy']}% ▸ +{play['mods']}**
            ▸ {play['score']} ▸ {play['combo']}x ▸ {play['statistics']}
            ▸ Score set <t:{play['date']}:R>
            """,
            color=int(str(ctx.author.color)[1:], 16) if ctx.author.color else discord.Color.blurple()
        )
        embed.set_author(
            name=f"{user_data['username']}: {user_data['pp']}pp (#{user_data['global_rank']} {user_data['country_code']}{user_data['country_rank']})",
            icon_url=user_data['avatar'],
            url=f"https://osu.ppy.sh/users/{user}/{clean_mode(mode, 'website')}"
        )
        embed.set_thumbnail(url=play['cover'])
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=ctx.author.avatar.url)
        
        await ctx.respond(embed=embed)
        
                
    @osu_group.command(name="link", description="Link your osu! account with your Discord account.")
    async def osu_link(self, ctx, username: str):
        id = username_to_id(username)
        if not id:
            await ctx.respond(f"Could not find an osu! account with the username `{username}`.", ephemeral=True)
            return
        
        db_osu_insert_user(ctx.author.id, id)

        await ctx.respond(f"Successfully linked your osu! account `{username}` to your Discord account.")


def setup(bot):
    bot.add_cog(Osu(bot))
