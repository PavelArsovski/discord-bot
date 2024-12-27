import discord
from discord.ext import commands
from discord import Member

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Astel Command
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, I am Astel! 👾")

    #Ping    
    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong!")

    # Welcome Message
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1318216623097643132)
        if channel:
            await channel.send(f"Welcome to the server, {member.mention}! 👾")

    # Goodbye Message
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1318216623097643132)
        if channel:
            await channel.send(f"Goodbye, {member.name}! 👾 We hope to see you again!")

async def setup(client):
    await client.add_cog(Greetings(client))