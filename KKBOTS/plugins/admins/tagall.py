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
    "kya yaar itna gumsoom rehte ho thoda ladkio se v baat kar liya kro achha lagega tumhe",
    "tumhari gf hai??",
    "bhai ye kya sun raha hu me?",
    "mujhe tumhare bare me kuch pata chala hai, kya wo sach hai??",
    "tum owner ki bandi se baat krte ho ruk avi owner ko batata hu",
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
    "owner ka lafda ho gya aaj bhai tamasha dekhnge saath me😁😀",
    "bhai owner ka breakup ho gya😥",
    "so sad for you, suna hai tumhara breakup ho gya😥",
    "oo hello dm mat kar mujhe, nhi tera chalan kat jayega",
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
    "apne group me [ @KK_VCMUSICBOT ] ko add kro or lag free music suno",
    "muast music bot hai [ @KK_VCMUSICBOT ] apne group me add kro or lag free music suno",
    "Truth And Dare Kheloge..? 😊",
    "Aaj Mummy Ne Data Yr🥺🥺",
    "Join Kar Lo🤗",
    "Ek Dil Hai Ek Dil Hi To Hai😗😗",
    "Tumhare Dost Kaha Gye🥺",
    "My Cute Owner{ @KernelKnight}🥰",
    "Kaha Khoye Ho Jaan😜",
    "Good N8 Ji Bhut Rat Ho gyi🥰",
]

NIGHT_TAG = [
    "Oye bahot raat ho gyi, sona nhi hai kya??",
    "oyee hoyee kiske saath baat kar rhe ho😁",
    "aaj raat ka scene bana le🤤",
    "kya kr rhe ho baby??",
    "itni raat me razai me ghus kr phone chala rhe ho ruko tumhari mummy ko bolti hu🙂",
    "raat bahot ho gyi so jao aap, nhi to group me khubsurat khubsurat ladkio se baat kro hehe 😍😘",
    "avi tak jaag rhe ho...hmm hmmm kya baat hai 😂",
    "aadhi raat ko ham doston..ki soi aatma ko jagaate hai...aur unake jaagane ke baad..ham khud so jaate hai !! 🤣😂🤣",
    "Oye So Gye Kya Online Aao😊",
    "goog night 😪",
    "so ja bachhe",
    "oye itni raat me akele kya kar raha aaj group me mast cute girls active hai aaj grup me",
    "good night radhe radhe",
    "so jao kl jaldi v uthna hai tumhe nhi to mummy ki flying chappal tumhare muhh pe padegi hehe",
    "so jao yaar wo nhi aane wali",
    "or bhai bhabhi kaisi hai??",
    "avi tak jag rhe ho? [@KK_VCMUSICBOT] ko apne group me add kro or lag free music suno..😋😘",
    "itni raat me kiske saath gulu gulu kr rhe ho..😁😂",
    "chupchap phone rakho or so jao 11 baj rhe 😐",
    "flirt karna band kr bhai raat bahaot ho gyi ab soja or bholi bhali ladkio ko v sone de",
    "mummy ko batau tere ki tu aadhi raat me masoom ladkio ke saath baat karta hai 😎",
    "so jao babu, nhi to apke dark circles aajayenge😥",
    "maine raat ko jaag kar dekha hai, subha hone me saalon lagte hain 🙃",
    "Raat me jagne wala har saksh aashiq nhi hota shaheb, kuch ko zimmedari sone nhi deti"
    "i love you baby😍, ye lo puchhiii😘😘 ab so jao chup chap!!",
    "mukkhi maar dungi ..so jao nhi to",
    "sab pata hai mujhe tum apne bandi se baat kr rhe ho, ruko tumhe papa ko batata hu avi",
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
    "OYE JANU VC AAO ME GANA SUNA RHI HU",
    "OYE EK CUTE LADKI VC ME HAI JALDI",
    "AAJA VC MOVIE DEKHNGE SAATH ME",
    "BHABHI KO LE KR JALDI VC AAO EK SURPRISE HAI",
    "OYEE JALDI VC AA GROUP KA OWNER OR USKI BANDI KA MAST FIGHT CHL RHA 😆😁",
    "GROUP KI SABSE CUTE GIRL VC PE LIVE HAI JALDI AA BHAI",
    "JALDI JOIN KAR VC OWNER ROMANCE KAR RAHA VC PE🤤😂",
    "OWNER KA PANGA HO GYA VC PE AAJA BHAI TERA HI INTEZAR KAR RAHA",
    "BHAI KYA KAR DIYA TUNE...TUJHSE YEH UMMID NHI THI, VC PE TERI HI BAAT CHL RHI 😔",
    "VC TAPAK TAJASWI LONDE",
    "CUTE BANDI VC PE HAI AAJ JAO JALDI"
]



@app.on_message(filters.command(["tagall", "all", "utag"], prefixes=PREFIXES))
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


@app.on_message(filters.command(["ntag"], prefixes=PREFIXES))
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
            txt = f"{usrtxt} {random.choice(NIGHT_TAG)}"
            await client.send_message(chat_id, txt)
            await asyncio.sleep(6)
            usrnum = 0
            usrtxt = ""
    try:
        spam_chats.remove(chat_id)
    except:
        pass


@app.on_message(filters.command(["cancel", "stop", "stopvctag", "stoptag", "stopntag"]))
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
        return await message.reply("ᴍᴇɴᴛɪᴏɴ ᴘʀᴏᴄᴇss sᴛᴏᴘᴘᴇᴅ")
