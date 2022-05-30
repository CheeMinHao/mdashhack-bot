import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import util

load_dotenv()

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    """
    Initiates Bot
    """
    await client.change_presence(status=discord.Status.online, activity=discord.Game('MDashHack 2022'))
    print('Bot is ready')

# ============================================================================================================

@client.command()
async def load(ctx, extension):
    """
    Loads Cogs
    """
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    """
    Unloads Cogs
    """
    client.unload_extension(f'cogs.{extension}')

@client.command()
async def reload(ctx, extension):
    """
    Reloads Cogs
    """
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# Initialise All Cog Files
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Runs Client depending on Client Token
client.run(os.getenv('TOKEN'))
