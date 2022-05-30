import discord
from discord.ext import commands
import util

class Purpose(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['readme'])
    async def _readme(self, ctx):

        if ctx.channel.id == int(980739089424855041):

            # If Yes, Purge the Old Read Me
            await ctx.channel.purge(limit=2)

            # Extract New Read Me Content
            read_me_content = util.get_read_me()

            # Create Embed for New Read Me
            embedVar = discord.Embed(title="Welcome to MDashHack 2022!", color=0x00ff00)
            embedVar.add_field(name="Hospitality Rules", value=read_me_content, inline=False)

            # Send New Read Me
            await ctx.channel.send(embed=embedVar)

        else:

            await ctx.channel.send("Wrong Channel")

    @commands.command(aliases = ['rules'])
    async def rules(self, ctx):

        if ctx.channel.id == int(980739089424855041):

            # If Yes, Purge the Old Rules
            await ctx.channel.purge(limit=2)

            # Extract New Rules Content
            read_me_content = util.get_rules()

            # Create Embed for New Rules
            embedVar = discord.Embed(title="Rules of MDashHack 2022", color=0x00ff00)
            embedVar.add_field(name="Rules", value=read_me_content, inline=False)

            # Send New Rules
            await ctx.channel.send(embed=embedVar)

        else:

            await ctx.channel.send("Wrong Channel")

    @commands.command(aliases = ['private'])
    async def private(self, ctx):
        await ctx.channel.purge(limit=2)
        embedVar = discord.Embed(title="Create Private Group", color=0x00ff00)
        embedVar.add_field(name="Create Your Very Own Private Chatroom!",value="Please react to the embed to get your own private group chat here in our discord!", inline=False)
        message = await ctx.channel.send(embed=embedVar)
        await message.add_reaction("🧠")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if reaction.emoji == '🧠' and reaction.message.channel.id == 980739089424855041:
            pass

def setup(client):
    client.add_cog(Purpose(client))