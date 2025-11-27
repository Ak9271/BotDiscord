import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready(): 
    print("Bot allumé ")
    #Commandes traditionnelles avec préfixe ! activées

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
        await good_bye_channel.send(f"Retourne dans ton pays {message.author} !")

    if message.content.lower() == "je t'aime":
        channel = message.channel
        await channel.send("Je t'aime aussi mon bb!")
    
    # Permettre les commandes traditionnelles avec !
    await bot.process_commands(message)

@bot.command(name="history")
async def history(ctx):
    user = ctx.author
    channel = ctx.channel

    commandes = []
    async for msg in channel.history(limit=100):
        if msg.author.id == user.id:
            commandes.append(f" - {msg.content}")
    if not commandes:
        await ctx.send("Pas de commandes dans l'historique")
        return
    
    history_commandes = "\n".join([f"{i+1}. {content}" for i, content in enumerate(reversed(commandes))])

    if len(history_commandes) > 2000:
        history_commandes = history_commandes[:1995] + "\n..."
    await ctx.send(f"Historique des tes commandes:\n{history_commandes}")


@bot.command(name="clearhistory")
async def clearhistory(ctx, confirm: str = None):
    
    user = ctx.author
    channel = ctx.channel

    if channel is None:
        await ctx.send("Cette commande doit être utilisée dans un salon textuel.")
        return

    if confirm != "true":
        await ctx.send(
            "Cette commande supprimera jusqu'aux 100 dernieres commandes que vous avez envoyées. "
            "Pour confirmer, utilisez `!clearhistory true`."
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

    await ctx.send(f"Suppression terminée : {supp_count} message supprimé.")

@bot.command(name="dernierecommande")
async def dernierecommande(ctx):
    user = ctx.author
    channel = ctx.channel

    last_command = None
    async for msg in channel.history(limit=100):
        if msg.author.id == user.id:
            last_command = msg.content
            break

    if last_command is None:
        await ctx.send("Aucune commande trouvée dans l'historique.")
    else:
        await ctx.send(f"Votre dernière commande était : {last_command}")

bot.run(TOKEN)