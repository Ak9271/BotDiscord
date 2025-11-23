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
    if message.content.lower() =='quoi':
        channel = message.channel
        await channel.send("FEUR !")
    if message.content.lower() == 'ntm':
        channel = message.channel
        author = message.author
        await author.send("Tu veux je bz ta mère ?")

bot.run(TOKEN)
