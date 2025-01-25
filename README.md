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

> [!NOTE]
> There are many specific references to me, the servers I'm in, and specific channels. Feel free to change or delete them!

---

## Setup

Follow these steps to set up and run the bot:

### 1. Install Python

Ensure you have **Python 3.7 or higher** installed on your system
You can download Python [here](https://www.python.org/downloads/)

### 2. Clone the Repository

Download or clone this repository to your local machine:

```bash
git clone https://github.com/tylersfoot/tylersbot.git
cd tylersbot
```

### 3. Install Dependencies

Use `pip` to install the required libraries:

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Create a `.env` file in the project directory and add the following variables:

```env
DISCORD_TOKEN='discord_bot_token'
OSU_CLIENT_ID='osu_api_client_id'
OSU_CLIENT_SECRET='osu_api_client_secret'
```

Replace the placeholders (your_discord_bot_token, etc.) with your actual credentials:

- `DISCORD_TOKEN`: Your Discord bot token (from the Discord Developer Portal)
- `OSU_CLIENT_ID` and `OSU_CLIENT_SECRET`: Your osu! API client ID and secret [(instructions)](https://osu.ppy.sh/docs/index.html#registering-an-oauth-application)

### 5. Start the bot

Run the bot with:

```bash
python -u bot.py
```

The bot will now start and log into Discord!

### Troubleshooting

- If you encounter any issues, ensure all dependencies are installed correctly and that your .env file is properly configured
- For more help, feel free to reach out!

---

## Features/Commands

### Notes

Command Table Explanation:

`Command`: the format of the slash command
> if it's in a command group, there will be a space (e.g. `/group command`)
> everything else is the parameters:type

`Description`: a description of what the command does

`Permissions`: what permission(s) the user needs to run the command
> `Dev`: can only be used by developers (note: will be removed soon)
> otherwise discord permissions (e.g. `manage_messages`, `ban_members`)

`Scope`: where the command is available:
> `Server`: A normal server slash command
> `Global`: command/app available everywhere (dms, other servers) - bot must be user installed

`Type`: whether it's a slash command or a user app
> `User`: available as a user app (right click on a user to use)
> `Slash`: available as a slash command

### bot.py

| Command                     | Description                                      | Permissions  | Scope  | Type  |
| ---                         | ---                                              | ---          | ---    | ---   |
| `/bot uptime`               | returns the uptime of the bot since last restart | -            | Server | Slash |
| `/bot ping`                 | returns the bot's latency/ping                   | -            | Server | Slash |
| `/bot unload extension:str` | unloads a specified cog or all cogs              | Dev          | Server | Slash |
| `/bot reload extension:str` | reloads/loads a specified cog or all cogs        | Dev          | Server | Slash |
| `/bot sync`                 | syncs all slash commands                         | Dev          | Server | Slash |
| `/bot clear_temp`           | deletes all files in the bot's temp folder       | Dev          | Server | Slash |
| `/bot stop`                 | stops the instance of the bot                    | Dev          | Server | Slash |

### calculator.py

| Command                     | Description                          | Permissions | Scope  | Type  |
| ---                         | ---                                  | ---         | ---    | ---   |
| `/calculate expression:str` | calculates the given math expression | -           | Global | Slash |

### fun.py

| Command                                                      | Description                     | Permissions | Scope  | Type  |
| ---                                                          | ---                             | ---         | ---    | ---   |
| `/fun 8ball question:str`                                    | lets the 8ball decide your fate | -           | Global | Slash |
| `/fun say message:str`                                       | makes the bot say a message     | -           | Global | Slash |
| `/fun coinflip`                                              | flips a coin                    | -           | Global | Slash |
| `/fun punch user:discord.Member`                             | punches the user mentioned      | -           | Global | Slash |
| `/fun doublepunch user1:discord.Member user2:discord.Member` | punches two users mentioned     | -           | Global | Slash |

Also has functionality for reacting to messages with certain keywords, and a rare chance to respond with a special message

### information.py

| Command                                             | Description                                        | Permissions | Scope  | Type        |
| ---                                                 | ---                                                | ---         | ---    | ---         |
| `/info suggestion text:str`                         | sends a suggestion to the developers               | -           | Global | Slash       |
| `/info bugreport text:str`                          | sends a bugreport to the developers                | -           | Global | Slash       |
| `/info server_count`                                | sends the number of servers the bot is in          | -           | Global | Slash       |
| `/info invite_link`                                 | sends the invite link for the bot & discord server | -           | Global | Slash       |
| `/info avatar member:discord.Member`                | sends the avatar for the user mentioned            | -           | Global | Slash, User |
| `/info serverinfo`                                  | sends information about the current server         | -           | Global | Slash       |
| `/info account_creation_date member:discord.Member` | sends the date of the user's account creation      | -           | Global | Slash, User |

### moderation.py

| Command                                                     | Description                                                                     | Permissions       | Scope  | Type  |
| ---                                                         | ---                                                                             | ---               | ---    | ---   |
| `/mod purge amount:int`                                     | purges (deletes) messages from a channel                                        | `manage_messages` | Server | Slash |
| `/mod kick user:discord.Member reason:str notify:bool=True` | kicks a user from the server with the specified reason, and whether to DM them  | `kick_members`    | Server | Slash |
| `/mod ban user:discord.Member reason:str notify:bool=True`  | bans a user from the server with the specified reason, and whether to DM them   | `ban_members`     | Server | Slash |
| `/mod unban user_id:str reason:str notify:bool=True`        | unbans a user from the server with the specified reason, and whether to DM them | `ban_members`     | Server | Slash |
| `/mod slowmode duration:str`                                | changes the slowmode for the current channel (`10s`, `5m`, `1h`, `off`)         | `manage_guild`    | Server | Slash |

Also has basic functionality for logging deleted messages

### qrcode.py

| Command           | Description                                                                                           | Permissions | Scope  | Type  |
| ---               | ---                                                                                                   | ---         | ---    | ---   |
| `/qr message:str` | generates a qr code image based on the message provided. also detects if an amongus is in the qr code | -           | Global | Slash |

### wiki.py

| Command                     | Description                                     | Permissions | Scope  | Type        |
| ---                         | ---                                             | ---         | ---    | ---         |
| `/wiki search request:str`  | searches sends a list of Wikipedia articles     | -           | Global | Slash       |
| `/wiki article request:str` | sends a summary of a specific Wikipedia article | -           | Global | Slash       |
| `/wiki random`              | sends a summary of a random Wikipedia article   | -           | Global | Slash       |

### osu.py

### wordle.py

(WIP)

### music.py

### selfroles.py

(WIP)

### commanderrorhandler.py

Handles customized error messages
