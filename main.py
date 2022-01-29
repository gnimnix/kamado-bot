import os

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


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.command()
async def play(ctx, url=""):
    voiceClient = await ctx.author.voice.channel.connect()
    if voiceClient == None:
        ctx.send("You are not in a voice channel. Please join a voice channel first")
        return

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["formats"][0]['url']
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        voiceClient.play(source)


@client.command()
async def pause(ctx):
    if ctx.voice_client != None:
        ctx.voice_client.pause()
        await ctx.send("Paused Audio")
    else:
        await ctx.send("No audio is playing")


@client.command()
async def resume(ctx):
    if ctx.voice_client != None:
        ctx.voice_client.resume()
        await ctx.send("Resumed Audio")
    else:
        await ctx.send("No audio is queued")


@client.command()
async def leave(ctx):
    if ctx.voice_client.is_connected():
        await ctx.voice_client.disconnect()
    else:
        await ctx.voice_client.send("The bot is not connected to a voice channel")


client.run(os.getenv("TOKEN"))
