import asyncio
import importlib

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from KKBOTS import LOGGER, app, userbot
from KKBOTS.core.call import KK
from KKBOTS.misc import sudo
from KKBOTS.plugins import ALL_MODULES
from KKBOTS.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS


async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("String Session Not Filled, Please Fill a Pyrogram V2 Session")
        
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("KKBOTS.plugins" + all_module)
    LOGGER("KKBOTS.plugins").info("All features have been successfully loaded.")
    await userbot.start()
    await KK.start()
    await KK.decorators()
    LOGGER("KKBOTS").info("╔═════ஜ۩۞۩ஜ════╗\n  ♨️𝗠𝗔𝗗𝗘 𝗕𝗬 𝗞𝗘𝗥𝗡𝗘𝗟 𝗞𝗡𝗜𝗚𝗛𝗧♨️\n╚═════ஜ۩۞۩ஜ════╝"
    )
    await idle()
    await app.stop()
    await userbot.stop()
    LOGGER("KKBOTS").info("                 ╔═════ஜ۩۞۩ஜ════╗\n  ♨️𝗠𝗔𝗗𝗘 𝗕𝗬 𝗞𝗘𝗥𝗡𝗘𝗟 𝗞𝗡𝗜𝗚𝗛𝗧♨️\n╚═════ஜ۩۞۩ஜ════╝")
    

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
