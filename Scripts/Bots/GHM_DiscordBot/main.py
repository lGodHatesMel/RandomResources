import os
import discord
from discord.ext import commands
import json
from datetime import timezone, datetime
import asyncio
from traitlets import This

# Define the bot object first
bot = commands.Bot(command_prefix="!", case_insensitive=True)

# Define a custom help command
class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    async def send_bot_help(self, mapping):
        ctx = self.context
        bot_commands = [command for command in bot.commands if not command.hidden]
        normal_commands = [command for command in bot_commands if "admin" not in command.name]  # Filter out admin-only commands
        embed = discord.Embed(title="Bot Commands", description="Available commands for all users:")
        for command in normal_commands:
            embed.add_field(name=f"!{command.name}", value=command.help, inline=False)
        await ctx.send(embed=embed)

    async def send_cog_help(self, cog):
        ctx = This.context
        commands_in_cog = [command for command in cog.get_commands() if not command.hidden]
        embed = discord.Embed(title=f"{cog.qualified_name} Commands", description=cog.description)
        for command in commands_in_cog:
            embed.add_field(name=f"!{command.name}", value=command.help, inline=False)
        await ctx.send(embed=embed)

# Attach the custom help command to the bot
bot.help_command = CustomHelpCommand()

# Function to load or create the config.json file
def load_or_create_config(bot):
    if hasattr(bot, 'config'):
        # If bot.config is already set, return it
        return bot.config

    if os.path.exists('config.json'):
        print("config.json already exists.")
    else:
        # Create a default config if it doesn't exist
        default_config = {
            "token": "YOUR_TOKEN_HERE",
            "prefix": "!",
            "enable_countdown": False,  # Use lowercase boolean
            "countdown_channel_id": None,  # Default to None
            "target_timestamp": None,  # Default to None
            "enable_welcomemessages": False,
            "welcome_channel_id": None,
            "log_mod_stuff": None
        }
        with open('config.json', 'w') as config_file:
            json.dump(default_config, config_file, indent=4)
        print("A new config.json file has been created with default values.")

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
        bot.config = config  # Set the config as an attribute of the bot instance
        return config

# Call the function with the bot object
config = load_or_create_config(bot)

# Function to load all cogs from the 'cogs' and 'mod_cogs' folders
def load_cogs():
    cog_directories = ['cogs', 'mod_cogs']
    for cog_directory in cog_directories:
        for filename in os.listdir(cog_directory):
            if filename.endswith('.py'):
                bot.load_extension(f'{cog_directory}.{filename[:-3]}')

# Load config data into a global variable accessible by extensions
config_data = load_or_create_config(bot)

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
