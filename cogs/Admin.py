import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.utils import get

class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Forbiden messages
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content == "Pavel":
            await message.delete()
            await message.channel.send("You can't use that name!")
        elif message.content == "Toxic":
            await message.channel.send("Toksiko e peder")
    
    #Kick
    @commands.command()
    @has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'User {member} has been kicked.')

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to kick people!")

    #Ban
    @commands.command()
    @has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'User {member} has been banned.')

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permissions to ban people!")

    #Embed
    @commands.command()
    async def embed(self, ctx):
        embed = discord.Embed(
            title="GitHub",
            url="https://github.com/PavelArsovski",
            description="Created for fun",
            color=0x4dff4d
        )
        embed.set_author(name="Pavel A.")
        embed.set_footer(text="2024®")
        await ctx.send(embed=embed)

    #Commands permission
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have a permission to run this command.")

    #Send a private message to a user.
    @commands.command()
    async def message(self, ctx, user: discord.Member, *, message=None):
        message = message or "Welcome to the server!"
        embed = discord.Embed(title=message)
        await user.send(embed=embed)
        
        
    #AddRoles
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def addRole(self, ctx, user: discord.Member, *, role: discord.Role):
        
        if role in user.roles:
            await ctx.send(f"{user.mention} alredy has this role, {role}")
        else:
            await user.add_roles(role)
            await ctx.send(f"Added {role} to {user.mention}")        

    @addRole.error
    async def addRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permision to use this command!")


    #RemoveRole
    @commands.command(pass_context = True)
    @commands.has_permissions(manage_roles = True)
    async def removeRole(self, ctx, user: discord.Member, *, role: discord.Role):
        
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f"Removed {role} from {user.mention}")
        else:
            await ctx.send(f"{user.mention} does not have the role {role}")        

    @removeRole.error
    async def removeRole_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permision to use this command!")


async def setup(client):
    await client.add_cog(Admin(client))