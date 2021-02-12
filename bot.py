import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from discord.utils import get
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL
import validators
import speech_recognition as sr
import urllib.request
import re

load_dotenv()

client = commands.Bot(command_prefix = '$')

def find(query):
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + query)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]

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
async def play(ctx, *url):
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    voice = get(client.voice_clients, guild=ctx.guild)

    link = '+'.join(url)
    if not voice.is_playing():
        if not validators.url(link):
            url = find(link)
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

# this is called from the background thread
def callback(recognizer, audio):
    try:
        print(recognizer.recognize_google(audio))
    except sr.RequestError as e:  
        print("error; {0}".format(e))

    except Exception as e:
        print (e)

r = sr.Recognizer()
m = sr.Microphone()
with m as source:
    r.adjust_for_ambient_noise(source)
# start listening in the background
stop_listening = r.listen_in_background(m, callback)
# `stop_listening` is now a function that, when called, stops background listening

# do some unrelated computations
client.run(os.getenv("TOKEN"))