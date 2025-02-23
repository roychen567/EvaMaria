import motor.motor_asyncio
from info import DATABASE_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]
mycol = mydb['CONNECTION']

async def add_connection(group_id, user_id):
    try:
        query = await mycol.find_one({"_id": user_id}, {"_id": 0, "active_group": 0})
        if query is not None:
            group_ids = [x["group_id"] for x in query["group_details"]]
            if group_id in group_ids:
                return False

        group_details = {"group_id": group_id}
        data = {
            '_id': user_id,
            'group_details': [group_details],
            'active_group': group_id,
        }

        if await mycol.count_documents({"_id": user_id}) == 0:
            await mycol.insert_one(data)
        else:
            await mycol.update_one(
                {'_id': user_id},
                {
                    "$push": {"group_details": group_details},
                    "$set": {"active_group": group_id}
                }
            )
        return True
    except Exception as e:
        logger.exception('Error occurred while adding connection:', exc_info=True)
        return False

async def active_connection(user_id):
    try:
        query = await mycol.find_one({"_id": user_id}, {"_id": 0, "group_details": 0})
        if not query:
            return None
        return int(query['active_group']) if query['active_group'] is not None else None
    except Exception as e:
        logger.exception('Error occurred while getting active connection:', exc_info=True)
        return None

async def all_connections(user_id):
    try:
        query = await mycol.find_one({"_id": user_id}, {"_id": 0, "active_group": 0})
        if query is not None:
            return [x["group_id"] for x in query["group_details"]]
        return None
    except Exception as e:
        logger.exception('Error occurred while getting all connections:', exc_info=True)
        return None

async def if_active(user_id, group_id):
    try:
        query = await mycol.find_one({"_id": user_id}, {"_id": 0, "group_details": 0})
        return query is not None and query['active_group'] == group_id
    except Exception as e:
        logger.exception('Error occurred while checking if active:', exc_info=True)
        return False

async def make_active(user_id, group_id):
    try:
        update = await mycol.update_one({'_id': user_id}, {"$set": {"active_group": group_id}})
        return update.modified_count != 0
    except Exception as e:
        logger.exception('Error occurred while making active:', exc_info=True)
        return False

async def make_inactive(user_id):
    try:
        update = await mycol.update_one({'_id': user_id}, {"$set": {"active_group": None}})
        return update.modified_count != 0
    except Exception as e:
        logger.exception('Error occurred while making inactive:', exc_info=True)
        return False

async def delete_connection(user_id, group_id):
    try:
        update = await mycol.update_one({"_id": user_id}, {"$pull": {"group_details": {"group_id": group_id}}})
        if update.modified_count == 0:
            return False
        
        query = await mycol.find_one({"_id": user_id}, {"_id": 0})
        if len(query["group_details"]) >= 1:
            if query['active_group'] == group_id:
                prvs_group_id = query["group_details"][-1]["group_id"]
                await mycol.update_one({'_id': user_id}, {"$set": {"active_group": prvs_group_id}})
        else:
            await mycol.update_one({'_id': user_id}, {"$set": {"active_group": None}})
        return True
    except Exception as e:
        logger.exception('Error occurred while deleting connection:', exc_info=True)
        return False
