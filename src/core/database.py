import sqlite3
from core.logger import log_info, log_error


DB_PATH = "data/bot_data.db"


# connect with the db and create tables if they don't exist
def db_initialize():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # osu table
    # user_id: discord user id
    # osu_id: osu id
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS osu_accounts (
        user_id INTEGER PRIMARY KEY,
        osu_id INTEGER NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guilds (
        guild_id INTEGER PRIMARY KEY,
        log_channel_id INTEGER NOT NULL
    )
    """)

    connection.commit()
    connection.close()
    log_info("Database initialized")


def db_osu_insert_user(user_id: int, osu_id: int):
    # inserts/updates an osu! user id into the database
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO osu_accounts (user_id, osu_id) VALUES (?, ?)",
            (user_id, osu_id),
        )
        connection.commit()
        log_info(f"Inserted user {user_id} with osu! id {osu_id}")
    except sqlite3.Error as e:
        log_error(f"Database error occurred: {e}")
    finally:
        connection.close()


def db_osu_get_user(user_id: int):
    # gets the osu! user id from the database
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT osu_id FROM osu_accounts WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        log_error(f"Database error occurred: {e}")
        return None
    finally:
        connection.close()


def db_guild_insert_log(guild_id: int, log_channel_id: int):
    # inserts/updates a guild's log channel into the database
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO guilds (guild_id, log_channel_id) VALUES (?, ?)",
            (guild_id, log_channel_id),
        )
        connection.commit()
        log_info(f"Linked log channel {log_channel_id} to guild {guild_id}")
    except sqlite3.Error as e:
        log_error(f"Database error occurred: {e}")
    finally:
        connection.close()


def db_guild_get_log(guild_id: int):
    # gets the guild's log channel from the database
    try:
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute(
            "SELECT log_channel_id FROM guilds WHERE guild_id = ?", (guild_id,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    except sqlite3.Error as e:
        log_error(f"Database error occurred: {e}")
        return None
    finally:
        connection.close()
