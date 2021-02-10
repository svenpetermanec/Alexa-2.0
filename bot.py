import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

load_dotenv()

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print('Alexa 2.0 online')

@client.command()
async def ping(ctx):
    await ctx.send(f'{round(client.latency * 1000)}ms')

@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()

@client.command()
async def play(ctx, url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    if not voice.is_playing():
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return

@client.command()
async def clear(ctx, ammount = 2):
    await ctx.channel.purge(limit = ammount)


client.run(os.getenv("TOKEN"))