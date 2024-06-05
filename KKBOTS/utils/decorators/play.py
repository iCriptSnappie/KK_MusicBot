import asyncio
import logging

from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from KKBOTS import YouTube, app
from KKBOTS.misc import SUDOERS
from KKBOTS.utils.database import (
    get_assistant,
    get_cmode,
    get_lang,
    get_playmode,
    get_playtype,
    is_active_chat,
    is_maintenance,
)
from KKBOTS.utils.inline import botplaylist_markup
from config import PLAYLIST_IMG_URL, SUPPORT_CHAT, adminlist
from strings import get_string

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

links = {}

def PlayWrapper(command):
    async def wrapper(client, message):
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)

            if message.sender_chat:
                upl = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="ʜᴏᴡ ᴛᴏ ғɪx ?",
                                callback_data="KKmousAdmin",
                            ),
                        ]
                    ]
                )
                return await message.reply_text(_["general_3"], reply_markup=upl)

            if await is_maintenance() is False:
                if message.from_user.id not in SUDOERS:
                    return await message.reply_text(
                        text=f"{app.mention} ɪs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ, ᴠɪsɪᴛ <a href={SUPPORT_CHAT}>sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ</a> ғᴏʀ ᴋɴᴏᴡɪɴɢ ᴛʜᴇ ʀᴇᴀsᴏɴ.",
                        disable_web_page_preview=True,
                    )

            try:
                await message.delete()
            except Exception as e:
                logger.error(f"Failed to delete message: {e}")

            audio_telegram = (
                (message.reply_to_message.audio or message.reply_to_message.voice)
                if message.reply_to_message
                else None
            )
            video_telegram = (
                (message.reply_to_message.video or message.reply_to_message.document)
                if message.reply_to_message
                else None
            )
            url = await YouTube.url(message)
            if audio_telegram is None and video_telegram is None and url is None:
                if len(message.command) < 2:
                    if "stream" in message.command:
                        return await message.reply_text(_["str_1"])
                    buttons = botplaylist_markup(_)
                    return await message.reply_photo(
                        photo=PLAYLIST_IMG_URL,
                        caption=_["play_18"],
                        reply_markup=InlineKeyboardMarkup(buttons),
                    )
            if message.command[0][0] == "c":
                chat_id = await get_cmode(message.chat.id)
                if chat_id is None:
                    return await message.reply_text(_["setting_7"])
                try:
                    chat = await app.get_chat(chat_id)
                except Exception as e:
                    logger.error(f"Failed to get chat: {e}")
                    return await message.reply_text(_["cplay_4"])
                channel = chat.title
            else:
                chat_id = message.chat.id
                channel = None
            playmode = await get_playmode(message.chat.id)
            playty = await get_playtype(message.chat.id)
            if playty != "Everyone":
                if message.from_user.id not in SUDOERS:
                    admins = adminlist.get(message.chat.id)
                    if not admins:
                        return await message.reply_text(_["admin_13"])
                    else:
                        if message.from_user.id not in admins:
                            return await message.reply_text(_["play_4"])
            if message.command[0][0] == "v":
                video = True
            else:
                if "-v" in message.text:
                    video = True
                else:
                    video = True if message.command[0][1] == "v" else None
            if message.command[0][-1] == "e":
                if not await is_active_chat(chat_id):
                    return await message.reply_text(_["play_16"])
                fplay = True
            else:
                fplay = None

            if not await is_active_chat(chat_id):
                userbot = await get_assistant(chat_id)
                try:
                    try:
                        get = await app.get_chat_member(chat_id, userbot.id)
                    except ChatAdminRequired:
                        return await message.reply_text(_["call_1"])
                    if (
                        get.status == ChatMemberStatus.BANNED
                        or get.status == ChatMemberStatus.RESTRICTED
                    ):
                        return await message.reply_text(
                            _["call_2"].format(
                                app.mention, userbot.id, userbot.name, userbot.username
                            )
                        )
                except UserNotParticipant:
                    if chat_id in links:
                        invitelink = links[chat_id]
                    else:
                        if message.chat.username:
                            invitelink = message.chat.username
                            try:
                                await userbot.resolve_peer(invitelink)
                            except Exception as e:
                                logger.error(f"Failed to resolve peer: {e}")
                        else:
                            try:
                                invitelink = await app.export_chat_invite_link(chat_id)
                            except ChatAdminRequired:
                                return await message.reply_text(_["call_1"])
                            except Exception as e:
                                logger.error(f"Failed to export chat invite link: {e}")
                                return await message.reply_text(
                                    _["call_3"].format(app.mention, type(e).__name__)
                                )

                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace(
                            "https://t.me/+", "https://t.me/joinchat/"
                        )
                    myu = await message.reply_text(_["call_4"].format(app.mention))
                    try:
                        await asyncio.sleep(1)
                        await userbot.join_chat(invitelink)
                    except InviteRequestSent:
                        try:
                            await app.approve_chat_join_request(chat_id, userbot.id)
                        except Exception as e:
                            logger.error(f"Failed to approve chat join request: {e}")
                            return await message.reply_text(
                                _["call_3"].format(app.mention, type(e).__name__)
                            )
                        await asyncio.sleep(3)
                        await myu.edit(_["call_5"].format(app.mention))
                    except UserAlreadyParticipant:
                        pass
                    except Exception as e:
                        logger.error(f"Failed to join chat: {e}")
                        return await message.reply_text(
                            _["call_3"].format(app.mention, type(e).__name__)
                        )

                    links[chat_id] = invitelink

                    try:
                        await userbot.resolve_peer(chat_id)
                    except Exception as e:
                        logger.error(f"Failed to resolve peer after joining: {e}")

            return await command(
                client,
                message,
                _,
                chat_id,
                video,
                channel,
                playmode,
                url,
                fplay,
            )
        except NameError as e:
            logger.error(f"NameError: {e}")
            await message.reply_text(f"» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : {e}")
        except Exception as e:
            logger.error(f"Exception: {e}")
            await message.reply_text(f"» sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ.\n\nᴇxᴄᴇᴘᴛɪᴏɴ : {e}")

    return wrapper