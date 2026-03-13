import discord
import kickmenu
from discord import app_commands
from discord.ext import commands, tasks
import os
import responses
import fun
import aiohttp
from datetime import datetime, timedelta
import yt_dl
import asyncio
import globals
from dotenv import load_dotenv
load_dotenv()

current_time = datetime.now()

# openai.api_key = os.getenv("OPENAI_API_KEY")

# FFMPEG_OPTIONS = {
# 'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
# 'options': '-vn'
# }


async def send_message(message):
    #try:
        response = await responses.handle_response(message)
        if response:
            await message.channel.send(response)

    #except Exception as e:
        #print(e)


def run_discord_bot():
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)
    token = os.getenv("DISCORD_TOKEN")
    


    @bot.event
    async def on_ready():
        print(f'Logged on as {bot.user}!')

        await bot.tree.sync()
        birthday_checker.start()  # Start the background task

    @bot.event
    async def on_message(message):
        if message.author == bot.user or message.author.id == os.getenv("MARINEY"):
            return

        if message.attachments:
            for attachment in message.attachments:
                if attachment.content_type.startswith('image'):
                    filename = attachment.filename
                    await attachment.save(filename)
                    print(f'saved image file: {filename}')
                    os.remove(filename)
                elif attachment.content_type.startswith('video') and message.content == "hailee":
                    filename = attachment.filename
                    await attachment.save(filename)
                    print(f'saved video file: {filename}')
                    await fun.violate_resolution(filename, "output.mp4", 36, 36)
                    file = discord.File('output.mp4')
                    await message.channel.send(file=file)
                    os.remove(filename)

        print(f'{message.author} said: "{message.content}" ({message.channel})')
        await send_message(message)
        await bot.process_commands(message)

    @bot.event
    async def on_message_delete(message):
        log_channel = bot.get_channel(1255847217365909546)

        if message.author.id == os.getenv("HAILEE"):
            return
        folder = "deletions"
        if not os.path.exists(folder):
            os.makedirs(folder)
        if message.attachments:
            for attachment in message.attachments:
                print(f'erm {message.author} deleted: {attachment}')
                await attachment.save(f"{folder}/{attachment.filename}")
        else:
            print(f'erm {message.author} deleted: {message.content}')
    @bot.event
    async def on_message_edit(before, after):
        log_channel = bot.get_channel(1255847217365909546)

        await log_channel.send(f'erm {before.author} edited: {before.content} -> {after.content}')

    @bot.event
    async def on_member_update(before, after):
        if before.nick != after.nick:
            channel = bot.get_channel(364144447220482051)
            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.member_update):
                if entry.user != after and not entry.user.guild_permissions.administrator and entry.user != after.guild.owner:
                    await channel.send(f"{entry.user.name} TRIED to change {after.name}'s nickname from {before.nick} to {after.nick}")
                    if after.nick != before.nick:
                        await after.edit(nick=before.nick) 

    # Birthday checking task - runs daily at midnight
    @tasks.loop(hours=24)
    async def birthday_checker():
        channel = bot.get_channel(364144447220482051)
        todays_birthdays = fun.check_today_birthdays()
        
        if todays_birthdays:
            for user_id, age in todays_birthdays:
                try:
                    user = await bot.fetch_user(user_id)
                    greeting = fun.birthday_greeting(user, age)
                    await channel.send(greeting)
                except Exception as e:
                    print(f"Error sending birthday greeting to user {user_id}: {e}")
    
    @birthday_checker.before_loop
    async def before_birthday_checker():
        await bot.wait_until_ready()
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        midnight = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
        wait_seconds = (midnight - now).total_seconds()
        await asyncio.sleep(wait_seconds)
                        

    """@bot.command() # deprecated
    async def hailee(ctx, *, message):
        print("this works")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot for a discord bot named hailee"},
                {"role": "user", "content": message}
            ]
        )
        await ctx.send(response['choices'][0]['message']['content'])
"""

    @bot.hybrid_command()
    async def shutup(ctx, member: discord.Member):
        current_time = discord.utils.utcnow()
        await member.timeout(current_time + timedelta(seconds=7), reason= "get bent")

    @bot.hybrid_command()
    async def iwanttoplayagame(ctx, member: discord.Member):
        menu = kickmenu.TimeoutMenu(member)
        await ctx.send(f"{member.name}, pick your fate!", view=menu)

    @bot.hybrid_command()
    async def heat_riser(ctx):
        globals.heat += 1
        await ctx.send("Raising the heat <:smugcanny:1373186622182395914>\nThe current heat is now " + str(globals.heat) + ":fire:")

    queue = []
    @bot.hybrid_command() # somewhat broken
    async def play(ctx, url: str):
        FFMPEG_OPTIONS = {
        'options': '-vn'
        }
        
        if ctx.message.author.voice is None:
            await ctx.send("get in voice chat first:bangbang:")
            return
        channel = ctx.message.author.voice.channel
        voice_client = ctx.voice_client
        if voice_client is None:
            voice_client = await channel.connect()
        else:
            await voice_client.move_to(channel)

        queue.append(yt_dl.yt_dl(url))
        if not voice_client.is_playing():
            try:
                source = discord.FFmpegPCMAudio(queue.pop(0), **FFMPEG_OPTIONS)
                voice_client.play(source, after=lambda e: check_queue())
                
                
            except Exception as e:
                print(f"Error playing music: {e}")
                await ctx.send(f"Error playing music: {e}")
        elif len(queue) > 0:
            print(f'queue length: {len(queue)}')
            

        async def check_queue():
            print(f'queue length: {len(queue)}')
            if len(queue) > 0:
                source = discord.FFmpegPCMAudio(queue.pop(0), **FFMPEG_OPTIONS)
                voice_client.play(source, after=lambda e: check_queue())
            else:
                print("queue empty")
    bot.run(token)