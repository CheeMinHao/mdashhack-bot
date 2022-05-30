from logging import raiseExceptions
import discord

async def check_read_me(bot, read_me_id):
    try:
        read_me_channel = bot.get_channel(int(read_me_id))
        await read_me_channel.fetch_message(read_me_channel.last_message_id)
    except AttributeError:
        raise Exception("Channel Not Found")
    except discord.errors.HTTPException:
        raise Exception("Read Me Message not Displayed, please display asap")
    return True

async def check_rules(bot, read_me_id):
    try:
        rules_channel = bot.get_channel(int(read_me_id))
        await rules_channel.fetch_message(rules_channel.last_message_id)
    except AttributeError:
        raise Exception("Channel Not Found")
    except discord.errors.HTTPException:
        raise Exception("Read Me Message not Displayed, please display asap")
    return True

def get_read_me():
    READ_ME_FILE = 'text_files/read_me.txt'
    with open(READ_ME_FILE, 'r') as f:
        return f.read()

def get_rules():
    READ_ME_FILE = 'text_files/rules.txt'
    with open(READ_ME_FILE, 'r') as f:
        return f.read()

# if __name__ == "__main__":
#     print(get_read_me())
