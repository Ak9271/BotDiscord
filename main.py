import os
import discord
import json
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from discord.ext import commands
from arbre_question import ArbreQuestion

TOKEN = os.getenv("TOKEN")

print ('Lancement du bot ...')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
etat_user = {}
HISTORY_FILE = Path(__file__).parent / "command_history.json"
QUOI_FILE = Path(__file__).parent / "QUOI.txt"
INSULTS_FILE = Path(__file__).parent / "insultes.txt"
COURS_FILE = Path(__file__).parent / "cours-maths.pdf"

def load_insult_patterns():
    patterns = set()
    try:
        if INSULTS_FILE.exists():
            for line in INSULTS_FILE.read_text(encoding="utf-8").splitlines():
                p = line.strip()
                if not p:
                    continue
                p = p.replace("’", "'").lower()
                patterns.add(p)
    except Exception:
        pass
    return patterns


INSULT_PATTERNS = load_insult_patterns()


def load_quoi_patterns():
    patterns = set()
    try:
        if QUOI_FILE.exists():
            for line in QUOI_FILE.read_text(encoding="utf-8").splitlines():
                p = line.strip()
                if not p:
                    continue
                # normalize fancy apostrophes and lowercase
                p = p.replace("’", "'").lower()
                patterns.add(p)
    except Exception:
        pass
    return patterns

QUI_PATTERNS = load_quoi_patterns()

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
        "timestamp": datetime.utcnow().isoformat()
    }
    data.setdefault(key, [])
    data[key].insert(0, entry)
    #garde max 500 entrées/user
    if len(data[key]) > 500:
        data[key] = data[key][:500]
    save_history(data)

@bot.event
async def on_ready(): 
    print(" ")
    print("Bot allumé ")

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
    
    # Répondre feur si une proposition de QUOI.txt apparaît
    try:
        #QUI_PATTERNS = pouvoir definir une regle externe
        if isinstance(message.content, str) and QUI_PATTERNS:
            msg_norm = message.content.replace("’", "'").lower()
            for pat in QUI_PATTERNS:
                if pat and pat in msg_norm:
                    await message.channel.send("FEUR !")
                    break
    except Exception:
        pass

    #Détecte toute insulte dans insultes.txt
    try:
        if isinstance(message.content, str) and INSULT_PATTERNS:
            msg_norm = message.content.replace("’", "'").lower()
            for ins in INSULT_PATTERNS:
                if ins and ins in msg_norm:
                    channel = message.channel
                    author = message.author
                    print(f"[MOD] Insulte détectée de {author} ({author.id}) dans {getattr(channel, 'id', 'unknown')}: '{message.content}'")

                    try:
                        await channel.send(f"Insulte détectée de {author.mention}. Tentative de sanction en cours...")
                    except Exception:
                        pass

                    # mute message de 1 minute
                    mute_success = False
                    try:
                        timeout_fn = getattr(author, 'timeout', None)
                        if callable(timeout_fn):
                            try:
                                await author.timeout(timedelta(minutes=1), reason="Insulte détectée")
                                mute_success = True
                            except TypeError:
                                try:
                                    await author.timeout(datetime.utcnow() + timedelta(minutes=1), reason="Insulte détectée")
                                    mute_success = True
                                except Exception:
                                    traceback.print_exc()
                        else:
                            try:
                                await author.edit(communication_disabled_until=datetime.utcnow() + timedelta(minutes=1))
                                mute_success = True
                            except Exception:
                                traceback.print_exc()
                    except Exception:
                        traceback.print_exc()

                    # envoyer confirmation en salon selon le résultat
                    try:
                        if mute_success:
                            await channel.send(f"{author.mention} a été mute pour 1 minute pour insulte.")
                        else:
                            await channel.send(f"Impossible d'appliquer le mute à {author.mention} (vérifier permis du bot).")
                    except Exception:
                        pass

                    # envoyer le message de réponse (conserver comportement précédent)
                    try:
                        await channel.send(f"Attention les insultes {author.mention} ?")
                    except Exception:
                        print(f"[MOD] Impossible d'envoyer un DM à {author} ({author.id})")
                    break
    except Exception:
        traceback.print_exc()
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
                    await message.channel.send(f"C'est perdu ! La réponse était {reponse_attendue}. \n {ArbreQuestion['echec']['conclusion']}")
                    try:
                        if COURS_FILE.exists():
                            try:
                                await message.channel.send(file=discord.File(str(COURS_FILE)))
                            except Exception:
                                pass
                            try:
                                await message.author.send(file=discord.File(str(COURS_FILE)))
                            except Exception:
                                pass
                        else:
                            try:
                                await message.channel.send("Le fichier `cours-maths.pdf` est introuvable")
                            except Exception:
                                pass
                    except Exception:
                        pass
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

@bot.command(name="commande", description="Affiche toutes les commandes disponibles")
async def commande(ctx):
    commandes = [cmd.name for cmd in bot.commands]
    commandes_list = "\n!".join(commandes)
    await ctx.send(f"Commandes disponibles :\n`!{commandes_list}`")

@bot.command(name="history")
async def history(ctx):
    user = ctx.author
    channel = ctx.channel
    data = load_history()
    entrees = data.get(str(user.id), [])
    if not entrees:
        await ctx.send("Pas de commandes dans l'historique pour cet utilisateur.")
        return

    # afficher du + ancien au + récent
    to_show = list(reversed(entrees))
    # afficher aussi salon pour contexte
    lines = [f"{i+1}. {item['content']} (salon: {item.get('channel_id')}) - {item['timestamp']}" for i, item in enumerate(to_show)]
    history_commandes = "\n".join(lines)

    if len(history_commandes) > 2000:
        history_commandes = history_commandes[:1995] + "\n..."
    await ctx.send(f"Historique des tes commandes dans ce salon:\n{history_commandes}")


@bot.command(name="clearHistory")
async def clearHistory(ctx, confirm: str = None):
    user = ctx.author
    if confirm != "true":
        await ctx.send(
            "Cette commande supprimera tout l'historique local pour l'utilisateur. "
            "Pour confirmer, utilisez `!clearHistory true`."
        )
        return

    #Supprimer historique local pour cet user
    try:
        data = load_history()
        user_list = data.get(str(user.id), [])
        removed = len(user_list)
        data[str(user.id)] = []
        save_history(data)
    except Exception as e:
        print(f"Erreur mise à jour historique local: {e}")
        await ctx.send("Une erreur est survenue lors de la suppression de l'historique local.")
        return

    await ctx.send(f"Suppression terminée : {removed} entrée(s) d'historique supprimée(s) du fichier local pour votre utilisateur.")

@bot.command(name="lastCommande")
async def lastCommande(ctx):
    user = ctx.author
    channel = ctx.channel

    #hasattr = verifie si l'objet a un attribut
    if channel is None or not hasattr(channel, 'history'):
        await ctx.send("Cette commande doit être utilisée dans un salon textuel.")
        return

    last_command = None
    #Utiliser l'historique JSON 
    data = load_history()
    entrees = data.get(str(user.id), [])
    filtered = [e['content'] for e in entrees]
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