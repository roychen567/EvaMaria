import logging
import logging.config
import os  
from datetime import datetime
from pyrogram import Client, __version__, idle
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from aiohttp import web
from plugins import web_server

# Get logging configurations
try:
    logging.config.fileConfig('logging.conf')
except Exception as e:
    logging.error(f"Failed to load logging configuration: {e}")

logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

PORT = os.environ.get("PORT", "8080")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
        )

    async def start(self):
        start_time = datetime.now()
        await super().start()

        try:
            await db.get_banned()
        except Exception as e:
            logging.error(f"Failed to get banned users or chats: {e}")

        try:
            await Media.ensure_indexes()
        except Exception as e:
            logging.error(f"Failed to ensure database indexes: {e}")

        try:
            await self.send_message(LOG_CHANNEL, LOG_STR)
        except Exception as e:
            logging.error(f"Failed to send start message to log channel: {e}")

        try:
            app_runner = web.AppRunner(await web_server())
            await app_runner.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app_runner, bind_address, PORT).start()
        except Exception as e:
            logging.error(f"Failed to start web server: {e}")

        end_time = datetime.now()
        logging.info(f"Bot started at {end_time}, duration: {end_time - start_time}")

    async def stop(self, *args):
        stop_time = datetime.now()
        logging.info(f"Stopping bot at {stop_time}")
        await super().stop()

app = Bot()
app.start()
idle()  # Keeps the bot running
app.stop()
