import random
from pyrogram import Client, filters
import requests

GPT_API_URL = "https://chatgpt.apinepdev.workers.dev"

MSG_POST_URL = ['', '']

@Client.on_message(filters.command("prompt"))
async def chat_gpt(client, message):
    if message.forward_from:
        return

    query = message.text.split(maxsplit=1)
    query = query[1] if len(query) > 1 else None

    if not query:
        if message.reply_to_message:
            replied_msg = await client.get_messages(message.chat.id, message.reply_to_message.message_id)
            if replied_msg and replied_msg.text:
                query = replied_msg.text
            else:
                await message.reply_text("❍ The replied message does not contain text.")
                return
        else:
            await message.reply_text("❍ Please provide a question after the /prompt command or reply to a message.")
            return

    try:
        response = requests.get(f"{GPT_API_URL}/?question={query}")

        if response.status_code == 200:
            result = response.json()
            answer = result.get("answer", "❍ No answer received from Chat AI.")
            # Select a random post URL
            signature = random.choice(MSG_POST_URL)
            reply_message = f"{answer}\n\n{signature}"
            await message.reply_text(reply_message)
        else:
            await message.reply_text("Error communicating with ChatGPT API.")
    except requests.exceptions.RequestException as e:
        await message.reply_text(f"Error: {str(e)}. Please try again later.")
    except Exception as e:
        await message.reply_text(f"Unexpected error: {str(e)}. Please try again later.")

