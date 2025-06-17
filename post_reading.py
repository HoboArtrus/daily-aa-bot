import discord
import asyncio
import os

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))

async def post_to_discord():
    client = discord.Client(intents=discord.Intents.default())

    @client.event
    async def on_ready():
        print(f"🤖 Logged in as {client.user}")
        channel = client.get_channel(DISCORD_CHANNEL_ID)
        if channel:
            print("📨 Channel found. Sending test message...")
            await channel.send("✅ Test message from AA Daily Reading Bot!")
            print("✅ Message sent.")
        else:
            print("❌ Channel not found.")
        await client.close()
        print("👋 Bot closed.")

    try:
        await client.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"🔥 Error: {e}")

if __name__ == "__main__":
    asyncio.run(post_to_discord())
