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

Development Discord Server: https://discord.gg/DKpCvsJ4fp

---

## Setup:

First, install the required libraries:

```
pip install -r requirements.txt
```

Create a `.env` file with the following template:

```
DISCORD_TOKEN = your_discord_bot_token
HUGGINGFACE_TOKEN = your_huggingface_token
CHATBOT_EMAIL = your_openai_email
CHATBOT_PASSWORD = your_openai_password
```

Finally, start the bot!

```
python bot.py
```

---

## Features/Commands:
### bot.py
`/uptime` - returns the uptime of the bot since last restart

`.prefix` - returns the current guild's prefix (soon depreciated)

`/ping` - returns the bot's ping

`/update_guilds` - updates the bot's guild count

`[DEV] /unload extension:str` - unloads a specified cog or all cogs

`[DEV] /reload extension:str` - reloads/loads a specified cog or all cogs

`[DEV] /sync` - syncs all slash commands

`[DEV] /clear_temp` - deletes all files in the bot's temp folder

### calculator.py
`/calc expression:str` - calculates the given expression

### chatbot.py
`/chat prompt:str` - sends a prompt to the chatbot and returns the response

`/chatlogin` - logs in to the chatbot

`/chatrefresh` - refreshes the chatbot's thread and deletes previous context

### commanderrorhandler.py
(WIP)

### fun.py
`/eightball question:str` - lets the 8ball decide your fate

`/say message:str` - makes the bot say the message specified

`/poll question:str` - creates a poll in the current channel

`/coinflip` - flips a coin. duh.

`/punch user:discord.Member` - punches the user mentioned

`/doublepunch user1:discord.Member user2:discord.Member` - punches two users mentioned

`/roundhousekick users:str` - roundhouse kicks all people mentioned

`[DEV] /removerole user:discord.Member role:discord.Role` - removes the specified role from the specified user

### imagegen.py
`/img prompt:str` - generates 9 images based on the prompt using Craiyon AI

### information.py
`/suggestion text:str` - sends a suggestion to the developer(s)

`/bugreport text:str` - sends a bugreport to the developer(s)

`/servercount` - returns the number of servers the bot is in

`/invitelink` - sends the invite link for the bot & the discord server

`/avatar member:discord.Member` - returns the avatar for the user mentioned (author if none)

`/serverinfo` - returns information about the current server

### moderation.py
(WIP)

### music.py
(WIP)

### osu.py
(WIP)

### qrcode.py

### selfroles.py
(WIP)

### wiki.py
`/wikisearch request:str` - returns a list of Wikipedia articles based on the request

`/wiki request:str` - returns a summary of the specified Wikipedia article

`/wikirandom` - returns the summary of a random Wikipedia article

### wordle.py
(WIP)
