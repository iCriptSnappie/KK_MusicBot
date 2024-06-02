from pyrogram import Client, filters
from KKBOTS import app
from config import OWNER_ID, PREFIXES
from pyrogram.types import Message


@app.on_message(filters.command(["post"], prefixes=PREFIXES) & filters.user(OWNER_ID))
async def copy_messages(_, message):

    if message.reply_to_message:
      
        destination_group_id = -1002158955950

        
        await message.reply_to_message.copy(destination_group_id)
        await message.reply("ᴅᴏɴᴇ✔")