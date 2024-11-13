import discord
import os
from discord.ext import commands
import asyncio  # Import for asynchronous scheduling

def convert(time):
    """Converts a time string (e.g., "10m", "2h") to seconds."""
    pos = ["s", "m", "h", "d"]
    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

intents = discord.Intents.default()
intents.message_content = False  # Enable message content intent

bot = commands.Bot(command_prefix='$', intents=intents)  # Replace '$' with your desired command prefix

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()  # Decorator to define a command
async def hello(ctx):  # Replace 'hello' with your desired command name
    await ctx.send('Hello!')
@bot.command()
async def remind(ctx, time_str, *, reminder):
    """Reminds the user after the specified time."""
    try:
        delay = convert(time_str)
        if delay < 0:
            await ctx.send("Invalid time format. Please use s, m, h, or d.")
            return

        await ctx.send(f"Alright, I'll remind you in {delay} seconds about: {reminder}")
        await asyncio.sleep(delay)
        await ctx.send(f"Reminder: {reminder}")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


bot.run(os.getenv('TOKEN'))  # Replace 'your_bot_token' with your actual bot token
