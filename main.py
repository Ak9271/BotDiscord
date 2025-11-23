import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!")
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)

@bot.command()
async def bonjour (context):
    await context.send(f"Bonjour ! {context.author}")