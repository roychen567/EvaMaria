# https://github.com/odysseusmax/animated-lamp/blob/master/bot/database/database.py
import motor.motor_asyncio
import logging
from info import (DATABASE_NAME, DATABASE_URI, IMDB, IMDB_TEMPLATE, MELCOW_NEW_USERS,
                  P_TTI_SHOW_OFF, SINGLE_BUTTON, SPELL_CHECK_REPLY, PROTECT_CONTENT)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Database:
    def __init__(self, uri, database_name):
        try:
            self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
            self.db = self._client[database_name]
            self.col = self.db.users
            self.grp = self.db.groups
            logger.info("Database connection established.")
        except Exception as e:
            logger.exception("Failed to connect to the database: %s", e)
            self._client = None
            self.db = None
            self.col = None
            self.grp = None

    def new_user(self, id, name):
        return {
            'id': id,
            'name': name,
            'ban_status': {
                'is_banned': False,
                'ban_reason': "",
            },
        }

    def new_group(self, id, title):
        return {
            'id': id,
            'title': title,
            'chat_status': {
                'is_disabled': False,
                'reason': "",
            },
        }

    async def add_user(self, id, name):
        user = self.new_user(id, name)
        try:
            await self.col.insert_one(user)
            logger.info(f"User {name} added to the database.")
        except Exception as e:
            logger.exception("Failed to add user %s: %s", name, e)

    async def is_user_exist(self, id):
        try:
            user = await self.col.find_one({'id': int(id)})
            return bool(user)
        except Exception as e:
            logger.exception("Failed to check if user %d exists: %s", id, e)
            return False

    async def total_users_count(self):
        try:
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            logger.exception("Failed to count users: %s", e)
            return 0

    async def remove_ban(self, id):
        ban_status = {
            'is_banned': False,
            'ban_reason': ''
        }
        try:
            await self.col.update_one({'id': int(id)}, {'$set': {'ban_status': ban_status}})
            logger.info(f"Ban removed for user {id}.")
        except Exception as e:
            logger.exception("Failed to remove ban for user %d: %s", id, e)

    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = {
            'is_banned': True,
            'ban_reason': ban_reason
        }
        try:
            await self.col.update_one({'id': int(user_id)}, {'$set': {'ban_status': ban_status}})
            logger.info(f"User {user_id} banned for reason: {ban_reason}.")
        except Exception as e:
            logger.exception("Failed to ban user %d: %s", user_id, e)

    async def get_ban_status(self, id):
        default = {
            'is_banned': False,
            'ban_reason': ''
        }
        try:
            user = await self.col.find_one({'id': int(id)})
            if not user:
                return default
            return user.get('ban_status', default)
        except Exception as e:
            logger.exception("Failed to get ban status for user %d: %s", id, e)
            return default

    async def get_all_users(self):
        try:
            users = await self.col.find({}).to_list(None)
            return users
        except Exception as e:
            logger.exception("Failed to get all users: %s", e)
            return []

    async def delete_user(self, user_id):
        try:
            await self.col.delete_many({'id': int(user_id)})
            logger.info(f"User {user_id} deleted from the database.")
        except Exception as e:
            logger.exception("Failed to delete user %d: %s", user_id, e)

    async def get_banned(self):
        try:
            users = self.col.find({'ban_status.is_banned': True})
            chats = self.grp.find({'chat_status.is_disabled': True})
            b_chats = [chat['id'] async for chat in chats]
            b_users = [user['id'] async for user in users]
            return b_users, b_chats
        except Exception as e:
            logger.exception("Failed to get banned users and chats: %s", e)
            return [], []

    async def add_chat(self, chat, title):
        chat_data = self.new_group(chat, title)
        try:
            await self.grp.insert_one(chat_data)
            logger.info(f"Chat {title} added to the database.")
        except Exception as e:
            logger.exception("Failed to add chat %s: %s", title, e)

    async def get_chat(self, chat):
        try:
            chat_data = await self.grp.find_one({'id': int(chat)})
            return chat_data.get('chat_status') if chat_data else False
        except Exception as e:
            logger.exception("Failed to get chat %d: %s", chat, e)
            return False

    async def re_enable_chat(self, id):
        chat_status = {
            'is_disabled': False,
            'reason': "",
        }
        try:
            await self.grp.update_one({'id': int(id)}, {'$set': {'chat_status': chat_status}})
            logger.info(f"Chat {id} re-enabled.")
        except Exception as e:
            logger.exception("Failed to re-enable chat %d: %s", id, e)

    async def update_settings(self, id, settings):
        try:
            await self.grp.update_one({'id': int(id)}, {'$set': {'settings': settings}})
            logger.info(f"Settings updated for chat {id}.")
        except Exception as e:
            logger.exception("Failed to update settings for chat %d: %s", id, e)

    async def get_settings(self, id):
        default = {
            'button': SINGLE_BUTTON,
            'botpm': P_TTI_SHOW_OFF,
            'file_secure': PROTECT_CONTENT,
            'imdb': IMDB,
            'spell_check': SPELL_CHECK_REPLY,
            'welcome': MELCOW_NEW_USERS,
            'template': IMDB_TEMPLATE
        }
        try:
            chat = await self.grp.find_one({'id': int(id)})
            return chat.get('settings', default) if chat else default
        except Exception as e:
            logger.exception("Failed to get settings for chat %d: %s", id, e)
            return default

    async def disable_chat(self, chat, reason="No Reason"):
        chat_status = {
            'is_disabled': True,
            'reason': reason,
        }
        try:
            await self.grp.update_one({'id': int(chat)}, {'$set': {'chat_status': chat_status}})
            logger.info(f"Chat {chat} disabled for reason: {reason}.")
        except Exception as e:
            logger.exception("Failed to disable chat %d: %s", chat, e)

    async def total_chat_count(self):
        try:
            count = await self.grp.count_documents({})
            return count
        except Exception as e:
            logger.exception("Failed to count chats: %s", e)
            return 0

    async def get_all_chats(self):
        try:
            chats = await self.grp.find({}).to_list(None)
            return chats
        except Exception as e:
            logger.exception("Failed to get all chats: %s", e)
            return []

    async def get_db_size(self):
        try:
            stats = await self.db.command("dbstats")
            return stats['dataSize']
        except Exception as e:
            logger.exception("Failed to get database size: %s", e)
            return 0

# Initialize database
db = Database(DATABASE_URI, DATABASE_NAME)
