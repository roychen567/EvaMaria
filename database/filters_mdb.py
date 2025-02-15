import logging
from struct import pack
import re
import base64
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from info import DATABASE_URI, DATABASE_NAME

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)

@instance.register
class Filter(Document):
    text = fields.StrField(attribute='_id')
    reply = fields.StrField(required=True)
    btn = fields.StrField(allow_none=True)
    file = fields.StrField(allow_none=True)
    alert = fields.StrField(allow_none=True)

    class Meta:
        collection_name = "filters"

async def add_filter(grp_id, text, reply_text, btn, file, alert):
    try:
        filter_entry = Filter(
            text=f"{grp_id}_{text}",
            reply=reply_text,
            btn=btn,
            file=file,
            alert=alert
        )
        await filter_entry.commit()
    except ValidationError:
        logger.exception("Validation error while saving filter")
        return False
    except DuplicateKeyError:
        logger.warning(f"Filter '{text}' already exists for group {grp_id}")
        return False
    except Exception:
        logger.exception("Error while saving filter")
        return False
    return True

async def find_filter(group_id, name):
    try:
        filter_entry = await Filter.find_one({"_id": f"{group_id}_{name}"})
        if filter_entry:
            return filter_entry.reply, filter_entry.btn, filter_entry.alert, filter_entry.file
    except Exception:
        logger.exception("Error while fetching filter")
    return None, None, None, None

async def get_filters(group_id):
    filters_list = []
    try:
        async for filter_entry in Filter.find({"_id": {"$regex": f"^{group_id}_"}}):
            filters_list.append(filter_entry.text.split("_", 1)[1])
    except Exception:
        logger.exception("Error while fetching filters")
        return []
    return filters_list

async def delete_filter(group_id, text):
    try:
        filter_entry = await Filter.find_one({"_id": f"{group_id}_{text}"})
        if filter_entry:
            await filter_entry.delete()
            return True
    except Exception:
        logger.exception("Error while deleting filter")
    return False

async def del_all(group_id):
    try:
        await Filter.collection.delete_many({"_id": {"$regex": f"^{group_id}_"}})
        return True
    except Exception:
        logger.exception("Error while deleting all filters")
    return False

def count_filters():
    try:
        return Filter.count_documents()
    except Exception:
        logger.exception("Error while counting filters")
        return 0
