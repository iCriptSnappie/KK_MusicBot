
from pyrogram import Client, filters
import random
from KKBOTS import app
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

SHAYRI = [
    "Teri mohabbat ki gehraai mein kho jaata hoon,\nTeri yaadon ke saath, ji ka saara khel kho jaata hoon.\nTeri baaton ka jaadu, dil ko chhu jaata hai,\nMohabbat ki raahon mein, main tere deewana ho jaata hoon.",
    "Teri har muskaan, dil ko bahla deti hai,\nTere bina main, adhoora sa mehsoos karta hoon.\nTeri yaadon mein, main kho jaata hoon har pal,\nTeri baahon mein, main kho jaata hoon saara jahaan.",
    "Mohabbat ki raahon mein, tumse milna hai mujhe,\nTeri har baat mein, main basa hoon sachmuch mein.\nTeri mohabbat ka sach, dil mein chhupa hai,\nTere saath har khushi, main ji raha hoon khoya hua.",
    "Teri mohabbat ki raahon mein kho jaata hoon,\nTere ishq ke geeton mein gunjne lagta hoon.\nTeri yaadon ki chaav mein bahak jaata hoon,\nMohabbat ki mithaas mein lipt jaata hoon.",
    "Teri har muskaan mere dil ko bhaati hai,\nTeri har baat mere dil ko bhaati hai.\nTere bina jeena lagta hai suna,\nTere pyaar ki boondein mere jeevan ko sajati hain.",
    "Teri mohabbat ka ehsaas hai zara,\nTere saath bitaaye har pal mein hain sacche khwaab hamare.\nTeri aankhon ki gehraai mein kho jaata hoon,\nMohabbat ki mithaas mein bahak jaata hoon.",
    "Teri mohabbat ka safar, dil ko chhu jaata hai,\nTere pyaar ki raahon mein, dil ko bahaka jaata hai.\nTere ishq ki raahon mein, dil ko kho jaata hai,\nMohabbat ka ehsaas, har pal mujhe sataata hai.",
    "Teri mohabbat ki baatein, dil ko chhu jaati hain,\nTeri yaadon ki mithaas, dil ko bahut sataati hai.\nTeri har muskaan, dil ko behlaati hai,\nMohabbat ki dhadkan, har pal mujhe behkaati hai.",
    "Teri mohabbat ki roshni, dil ko choomti hai,\nTeri mohabbat ki awaaz, dil ko bahut bhaati hai.\nTere bina jeena, dil ko bechain karta hai,\nTeri mohabbat mein, main khud ko kho jaata hoon.",
    "Teri mohabbat ka safar, lamba hai aur gehra,\nTere bina jeena, lagta hai bas ek sapna.\nTere ishq mein khoya, har pal hoon main,\nTeri yaadon mein uljha, beeta jaata hoon.",
    "Teri mohabbat ka sach, dil mein basa hai,\nTere bina jeena, dil ko sataata hai.\nTeri yaadon mein kho kar, jeena mushkil hai,\nMohabbat ki raahon mein, tere saath bitaana hai.",
    "Teri mohabbat ka izhaar kaise karun,\nTere bina zindagi adhoori si lagti hai.\nTeri aankhon mein hai mohabbat ki kahani,\nTere ishq mein har roz nayi zindagi paata hoon."
]

# Command
SHAYRI_COMMAND = ["gf", "bf", "shayri", "shayari", "sari", "shari", "love"]

# Command handler for groups
@app.on_message(filters.command(SHAYRI_COMMAND) & filters.group)
async def shayari_group(client: Client, message: Message):
    await send_shayari(message)

# Command handler for private messages
@app.on_message(filters.command(SHAYRI_COMMAND) & filters.private)
async def shayari_private(client: Client, message: Message):
    await send_shayari(message)

# Function to send shayari with inline keyboard
async def send_shayari(message: Message):
    if SHAYRI:
        shayari_text = random.choice(SHAYRI)
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "ɢʀᴏᴜᴘ", url="https://t.me/KernelKnightChats"),
                    InlineKeyboardButton(
                        "ᴄʜᴀɴɴᴇʟ", url="https://t.me/KernelKnight")
                ]
            ]
        )
        await message.reply_text(text=shayari_text, reply_markup=reply_markup)
    else:
        await message.reply_text(text="No shayaris available right now.")