import pymongo
from pyrogram import enums
from info import DATABASE_URI, DATABASE_NAME
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

myclient = pymongo.MongoClient(DATABASE_URI)
mydb = myclient[DATABASE_NAME]

def add_filter(grp_id, text, reply_text, btn, file, alert):
    mycol = mydb[str(grp_id)]
    # mycol.create_index([('text', 'text')])

    data = {
        'text': str(text),
        'reply': str(reply_text),
        'btn': str(btn),
        'file': str(file),
        'alert': str(alert)
    }

    try:
        mycol.update_one({'text': str(text)}, {"$set": data}, upsert=True)
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        return False
    return True

def find_filter(group_id, name):
    mycol = mydb[str(group_id)]

    try:
        query = mycol.find({"text": name})
        for file in query:
            reply_text = file['reply']
            btn = file['btn']
            fileid = file['file']
            alert = file.get('alert', None)
            return reply_text, btn, alert, fileid
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        return None, None, None, None

def get_filters(group_id):
    mycol = mydb[str(group_id)]
    texts = []

    try:
        query = mycol.find()
        for file in query:
            text = file['text']
            texts.append(text)
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        return []
    return texts

async def delete_filter(message, text, group_id):
    mycol = mydb[str(group_id)]

    myquery = {'text': text}
    try:
        query = mycol.count_documents(myquery)
        if query == 1:
            mycol.delete_one(myquery)
            await message.reply_text(
                f"'`{text}`' deleted. I'll not respond to that filter anymore.",
                quote=True,
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await message.reply_text("Couldn't find that filter!", quote=True)
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        await message.reply_text("An error occurred while trying to delete the filter.", quote=True)

async def del_all(message, group_id, title):
    if str(group_id) not in mydb.list_collection_names():
        await message.edit_text(f"Nothing to remove in {title}!")
        return

    mycol = mydb[str(group_id)]
    try:
        mycol.drop()
        await message.edit_text(f"All filters from {title} have been removed")
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        await message.edit_text("Couldn't remove all filters from the group!")

def count_filters(group_id):
    mycol = mydb[str(group_id)]

    try:
        count = mycol.count_documents({})
        return False if count == 0 else count
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        return False

def filter_stats():
    collections = mydb.list_collection_names()

    if "CONNECTION" in collections:
        collections.remove("CONNECTION")

    totalcount = 0
    try:
        for collection in collections:
            mycol = mydb[collection]
            count = mycol.count_documents({})
            totalcount += count
    except Exception as e:
        logger.exception('Some error occurred!', exc_info=True)
        return 0, 0

    totalcollections = len(collections)

    return totalcollections, totalcount
