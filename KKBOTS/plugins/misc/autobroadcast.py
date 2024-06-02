import asyncio
import datetime
from KKBOTS import app
from pyrogram import Client
from KKBOTS.utils.database import get_served_chats
from config import START_IMG_URL, AUTO_GCAST_MSG, AUTO_GCAST
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

AUTO_GCASTS = "{AUTO_GCAST}" if AUTO_GCAST else False


MESSAGE = f"""**🔼Introducing the Advanced Music Player Bot for Telegram Groups & Channels! 💌🎊

🔥🔥 Play music directly in voice chat with ease! 🎧🎧�

**Features:**

- Play, pause, control volume directly in chat.
- Welcome messages, left chat notifications, and more!
- Tag all, voice chat tag, ban/mute, lyrics, song/video downloads, and more! 💫💫�

🌈🌈🌈Simply click [here](https://t.me/{app.username}?start=help) or use the command "/start".

🆒 **Bot Username:** @{app.username}"""

BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🙈 ᴋɪᴅɴᴀᴘ ᴍᴇ 🙈", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users")
        ]
    ]
)

caption = f"""{AUTO_GCAST_MSG}""" if AUTO_GCAST_MSG else MESSAGE


async def send_message_to_chats():
    try:
        chats = await get_served_chats()

        for chat_info in chats:
            chat_id = chat_info.get('chat_id')
            if isinstance(chat_id, int):  # Check if chat_id is an integer
                try:
                    await app.send_photo(chat_id, photo=START_IMG_URL, caption=caption, reply_markup=BUTTON)
                    await asyncio.sleep(5)  # Sleep for 5 second between sending messages
                except Exception as e:
                    pass  # Do nothing if an error occurs while sending message
    except Exception as e:
        pass  # Do nothing if an error occurs while fetching served chats

async def continuous_broadcast():
    while True:
        await send_message_to_chats()

        # Wait for 50000 seconds before next broadcast
        await asyncio.sleep(50000)

# Start the continuous broadcast loop if AUTO_BROADCAST is True
if AUTO_GCASTS:  
    asyncio.create_task(continuous_broadcast())

