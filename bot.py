import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import validators
import getUrlByName

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
    if ctx.author.voice is None:
        await ctx.send('You need to be in a voice channel to use this command')
    else:
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
        if not validators.url(url):
            url = getUrlByName.find(url)
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
        voice.is_playing()
        await ctx.send('Now playing ' + url)
    else:
        await ctx.send("Already playing song")
        return

@client.command()
async def clear(ctx, ammount = 2):
    await ctx.channel.purge(limit = ammount)

@client.command()
async def skip(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.pause()

@client.command()
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    voice.resume()

client.run(os.getenv("TOKEN"))