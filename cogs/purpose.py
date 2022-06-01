import discord
from discord.ext import commands
import util
from dotenv import load_dotenv
import os

load_dotenv()

# Choose your environment
ENVIRONMENT = 'MDHACK'
# ENVIRONMENT = 'TESTING'

class Purpose(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.private_embed = None
        self.team_leader = None
        self.room_counter = 1

    @commands.command(aliases = ['readme'])
    async def _readme(self, ctx):

        """
        Initialises README for Participants to read when they first enter the server
        """

        # Checks if Sender is at the right channel and is an Organisor
        if ctx.channel.id == int(os.getenv(f'{ENVIRONMENT}_README_CHANNEL_ID')) and \
            discord.utils.get(ctx.guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE')) in ctx.author.roles:

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
            
            # If not, output error
            await ctx.channel.send("Wrong Channel/Not allowed to use this command")

    @commands.command(aliases = ['rules'])
    async def _rules(self, ctx):

        """
        Initialises Rules for Participants to read
        """

        # Checks if Sender is at the right channel and is an Organisor
        if ctx.channel.id == int(os.getenv(f'{ENVIRONMENT}_RULES_CHANNEL_ID')) and \
            discord.utils.get(ctx.guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE')) in ctx.author.roles:

            # If Yes, Purge the Old Rules
            await ctx.channel.purge(limit=2)

            # Extract New Rules Content
            general_rules = util.get_rules('general')
            voice_chat_rules = util.get_rules('voice_chat')
            bot_command_rules = util.get_rules('bot_command')

            # Create Embed for New Rules
            embedVar = discord.Embed(title="Rules of MDashHack 2022", color=0x00ff00)
            embedVar.add_field(name="General Rules", value=general_rules, inline=False)
            embedVar.add_field(name="Voice Chat Rules", value=voice_chat_rules, inline=False)
            embedVar.add_field(name="Bot Command Rules", value=bot_command_rules, inline=False)

            # Send New Rules
            await ctx.channel.send(embed=embedVar)

        else:
            
            # If not, output error
            await ctx.channel.send("Wrong Channel/Not allowed to use this command")

    @commands.command(aliases = ['topicselect'])
    async def _topic_selection(self, ctx):

        """
        Initialises Embed for participants to select their topic
        """

        # Checks if Sender is at the right channel and is an Organisor
        if ctx.channel.id == int(os.getenv(f'{ENVIRONMENT}_TOPIC_SELECTION_CHANNEL_ID')) and \
            discord.utils.get(ctx.guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE')) in ctx.author.roles:

            # If Yes, Purge the Old Read Me
            await ctx.channel.purge(limit=2)

            problem_statements = util.get_problem_statements()

            # Create new embed
            embedVar = discord.Embed(title="Choose Your Problem Statement", color=0x00ff00)
            embedVar.add_field(name="List of Choices",value=problem_statements, inline=False)

            # Send New Read Me
            message = await ctx.channel.send(embed=embedVar)
            await message.add_reaction('1️⃣')
            await message.add_reaction('2️⃣')
            await message.add_reaction('3️⃣')
            await message.add_reaction('4️⃣')
            await message.add_reaction('5️⃣')
            await message.add_reaction('6️⃣')

        else:
            
            # If not, output error
            await ctx.channel.send("Wrong Channel/Not allowed to use this command")

    @commands.command(aliases = ['teamleader'])
    async def _team_leader(self, ctx):

        """
        Initiates the Embed which allows participants to react to get team leader role
        """
        # Check if at right channel and is admin of the server
        if ctx.channel.id == int(os.getenv(f'{ENVIRONMENT}_TEAM_LEADER_CHANNEL_ID')) and \
            discord.utils.get(ctx.guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE')) in ctx.author.roles:

            # Clear old Embed
            await ctx.channel.purge(limit=2)

            # Create new embed
            embedVar = discord.Embed(title="Be The Team Leader!", color=0x00ff00)
            embedVar.add_field(name="React to the Message if You're the Leader of your Team",value="Team leaders will get private access to certain channels that may benefit you and your team.", inline=False)
            
            # Send new embed to channel and add reaction
            message = await ctx.channel.send(embed=embedVar)
            self.team_leader = message.id
            await message.add_reaction("💥")


    @commands.command(aliases = ['private'])
    async def _private(self, ctx):

        """
        Initiates the Embed which participants can create private rooms from here
        """
        # Check if at right channel and is admin of the server
        if discord.utils.get(ctx.guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE')) in ctx.author.roles:

            # Clear old Embed
            await ctx.channel.purge(limit=2)

            # Create new embed
            embedVar = discord.Embed(title="Create Private Group", color=0x00ff00)
            embedVar.add_field(name="Create Your Very Own Private Chatroom!",value="Please react to the embed to get your own private group chat here in our discord!", inline=False)
            
            # Send new embed to channel and add reaction
            message = await ctx.channel.send(embed=embedVar)
            self.private_embed = message.id
            await message.add_reaction("🧠")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):

        """
        Allows user to be in a private channel after reacting to the message
        """

        # Get Server ID, server
        guild_id = int(os.getenv(f'{ENVIRONMENT}_GUILD_ID'))
        guild = self.client.get_guild(guild_id)

        # Check if reaction emoji is as provided and reaction is according to the embed
        if reaction.emoji == '🧠' and reaction.count > 1 and reaction.message.id == self.private_embed:

            # Get member who reacted, and the admin role
            member = user
            admin_role = discord.utils.get(guild.roles, name=os.getenv(f'{ENVIRONMENT}_ADMIN_ROLE'))
            category = discord.utils.get(guild.categories, name=os.getenv(f'{ENVIRONMENT}_PRIVATE_ROOM_CATEGORY'))
            print(admin_role, category)

            # Initialise Overwrite Permissions
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                member: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
            }
            
            # Create text channel with said overwrites
            await guild.create_text_channel(f'mdhack-group-{self.room_counter}', overwrites=overwrites, category=category, sync_permissions=False)
            self.room_counter += 1

        elif reaction.emoji == '💥' and reaction.count > 1 and reaction.message.id == self.team_leader:
            member = user
            role = discord.utils.get(guild.roles, name=os.getenv(f'{ENVIRONMENT}_TEAM_LEADER_ROLE'))
            await member.add_roles(role)

def setup(client):
    client.add_cog(Purpose(client))