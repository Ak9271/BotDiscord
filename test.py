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
    if message.content =='quoi':
        channel = message.channel
        await channel.send("FEUR !")

bot.run(TOKEN)
