import os
import discord
from discord.ext import commands
from arbre_question import ArbreQuestion, generer_calcul_1, generer_calcul_2, generer_calcul_3, generer_calcul_4, generer_calcul_5, generer_calcul_6

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
etat_user = {}

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
    
    # Gestion des reposes
    if message.author.id in etat_user and not message.content.startswith('!'):
        user_state = etat_user[message.author.id]
        reponse_user = message.content
        reponse_attendue = str(user_state['reponse_attendue'])

        if reponse_user == reponse_attendue:
            #Bonne reponse
            etape_actuelle_key = user_state['etape']
            etape_actuelle = ArbreQuestion[etape_actuelle_key]
            next_step_key = etape_actuelle.get("reussite")

            if next_step_key == "conclusion_finale" or next_step_key is None:
                await message.channel.send(f"{ArbreQuestion['conclusion_finale']['conclusion']}")
                del etat_user[message.author.id]
            else:
                #Générer prochaine question
                next_step = ArbreQuestion[next_step_key]
                question_text, reponse_attendue = next_step["generateur"]()

                etat_user[message.author.id] = {
                    'etape': next_step_key,
                    'reponse_attendue': reponse_attendue,
                    'tentatives': next_step["erreur_max"]
                }

                msg = f"✅ Bravo ! Question suivante :\n**{question_text}**\n*Tentatives restantes : {next_step['erreur_max']}* ✅"
                await message.channel.send(msg)
        else:
            #Mauvaise reponse
            user_state['tentatives'] -= 1
            if user_state['tentatives'] <= 0:
                etape_actuelle_key = user_state['etape']
                etape_actuelle = ArbreQuestion[etape_actuelle_key]
                next_step_key = etape_actuelle.get("echec_progression")

                if next_step_key == "conclusion_finale" or next_step_key is None:
                    await message.channel.send(f"Dommage, c'est perdu ! La réponse était {reponse_attendue}. {ArbreQuestion['echec']['conclusion']}")
                    del etat_user[message.author.id]
                else:
                    #Générer prochaine question après échec
                    next_step = ArbreQuestion[next_step_key]
                    question_text, reponse_attendue = next_step["generateur"]()

                    etat_user[message.author.id] = {
                        'etape': next_step_key,
                        'reponse_attendue': reponse_attendue,
                        'tentatives': next_step["erreur_max"]
                    }

                    msg = f"❌ Mauvaise réponse. Progression vers une autre question :\n**{question_text}**\n*Tentatives restantes : {next_step['erreur_max']}* ❌"
                    await message.channel.send(msg)
            else:
                await message.channel.send(f"❌ Mauvaise réponse. Il te reste {user_state['tentatives']} tentatives. ❌")

        return

    #Permettre commandes de base avec "!"
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

@bot.command(name="quiz", aliases=["quizz"])
async def quiz(ctx):
    print(f"Commande quiz lancée par {ctx.author}")
    user_id = ctx.author.id
    etape1_key = "start"
    etape1 = ArbreQuestion[etape1_key]

    if user_id in etat_user:
        await ctx.send("Tu fais déjà un quiz .")
        return

    question_text, reponse_attendue = etape1["generateur"]()

    etat_user[user_id] = {
        'etape': etape1_key,
        'reponse_attendue': reponse_attendue,
        'tentatives': etape1["erreur_max"]
    }

    message = f"Bonjour {ctx.author.mention} ! Commençons le questionnaire de calcul mental.\n\n"
    message += f"**CALCUL :** {question_text}\n"
    message += f"*Tentatives restantes : {etape1['erreur_max']}*"
    await ctx.send(message)

bot.run(TOKEN)
