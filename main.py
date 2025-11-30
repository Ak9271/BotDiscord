import os
import discord
import json
from pathlib import Path
from datetime import datetime
from discord.ext import commands
from arbre_question import ArbreQuestion

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
etat_user = {}
HISTORY_FILE = Path(__file__).parent / "command_history.json"


def load_history():
    if not HISTORY_FILE.exists():
        return {}
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_history(data: dict):
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to save history: {e}")


def add_history_entry(user_id: int, content: str, channel_id: int):
    data = load_history()
    key = str(user_id)
    entry = {
        "content": content,
        "channel_id": str(channel_id),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    data.setdefault(key, [])
    data[key].insert(0, entry)
    #garde max 500 entrées/user
    if len(data[key]) > 500:
        data[key] = data[key][:500]
    save_history(data)

@bot.event
async def on_ready(): 
    print("Bot allumé ")
    #Commandes de base avec préfixe "!"

@bot.event
async def on_message(message: discord.Message):
    #Pour pas que le bot se declenche lui meme
    if message.author.bot:
        return
    try:
        if isinstance(message.content, str) and message.content.startswith(('!', '/')):
            add_history_entry(message.author.id, message.content, message.channel.id if hasattr(message.channel, 'id') else None)
    except Exception:
        pass
    
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
    
    # Gestion des réposes
    if message.author.id in etat_user and not message.content.startswith('!'):
        user_state = etat_user[message.author.id]
        reponse_user = message.content
        reponse_attendue = str(user_state['reponse_attendue'])

        if reponse_user == reponse_attendue:
            #Bonne reponse
            etape_actuelle_key = user_state['etape']
            etape_actuelle = ArbreQuestion[etape_actuelle_key]
            next_step_key = etape_actuelle.get("reussite") or etape_actuelle.get("suivant")

            if next_step_key and next_step_key not in ArbreQuestion:
                match = next((k for k in ArbreQuestion.keys() if k.startswith(next_step_key)), None)
                if match:
                    next_step_key = match

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
                    'tentatives': next_step.get("erreur_max", 1)
                }

                msg = f"✅ Bravo ! Question suivante :\n**{question_text}**\n*Tentatives restantes : {next_step['erreur_max']}* ✅"
                await message.channel.send(msg)
        else:
            #Mauvaise reponse
            user_state['tentatives'] -= 1
            if user_state['tentatives'] <= 0:
                etape_actuelle_key = user_state['etape']
                etape_actuelle = ArbreQuestion[etape_actuelle_key]
                next_step_key = etape_actuelle.get("echec_progression") or etape_actuelle.get("suivant")

                if next_step_key and next_step_key not in ArbreQuestion:
                    match = next((k for k in ArbreQuestion.keys() if k.startswith(next_step_key)), None)
                    if match:
                        next_step_key = match

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
                        'tentatives': next_step.get("erreur_max", 1)
                    }

                    msg = f"❌ Mauvaise réponse. Progression vers une autre question :\n**{question_text}**\n*Tentatives restantes : {next_step.get('erreur_max',1)}* ❌"
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
    data = load_history()
    entrees = data.get(str(user.id), [])
    # filtrer par channel
    filtered = [e for e in entrees if e.get("channel_id") == str(channel.id)]
    if not filtered:
        await ctx.send("Pas de commandes dans l'historique pour ce salon.")
        return

    # afficher du + ancien au + récent
    to_show = list(reversed(filtered))
    lines = [f"{i+1}. {item['content']} ({item['timestamp']})" for i, item in enumerate(to_show)]
    history_commandes = "\n".join(lines)

    if len(history_commandes) > 2000:
        history_commandes = history_commandes[:1995] + "\n..."
    await ctx.send(f"Historique des tes commandes dans ce salon:\n{history_commandes}")


@bot.command(name="clearHistory")
async def clearHistory(ctx, confirm: str = None):
    
    user = ctx.author
    channel = ctx.channel

    if channel is None:
        await ctx.send("Cette commande doit être utilisée dans un salon textuel.")
        return

    if confirm != "true":
        await ctx.send(
            "Cette commande supprimera jusqu'aux 100 dernieres commandes que vous avez envoyées. "
            "Pour confirmer, utilisez `!clearHistory true`."
        )
        return

    #Supp l'historique sur json et non sur discord
    try:
        data = load_history()
        user_list = data.get(str(user.id), [])
        new_list = [e for e in user_list if e.get("channel_id") != str(channel.id)]
        removed = len(user_list) - len(new_list)
        data[str(user.id)] = new_list
        save_history(data)
    except Exception as e:
        print(f"Erreur mise à jour historique local: {e}")
        await ctx.send("Une erreur est survenue lors de la suppression de l'historique local.")
        return

    await ctx.send(f"Suppression terminée : {removed} entrée(s) d'historique supprimée(s) du fichier local.")

@bot.command(name="lastCommande")
async def lastCommande(ctx):
    user = ctx.author
    channel = ctx.channel

    #hasattr = verifie si l'objet a un attribut
    if channel is None or not hasattr(channel, 'history'):
        await ctx.send("Cette commande doit être utilisée dans un salon textuel.")
        return

    last_command = None
    # Utiliser l'historique JSON stocké
    data = load_history()
    entrees = data.get(str(user.id), [])
    #Garder que le salon actuel
    filtered = [e['content'] for e in entrees if e.get('channel_id') == str(channel.id)]
    if len(filtered) >= 2:
        await ctx.send(f"Votre avant-dernière commande était : {filtered[1]}")
    elif len(filtered) == 1:
        await ctx.send("Il n'y a qu'une seule commande dans l'historique.")
    else:
        await ctx.send("Aucune commande trouvée dans l'historique.")

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
