import discord
from discord.ext import commands
from reve_api import ReveAPI
# Discord bot token (Discord Developer Portal'dan alınır)
TOKEN = ""
# Reve API key
REVE_API_KEY = ""
# Bot ayarları
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
# ReveAPI instance
reve = ReveAPI(api_key=REVE_API_KEY)

@bot.event
async def on_ready():
    print(f"Bot giriş yaptı: {bot.user}")

@bot.event
async def on_message(message):
    # Bot kendi mesajına cevap vermesin
    if message.author == bot.user:
        return
    prompt = message.content
    await message.channel.send(" Görsel oluşturuluyor, lütfen bekleyin...")
    result = reve.generate_image(
        prompt=prompt,
        save_image="output.png"
    )
    if result and "image" in result:
        await message.channel.send(file=discord.File("output.png"))
    else:
        await message.channel.send("❌ Görsel oluşturulamadı.")
    await bot.process_commands(message)

bot.run(TOKEN)