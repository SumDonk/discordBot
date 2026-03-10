import random
from datetime import datetime, timedelta
import time
import discord
import bot
import fun
from dotenv import load_dotenv
import os

load_dotenv()

joe = os.getenv("JOE")
guac = os.getenv("GUAC")
donk = os.getenv("DONK")
jon = os.getenv("JON")
brandon = os.getenv("BRANDON")
ismael = os.getenv("ISMAEL")
mariney = os.getenv("MARINEY")
hailee = os.getenv("HAILEE")
aaryn = os.getenv("AARYN")
import globals

async def handle_response(message):
    msg = message.content.lower()
    print(globals.heat)
    heat = globals.heat
    # certainties (need to execute)
    if message.author.id == 193940138680778753:
        if random.randint(1, 75) == 1:
            await message.channel.send("you're talking too much <:shutup:1112973051869544508>")
            await message.author.timeout(timedelta(minutes=(1*heat)), reason="get bent")
            globals.heat = 1
    elif random.randint(1, 5) == 1:
        await message.channel.send("you're talking too much <:shutup:1112973051869544508>")
        # environment variables are strings, so compare to str(message.author.id)
        if str(message.author.id) == donk:
            await message.channel.send("that was meant for donk, but we're doubling it and giving it to the next person!")
            globals.heat *= 2
            await message.channel.send("The current heat is now " + str(globals.heat) + ":fire:")
        elif str(message.author.id) == guac:
            await message.channel.send("that was meant for guac, but we're doubling it and giving it to the next person!")
            globals.heat *= 2
            await message.channel.send("The current heat is now " + str(globals.heat) + ":fire:")
        else:
            await message.author.timeout(timedelta(minutes=(1*globals.heat)), reason="get bent")
            globals.heat = 1
            await message.channel.send("heat has been reset")

    if msg.startswith("hailee kick"):
        if message.mentions:
            if message.author.guild_permissions.administrator:
                mentioned_user = message.mentions[0]
                file = discord.File('images/guess.jpg')
                await message.channel.send(file=file)
                await fun.kick_game(mentioned_user, message)
            else:
                await message.channel.send("YOU DONT HAVE PERMS")
        else:
            await message.channel.send("KICK WHO??")

    if msg.startswith("hailee strike"):
        if message.mentions:
            if message.author.guild_permissions.administrator:
                mentioned_user = message.mentions[0]
                return f"this guy has {fun.give_strike(mentioned_user)} strikes!"
            else:
                await message.channel.send("YOU DONT HAVE PERMS")
        else:
            await message.channel.send("STRIKE WHO??")
    if msg == "hailee show me the strikes":
        await fun.display_all_strikes(message)
    if msg.startswith("flop"):
        if message.mentions:
            mentioned_user = message.mentions[0]
            return f"{fun.flopper_engage(mentioned_user)}, is in flop mode!"
        else:
            await message.channel.send("FLOP WHO??")         
    if msg.startswith("unflop"):
        if message.mentions:
            mentioned_user = message.mentions[0]
            if mentioned_user != message.author:
                return f"{fun.flopper_disengage(mentioned_user)}, is out of flop mode, lucky you"
        else:
            await message.channel.send("UNFLOP WHO??")
    if fun.is_flopped(message):
        emoji = "<:flopper:1108249593717719212>"
        await message.add_reaction(emoji)
    hit = random.randint(1, 6)
    if hit <= 3:
        # image reactions
        if msg == "overwatch" or msg == "ow":
            file = discord.File('videos/overwatch.mp4')
            await message.channel.send(file=file)
        if msg == "kill yourself" or msg == "kys":
            file = discord.File('images/kms.png')
            await message.channel.send(file=file)
            await message.channel.send('why are you so mean')
        if msg == "swag":
            file = discord.File('images/swag.jpg')
            await message.channel.send(file=file)
        if msg == "marine" or msg == "ismael":
            file = discord.File('images/ismael.png')
            await message.channel.send(file=file)
        if msg == "bisbol":
            file = discord.File('images/bisbolwoman.png')
            await message.channel.send(file=file)
        if msg == "fake" or msg == 'mark':
            file = discord.File('images/mark.jpg')
            await message.channel.send(file=file)
            await message.channel.send("did someone say fake??")
        if "love" in msg or "friendship" in msg:
            file = discord.File('images/loveandfriendship.png')
            await message.channel.send(file=file)
        # specific tags for specific users:
        if joe in msg:
            return "<:flopper:1108249593717719212>"
        if guac in msg:
            return "$19 fortnite card"
        if donk in msg:
            return "<:theslop:1086943708722774046>"
        if jon in msg:
            return "<:slow:932017465343500328>"
        if brandon in msg:
            return "take a guess <:chomp:614018248215887872>"
        if ismael in msg:
            return "<:suicide:836482780169764864>"
        if mariney in msg:
            return "I'M IN CHARGE NOW"
        if hailee in msg:
            return "don't you tag me"
        if aaryn in msg:
            return "<:bruh:1201458023424602132>"
        # the rest of em
        if 'fortnite' in msg or 'fort' in msg:
            await message.channel.send("i love fortnite so much...")
        if 'sleepnite' in msg or 'bedtime' in msg:
            await message.channel.send("oh yeah oh yeah its time for bed!")
        if 'chomp' in msg:
            await message.channel.send("<:chomp:614018248215887872>")
        if 'admin' in msg:
            await message.channel.send("looks like someone is getting their perms taken away!")
        if msg == "papa":
            time.sleep(0.776)
            await message.channel.send('tutu')
            time.sleep(1.392)
            await message.channel.send('tutu')
            time.sleep(1.097)
            await message.channel.send('tu')
            time.sleep(0.240)
            await message.channel.send('wawa')
        if "brawl" in msg or "melty" in msg:
            await message.channel.send("hop on fortnite instead!!")
        if "prom" in msg:
            await message.channel.send("OMG of course!!")
            time.sleep(2)
            await message.channel.send("sike")
