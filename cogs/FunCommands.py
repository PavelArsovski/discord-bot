import discord
from discord.ext import commands
import random
import os

class FunCommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    # Coin
    @commands.command()
    async def coin(self, ctx):
        result = random.choice(["Heads", "Tails"])
        await ctx.send(f"The coin landed on: {result}")

    # Dice
    @commands.command()
    async def dice(self, ctx, sides: int = 6):
        result = random.randint(1, sides)
        await ctx.send(f"🎲 You rolled a {result} on a {sides}-sided dice!")

    # Russian Roulette
    @commands.command()
    async def russian(self, ctx):
        chamber = random.randint(1, 6)  
        trigger_pull = random.randint(1, 6)

        if chamber == trigger_pull:
            await ctx.send(f"💥 Bang! {ctx.author.mention}, you got shot!")
        else:
            await ctx.send(f"🔫 Click! {ctx.author.mention}, you survived this round.")

    # Roulette
    @commands.command()
    async def rulet(self, ctx, bet_number: int = None):
                
        if bet_number is None or bet_number < 0 or bet_number > 36:
            await ctx.send("Please provide a number between 0 and 36 to bet on. Example: !rullet 17")
            return
        
        spin_result = random.randint(0, 36)
        
        if bet_number == spin_result:
            await ctx.send(f"🎰 The wheel spun... and landed on {spin_result}! {ctx.author.mention}, you win! 🎉")
        else:
            await ctx.send(f"🎰 The wheel spun... and landed on {spin_result}. Sorry {ctx.author.mention}, you lost. Try again!")

async def setup(client):
    await client.add_cog(FunCommands(client))