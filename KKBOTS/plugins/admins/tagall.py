from KKBOTS import app 
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.errors import UserNotParticipant
from pyrogram.types import ChatPermissions
from config import PREFIXES

spam_chats = []

EMOJI = [ "🦋🦋🦋🦋🦋",
          "🧚🌸🧋🍬🫖",
          "🥀🌷🌹🌺💐",
          "🌸🌿💮🌱🌵",
          "❤️💚💙💜🖤",
          "💓💕💞💗💖",
          "🌸💐🌺🌹🦋",
          "🍔🦪🍛🍲🥗",
          "🍎🍓🍒🍑🌶️",
          "🧋🥤🧋🥛🍷",
          "🍬🍭🧁🎂🍡",
          "🍨🧉🍺☕🍻",
          "🥪🥧🍦🍥🍚",
          "🫖☕🍹🍷🥛",
          "☕🧃🍩🍦🍙",
          "🍁🌾💮🍂🌿",
          "🌨️🌥️⛈️🌩️🌧️",
          "🌷🏵️🌸🌺💐",
          "💮🌼🌻🍀🍁",
          "🧟🦸🦹🧙👸",
          "🧅🍠🥕🌽🥦",
          "🐷🐹🐭🐨🐻‍❄️",
          "🦋🐇🐀🐈🐈‍⬛",
          "🌼🌳🌲🌴🌵",
          "🥩🍋🍐🍈🍇",
          "🍴🍽️🔪🍶🥃",
          "🕌🏰🏩⛩️🏩",
          "🎉🎊🎈🎂🎀",
          "🪴🌵🌴🌳🌲",
          "🎄🎋🎍🎑🎎",
          "🦅🦜🕊️🦤🦢",
          "🦤🦩🦚🦃🦆",
          "🐬🦭🦈🐋🐳",
          "🐔🐟🐠🐡🦐",
          "🦩🦀🦑🐙🦪",
          "🐦🦂🕷️🕸️🐚",
          "🥪🍰🥧🍨🍨",
          " 🥬🍉🧁🧇",
        ]

TAGMES = [
    "Hey Baby Kaha Ho🤗🥱",
    "Oye So Gye Kya Online Aao😊",
    "Vc Chalo Baten Karte Hain Kuch Kuch😃",
    "Khana Kha Liye Ji..??🥲",
    "Ghar Me Sab Kaise Hain Ji🥺",
    "Pta Hai Bohot Miss Kar Rhi Thi Aapko🤭",
    "Oye Hal Chal Kesa Hai..??🤨",
    "Meri Bhi Setting Karba Doge..??🙂",
    "Aapka Name Kya hai..??🥲",
    "Nasta Hua Aapka..??😋",
    "Mere Ko Apne Group Me Kidnap Kr Lo😍",
    "Aapki Partner Aapko Dhund Rhe Hain Jldi Online Aayiae😅😅",
    "Mere Se Dosti Krogge..??🤔",
    "Sone Chal Gye Kya🙄🙄",
    "Ek Song Play Kro Na Plss😕",
    "Aap Kaha Se Ho..??🙃",
    "Hello Ji Namaste😛",
    "Hello Baby Kkrh..?🤔",
    "Do You Know Who Is My Owner.?",
    "Chlo Kuch Game Khelte Hain.🤗",
    "Aur Batao Kaise Ho Baby😇",
    "Tumhari Mummy Kya Kar Rahi Hai🤭",
    "Mere Se Bat Noi Krogge🥺🥺",
    "Oye Pagal Online Aa Ja😶",
    "Aaj Holiday Hai Kya School Me..??🤔",
    "Oye Good Morning😜",
    "Suno Ek Kam Hai Tumse🙂",
    "Koi Song Play Kro Na😪",
    "Nice To Meet Uh☺",
    "Hello🙊",
    "Study Comlete Hua??😺",
    "Bolo Na Kuch Yrr🥲",
    "Sonali Kon Hai...??😅",
    "Tumhari Ek Pic Milegi..?😅",
    "Mummy Aa Gyi Kya😆😆😆",
    "Or Batao Bhabhi Kaisi Hai😉",
    "I Love You🙈🙈🙈",
    "Do You Love Me..?👀",
    "Rakhi Kab Band Rahi Ho.??🙉",
    "Ek Song Sunau..?😹",
    "Online Aa Ja Re Song Suna Rahi Hu😻",
    "Instagram Chlate Ho..??🙃",
    "Whatsapp Number Doge Apna Tum..?😕",
    "Tumhe Kon Sa Music Sunna Pasand Hai..?🙃",
    "Sara Kam Khatam Ho Gya Aapka..?🙃",
    "Kaha Se Ho Aap😊",
    "Suno Na🧐",
    "Mera Ek Kaam Kar Doge..?",
    "By Tata Mat Bat Karna Aaj Ke Bad😠",
    "Mom Dad Kaise Hain..?❤",
    "Kya Hua..?👱",
    "Bohot Yaad Aa Rhi Hai 🤧❣️",
    "Bhool Gye Mujhe😏😏",
    "Juth Nhi Bolna Chahiye🤐",
    "Kha Lo Bhaw Mat Kro Baat😒",
    "Kya Hua😮😮",
    "Hii👀",
    "Aapke Jaisa Dost Ho Sath Me Fir Gum Kis Bat Ka 🙈",
    "Aaj Mai Sad Hu ☹️",
    "Musjhse Bhi Bat Kar Lo Na 🥺🥺",
    "Kya Kar Rahe Ho👀",
    "Kya Hal Chal Hai 🙂",
    "Kaha Se Ho Aap..?🤔",
    "Chatting Kar Lo Na..🥺",
    "Me Masoom Hu Na🥺🥺",
    "Kal Maja Aya Tha Na🤭😅",
    "Group Me Bat Kyu Nahi Karte Ho😕",
    "Aap Relationship Me Ho..?👀",
    "Kitna Chup Rahte Ho Yrr😼",
    "Aapko Gana Gane Aata Hai..?😸",
    "Ghumne Chaloge..??🙈",
    "Khush Raha Karo ✌️🤞",
    "Ham Dost Ban Sakte Hai...?🥰",
    "Kuch Bol Kyu Nhi Rahe Ho..🥺🥺",
    "Kuch Members Add Kar Do 🥲",
    "Single Ho Ya Mingle 😉",
    "Aao Party Karte Hain😋🥳",
    "Hemloo🧐",
    "Mujhe Bhul Gye Kya🥺",
    "Yaha Aa Jao:-[@KernelKnightChats]  Masti Karenge 🤭🤭",
    "Truth And Dare Kheloge..? 😊",
    "Aaj Mummy Ne Data Yr🥺🥺",
    "Join Kar Lo🤗",
    "Ek Dil Hai Ek Dil Hi To Hai😗😗",
    "Tumhare Dost Kaha Gye🥺",
    "My Cute Owner{ @KernelKnight}🥰",
    "Kaha Khoye Ho Jaan😜",
    "Good N8 Ji Bhut Rat Ho gyi🥰",
]

VC_TAG = [
    "OYE VC AAO NA PLS🥲",
    "JOIN VC FAST ITS IMAPORTANT😬",
    "COME VC BABY FAST🏓",
    "BABY TUM BHI THORA VC AANA🥰",
    "OYE CHAMTU VC AA EK EAM HAI🤨",
    "SUNO VC JOIN KR LO🤣",
    "VC AA JAIYE EK BAR😁",
    "VC TAPKO GAME CHALU HAI⚽",
    "VC AAO BARNA BAN HO JAOGE🥺",
    "SORRY VABY PLS VC AA JAO NA😥",
    "VC AANA EK CHIJ DIKHTI HU🙄",
    "VC ME CHECK KRKE BATAO TO SONG PLAY HO RHA H?🤔",
    "VC JOIN KRNE ME KYA JATA H THORA DER KAR LO NA🙂",
]



@app.on_message(filters.command(["tagall", "all", "tagmember", "utag", "stag", "hftag", "bstag", "eftag", "tag", "etag", "utag", "atag" ], prefixes=PREFIXES))
async def mentionall(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")

    if message.reply_to_message and message.text:
        return await message.reply("/tagall Good Morning 👈 ᴛʀʏ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏʀ ᴛᴀɢɢɪɴɢ...")
    elif message.text:
        mode = "text_on_cmd"
        msg = message.text
    elif message.reply_to_message:
        mode = "text_on_reply"
        msg = message.reply_to_message
        if not msg:
            return await message.reply("/tagall Good Morning 👈 ᴛʀʏ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏʀ ᴛᴀɢɢɪɴɢ...")
    else:
        return await message.reply("/tagall Good Morning 👈 ᴛʀʏ ʟɪᴋᴇ ᴛʜɪs / ʀᴇᴘʟʏ ᴀɴʏ ᴍᴇssᴀɢᴇ ɴᴇxᴛ ᴛɪᴍᴇ ғᴏʀ ᴛᴀɢɢɪɴɢ...")
    if chat_id in spam_chats:
        return await message.reply("ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            if mode == "text_on_cmd":
                txt = f"{usrtxt} {random.choice(TAGMES)}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(f"[{random.choice(EMOJI)}](tg://user?id={usr.user.id})")
            await asyncio.sleep(6)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["vctag"], prefixes=PREFIXES))
async def mention_allvc(client, message):
    chat_id = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴘs.")

    is_admin = False
    try:
        participant = await client.get_chat_member(chat_id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    if chat_id in spam_chats:
        return await message.reply("ᴘʟᴇᴀsᴇ ᴀᴛ ғɪʀsᴛ sᴛᴏᴘ ʀᴜɴɴɪɴɢ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss...")
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ""
    async for usr in client.get_chat_members(chat_id):
        if not chat_id in spam_chats:
            break
        if usr.user.is_bot:
            continue
        usrnum += 1
        usrtxt += f"[{usr.user.first_name}](tg://user?id={usr.user.id}) "

        if usrnum == 1:
            txt = f"{usrtxt} {random.choice(VC_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(6)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass



@app.on_message(filters.command(["cancel", "stop"]))
async def cancel_spam(client, message):
    if not message.chat.id in spam_chats:
        return await message.reply("ᴄᴜʀʀᴇɴᴛʟʏ ɪ'ᴍ ɴᴏᴛ ᴛᴀɢɢɪɴɢ.")
    is_admin = False
    try:
        participant = await client.get_chat_member(message.chat.id, message.from_user.id)
    except UserNotParticipant:
        is_admin = False
    else:
        if participant.status in (
            ChatMemberStatus.ADMINISTRATOR,
            ChatMemberStatus.OWNER
        ):
            is_admin = True
    if not is_admin:
        return await message.reply("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ, ᴏɴʟʏ ᴀᴅᴍɪɴs ᴄᴀɴ ᴛᴀɢ ᴍᴇᴍʙᴇʀs.")
    else:
        try:
            spam_chats.remove(message.chat.id)
        except:
            pass
        return await message.reply("♦ ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ ♦")
