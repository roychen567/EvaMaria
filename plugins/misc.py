import os
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from info import IMDB_TEMPLATE
from utils import extract_user, get_poster
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Initialize the Pyrogram Client
app = Client("my_bot")


@app.on_message(filters.command('id'))
async def show_id(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ First Name:</b> {first}\n<b>➲ Last Name:</b> {last}\n<b>➲ Username:</b> {username}\n<b>➲ Telegram ID:</b> <code>{user_id}</code>\n<b>➲ Data Centre:</b> <code>{dc_id}</code>",
            quote=True
        )
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += (
            "<b>➲ Chat ID</b>: "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
                "<b>➲ Replied User ID</b>: "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ User ID</b>: "
                f"<code>{message.from_user.id if message.from_user else 'Anonymous'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
        )


@app.on_message(filters.command(["info"]))
async def who_is(client, message):
    status_message = await message.reply_text("`Fetching user info...`")
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("No valid user_id / message specified")

    message_out_str = ""
    message_out_str += f"<b>➲ First Name:</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>None</b>"
    message_out_str += f"<b>➲ Last Name:</b> {last_name}\n"
    message_out_str += f"<b>➲ Telegram ID:</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>None</b>"
    dc_id = from_user.dc_id or "[User doesn't have a valid DP]"
    message_out_str += f"<b>➲ Data Centre:</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲ Username:</b> @{username}\n"
    message_out_str += f"<b>➲ User Link:</b> <a href='tg://user?id={from_user.id}'><b>Click Here</b></a>\n"

    if message.chat.type in (enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (
                chat_member_p.joined_date or datetime.now()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>➲ Joined this Chat on:</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass

    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        buttons = [[
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        try:
            await message.reply_photo(
                photo=local_user_photo,
                quote=True,
                reply_markup=reply_markup,
                caption=message_out_str,
                parse_mode=enums.ParseMode.HTML,
                disable_notification=True
            )
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = chat_photo.big_file_id
            local_user_photo = pic.replace('.jpg', "._V1_UX360.jpg")
            await message.reply_photo(
                photo=local_user_photo,
                quote=True,
                reply_markup=reply_markup,
                caption=message_out_str,
                parse_mode=enums.ParseMode.HTML,
                disable_notification=True
            )
        except Exception as e:
            logger.exception(e)
            await message.reply(caption=message_out_str, reply_markup=reply_markup, disable_web_page_preview=False)
        finally:
            os.remove(local_user_photo)
    else:
        buttons = [[
            InlineKeyboardButton('🔐 Close', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )

    await status_message.delete()


@app.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Searching IMDb')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("No results found")

        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.get('movieID')}",
                )
            ]
            for movie in movies
        ]

        await k.edit('Here is what I found on IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Give me a movie or series name')


@app.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, query: CallbackQuery):
    _, movie_id = query.data.split('#')
    imdb = await get_poster(query=movie_id, id=True)

    btn = [
        [
            InlineKeyboardButton(
                text=f"{imdb.get('title')}",
                url=imdb.get('url'),
            )
        ]
    ]

    message = query.message.reply_to_message or query.message
    if imdb:
        caption = IMDB_TEMPLATE.format(
            query=imdb.get('title'),
            title=imdb.get('title'),
            votes=imdb.get('votes'),
            aka=imdb.get('aka'),
            seasons=imdb.get('seasons'),
            box_office=imdb.get('box_office'),
            localized_title=imdb.get('localized_title'),
            kind=imdb.get('kind'),
            imdb_id=imdb.get('imdb_id'),
            cast=imdb.get('cast'),
            runtime=imdb.get('runtime'),
            countries=imdb.get('countries'),
            certificates=imdb.get('certificates'),
            languages=imdb.get('languages'),
            director=imdb.get('director'),
            writer=imdb.get('writer'),
            producer=imdb.get('producer'),
            composer=imdb.get('composer'),
            cinematographer=imdb.get('cinematographer'),
            music_team=imdb.get('music_team'),
            distributors=imdb.get('distributors'),
            release_date=imdb.get('release_date'),
            year=imdb.get('year'),
            genres=imdb.get('genres'),
            poster=imdb.get('poster'),
            plot=imdb.get('plot'),
            rating=imdb.get('rating'),
            url=imdb.get('url'),
            **locals()
        )
    else:
        caption = "No results found"

    if imdb.get('poster'):
        try:
            await query.message.reply_photo(
                photo=imdb.get('poster'),
                caption=caption,
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await query.message.reply_photo(
                photo=poster,
                caption=caption,
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except Exception as e:
            logger.exception(e)
            await query.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        finally:
            await query.message.delete()
    else:
        await query.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)

    await query.answer()

# Run the application
if __name__ == '__main__':
    app.run()
