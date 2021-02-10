import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = '-')

@client.event
async def on_ready():
    print('Alexa 2.0 online')

client.run(os.getenv("TOKEN"))