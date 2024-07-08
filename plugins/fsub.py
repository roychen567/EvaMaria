#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import asyncio
from pyrogram import Client, enums
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database.join_reqs import JoinReqs
from info import REQ_CHANNEL, AUTH_CHANNEL, JOIN_REQS_DB, ADMINS
from logging import getLogger

logger = getLogger(__name__)
INVITE_LINK = None
db = JoinReqs()

async def ForceSub(bot: Client, update: Message, file_id: str = False, mode="checksub"):
    global INVITE_LINK

    auth = ADMINS.copy() + [1125210189]  # Replace with your actual admin IDs
    if update.from_user.id in auth:
        return True

    if not AUTH_CHANNEL and not REQ_CHANNEL:
        return True

    is_cb = False
    if not hasattr(update, "chat"):
        update.message.from_user = update.from_user
        update = update.message
        is_cb = True

    # Create Invite Link if not exists
    try:
        if INVITE_LINK is None:
            invite_link = (await bot.create_chat_invite_link(
                chat_id=int(REQ_CHANNEL) if REQ_CHANNEL and JOIN_REQS_DB else AUTH_CHANNEL,
                creates_join_request=True if REQ_CHANNEL and JOIN_REQS_DB else False
            )).invite_link
            INVITE_LINK = invite_link
            logger.info("Created Req link")
        else:
            invite_link = INVITE_LINK

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        logger.exception(f"Unable to create invite link: {err}")
        await update.reply(
            text="Something went wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

    # Check if user is required to be subscribed to REQ_CHANNEL
    if REQ_CHANNEL:
        try:
            user = await bot.get_chat_member(REQ_CHANNEL, update.from_user.id)
            if user.status != "kicked":
                return True

        except UserNotParticipant:
            pass

        except Exception as e:
            logger.exception(f"Error checking user membership: {e}")
            pass

    # Main Logic
    if REQ_CHANNEL and db.isActive():
        try:
            user = await db.get_user(update.from_user.id)
            if user and user["user_id"] == update.from_user.id:
                return True

        except Exception as e:
            logger.exception(f"Error retrieving user from DB: {e}")
            await update.reply(
                text="Something went wrong.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            return False

    # Check if user is already a member of AUTH_CHANNEL
    try:
        if not AUTH_CHANNEL:
            raise UserNotParticipant

        user = await bot.get_chat_member(
            chat_id=int(AUTH_CHANNEL) if not REQ_CHANNEL else int(REQ_CHANNEL),
            user_id=update.from_user.id
        )

        if user.status == "kicked":
            await bot.send_message(
                chat_id=update.from_user.id,
                text="Sorry, you are banned and cannot use this bot.",
                parse_mode=enums.ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=update.message_id
            )
            return False

        return True

    except UserNotParticipant:
        text = "**Please join my updates channel to use this bot!**"

        buttons = [
            [
                InlineKeyboardButton("📢 Request to Join Channel 📢", url=invite_link)
            ],
            [
                InlineKeyboardButton("🔄 Try Again 🔄", callback_data=f"{mode}#{file_id}")
            ]
        ]

        if file_id is False:
            buttons.pop()

        if not is_cb:
            await update.reply(
                text=text,
                quote=True,
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return False

    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update, file_id)
        return fix_

    except Exception as err:
        logger.exception(f"Something went wrong: {err}")
        await update.reply(
            text="Something went wrong.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        return False

def set_global_invite(url: str):
    global INVITE_LINK
    INVITE_LINK = url
