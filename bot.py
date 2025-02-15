import logging
import logging.config
import os  
import asyncio  
from datetime import datetime
from pyrogram import Client, idle
from database.ia_filterdb import Media, db as clientDB
from database.users_chats_db import db
from info import *
from aiohttp import web
from plugins import web_server
from plugins.commands import *
from utils import Temp  # Ensure Temp is properly defined in utils.py

# Configure Logging
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
            plugins=dict(root="plugins")  # Ensure plugins are loaded
        )

async def start(self, **kwargs):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        await Media2.ensure_indexes()
        me = await self.get_me()
        self.me = me
        await load_datas(self)
        #choose the right db by checking the free space
        stats = await clientDB.command('dbStats')
        #calculating the free db space from bytes to MB
        free_dbSize = round(512-((stats['dataSize']/(1024*1024))+(stats['indexSize']/(1024*1024))), 2)
        if SECONDDB_URI and free_dbSize<10: #if the primary db have less than 10MB left, use second DB.
            tempDict["indexDB"] = SECONDDB_URI
            logging.info(f"Since Primary DB have only {free_dbSize} MB left, Secondary DB will be used to store datas.")
        elif SECONDDB_URI is None:
            logging.error("Missing second DB URI !\n\nAdd SECONDDB_URI now !\n\nExiting...")
            exit()
        else: logging.info(f"Since primary DB have enough space ({free_dbSize}MB) left, It will be used for storing datas.")
        # ---------------------
        if temp.REQ_CHANNEL:
            try: temp.LINK_ONE = (await self.create_chat_invite_link(chat_id=temp.REQ_CHANNEL, creates_join_request=True)).invite_link 
            except Exception as a:
                logging.warning(a)
                logging.warning("Bot can't Export Invite link from Force Sub Channel!")
                logging.warning(f"Please Double check the REQ_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {REQ_CHANNEL}")
                logging.info("\nBot Stopped. Join https://t.me/EbizaSupport for support")
                sys.exit()
        # ---------------------
        await choose_mediaDB()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)
        logging.info(script.LOGO)
        tz = pytz.timezone('Asia/Kolkata')
        today = date.today()
        now = datetime.now(tz)
        time = now.strftime("%H:%M:%S %p")
        await self.send_message(chat_id=LOG_CHANNEL, text=script.RESTART_TXT.format(today, time))

    async def stop(self, *args):
        stop_time = datetime.now()
        logging.info(f"Stopping bot at {stop_time}")
        await super().stop()
        logging.info("Bot stopped. Bye.")

app = Bot()

async def main():
    await app.start()
    print("🚀 Bot is running...")  # Confirm in console
    await idle()  # Keeps the bot running and responding
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
