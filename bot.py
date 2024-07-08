import logging
import logging.config
from datetime import datetime
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR, LOG_CHANNEL
from utils import temp
from typing import Union, Optional, AsyncGenerator
from pyrogram import types
from os import environ
from aiohttp import web
from plugins import web_server

# Get logging configurations
try:
    logging.config.fileConfig('logging.conf')
except Exception as e:
    print(f"Failed to load logging configuration: {e}")

logging.getLogger().setLevel(logging.INFO)
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
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        start_time = datetime.now()
        logging.info(f"Starting bot at {start_time}")

        try:
            b_users, b_chats = await db.get_banned()
            temp.BANNED_USERS = b_users
            temp.BANNED_CHATS = b_chats
        except Exception as e:
            logging.error(f"Failed to get banned users or chats: {e}")

        await super().start()
        
        try:
            await Media.ensure_indexes()
        except Exception as e:
            logging.error(f"Failed to ensure Media indexes: {e}")

        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

        try:
            await self.send_message(chat_id=LOG_CHANNEL, text="restarted ❤️‍🩹")
        except Exception as e:
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

        await super().stop()

        end_time = datetime.now()
        logging.info(f"Bot stopped at {end_time}, duration: {end_time - stop_time}")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = offset
        while current < limit:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            start_time = datetime.now()
            try:
                messages = await self.get_messages(chat_id, list(range(current, current + new_diff + 1)))
            except Exception as e:
                logging.error(f"Failed to retrieve messages: {e}")
                return

            end_time = datetime.now()
            logging.info(f"Retrieved messages for {chat_id} from {current} to {current + new_diff}, duration: {end_time - start_time}")

            for message in messages:
                yield message
                current += 1

app = Bot()
app.run()
