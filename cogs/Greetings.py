import discord
from discord.ext import commands
from discord import Member

class Greetings(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Astel
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello, I am Astel!👾")

    #Hello
    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(1318216623097643132)
        if channel:
            await channel.send("Welcome!👾")

    #Goodbye
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.client.get_channel(1318216623097643132)
        if channel:
            await channel.send("Goodbye!👾")
    
async def setup(client):
    await client.add_cog(Greetings(client))