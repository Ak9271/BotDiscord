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
    
    history_commandes = "\n".join([f"{i+1}. {content}" for i, content in enumerate(reversed(commandes))])

    if len(history_commandes) > 2000:
        history_commandes = history_commandes[:1995] + "\n..."
    await interaction.followup.send(f"Historique des tes commandes:\n{history_commandes}")


@bot.tree.command(name="clearhistory", description="Supprime votre historique de messages dans ce canal (confirmation requise)")
async def clearhistory(interaction: discord.Interaction, confirm: bool = False):
    
    user = interaction.user
    channel = interaction.channel

    if channel is None:
        await interaction.response.send_message("Cette commande doit être utilisée dans un salon textuel.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    if not confirm:
        await interaction.followup.send(
            "Cette commande supprimera jusqu'aux 100 dernieres commandes que vous avez envoyées. "
            "Pour confirmer, réexécutez la commande et mettre `confirm=true`.",
            ephemeral=True,
        )
        return

    supp_count = 0
    async for msg in channel.history(limit=100):
        if msg.author.id == user.id:
            try:
                await msg.delete()
                supp_count += 1
            except Exception as e:
                print(f"Erreur suppression message {msg.id}: {e}")

    await interaction.followup.send(f"Suppression terminée : {supp_count} message supprimé.", ephemeral=True)

@bot.tree.command(name="dernierecommande", description="Affiche la dernière commande entrée")
async def dernierecommande(interaction: discord.Interaction):
    user = interaction.user
    channel = interaction.channel

    await interaction.response.defer()

    last_command = None
    async for msg in channel.history(limit=100):
        if msg.author.id == user.id:
            last_command = msg.content
            break

    if last_command is None:
        await interaction.followup.send("Aucune commande trouvée dans l'historique.")
    else:
        await interaction.followup.send(f"Votre dernière commande était : {last_command}")

bot.run(TOKEN)