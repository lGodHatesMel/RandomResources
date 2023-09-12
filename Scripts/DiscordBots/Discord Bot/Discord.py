import discord
from discord.ext import commands
import json
import datetime
import asyncio
from datetime import timezone, datetime

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Create an instance of the bot
bot = commands.Bot(command_prefix=config['prefix'])

# Global variable to store the countdown message
countdown_message = None

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'--------------------------------------')
    print(f'User Logged in: {bot.user.name}')
    print(f'--------------------------------------')

     # Start the countdown loop when the bot is ready
    await run_countdown()

# Function to run the countdown (if enabled)
async def run_countdown():
    if config.get('enable_countdown', False):  # Check if "enable_countdown" is set to True
        global countdown_message
        countdown_channel_id = config.get('countdown_channel_id')
        target_timestamp = config.get('target_timestamp')
        channel = bot.get_channel(countdown_channel_id)  # Get the channel using the ID

        current_timestamp = datetime.now(timezone.utc).timestamp()
        time_remaining = target_timestamp - current_timestamp

        if time_remaining <= 0:
            countdown_text = """
            <:shiny:1072343743778259015> DLC IS NOW OUT!!! <:shiny:1072343743778259015>
            <:shiny:1072343743778259015> Countdown has ended! <:shiny:1072343743778259015>
            <:shiny:1072343743778259015> HAPPY GAMING <:shiny:1072343743778259015>
            """
        else:
            days = int(time_remaining // 86400)
            hours = int((time_remaining % 86400) // 3600)
            minutes = int((time_remaining % 3600) // 60)
            countdown_text = f"""
            ***UPDATED FOR REAL TIME RELEASE***   
            **POKEMON SCARLET & VIOLET DLC DROPS IN**
            <:happySquirtle:1071190313344958605> `{days} days, {hours} hours, {minutes} minutes` <:shiny:1072343743778259015>

            These Should be the times Pokemon Scarlet Violet DLC should be released in these Time Zones:
            `Sept 12, 9:00 PM EST`
            `Sept 13, 10:00 AM JST`
            `Sept 12, 6:00 PM PT`
            `Sept 12, 8:00 PM CT`
            NOTE: Could be around an hour difference..."""

        if countdown_message is None:
            countdown_message = await channel.send(countdown_text)
        else:
            await countdown_message.edit(content=countdown_text)

        await asyncio.sleep(60)  # Sleep for 60 seconds before running again
        await run_countdown()  # Recursive call to keep running the countdown

    bot.load_extension('info')
    bot.load_extension('streams')
    bot.load_extension('pokemonbots')

bot.run(config['token'])