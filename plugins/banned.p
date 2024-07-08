from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from utils import temp
from database.users_chats_db import db
from info import SUPPORT_CHAT

async def banned_users(_, __, message: Message):
    return (
        message.from_user is not None and message.from_user.id in temp.BANNED_USERS
    )

banned_user = filters.create(banned_users)

async def disabled_chat(_, __, message: Message):
    return message.chat.id in temp.BANNED_CHATS

disabled_group = filters.create(disabled_chat)

@Client.on_message(filters.private & banned_user & filters.incoming)
async def ban_reply(client, message: Message):
    ban = await db.get_ban_status(message.from_user.id)
    await message.reply(f'Sorry Dude, You are Banned from using me. \nBan Reason: {ban["ban_reason"]}')

@Client.on_message(filters.group & disabled_group & filters.incoming)
async def grp_bd(client, message: Message):
    buttons = [[
        InlineKeyboardButton('𝚂𝚞𝚙𝚙𝚘𝚛𝚝', url=f'https://t.me/{SUPPORT_CHAT}')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    vazha = await db.get_chat(message.chat.id)
    k = await message.reply(
        text=f"CHAT NOT ALLOWED 🐞\n\nMy admins have restricted me from working here! If you want to know more about it, contact support.\nReason: <code>{vazha['reason']}</code>.",
        reply_markup=reply_markup
    )
    try:
        await k.pin()
    except:
        pass
    await client.leave_chat(message.chat.id)

