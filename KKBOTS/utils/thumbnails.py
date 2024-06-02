import os
import re
import random
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageFont, ImageOps
from unidecode import unidecode
from youtubesearchpython import VideosSearch

from KKBOTS import app
from config import YOUTUBE_IMG_URL

MAX_WIDTH = 1280
MAX_HEIGHT = 720
FONT_SIZE = 30
MAX_TITLE_LENGTH = 60

def change_image_size(max_width, max_height, image):
    width_ratio = max_width / image.size[0]
    height_ratio = max_height / image.size[1]
    new_width = int(width_ratio * image.size[0])
    new_height = int(height_ratio * image.size[1])
    return image.resize((new_width, new_height))

def clear_text(text):
    words = text.split(" ")
    title = ""
    for word in words:
        if len(title) + len(word) < MAX_TITLE_LENGTH:
            title += " " + word
    return title.strip()

async def get_thumb(video_id):
    if os.path.isfile(f"cache/{video_id}.png"):
        return f"cache/{video_id}.png"

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            title = result.get("title", "Unsupported Title").title()
            duration = result.get("duration", "Unknown Mins")
            views = result.get("viewCount", {}).get("short", "Unknown Views")
            channel = result.get("channel", {}).get("name", "Unknown Channel")
            thumbnail = result.get("thumbnails", [])[0].get("url", "").split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    async with aiofiles.open(f"cache/thumb{video_id}.png", mode="wb") as f:
                        await f.write(await resp.read())

        border_color = random.choice(["white", "red", "orange", "yellow", "green", "cyan", "azure", "blue", "violet", "magenta", "pink"])
        youtube = Image.open(f"cache/thumb{video_id}.png")
        image_resized = change_image_size(MAX_WIDTH, MAX_HEIGHT, youtube)
        enhanced_image = ImageEnhance.Brightness(image_resized).enhance(1.1)
        enhanced_image = ImageEnhance.Contrast(enhanced_image).enhance(1.1)
        bordered_image = ImageOps.expand(enhanced_image, border=7, fill=border_color)
        background = change_image_size(MAX_WIDTH, MAX_HEIGHT, bordered_image)

        draw = ImageDraw.Draw(background)
        arial = ImageFont.truetype("KKBOTS/assets/font2.ttf", FONT_SIZE)
        font = ImageFont.truetype("KKBOTS/assets/font.ttf", FONT_SIZE)

        draw.text((1110, 8), unidecode(app.name), fill="white", font=arial)
        draw.text((1, 1), f"{channel} | {views[:23]}", (1, 1, 1), font=arial)
        draw.text((1, 1), clear_text(title), (1, 1, 1), font=font)
        draw.line([(1, 1), (1, 1)], fill="white", width=1, joint="curve")
        draw.ellipse([(1, 1), (2, 1)], outline="white", fill="white", width=1)
        draw.text((1, 1), "00:00", (1, 1, 1), font=arial)
        draw.text((1, 1), f"{duration[:23]}", (1, 1, 1), font=arial)

        os.remove(f"cache/thumb{video_id}.png")
        background.save(f"cache/{video_id}.png")
        return f"cache/{video_id}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
