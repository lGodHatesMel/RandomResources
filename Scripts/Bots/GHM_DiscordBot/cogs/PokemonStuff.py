import os
import discord
from discord.ext import commands
import datetime
import random
from data import pokemon_facts

class POKEMON_COMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pokefacts', aliases=['pkf', 'funfact'], help='Get a random Pokémon fact.')
    async def pokefacts(self, ctx):
        # Select a random Pokémon fact from the list
        random_fact = random.choice(pokemon_facts)
        # Send the fact as a message
        await ctx.send(f'**Random Pokémon Fact:**\n{random_fact}')

    @commands.command(name='requestlist', aliases=['rl'], help='Gives link for Special Request List.')
    async def requestlist_link(self, ctx):
        requestlist_url = "https://docs.google.com/spreadsheets/d/1eP8sh8rtrB_1QY4Ti5muOf4uRXKzbF4fbU_58XiCoEs/edit?usp=sharing"
        await ctx.send(f"Heres a link to the special request list:\n{requestlist_url}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='raidsheet', aliases=['raidpokemon'], help='Gives link for all possible Raid Pokemon.')
    async def raidsheet_link(self, ctx):
        raidsheet_url = "https://drive.google.com/drive/folders/1dWCQnNXs8JvCWh99PjU8s39aaa2m9l9N"
        await ctx.send(f"Here is the Raid Docs for all the possible raids you can pick from:\n{raidsheet_url}\n\nNote: You need the ID. So for example for the top right raid you would do `2addraid ID`")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='tradecommands', help='Gives a list of trade commands')
    async def tradecommands(self, ctx):
        trade_commands = "Here are the trade commands for the bots:"
        await ctx.send(f"{trade_commands}\nPokemon Scarlet Violet - `!svtrade`\nPokemon Sword Shield - `!swshtrade`\nPokemon Legends: Arceus - `!platrade`")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='showdown', help='Usage: !showdown [Game: "sv, swsh, pla, bdsp"] [Pokemon Name]')
    async def random_poke_set(self, ctx, game, pokemon_name):
        try:
            # Convert game and valid_games to lowercase
            game = game.lower()
            valid_games = ['sv', 'swsh', 'pla', 'bdsp']

            # Validate game to prevent directory traversal
            if game not in valid_games:
                await ctx.send(f"Invalid game '{game}'. Valid games are: {', '.join(valid_games)}")
                return

            # Convert Pokémon name to lowercase
            pokemon_name = pokemon_name.lower()

            # Get the path to the sets folder and the specific file
            sets_folder = os.path.join('sets', game)
            file_path = os.path.join(sets_folder, f"{pokemon_name}.txt")

            # Check if the file exists
            if not os.path.exists(file_path):
                await ctx.send(f"No sets found for {pokemon_name} [{game}].")
                return

            # Read sets from the file
            with open(file_path, 'r') as file:
                sets_data = file.read().split('===')

            # Filter out empty strings
            sets_data = [set_data.strip() for set_data in sets_data if set_data.strip()]

            if sets_data:
                # Choose a random set for the Pokémon
                random_set = random.choice(sets_data)
                await ctx.send(f"\n**Random set for {pokemon_name.capitalize()} [{game.upper()}]:**\n{random_set}\n")
            else:
                await ctx.send(f"No sets found for {pokemon_name.capitalize()} [{game.upper()}].")
        except Exception as e:
            print(e)
            await ctx.send("An error occurred while fetching Pokémon sets.")

    @commands.command(name='addset', help='Usage: !addset [Game: "sv, swsh, pla, bdsp"] [Pokemon Name] [Set Details]')
    @commands.has_role("Admin")
    async def add_set(self, ctx, game, pokemon_name, *set_details):
        try:
            # Convert game and valid_games to lowercase
            game = game.lower()
            valid_games = ['sv', 'swsh', 'pla', 'bdsp']

            # Validate game to prevent directory traversal
            if game not in valid_games:
                await ctx.send(f"Invalid game '{game}'. Valid games are: {', '.join(valid_games)}")
                return

            # Convert Pokémon name to lowercase
            pokemon_name = pokemon_name.lower()

            # Get the path to the sets folder and the specific file
            sets_folder = os.path.join('sets', game)
            file_path = os.path.join(sets_folder, f"{pokemon_name}.txt")

            # Create the formatted set details
            #formatted_set = format_set_details(f"{pokemon_name.capitalize()} {' '.join(set_details)}")
            formatted_set = format_set_details(f"{' '.join(set_details)}")

            # Add the new set details to the file with desired formatting
            with open(file_path, 'a') as file:
                file.write(f"\n===\n{formatted_set}")

            await ctx.send(f"New set added for {pokemon_name.capitalize()} [{game.upper()}].")

        except Exception as e:
            print(e)
            await ctx.send("An error occurred while adding the set.")


# Function to format set details with line breaks
def format_set_details(set_details):
    splittables = [
        "Ability:", "EVs:", "IVs:", "Shiny:", "Gigantamax:", "Ball:", "- ", "Level:",
        "Happiness:", "Language:", "OT:", "OTGender:", "TID:", "SID:", "Alpha:", "Tera Type:",
        "Adamant Nature", "Bashful Nature", "Brave Nature", "Bold Nature", "Calm Nature",
        "Careful Nature", "Docile Nature", "Gentle Nature", "Hardy Nature", "Hasty Nature",
        "Impish Nature", "Jolly Nature", "Lax Nature", "Lonely Nature", "Mild Nature",
        "Modest Nature", "Naive Nature", "Naughty Nature", "Quiet Nature", "Quirky Nature",
        "Rash Nature", "Relaxed Nature", "Sassy Nature", "Serious Nature", "Timid Nature",
        "*",
    ]

    for i in splittables:
        if i in set_details:
            set_details = set_details.replace(i, f"\n{i}")

    return set_details

def setup(bot):
    bot.add_cog(POKEMON_COMMANDS(bot))
