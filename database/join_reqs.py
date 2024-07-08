#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import motor.motor_asyncio
import logging
from info import REQ_CHANNEL, JOIN_REQS_DB

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class JoinReqs:
    def __init__(self):
        if JOIN_REQS_DB:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
            self.db = self.client["JoinReqs"]
            self.col = self.db[str(REQ_CHANNEL)]
            self.chat_col = self.db["ChatId"]
            logger.info("Database connection established.")
        else:
            self.client = None
            self.db = None
            self.col = None
            logger.warning("Database connection details not provided.")

    def is_active(self):
        return self.client is not None

    async def add_user(self, user_id, first_name, username, date):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return
        
        try:
            await self.col.insert_one({
                "_id": int(user_id),
                "user_id": int(user_id),
                "first_name": first_name,
                "username": username,
                "date": date
            })
            logger.info(f"User {username} added to the database.")
        except Exception as e:
            logger.exception(f"Failed to add user {username}: {e}")

    async def get_user(self, user_id):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return None
        
        try:
            user = await self.col.find_one({"user_id": int(user_id)})
            return user
        except Exception as e:
            logger.exception(f"Failed to get user {user_id}: {e}")
            return None

    async def get_all_users(self):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return []

        try:
            users = await self.col.find().to_list(None)
            return users
        except Exception as e:
            logger.exception(f"Failed to get all users: {e}")
            return []

    async def delete_user(self, user_id):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return

        try:
            await self.col.delete_one({"user_id": int(user_id)})
            logger.info(f"User {user_id} deleted from the database.")
        except Exception as e:
            logger.exception(f"Failed to delete user {user_id}: {e}")

    async def delete_all_users(self):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return

        try:
            await self.col.delete_many({})
            logger.info("All users deleted from the database.")
        except Exception as e:
            logger.exception("Failed to delete all users: {e}")

    async def get_all_users_count(self):
        if not self.is_active():
            logger.error("Database connection is not active.")
            return 0

        try:
            count = await self.col.count_documents({})
            return count
        except Exception as e:
            logger.exception("Failed to get users count: {e}")
            return 0
