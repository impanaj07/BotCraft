# index.py

import discord
from discord.ext import commands

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
# If you need member or presence intents, enable them like this:
# intents.members = True
# intents.presences = True

# Create an instance of a bot with command prefix '!' and specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event that runs when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

# Command to share resources
@bot.command(name='share')
async def share_resource(ctx, *, resource: str):
    """Command for users to share resources."""
    await ctx.send(f'New Resource Shared: {resource}')

# Command to list shared resources (for simplicity, we'll use an in-memory list)
shared_resources = []

@bot.command(name='list_resources')
async def list_resources(ctx):
    """Command to list all shared resources."""
    if not shared_resources:
        await ctx.send("No resources have been shared yet.")
    else:
        await ctx.send("Shared Resources:\n" + "\n".join(shared_resources))

@bot.command(name='add_resource')
async def add_resource(ctx, *, resource: str):
    """Command for users to add resources."""
    shared_resources.append(resource)
    await ctx.send(f'Resource added: {resource}')

# Run the bot with your token (replace 'YOUR_DISCORD_BOT_TOKEN' with your actual token)
TOKEN = 'MTMwNjEzNjY0Mjg1MTE3NjUxOQ.GPS2dV.vp5tvMKnBeNDWDW5J1xklBaKEVKRlxapoSElQg'
bot.run(TOKEN)