import logging
import logging.config
import os  # Import os module for environment variables
from datetime import datetime
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from typing import Union, Optional, AsyncGenerator
from aiohttp import web
from aiohttp import web
from plugins import web_server

# Get logging configurations
try:
    logging.config.fileConfig('logging.conf')
except Exception as e:
	@@ -23,13 +23,13 @@
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

PORT = environ.get("PORT", "8080")

class Bot(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
	@@ -50,7 +50,7 @@ async def start(self):
            logging.error(f"Failed to get banned users or chats: {e}")

        await super().start()
        
        try:
            await Media.ensure_indexes()
        except Exception as e:
	@@ -70,16 +70,22 @@ async def start(self):
            logging.error(f"Failed to send start message to log channel: {e}")

        try:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, bind_address, PORT).start()
        except Exception as e:
            logging.error(f"Failed to start web server: {e}")

        end_time = datetime.now()
        logging.info(f"Bot started at {end_time}, duration: {end_time - start_time}")

    async def stop(self, *args):
        stop_time = datetime.now()
        logging.info(f"Stopping bot at {stop_time}")
	@@ -102,7 +108,7 @@ async def iter_messages(
                return
            start_time = datetime.now()
            try:
                messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            except Exception as e:
                logging.error(f"Failed to retrieve messages: {e}")
                return
	@@ -114,5 +120,6 @@ async def iter_messages(
                yield message
                current += 1

app = Bot()
app.run()
