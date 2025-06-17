import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os

print(f"🔧 Loaded DISCORD_CHANNEL_ID from env: '{os.getenv('DISCORD_CHANNEL_ID')}'")

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
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f"🤖 Logged in as {client.user}")
        print(f"📌 Looking for channel ID: {DISCORD_CHANNEL_ID}")
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            print("📨 Channel found. Attempting to send message...")
            try:
                await channel.send(fetch_daily_reading())
                print("✅ Message sent.")
            except Exception as send_error:
                print(f"❌ Failed to send message: {send_error}")
        else:
            print("❌ Channel not found. Check ID or bot permissions.")
        await client.close()
        print("👋 Bot closed.")

    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"🔥 Login error: {e}")

if __name__ == "__main__":
    asyncio.run(post_to_discord())
