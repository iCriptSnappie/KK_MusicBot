from pyrogram import Client
import re
from os import getenv
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from pyrogram import filters
load_dotenv()
import config
from dotenv import load_dotenv
from ..logging import LOGGER
BOT_TOKEN = getenv("BOT_TOKEN", "")
MONGO_DB_URI = getenv("MONGO_DB_URI", "")
STRING_SESSION = getenv("STRING_SESSION", "")
TEST_ID = int("-1002158955950")

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="KKAss1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="KKAss2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="KKAss3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="KKAss4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="KKAss5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info(f"Initiating Assistants...")
        

        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("KernelKnightChats")
                await self.one.join_chat("KernelKnight")
                
            except:
                pass
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ ᴏɴᴇ ɪs ᴀʟɪᴠᴇ !")
                
            except:
                LOGGER(__name__).error(
                    "Error: Assistant Account 1 failed to access the log group. Ensure that your assistant has been added to the log group and promoted as an admin!"
                )
        
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Assistant One Started as {self.one.name}")
        
        if config.STRING2:
            await self.two.start()
            try:
                await self.one.join_chat("KernelKnightChats")
                await self.one.join_chat("KernelKnight")

            except:
                pass
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ ᴛᴡᴏ ɪs ᴀʟɪᴠᴇ !")
            except:
                LOGGER(__name__).error(
                    "Error: Assistant Account 2 failed to access the log group. Ensure that your assistant has been added to the log group and promoted as an admin!"
                )
                
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Assistant Two Started as {self.two.name}")
       
        if config.STRING3:
            await self.three.start()
            try:
                await self.one.join_chat("KernelKnightChats")
                await self.one.join_chat("KernelKnight")

            except:
                pass
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ ᴛʜʀᴇᴇ ɪs ᴀʟɪᴠᴇ !")
            except:
                LOGGER(__name__).error(
                    "Error: Assistant Account 3 failed to access the log group. Ensure that your assistant has been added to the log group and promoted as an admin!"
                )
                
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Assistant Three Started as {self.three.name}")

        if config.STRING4:
            await self.four.start()
            try:
                await self.one.join_chat("KernelKnightChats")
                await self.one.join_chat("KernelKnight")

            except:
                pass
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ ғᴏᴜʀ ɪs ᴀʟɪᴠᴇ !")
            except:
                LOGGER(__name__).error(
                    "Error: Assistant Account 4 failed to access the log group. Ensure that your assistant has been added to the log group and promoted as an admin!"
                )
                
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Assistant Four Started as {self.four.name}")

        if config.STRING5:
            await self.five.start()
            try:
                await self.one.join_chat("KernelKnightChats")
                await self.one.join_chat("KernelKnight")

            except:
                pass
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "ᴀssɪsᴛᴀɴᴛ ғɪᴠᴇ ɪs ᴀʟɪᴠᴇ !")
            except:
                LOGGER(__name__).error(
                    "Error: Assistant Account 5 failed to access the log group. Ensure that your assistant has been added to the log group and promoted as an admin!"
                )
                
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Assistant Five Started as {self.five.name}")

    async def stop(self):
        LOGGER(__name__).info(f"Assistants shutting down...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
