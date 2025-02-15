import os
import logging
import asyncio
import sys
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details
from database.users_chats_db import db
from info import CHANNELS, ADMINS, LOG_CHANNEL, PICS, BATCH_FILE_CAPTION, CUSTOM_FILE_CAPTION
from utils import get_size, save_group_settings
from utils import Temp  # Import the class separately
from plugins.fsub import ForceSub
import base64
from Script import script

logger = logging.getLogger(__name__)

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    print("✅ Start command received!")  # Debug log
    try:
        if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            print("➡️ Start command in a group chat")  # Debug log
        else:
            print(f"➡️ Start command in a private chat by {message.from_user.id}")  # Debug log
            buttons = [
                [InlineKeyboardButton('🤖 𝚄𝚙𝚍𝚊𝚝𝚎𝚜', url='https://t.me/+N8PS75om8Zw5ZjE1')],
                [InlineKeyboardButton('ℹ️ 𝙷𝚎𝚕𝚙', url=f"https://t.me/{temp.U_NAME}?start=help")],
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
            await asyncio.sleep(2)
            if not await db.get_chat(message.chat.id):
                total = await client.get_chat_members_count(message.chat.id)
                await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
                await db.add_chat(message.chat.id, message.chat.title)
            return
       is_user_exist = await db.is_user_exist(message.from_user.id)  # Await first
if len(message.command) != 2:
    # Code here...
elif not is_user_exist:  # Now use it
    await db.add_user(message.from_user.id, message.from_user.first_name)
    await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
        
        if len(message.command) != 2:
            buttons = [
                [InlineKeyboardButton('🔸 ɢʀᴏᴜᴘ 🔸', url='https://t.me/+N8PS75om8Zw5ZjE1'),
                 InlineKeyboardButton('🔸ᴜᴘᴅᴀᴛᴇ 🔸', url='https://t.me/+sVl4djnLE6plZDE1')],
                [InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')],
                [InlineKeyboardButton('🔹 ʜᴇʟᴘ 🔹', callback_data='help'),
                 InlineKeyboardButton('🔹 ᴀʙᴏᴜᴛ 🔹', callback_data='about')],
                [InlineKeyboardButton('👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 👨‍💻', url='https://t.me/MB_Owner')]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_video(
                video=PICS,
                caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
            return

        command = message.command[1]
        if command == "subscribe":
            await ForceSub(client, message)
        else:
            buttons = [
                [InlineKeyboardButton('🔸 ɢʀᴏᴜᴘ 🔸', url='https://t.me/+N8PS75om8Zw5ZjE1'),
                 InlineKeyboardButton('🔸ᴜᴘᴅᴀᴛᴇ 🔸', url='https://t.me/+sVl4djnLE6plZDE1')],
                [InlineKeyboardButton('➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕', url=f'http://t.me/{temp.U_NAME}?startgroup=true')],
                [InlineKeyboardButton('🔹 ʜᴇʟᴘ 🔹', callback_data='help'),
                 InlineKeyboardButton('🔹 ᴀʙᴏᴜᴛ 🔹', callback_data='about')],
                [InlineKeyboardButton('👨‍💻 ᴅᴇᴠᴇʟᴏᴘᴇʀ 👨‍💻', url='https://t.me/MB_Owner')]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await message.reply_video(
                video=PICS,
                caption=script.START_TXT.format(message.from_user.mention, temp.U_NAME, temp.B_NAME),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    except Exception as e:
        logger.exception("Error in start command: %s", e)

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(client, message):
    try:
        if isinstance(CHANNELS, (int, str)):
            channels = [CHANNELS]
        elif isinstance(CHANNELS, list):
            channels = CHANNELS
        else:
            raise ValueError("Unexpected type of CHANNELS")

        text = '📑 **Indexed channels/groups**\n'
        for channel in channels:
            chat = await client.get_chat(channel)
            text += '\n@' + chat.username if chat.username else '\n' + chat.title or chat.first_name

        text += f'\n\n**Total:** {len(CHANNELS)}'

        if len(text) < 4096:
            await message.reply(text)
        else:
            file_name = 'Indexed_channels.txt'
            with open(file_name, 'w') as f:
                f.write(text)
            await message.reply_document(file_name)
            os.remove(file_name)
    except Exception as e:
        logger.exception("Error in channel_info command: %s", e)

@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(client, message):
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        logger.exception("Error in log_file command: %s", e)

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(client, message):
    try:
        reply = message.reply_to_message
        if reply and reply.media:
            msg = await message.reply("Processing...⏳", quote=True)
        else:
            await message.reply('Reply to file with /delete which you want to delete', quote=True)
            return

        media = reply.video or reply.document or reply.audio
        if media is None:
            await msg.edit('This is not supported file format')
            return

        file_id, file_ref = unpack_new_file_id(media.file_id)

        result = await Media.collection.delete_one({
            '_id': file_id,
        })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
            result = await Media.collection.delete_many({
                'file_name': file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                result = await Media.collection.delete_many({
                    'file_name': media.file_name,
                    'file_size': media.file_size,
                    'mime_type': media.mime_type
                })
                if result.deleted_count:
                    await msg.edit('File is successfully deleted from database')
                else:
                    await msg.edit('File not found in database')
    except Exception as e:
        logger.exception("Error in delete command: %s", e)

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(client, message):
    try:
        await message.reply_text(
            'This will delete all indexed files.\nDo you want to continue??',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="YES", callback_data="autofilter_delete")],
                    [InlineKeyboardButton(text="CANCEL", callback_data="close_data")],
                ]
            ),
            quote=True,
        )
    except Exception as e:
        logger.exception("Error in delete_all_index command: %s", e)

@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(client, message):
    try:
        await Media.collection.drop()
        await message.answer('Piracy Is Crime')
        await message.message.edit('Successfully Deleted All The Indexed Files.')
    except Exception as e:
        logger.exception("Error in delete_all_index_confirm callback: %s", e)

@Client.on_message(filters.command('settings') & filters.user(ADMINS))
async def settings(client, message):
    try:
        userid = message.from_user.id if message.from_user else None
        if not userid:
            return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
        chat_type = message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await message.reply_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await message.reply_text("I'm not connected to any groups!", quote=True)
                return

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = message.chat.id
            title = message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        settings = await get_settings(grp_id)

        if settings is not None:
            buttons = [
                [InlineKeyboardButton('Filter Button', callback_data=f'setgs#button#{settings["button"]}#{grp_id}'),
                 InlineKeyboardButton('Single' if settings["button"] else 'Double', callback_data=f'setgs#button#{settings["button"]}#{grp_id}')],
                [InlineKeyboardButton('Bot PM', callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}'),
                 InlineKeyboardButton('✅ Yes' if settings["botpm"] else '❌ No', callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}')],
                [InlineKeyboardButton('File Secure', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}'),
                 InlineKeyboardButton('✅ Yes' if settings["file_secure"] else '❌ No', callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}')],
                [InlineKeyboardButton('IMDB', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}'),
                 InlineKeyboardButton('✅ Yes' if settings["imdb"] else '❌ No', callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}')],
                [InlineKeyboardButton('Spell Check', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}'),
                 InlineKeyboardButton('✅ Yes' if settings["spell_check"] else '❌ No', callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}')],
                [InlineKeyboardButton('Welcome', callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}'),
                 InlineKeyboardButton('✅ Yes' if settings["welcome"] else '❌ No', callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}')],
            ]

            reply_markup = InlineKeyboardMarkup(buttons)

            await message.reply_text(
                text=f"<b>Change Your Settings for {title} As Your Wish ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
    except Exception as e:
        logger.exception("Error in settings command: %s", e)

@Client.on_message(filters.command('restart') & filters.user(ADMINS))
async def restart_bot(client, message):
    try:
        msg = await message.reply_text(text="<b>Bot Restarting ...</b>")
        await msg.edit("<b>Restart Successfully Completed ✅</b>")
        os.system("git pull -f && pip3 install --no-cache-dir -r requirements.txt")
        execle(sys.executable, sys.executable, "bot.py", environ)
    except Exception as e:
        logger.exception("Error in restart_bot command: %s", e)

@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    try:
        sts = await message.reply("Checking template")
        userid = message.from_user.id if message.from_user else None
        if not userid:
            return await message.reply(f"You are anonymous admin. Use /connect {message.chat.id} in PM")
        chat_type = message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await message.reply_text("Make sure I'm present in your group!!", quote=True)
                    return
            else:
                await message.reply_text("I'm not connected to any groups!", quote=True)
                return

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = message.chat.id
            title = message.chat.title

        else:
            return

        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            return

        if len(message.command) < 2:
            return await sts.edit("No Input!!")
        
        template = message.text.split(" ", 1)[1]
        await save_group_settings(grp_id, 'template', template)
        await sts.edit(f"Successfully changed template for {title} to\n\n{template}")
    except Exception as e:
        logger.exception("Error in save_template command: %s", e)
