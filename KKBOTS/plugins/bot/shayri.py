
from pyrogram import Client, filters
import requests
import random
import os
import re
import asyncio
import time
from KKBOTS import app

from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

SHAYRI = [  ]

# Command
SHAYRI_COMMAND = ["gf", "bf", "shayri", "shayari", "sari", "shari", "love"]

@app.on_message(
    filters.command(SHAYRI_COMMAND)
    & filters.group
    )
async def help(client: Client, message: Message):
    await message.reply_text(
        text = random.choice(SHAYRI),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url=f"https://t.me/KernelKnightChats"),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/KernelKnight")
                    
                ]
            ]
        ),
    )

@app.on_message(
    filters.command(SHAYRI_COMMAND)
    & filters.private
    )
async def help(client: Client, message: Message):
    await message.reply_text(
        text = random.choice(SHAYRI),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url=f"https://t.me/KernelKnightChats"),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url=f"https://t.me/KernelKnight")
                    
                ]
            ]
        ),
    )
