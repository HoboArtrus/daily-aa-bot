import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

def fetch_daily_reading():
    url = "https://www.aahappyhour.com/daily-readings/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", class_="entry-content")
    if not content_div:
        return "Could not fetch today's reading."
    reading = content_div.get_text(separator="\n", strip=True)
    return f"📖 **AA Daily Reading** 📖\n\n{reading}"

async def post_to_discord():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            await channel.send(fetch_daily_reading())
            print("✅ Posted daily reading")
        else:
            print("❌ Channel not found")
        await client.close()

    await client.start(DISCORD_TOKEN)

if __name__ == "__main__":
    asyncio.run(post_to_discord())