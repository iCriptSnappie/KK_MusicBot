from KKBOTS import app
from pyrogram import filters
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
import random
import asyncio
import os
import time
import aiohttp
from pathlib import Path
from logging import getLogger

# In-memory storage for the welcome feature state
welcome_enabled = {}

random_photo = [
    "https://graph.org/file/4dfce969e9455b81063ef.jpg",
    "https://graph.org/file/0591e20168536ef2c1cda.jpg",
]

get_font = lambda font_size, font_path: ImageFont.truetype(font_path, font_size)
resize_text = (
    lambda text_size, text: (text[:text_size] + "...").upper()
    if len(text) > text_size
    else text.upper()
)

async def get_userinfo_img(bg_path: str, font_path: str, user_id: Union[int, str], profile_path: Optional[str] = None):
    bg = Image.open(bg_path)
    if profile_path:
        img = Image.open(profile_path)
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice([(0, 0), img.size], 0, 360, fill=255)
        circular_img = Image.new("RGBA", img.size, (0, 0, 0, 0))
        circular_img.paste(img, (0, 0), mask)
        resized = circular_img.resize((400, 400))
        bg.paste(resized, (440, 160), resized)

    img_draw = ImageDraw.Draw(bg)
    img_draw.text(
        (529, 627),
        text=str(user_id).upper(),
        font=get_font(46, font_path),
        fill=(255, 255, 255),
    )
    path = f"./userinfo_img_{user_id}.png"
    bg.save(path)
    return path

bg_path = "KKBOTS/assets/userinfo.png"
font_path = "KKBOTS/assets/hiroko.ttf"

async def handle_member_update(client: app, member: ChatMemberUpdated):
    chat = member.chat

    # Check if the welcome feature is enabled for this chat
    if not welcome_enabled.get(chat.id, True):
        return

    count = await app.get_chat_members_count(chat.id)
    if member.new_chat_member:
        user = member.new_chat_member.user
        try:
            if user.photo:
                photo = await app.download_media(user.photo.big_file_id)
                welcome_photo = await get_userinfo_img(
                    bg_path=bg_path,
                    font_path=font_path,
                    user_id=user.id,
                    profile_path=photo,
                )
            else:
                welcome_photo = random.choice(random_photo)

            caption = (
                f"════❰𝙒𝙚𝙡𝙘𝙤𝙢𝙚❱══❍⊱❁۪۪\n"
                f"                    𝙏𝙤\n        {chat.title}\n"
                f"══════════════❍⊱❁۪۪\n\n"
                f"𝐍𝐀𝐌𝐄 » {member.new_chat_member.user.mention}\n"
                f"𝐔𝐒𝐄𝐑𝐍𝐀𝐌𝐄 » **@{member.new_chat_member.user.username}**\n"
                f"𝐔𝐒𝐄𝐑-𝐈𝐃 » `{member.new_chat_member.user.id}`\n\n"
                f"┏━━━━━━➣\n"
                f"┣⪼𝐁𝐎𝐍𝐃 𝐎𝐅 𝐋𝐔𝐕 𝐍 𝐓𝐑𝐔𝐒𝐓🌷\n"
                f"┣⪼𝐑𝐄𝐒𝐏𝐄𝐂𝐓 𝐄𝐀𝐂𝐇 𝐎𝐓𝐇𝐄𝐑✌️\n"
                f"┣⪼ 𝐕𝐂 24/7💀\n"
                f"┣⪼𝐅𝐎𝐋𝐋𝐎𝐖 𝐑𝐔𝐋𝐄𝐒💅\n"
                f"┗━━━━━━➣\n\n"
                f"–––––––––––––––––––––––––––\n"
                f"**🔐ʟɪɴᴋ » @{chat.username}**\n"
                f"**👥ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀ ɴᴏᴡ » {count}**\n"
                f"–––––––––––––––––––––––––––"
            )
            button_text = "๏ ᴠɪᴇᴡ ɴᴇᴡ ᴍᴇᴍʙᴇʀ ๏"
            add_button_text = "๏ ᴋɪᴅɴᴀᴘ ᴍᴇ ๏"
            deep_link = f"tg://openmessage?user_id={user.id}"
            add_link = f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
            await client.send_photo(
                chat_id=member.chat.id,
                photo=welcome_photo,
                caption=caption,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, url=deep_link)],
                    [InlineKeyboardButton(text=add_button_text, url=add_link)],
                ])
            )
        except RPCError as e:
            print(e)

@app.on_chat_member_updated(filters.group, group=10)
async def member_update_handler(client: app, member: ChatMemberUpdated):
    await handle_member_update(client, member)

@app.on_message(filters.command("welcome") & filters.group)
async def welcome_command_handler(client: app, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply("Usage: /welcome [on|off]")
        return

    state = message.command[1].lower()
    if state == "on":
        welcome_enabled[chat_id] = True
        await message.reply("Welcome messages have been enabled.")
    elif state == "off":
        welcome_enabled[chat_id] = False
        await message.reply("Welcome messages have been disabled.")
    else:
        await message.reply("Usage: /welcome [on|off]")
