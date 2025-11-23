import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready(): 
    print("Bot allumé ")
    #Synchroniser commandes
    try:
        synchronise = await bot.tree.sync()
        print(f"Commandes '/' synchronisées: {len(synchronise)}")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: discord.Message):
    #Pour pas que le bot se declenche lui meme
    if message.author.bot:
        return
    
    if message.content.lower() =='quoi':
        channel = message.channel
        await channel.send("FEUR !")

    if message.content.lower() == 'ntm':
        channel = message.channel
        author = message.author
        await author.send("Tu veux je bz ta mère ?")

    if message.content.lower() == 'au revoir':
        good_bye_channel = bot.get_channel(1442268548436332765)
        await good_bye_channel.send(f"Au revoir {message.author} !")

@bot.tree.command(name="youtube")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Voici le lien de la vidéo : https://youtu.be/xvFZjo5PgG0?si=kTfrnDxnsbj0axPe")

bot.run(TOKEN)
