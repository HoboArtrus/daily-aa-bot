import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

def fetch_daily_reading():
    print("🔍 Fetching daily reading from website...")
    url = "https://www.aahappyhour.com/daily-readings/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", class_="entry-content")
    if not content_div:
        print("❌ Could not find the reading on the page.")
        return "Could not fetch today's reading."
    reading = content_div.get_text(separator="\n", strip=True)
    print("✅ Successfully fetched reading.")
    return f"📖 **AA Daily Reading** 📖\n\n{reading}"

async def post_to_discord():
    print("🚀 Starting bot...")
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"🤖 Logged in as {client.user}")
    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"🔥 Unexpected error: {e}")
