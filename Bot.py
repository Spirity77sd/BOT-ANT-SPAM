import discord
from discord.ext import commands
import asyncio

TOKEN = "SEU_TOKEN_AQUI"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

spam_users = {}

@bot.event
async def on_ready():
    print(f"Logado como {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    user_id = message.author.id
    if user_id not in spam_users:
        spam_users[user_id] = []

    spam_users[user_id].append(message.created_at.timestamp())

    # Remove mensagens antigas
    spam_users[user_id] = [t for t in spam_users[user_id] if message.created_at.timestamp() - t < 5]

    if len(spam_users[user_id]) > 5:
        await message.author.kick(reason="Spam detectado!")
        await message.channel.send(f"{message.author.mention} foi expulso por spam!")
        del spam_users[user_id]

    await bot.process_commands(message)

bot.run(TOKEN)
