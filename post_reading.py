import requests
from bs4 import BeautifulSoup
import discord
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID_RAW = os.getenv("DISCORD_CHANNEL_ID")

# Debug prints — safe versions
print(f"🔒 DISCORD_TOKEN is {'set' if DISCORD_TOKEN else 'MISSING'}")
print(f"📢 Raw Channel ID: {DISCORD_CHANNEL_ID_RAW}")

try:
    DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID_RAW)
except Exception as e:
    print(f"❌ Error converting channel ID to int: {e}")
    DISCORD_CHANNEL_ID = None


# Debug prints — safe versions
print(f"🔒 DISCORD_TOKEN is {'set' if DISCORD_TOKEN else 'MISSING'}")
print(f"📢 Raw Channel ID: {DISCORD_CHANNEL_ID_RAW}")

try:
    DISCORD_CHANNEL_ID = int(DISCORD_CHANNEL_ID_RAW)
except Exception as e:
    print(f"❌ Error converting channel ID to int: {e}")
    DISCORD_CHANNEL_ID = None


def fetch_daily_reading():
    print("📚 Fetching daily reading from website...")
    url = "https://www.aahapphour.com/daily-readings/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    content_div = soup.find("div", class_="entry-content")

    if not content_div:
        print("❌ Could not find the reading on the page.")
        return "Could not fetch today's reading."

    reading = content_div.get_text(separator="\n", strip=True)
    print("✅ Successfully fetched reading.")
    return f"**AA Daily Reading**\n\n{reading}"

async def post_to_discord():
    print("🚀 Starting bot...")
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"✅ Logged in as {client.user}")
        
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel is None:
            print("❌ Channel not found. Check the CHANNEL ID.")
        else:
            message = fetch_daily_reading()
            try:
                await channel.send(message)
                print("📨 Successfully sent message.")
            except Exception as send_error:
                print(f"⚠️ Error sending message: {send_error}")

        await client.close()

    try:
        await client.start(DISCORD_TOKEN)
    except Exception as start_error:
        print(f"🔥 Unexpected error: {start_error}")

if __name__ == "__main__":
    asyncio.run(post_to_discord())
