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

@bot.tree.command(name="history", description="Affiche l'historique des commandes")
async def history(interaction: discord.Interaction):
    user = interaction.user
    channel = interaction.channel
    #eviter les erreurs si trop long
    await interaction.response.defer()

    commandes = []
    async for msg in channel.history(limit=100):
        if msg.author.id == user.id:
            commandes.append(f" - {msg.content}")
    if not commandes:
        await interaction.followup.send("Pas de commandes dans l'historique")
        return
    
    history_commandes = "\n".join(commandes)

    if len(history_commandes) > 2000:
        history_commandes = history_commandes[:1995] + "\n..."
    await interaction.followup.send(f"Historique des tes commandes:\n{history_commandes}")


bot.run(TOKEN)
