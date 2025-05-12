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

Invite the bot [here!](https://discord.com/oauth2/authorize?client_id=1059528586815606784)

> [!NOTE]
> There are many specific references to me, the servers I'm in, and specific channels. Feel free to change or delete them!

---

## Setup

The bot can be run [manually](#manual-setup) using Python and a virtual environment, or using [Docker](#docker-setup) for containerized deployment.

### Troubleshooting

- If you encounter any issues, ensure all dependencies are installed correctly and that your .env file is properly configured
- For more help, feel free to reach out!

---

## Manual setup

### 1. Install Python

Ensure you have **Python 3.9 or higher** installed on your system. You can download Python [here](https://www.python.org/downloads/).

### 2. Clone the Repository

Download or clone the repository to your local machine:

```bash
git clone https://github.com/tylersfoot/tylersbot.git
cd tylersbot
```

### 3. Install Dependencies

> [!NOTE]
> To keep your dependencies isolated, it’s recommended to use a virtual environment!
> [Follow this guide](https://docs.python.org/3/tutorial/venv.html) to set up and activate a venv.

Use `pip` to install the required libraries:

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory and add the following variables:

```env
DISCORD_TOKEN='discord_bot_token'
OSU_CLIENT_ID='osu_api_client_id'
OSU_CLIENT_SECRET='osu_api_client_secret'
```

Replace the placeholders with your actual credentials:

- `DISCORD_TOKEN`: Your Discord bot token (from the Discord Developer Portal)
- `OSU_CLIENT_ID` and `OSU_CLIENT_SECRET`: Your osu! API client ID and secret [(instructions)](https://osu.ppy.sh/docs/index.html#registering-an-oauth-application)

### 5. Start the Bot

Run the bot with:

```bash
python -u bot.py
```

The bot will now start and log into Discord!

---

## Docker Setup

### 1. Build and Run the Container

```bash
docker compose up --build -d
```

### 2. Configure Environment Variables

Create a `.env` file in the project directory and add the following variables:

```env
DISCORD_TOKEN='discord_bot_token'
OSU_CLIENT_ID='osu_api_client_id'
OSU_CLIENT_SECRET='osu_api_client_secret'
```

### 3. Data Persistence

The bot saves logs, databases, and temporary files to the `./data/` directory, which is mapped as a persistent volume from `/app/data/` in the container.
For more info, see the [compose.yaml](compose.yaml) and [Dockerfile](Dockerfile).

---

## Commands & Internals

A full list of slash commands (with descriptions, parameters, and permissions), along with info about the bot's internals (logging, error handling, database) are documented in [COMMANDS.md](COMMANDS.md).
