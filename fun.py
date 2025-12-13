from time import time
import ffmpeg
import os
import pymongo
import random
import kickmenu


# Strike system no longer works
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Hailee"]
collection = mydb["Strikes"]


async def violate_resolution(in_file, out_file, resolutionX, resolutionY):
    if os.path.exists(out_file):
        os.remove(out_file)
    input_stream = ffmpeg.input(in_file)
    output = ffmpeg.output(input_stream, out_file, vf=f"scale={resolutionX}:{resolutionY}")
    ffmpeg.run(output)


async def display_all_strikes(msgobj):
    # Retrieve all documents from the collection
    user_data = collection.find({})

    for user in user_data:
        username = user['username']
        discriminator = user['discriminator']
        guild_id = user['guild_id']
        strikes = user.get('strikes', 0)
        print(f"User: {username}#{discriminator}, Guild ID: {guild_id}, Strikes: {strikes}")
        await msgobj.channel.send(f"{username}#{discriminator} has {strikes} strike(s)")


def give_strike(user):
    username = user.name
    discriminator = user.discriminator
    guild_id = user.guild.id

    user_data = collection.find_one({'username': username, 'discriminator': discriminator, 'guild_id': guild_id})

    if user_data:
        strikes = user_data.get('strikes', 0)
        new_strikes = strikes + 1
        collection.update_one({'username': username, 'discriminator': discriminator, 'guild_id': guild_id},
                              {'$set': {'strikes': new_strikes}})

        print(f"Strike added for {user}. Total strikes: {new_strikes}")
    else:
        user_info = {
            'username': username,
            'discriminator': discriminator,
            'guild_id': guild_id,
            'strikes': 1
        }
        collection.insert_one(user_info)

        print(f"User {user} not found. Added with 1 strike.")
    if new_strikes:
        return new_strikes
    else:
        return "looks like this is your first strike buddy, cant wait for more!"


flopped_users = {}

def is_flopped(user):
    return user.author.id in flopped_users

def flopper_engage(user):
    flopped_users[user.id] = True
    return user.name

def flopper_disengage(user):
    if user.id in flopped_users:
        del flopped_users[user.id]
    return user.name

async def kick_game(user, msgobj):
    number = random.randint(1, 10)
    left_hand = False
    right_hand = False
    if number > 5:
        left_hand = True
    else:
        right_hand = True
    await kickmenu.show_menu(msgobj)

