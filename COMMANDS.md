# tylersbot — Command Reference

This document lists all slash commands and internal functionality available in the `tylersbot` Discord bot.

- For setup instructions, see the [README](./README.md)

---

## Command Table Guide

Each command entry is documented using the following columns:

- **Command** — the full slash command syntax  
  - if it’s in a command group, it’ll show like `/group command`  
  - parameters are formatted as `param:type` (with `?` for optional)
- **Description** — what the command does
- **Permissions** — user permissions required to use it
  - `Dev`: can only be used by developers (deprecated soon)  
  - otherwise, Discord permissions (e.g., `manage_messages`, `ban_members`)
- **Scope** — where the command is available
  - `Server`: a normal server slash command
  - `Global`: a command/app available everywhere (dms/servers) - bot must be user installed
- **Type** — whether it's a slash or user app command
  - `User`: available as a user app (right click on a user to use)
  - `Slash`: available as a slash command

---

## Core Bot Commands

Source: [bot.py](bot.py)

| Command                     | Description                                      | Permissions  | Scope  | Type  |
| ---                         | ---                                              | ---          | ---    | ---   |
| `/bot uptime`               | returns the uptime of the bot since last restart | -            | Server | Slash |
| `/bot ping`                 | returns the bot's latency/ping                   | -            | Server | Slash |
| `/dev unload extension:str` | unloads a specified cog or all cogs              | Dev          | Server | Slash |
| `/dev reload extension:str` | reloads/loads a specified cog or all cogs        | Dev          | Server | Slash |
| `/dev sync`                 | syncs all slash commands                         | Dev          | Server | Slash |
| `/dev clear_temp`           | deletes all files in the bot's temp folder       | Dev          | Server | Slash |
| `/dev stop`                 | stops the instance of the bot                    | Dev          | Server | Slash |

---

## Fun & Misc

Source: [fun.py](cogs/fun.py)

- Can be configured to react to certain keywords in messages
- Rare chance to send special responses

| Command                                                      | Description                     | Permissions | Scope  | Type  |
| ---                                                          | ---                             | ---         | ---    | ---   |
| `/fun 8ball question:str`                                    | lets the 8ball decide your fate | -           | Global | Slash |
| `/fun say message:str`                                       | makes the bot say a message     | -           | Global | Slash |
| `/fun coinflip`                                              | flips a coin                    | -           | Global | Slash |
| `/fun punch user:discord.Member`                             | punches the user mentioned      | -           | Global | Slash |
| `/fun doublepunch user1:discord.Member user2:discord.Member` | punches two users mentioned     | -           | Global | Slash |

---

## Information

Source: [information.py](cogs/information.py)

| Command                                              | Description                                        | Permissions | Scope  | Type        |
| ---                                                  | ---                                                | ---         | ---    | ---         |
| `/info suggestion text:str`                          | sends a suggestion to the developers               | -           | Global | Slash       |
| `/info bugreport text:str`                           | sends a bugreport to the developers                | -           | Global | Slash       |
| `/info server_count`                                 | sends the number of servers the bot is in          | -           | Global | Slash       |
| `/info invite`                                       | sends the invite link for the bot & discord server | -           | Global | Slash       |
| `/info avatar member:discord.Member?`                | sends the avatar for the user mentioned            | -           | Global | Slash, User |
| `/info server_info`                                   | sends information about the current server         | -           | Global | Slash       |
| `/info account_creation_date member:discord.Member?` | sends the date of the user's account creation      | -           | Global | Slash, User |

---

## Moderation

Source: [moderation.py](cogs/moderation.py)

- Has functionality for logging deleted messages in a server (set using `/mod log_channel`)

| Command                                                     | Description                                                                     | Permissions       | Scope  | Type  |
| ---                                                         | ---                                                                             | ---               | ---    | ---   |
| `/mod purge amount:int`                                     | purges (deletes) messages from a channel                                        | `manage_messages` | Server | Slash |
| `/mod kick user:discord.Member reason:str notify:bool=True` | kicks a user from the server with the specified reason, and whether to DM them  | `kick_members`    | Server | Slash |
| `/mod ban user:discord.Member reason:str notify:bool=True`  | bans a user from the server with the specified reason, and whether to DM them   | `ban_members`     | Server | Slash |
| `/mod unban user_id:str reason:str notify:bool=True`        | unbans a user from the server with the specified reason, and whether to DM them | `ban_members`     | Server | Slash |
| `/mod slowmode duration:str`                                | changes the slowmode for the current channel (`10s`, `5m`, `1h`, `off`)         | `manage_guild`    | Server | Slash |
| `/mod log_channel channel:discord.TextChannel`              | sets the log channel for a server                                               | `manage_guild`    | Server | Slash |

---

## Calculator

Source: [calculator.py](cogs/calculator.py)

| Command                     | Description                          | Permissions | Scope  | Type  |
| ---                         | ---                                  | ---         | ---    | ---   |
| `/calculate expression:str` | calculates the given math expression | -           | Global | Slash |

---

## QR Codes

Source: [qrcode.py](cogs/qrcode.py)

| Command           | Description                                                                                           | Permissions | Scope  | Type  |
| ---               | ---                                                                                                   | ---         | ---    | ---   |
| `/qr message:str` | generates a qr code image based on the message provided. also detects if an amongus is in the qr code | -           | Global | Slash |

---

## Wikipedia

Source: [wiki.py](cogs/wiki.py)

| Command                     | Description                                     | Permissions | Scope  | Type  |
| ---                         | ---                                             | ---         | ---    | ---   |
| `/wiki search request:str`  | sends a list of Wikipedia articles              | -           | Global | Slash |
| `/wiki article request:str` | sends a summary of a specific Wikipedia article | -           | Global | Slash |
| `/wiki random`              | sends a summary of a random Wikipedia article   | -           | Global | Slash |

---

## osu! Integration

Source: [osu.py](cogs/osu.py)

| Command                                        | Description                                           | Permissions | Scope  | Type  |
| ---                                            | ---                                                   | ---         | ---    | ---   |
| `/osu link username:str`                       | links an osu! account with the user's discord account | -           | Global | Slash |
| `/osu play mode:str? index:int? user:str?`     | sends an osu! play from the user's top plays          | -           | Global | Slash |
| `/osu recent mode:str? user:str?`              | sends the user's most recent osu! play                | -           | Global | Slash |

---

## Internals

### Error Handling

#### Command Error Handler

Source: [commanderrorhandler.py](cogs/commanderrorhandler.py)

Handles all command-related errors in a centralized way.

- Catches both command-specific and general errors
- Displays custom error messages using Discord embeds
- Integrates with `customexceptions.py` for better error reuse
- Prevents default traceback spam in Discord

#### Custom Exceptions

Source: [customexceptions.py](core/customexceptions.py)

Defines reusable exceptions for common error types.

- Used to raise shared logic-based errors across multiple commands
- Pairs with `commanderrorhandler.py` for clean display
- Reduces repetitive checks and messages in individual cogs

---

### Logging

Source: [logger.py](core/logger.py)

A basic logging system with 3 levels: `info`, `warning`, and `error`.

- Outputs to console
- Writes to `data/bot.log`
- Can optionally send logs to a Discord channel if configured

---

### Database

Source: [database.py](core/database.py)

Handles persistent data storage using SQLite.

- Manages osu! account linking per user
- Stores server-specific log channel settings
- DB file is stored in `data/bot_data.db`
