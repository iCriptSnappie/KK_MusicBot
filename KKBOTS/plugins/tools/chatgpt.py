import requests
import random
from KKBOTS import telethn as tbot
from KKBOTS.events import register
from pyrogram.types import Message

GPT_API_URL = "https://chatgpt.apinepdev.workers.dev"

MSG_POST_URL = ['', '']

@register(pattern="^/prompt(?: (.*)|$)")
async def chat_gpt(event):
    if event.fwd_from:
        return

    query = event.pattern_match.group(1)

    if not query:
        if event.reply_to_message:
            replied_msg = await event.get_reply_message()
            if replied_msg and replied_msg.text:
                query = replied_msg.text
            else:
                await event.reply("❍ The replied message does not contain text.")
                return
        else:
            await event.reply("❍ Please provide a question after the /prompt command or reply to a message.")
            return

    try:
        response = requests.get(f"{GPT_API_URL}/?question={query}")

        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "❍ No answer received from Chat AI.")
            # Select a random post URL
            signature = random.choice(MSG_POST_URL)
            reply_message = f"{answer}\n\n{signature}"
            await event.reply(reply_message)
        else:
            await event.reply("Error communicating with ChatGPT API.")
    except requests.exceptions.RequestException as e:
        await event.reply(f"Error: {str(e)}. Please try again later.")
    except Exception as e:
        await event.reply(f"Unexpected error: {str(e)}. Please try again later.")