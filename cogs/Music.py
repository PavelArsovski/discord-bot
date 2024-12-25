import discord
from discord.ext import commands
import yt_dlp
import asyncio
from collections import deque

yt_dlp.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best",
    "postprocessors": [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",
    }],
    "quiet": True,
}

ffmpeg_options = {
    "options": "-vn"
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if "entries" in data:
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.queue = deque()

    def play_next(self, ctx):
        """Play the next song in the queue."""
        if self.queue:
            song = self.queue.popleft()
            ctx.voice_client.play(
                song['player'],
                after=lambda e: self.play_next(ctx) if e is None else print(f"Player error: {e}")
            )
            asyncio.run_coroutine_threadsafe(ctx.send(f"Now playing: {song['title']}"), self.client.loop)

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("You are not in a voice channel! Please join one to use this command.")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            self.queue.clear()  
            await ctx.send("Disconnected from the voice channel.")
        else:
            await ctx.send("I'm not connected to any voice channel!")

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a song from YouTube by search query or URL."""
        async with ctx.typing():
            try:
                # Check if the query is a URL; if not, perform a YouTube search
                if not query.startswith("http"):
                    search_query = f"ytsearch:{query}"
                    info = await self.client.loop.run_in_executor(None, lambda: ytdl.extract_info(search_query, download=False))
                    if "entries" in info and len(info["entries"]) > 0:
                        video = info["entries"][0]
                        url = video["webpage_url"]
                    else:
                        await ctx.send("No results found for your search.")
                        return
                else:
                    url = query

                player = await YTDLSource.from_url(url, loop=self.client.loop, stream=True)
                
                if not ctx.voice_client.is_playing():
                    ctx.voice_client.play(
                        player,
                        after=lambda e: self.play_next(ctx) if e is None else print(f"Player error: {e}")
                    )
                    await ctx.send(f"Now playing: {player.title}")
                else:
                    self.queue.append({'player': player, 'title': player.title})
                    await ctx.send(f"Added to queue: {player.title}")
            except Exception as e:
                await ctx.send(f"The bot need to join the channel first!")

    @commands.command()
    async def queue(self, ctx):
        if self.queue:
            queue_list = "\n".join(f"{idx + 1}. {song['title']}" for idx, song in enumerate(self.queue))
            await ctx.send(f"Current queue:\n{queue_list}")
        else:
            await ctx.send("The queue is currently empty.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Skipped the current song!")
        else:
            await ctx.send("There's no song currently playing.")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Paused the song.")
        else:
            await ctx.send("There's no song currently playing.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Resumed the song.")
        else:
            await ctx.send("There's no song currently paused.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            self.queue.clear()  
            await ctx.send("Stopped the song and cleared the queue.")
        else:
            await ctx.send("There's no song currently playing.")

async def setup(client):
    await client.add_cog(Music(client))