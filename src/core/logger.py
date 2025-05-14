import discord
import datetime
import os
import asyncio
from core.paths import DATA_PATH
from config.config import LOG_CHANNEL_IDS

log_file_path = os.path.join(DATA_PATH, "bot.log")
bot = None

# ansi color codes
LOG_COLORS = {
    "INFO": "\033[92m",  # green
    "WARNING": "\033[93m",  # yellow
    "ERROR": "\033[91m",  # red
    "DIM": "\033[90m",  # dark gray
    "RESET": "\033[0m",
}


def logger_initialize(bot_instance):
    global bot
    bot = bot_instance

    # init bot.log file
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    with open(log_file_path, "w"):
        pass
    asyncio.create_task(
        _log(
            "INFO",
            f"Logger initialized. Logging to {log_file_path}",
            discord.Color.green(),
        )
    )


async def _log(level: str, message: str, color: discord.Color):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    dim = LOG_COLORS["DIM"]
    level_color = LOG_COLORS.get(level, "")
    reset = LOG_COLORS["RESET"]

    log_message = f"[{timestamp}] [{level}] {message}"
    log_message_color = (
        f"[{dim}{timestamp}{reset}] [{level_color}{level}{reset}] {message}"
    )
    print(log_message_color)

    # write to log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message + "\n")

    # send to discord channel
    embed = discord.Embed(title=f"Logger: [{level}]", description=message, color=color)
    embed.timestamp = datetime.datetime.now()

    for channel_id in LOG_CHANNEL_IDS:
        try:
            channel = await bot.fetch_channel(channel_id)
            if channel:
                await channel.send(embed=embed)
        except Exception as e:
            print(f"Failed to send log to channel {channel_id}: {e}")


def log_info(message):
    asyncio.create_task(_log("INFO", message, discord.Color.green()))


def log_warning(message):
    asyncio.create_task(_log("WARNING", message, discord.Color.yellow()))


def log_error(message):
    asyncio.create_task(_log("ERROR", message, discord.Color.red()))
