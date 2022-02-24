import os

import asyncio
import discord
from discord.ext import commands
import youtube_dl


FFMPEG_OPTIONS = {
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
    "options": "-vn"
}
YDL_OPTIONS = {
    "format": "bestaudio"
}


client = commands.Bot(command_prefix='!')
playlist = []


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.command()
async def play(ctx, url=""):
    
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voiceClient == None:
        voiceClient = await ctx.author.voice.channel.connect()
    
    if voiceClient == None:
        ctx.send("You are not in a voice channel. Please join a voice channel first")
        return

    if voiceClient.is_playing():
        playlist.append(url.lstrip())
        await ctx.send(f"Queued {url.lstrip()}")
    else:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            voiceClient.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(next(ctx), client.loop))


async def next(ctx):
    if len(playlist) > 0:
        voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
        url = playlist.pop(0)
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            voiceClient.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(next(ctx), client.loop))


@client.command()
async def pause(ctx):
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voiceClient != None:
        voiceClient.pause()
        await ctx.send("Paused Audio")
    else:
        await ctx.send("No audio is playing")


@client.command()
async def resume(ctx):
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voiceClient != None:
        voiceClient.resume()
        await ctx.send("Resumed Audio")
    else:
        await ctx.send("No audio is queued")
        
        
@client.command()
async def skip(ctx):
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    


@client.command()
async def leave(ctx):
    voiceClient = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voiceClient.is_connected():
        await voiceClient.disconnect()
    else:
        await voiceClient.send("The bot is not connected to a voice channel")


client.run(os.getenv("TOKEN"))
