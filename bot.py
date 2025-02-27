from pyrogram import Client, filters
from motor.motor_asyncio import AsyncIOMotorClient
import requests
import asyncio

# Bot Configuration
API_ID = 29319456
API_HASH = "04e9939d28ffa58fee1d6461edb6138f"
BOT_TOKEN = "8092772448:AAETxWCs1Sptp8fjS7TGjTchbSw0kSoAXLA"
LOG_CHANNEL = -1002331535916
ALLOWED_USERS = [7931831907, 6509334754]
MONGO_URI = "mongodb+srv://bimandey43:2JDI1S2tE3uxt4SQ@cluster0.iadsz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
SHORTLINK_API = "https://onylinks.com/api?api=e7f6e1fc8784eea51294ca8104fff619fd60cd15&url={}&alias={}" 

app = Client("MovieBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
db_client = AsyncIOMotorClient(MONGO_URI)
db = db_client["telegram_file_bot"]
collection = db["files"]

@app.on_message(filters.private & filters.text)
async def search_movie(client, message):
    if message.from_user.id not in ALLOWED_USERS:
        await message.reply_text("❌ You are not authorized to use this bot!")
        return
    
    query = message.text
    async for msg in client.search_messages(LOG_CHANNEL, query):
        file_id = msg.document.file_id if msg.document else None
        if file_id:
            short_link = SHORTLINK_API.format(f"https://t.me/{client.me.username}?start={file_id}", query)
            response = requests.get(short_link).json()
            short_url = response.get("shortenedUrl", "")
            
            if short_url:
                await message.reply_text(f"🎬 Here is your movie: {short_url}")
                return
    
    await message.reply_text("❌ Movie not found!")

@app.on_message(filters.command("start") & filters.private)
async def send_file(client, message):
    command_args = message.text.split()
    if len(command_args) > 1:
        file_id = command_args[1]
        try:
            sent_message = await message.reply_document(file_id, caption="Here is your movie! 🎬")
            await asyncio.sleep(600)  # 10 minutes delay
            await sent_message.delete()
        except Exception as e:
            await message.reply_text(f"Error: {e}")
    else:
        await message.reply_text("Send me a movie name to search!")

app.run()
