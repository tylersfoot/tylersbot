import discord
import datetime
import os
import asyncio

log_channel_ids = [1332622268483764234]
log_file_path = "data/bot.log"
bot = None

def logger_initialize(bot_instance):
    global bot
    bot = bot_instance
    
    # init bot.log file
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    if os.path.exists(log_file_path):
        os.remove(log_file_path)
    with open(log_file_path, "w"):
        pass
    print(f"Logger initialized. Logging to {log_file_path}")
 
    
async def _log(level: str, message: str, color: discord.Color):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{level}] {message}"
    
    # print log
    print(log_message)
    
    # write to log file
    with open(log_file_path, "a") as log_file:
        log_file.write(log_message + "\n")
    
    # send to discord channel
    embed = discord.Embed(
        title=f"Logger: [{level}]",
        description=message,
        color=color
    )
    embed.timestamp = datetime.datetime.now()
    
    for channel_id in log_channel_ids:
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