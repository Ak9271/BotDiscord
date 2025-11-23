import os
import discord

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = discord.Client(intents=discord.Intents.all())

@bot.event
async def on_ready(): 
    print("Bot allumé ")

@bot.event
async def on_message(message: discord.Message):
    if message.content =='bonjour':
        channel = message.channel
        await channel.send("Salut")

bot.run(TOKEN)
