import discord
from discord.ext import commands
from discord import Interaction
import os
import asyncio
from apikeys import *

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True

client = commands.Bot(command_prefix='!', intents=intents)

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Activity(type = discord.ActivityType.listening, name = 'The Void'))
    print("The bot is now ready to use")
    print("---------------------------")
    

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            

async def  main():
    async with client:
        await load()
        await client.start(BOTTOKEN)    

asyncio.run(main())