import os
import discord

TOKEN = os.getenv("TOKEN")
bot = discord.Client(intents=discord.Intents.all())
bot.run(TOKEN)

print ('Lancement du bot')