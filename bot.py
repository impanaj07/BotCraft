import discord
from discord.ext import commands
from discord import app_commands
from database import create_table, add_profile, get_profiles, add_mentor, get_mentors
import random

# Initialize the database and create the tables
create_table()

# Define intents
intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent

# Create an instance of a bot with specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    await bot.tree.sync()  # Sync the command tree with Discord

# Slash command to add a mentor
@bot.tree.command(name='add_mentor', description='Add a mentor with skills and interests.')
async def add_mentor_command(interaction: discord.Interaction, name: str, skills: str, interests: str):
    """Command to add a mentor."""
    mentor_id = interaction.user.id  # You might want to use a different ID system for mentors.
    add_mentor(mentor_id, name, skills, interests)
    
    await interaction.response.send_message(f'Mentor added:\nName: {name}\nSkills: {skills}\nInterests: {interests}')

# Slash command to create a user profile
@bot.tree.command(name='create_profile', description='Create your matchmaking profile.')
async def create_profile(interaction: discord.Interaction, skills: str, interests: str):
    """Command for users to create their matchmaking profile."""
    user_id = interaction.user.id
    username = interaction.user.name
    add_profile(user_id, username, skills, interests)
    
    await interaction.response.send_message(f'Profile created for {username}:\nSkills: {skills}\nInterests: {interests}')

# Slash command to find a suitable mentor based on user's skills and interests
@bot.tree.command(name='findmentor', description='Find a suitable mentor based on your skills and interests.')
async def findmentor(interaction: discord.Interaction):
    """Find a suitable mentor based on user's skills and interests."""
    
    user_id = interaction.user.id
    profiles = get_profiles()
    
    user_profile = next((p for p in profiles if p[0] == user_id), None)
    
    if not user_profile:
        await interaction.response.send_message("You need to create a profile first using /create_profile.")
        return
    
    user_skills = user_profile[2].split(', ')  # Assuming skills are stored as comma-separated values
    
    # Get all mentors from the database
    mentors = get_mentors()
    
    # Find suitable mentors based on matching skills or interests
    suitable_mentors = []
    
    for mentor in mentors:
        mentor_skills = mentor[2].split(', ')
        
        # Check for matching skills or interests (you can enhance this logic)
        if any(skill in mentor_skills for skill in user_skills):
            suitable_mentors.append(mentor)

    if suitable_mentors:
        mentor_info = random.choice(suitable_mentors)  # Randomly select one suitable mentor
        await interaction.response.send_message(f"You've been matched with Mentor {mentor_info[1]}!\nSkills: {mentor_info[2]}\nInterests: {mentor_info[3]}")
    else:
        await interaction.response.send_message("No suitable mentors found.")

# Slash command to match users based on profiles
@bot.tree.command(name='match', description='Find potential matches based on profiles.')
async def match(interaction: discord.Interaction):
    """Command to find matches based on profiles."""
    profiles = get_profiles()

    if len(profiles) < 2:
        await interaction.response.send_message("Not enough profiles for matching.")
        return
    
    matches = []
    
    for user_id, username, skills, interests in profiles:
        if user_id != interaction.user.id:  # Avoid matching with self
            matches.append((username, skills))
    
    if matches:
        response = "Potential Matches:\n" + "\n".join([f"{name}: Skills - {skills}" for name, skills in matches])
        await interaction.response.send_message(response)
    else:
        await interaction.response.send_message("No matches found.")

# Slash command for icebreaker questions
@bot.tree.command(name='icebreaker', description='Get an icebreaker question.')
async def icebreaker(interaction: discord.Interaction):
   """Send an icebreaker question to the user."""
   icebreakers = [
       "What's your favorite programming language?",
       "What's the most challenging project you've worked on?"
   ]
   prompt = random.choice(icebreakers)
   await interaction.response.send_message(prompt)

# Slash command for feedback
@bot.tree.command(name='feedback', description='Provide feedback about the bot.')
async def feedback(interaction: discord.Interaction, feedback: str):
   """Process user feedback."""
   await interaction.response.send_message("Thank you for your feedback!")

# Run the bot with your token (replace 'YOUR_DISCORD_BOT_TOKEN' with your actual token)
TOKEN = 'MTMwNjE1ODQ5MTQ3NTY0NDQ1OQ.G7WvBW._byfpXls-L9zCx0QD1ZA55UBfqgMY8aQKqqiGo'  # Make sure to replace this with your actual bot token.
bot.run(TOKEN)

