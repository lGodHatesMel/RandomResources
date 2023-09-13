import os
import discord
from discord.ext import commands
import json
from datetime import timezone, datetime
import asyncio

# Function to load or create the config.json file
def load_or_create_config():
    if os.path.exists('config.json'):
        # Config file already exists
        print("config.json already exists.")
    else:
        # Create a default config if it doesn't exist
        default_config = {
            "token": "YOUR_TOKEN_HERE",
            "prefix": "!",
            "enable_countdown": False,  # Use lowercase boolean
            "countdown_channel_id": None,  # Default to None
            "target_timestamp": None  # Default to None
        }
        with open('config.json', 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
        print("A new config.json file has been created with default values.")

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        return config

config = load_or_create_config()

bot = commands.Bot(command_prefix=config['prefix'], case_insensitive=True)

cogs_dir = 'cogs'

# Function to load all cogs from the 'cogs' folder
def load_cogs():
    for filename in os.listdir(cogs_dir):
        if filename.endswith('.py'):
            bot.load_extension(f'{cogs_dir}.{filename[:-3]}')

load_cogs()

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'===========================================================')
    print(f'Bot Name: {bot.user.name}')
    print(f'Discord Server Joined: {bot.guilds[0].name}')
    print(f'Bot UID: {bot.user.id}')
    print(f'===========================================================')

    # Check if the bot is a member of any servers
    if len(bot.guilds) > 0:
        joined_server = bot.guilds[0]  # Assuming the bot is only in one server
        joined_time = joined_server.me.joined_at.strftime('%Y-%m-%d %H:%M:%S')
        print(f'Joined Server at: {joined_time}')
    print(f'===========================================================')

bot.run(config['token'])
