<img align="right" src="https://raw.githubusercontent.com/tylersfoot/tylersbot/main/assets/icon.png" height="200" width="200">

# tylersbot

[![Discord](https://discordapp.com/api/guilds/962179884627669062/widget.png)](https://discord.gg/DKpCvsJ4fp)
[![License](https://img.shields.io/github/license/tylersfoot/tylersbot)](LICENSE)
![Last Commit](https://img.shields.io/github/last-commit/tylersfoot/tylersbot)
![Commit Frequency](https://img.shields.io/github/commit-activity/y/tylersfoot/tylersbot)
![Followers](https://img.shields.io/github/followers/tylersfoot)
![Stars](https://img.shields.io/github/stars/tylersfoot/tylersbot)
![Files](https://img.shields.io/github/directory-file-count/tylersfoot/tylersbot)
![Size](https://img.shields.io/github/repo-size/tylersfoot/tylersbot)
![Language](https://img.shields.io/github/languages/top/tylersfoot/tylersbot)

My personal Discord bot, developed using Pycord (migrated from discord.py). My first major coding project. Feel free to give me any questions, feedback, suggestions, bug reports, or to use the code for yourself.

Development Discord Server: [https://discord.gg/DKpCvsJ4fp](https://discord.gg/DKpCvsJ4fp)

---

## Setup

Install Python 3.7+

Download the repository files

Install the required libraries:

```bash
pip install -r requirements.txt
```

Create a `.env` file with the following template:

```env
DISCORD_TOKEN = your_discord_bot_token
HUGGINGFACE_TOKEN = your_huggingface_token
CHATBOT_EMAIL = your_openai_email
CHATBOT_PASSWORD = your_openai_password
```

Finally, start the bot!

```bash
python bot.py
```

Note: There are references to me or the servers I'm in. Feel free to change them, such as: reporting errors to tylersfoot#8888 and the `developers` variable in `bot.py`.

---

## Features/Commands

[DEV] = developer only command (temporary)

(user) = available as a user app (right click on user to use)

(global) = command available everywhere (dms, other servers) - USER INSTALL ONLY

### bot.py

`/uptime` - returns the uptime of the bot since last restart

`/ping` - returns the bot's latency/ping

`[DEV] /unload extension:str` - unloads a specified cog or all cogs

`[DEV] /reload extension:str` - reloads/loads a specified cog or all cogs

`[DEV] /sync` - syncs all slash commands

`[DEV] /clear_temp` - deletes all files in the bot's temp folder

`[DEV] /stopbot` - stops the instance of the bot

### calculator.py

`/calculate expression:str` - calculates the given mathematical expression

### commanderrorhandler.py

Handles customized error messages

### fun.py

`/8ball question:str` - (global) lets the 8ball decide your fate

`/say message:str` - (global) makes the bot say the message specified

`/coinflip` - (global) flips a coin. duh.

`/punch user:discord.Member` - (global) punches the user mentioned

`/doublepunch user1:discord.Member user2:discord.Member` - (global) punches two users mentioned

Also has functionality for reacting to messages with certain keywords, and a rare chance to respond with a special message

### information.py

`/suggestion text:str` - sends a suggestion to the developer(s)

`/bugreport text:str` - sends a bugreport to the developer(s)

`/server_count` - returns the number of servers the bot is in

`/invite_link` - (global) sends the invite link for the bot & the discord server

`/avatar member:discord.Member` - (global) (user) returns the avatar for the user mentioned (author if none)

`/serverinfo` - (global) returns information about the current server

`/account_creation_date member:discord.Member` - (global) (user) returns the date of the user's account creation

### moderation.py

`/purge amount:int` - purges (deletes) a certain amount of messages from a channel

`/kick user:discord.Member reason:str notify:bool=True` - kicks a user from the server with the specified reason, and whether to DM them

`/ban user:discord.Member reason:str notify:bool=True` - bans a user from the server with the specified reason, and whether to DM them

`/unban user_id:str reason:str notify:bool=True` - unbans a user from the server with the specified reason, and whether to DM them

`/slowmode duration:str` - changes the slowmode for the current channel. string is parsed as a time (`10s`, `5m`, `1h`, `off`, etc.)

Also has functionality for logging deleted messages

### qrcode.py

`/qr message:str` - generates a qr code image based on the message provided. also detects if an amongus is in the qr code :)

### osu.py


### wiki.py
`/wikisearch request:str` - returns a list of Wikipedia articles based on the request

`/wiki request:str` - returns a summary of the specified Wikipedia article

`/wikirandom` - returns the summary of a random Wikipedia article

### wordle.py
(WIP)

### music.py




### selfroles.py
(WIP)
