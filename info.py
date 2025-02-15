import re
from os import environ

id_pattern = re.compile(r'^-?\d+$')  # Updated regex pattern to match IDs correctly

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# Bot information
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '21958444'))
API_HASH = environ.get('API_HASH', 'c7c23aa495b8cfa4cd784efab9de559f')
BOT_TOKEN = environ.get('BOT_TOKEN', '8108479997:AAH8YQ3EGPBQBnNaBQlyKKSt3dOpbstbFr4')

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', '300'))
USE_CAPTION_FILTER = is_enabled(environ.get('USE_CAPTION_FILTER', 'False'), False)
PICS = environ.get('PICS', 'https://graph.org/file/9837e20755a4e559e0bd6-26ca2b16d0f1a1b1d6.jpg')

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7187011796').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002203759750').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
AUTH_CHANNEL = int(environ.get('AUTH_CHANNEL', '-1001868251572'))  # Assuming AUTH_CHANNEL is an integer
AUTH_GROUPS = [int(ch) for ch in environ.get('AUTH_GROUP', '-1001697068765').split()] if environ.get('AUTH_GROUP') else []

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://roychen346:roychen346@ironman.upudl.mongodb.net/?retryWrites=true&w=majority&appName=ironman")
DATABASE_NAME = environ.get('DATABASE_NAME', "ironman")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

# Request Fsub
REQ_CHANNEL = int(environ.get("REQ_CHANNEL", "-1002486327315")) if environ.get("REQ_CHANNEL") else None
JOIN_REQS_DB = environ.get("JOIN_REQS_DB", DATABASE_URI)

# Others
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002438691201'))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'MOVIE_BAZAR')
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', 'True'), False)
IMDB = is_enabled(environ.get('IMDB', 'False'), True)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', 'True'), False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "<b><i>{file_name} \n🔘 size - {file_size}</i></b>")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", "<b><i>{file_name} \n🔘 size - {file_size}</i></b>")
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "🏷 𝖳𝗂𝗍𝗅𝖾: <a href={url}>{title}</a> \n🔮 𝖸𝖾𝖺𝗋: {year} \n⭐️ 𝖱𝖺𝗍𝗂𝗇𝗀𝗌: {rating}/ 10 \n🎭 𝖦𝖾𝗇𝖾𝗋𝗌: {genres} \n\n🎊 𝖯𝗈𝗐𝖾𝗋𝖾𝖽 𝖡𝗒 [ᴀᴍ_ᴛᴇᴄʜ](https://t.me/Am_RoBots)")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = int(environ.get("MAX_LIST_ELM", 0)) if environ.get("MAX_LIST_ELM") else None
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in environ.get('FILE_STORE_CHANNEL', '').split()] if environ.get('FILE_STORE_CHANNEL') else []
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', 'False'), True)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', 'False'), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', 'False'), True)

# Logging configuration string
LOG_STR = f"Current Customized Configurations:\n"
LOG_STR += f"IMDB Results: {'Enabled' if IMDB else 'Disabled'}\n"
LOG_STR += f"P_TTI_SHOW_OFF: {'Enabled' if P_TTI_SHOW_OFF else 'Disabled'}\n"
LOG_STR += f"SINGLE_BUTTON: {'Enabled' if SINGLE_BUTTON else 'Disabled'}\n"
LOG_STR += f"CUSTOM_FILE_CAPTION: {'Enabled' if CUSTOM_FILE_CAPTION else 'Disabled'}\n"
LOG_STR += f"LONG_IMDB_DESCRIPTION: {'Enabled' if LONG_IMDB_DESCRIPTION else 'Disabled'}\n"
LOG_STR += f"SPELL_CHECK_REPLY: {'Enabled' if SPELL_CHECK_REPLY else 'Disabled'}\n"
LOG_STR += f"MAX_LIST_ELM: {MAX_LIST_ELM}\n"
LOG_STR += f"IMDB_TEMPLATE: {IMDB_TEMPLATE}"

# Print out the logging configuration string
print(LOG_STR)
