import discord
from discord.ext import commands
import datetime
import requests
import random
import os

pokemon_facts = [
    "Pikachu's name is a combination of 'pika' (electric spark sound) and 'chu' (mouse sound).",
    "The first generation of Pokémon, Generation I, consisted of 151 different species.",
    "Mew, the 151st Pokémon, was added secretly to the first-generation games.",
    "Lavender Town became infamous due to rumors of a theme song causing headaches and nightmares.",
    "Many Pokémon are inspired by real animals and objects, like Ekans and Muk.",
    "Blissey has the highest base HP stat of all Pokémon.",
    "Legendary Pokémon, like Mewtwo and Arceus, are extremely rare and have special roles.",
    "The Pokémon with the longest English name is 'Crabominable.'",
    "Rhydon was the first Pokémon ever designed by Satoshi Tajiri and Ken Sugimori.",
    "Pokémon games are available in numerous languages, including English.",
    "The Pokémon World Championships are held annually for video games and trading card game tournaments.",
    "Eevee can evolve into eight different forms, known as 'Eeveelutions.'",
    "Pokémon has had a profound impact on pop culture with TV series, movies, trading card games, and more.",
    "The original Pokémon Red and Green games were developed by Game Freak and published by Nintendo in 1996 (Japan) and 1998 (North America).",
    "The concept of Pokémon was inspired by Satoshi Tajiri's childhood interest in collecting creatures and his desire to connect Game Boy devices for trading.",
    "The rarest Pokémon card is the Pikachu Illustrator card, with only a few in existence. It was never released commercially and was given to winners of a Pokémon illustration contest.",
    "In the Pokémon world, there are many different regions, each with its own unique Pokémon species and culture, such as Kanto, Johto, and Sinnoh.",
    "Ash Ketchum, the protagonist of the Pokémon animated series, is known as Satoshi in Japan, named after Pokémon's creator, Satoshi Tajiri.",
    "Meowth, one of the Team Rocket trio's Pokémon, is known for being one of the few Pokémon that can speak human language.",
    "The Pokémon franchise includes a wide range of spin-off games, including Pokémon Snap, Pokémon Mystery Dungeon, and Pokémon GO.",
    "The first Pokémon movie, titled 'Pokémon: The First Movie - Mewtwo Strikes Back,' was released in 1998, followed by numerous other Pokémon movies.",
    "The Pokémon theme song, 'Gotta Catch 'Em All,' is one of the most recognizable and catchy theme songs in the history of animated series.",
    "Jigglypuff is known for putting opponents to sleep by singing a lullaby and then drawing on their faces with its marker-like pen.",
    "The original Pokémon Red and Green games allowed players to encounter a glitch Pokémon known as 'MissingNo,' which could duplicate items.",
    "Magikarp is often considered one of the weakest Pokémon but can evolve into the powerful Gyarados.",
    "The move 'Splash' has no effect in battles except for one special Magikarp in the Pokémon series that can use it to defeat a powerful opponent.",
    "The Pokémon world features a variety of items like Potions, Poké Balls, and Rare Candies to aid trainers in their journey.",
    "The Legendary Pokémon Articuno, Zapdos, and Moltres are inspired by the three legendary birds of Greek mythology: Articuno represents the north wind, Zapdos represents lightning, and Moltres represents fire.",
    "The Pokémon Ditto is known for its ability to transform into other Pokémon. It can breed with almost any Pokémon and produce offspring of that species.",
    "The type chart in Pokémon determines the strengths and weaknesses of different types, such as Water being strong against Fire but weak against Grass.",
    "The original Pokémon games were developed with the help of the Game Boy's link cable, allowing players to trade and battle Pokémon with their friends.",
    "The Pokémon anime series has been running since 1997 and has over a thousand episodes.",
    "Mewtwo, one of the most iconic Legendary Pokémon, was genetically created from the DNA of Mew.",
    "The Pokémon world is home to various villainous teams like Team Rocket, Team Aqua, and Team Galactic, each with its own nefarious plans.",
    "The Pokémon Pikachu is the franchise's official mascot and is featured prominently in marketing and promotional materials.",
    "The term 'shiny Pokémon' refers to rare variants of Pokémon with different color palettes. They have a 1 in 4,096 chance of appearing in the wild.",
    "There are different types of Poké Balls, each with varying levels of effectiveness in catching Pokémon. The Master Ball is the rarest and guarantees a capture.",
    "The Pokémon games often have two versions (e.g., Pokémon Red and Blue) with some exclusive Pokémon in each version, encouraging trading between players.",
    "The Pokémon Togepi is known for its ability to hatch from eggs, symbolizing new beginnings in the Pokémon world.",
    "Eevee's evolution into Espeon or Umbreon depends on the time of day in the games, adding a day-night mechanic to its evolution.",
    "The Legendary Pokémon Rayquaza is said to have the power to quell clashes between Kyogre and Groudon, two other Legendary Pokémon.",
    "The Pokémon Clefairy was originally considered to be the mascot of the franchise before Pikachu took its place.",
    "The Pokémon series has its own trading card game, which has been popular since its launch in the late 1990s.",
    "The Pokémon series has introduced various regions, including the tropical Alola region and the Galar region inspired by the United Kingdom.",
    "Mimikyu, a Ghost/Fairy-type Pokémon, wears a Pikachu costume to make friends because it believes that people dislike its true appearance.",
    "The Pokémon Psyduck is known for its chronic headaches, which can trigger its powerful Psychic-type abilities when the pain becomes too much to bear.",
    "The Pokémon Slowpoke has a tail that can detach and regenerate, leading to the creation of a dish called 'Slowpoke Tail' in the Pokémon world.",
    "The Pokémon franchise holds the Guinness World Record for the most successful video game-based media franchise.",
    "The Pokémon Ditto is the only Pokémon that can breed with genderless Pokémon and produce offspring.",
    "The evolution of Eevee into Glaceon or Leafeon depends on specific locations in the games, adding an environmental factor to its evolution.",
    "The Pokémon Meowth is known for its signature move 'Pay Day,' which can earn trainers extra in-game currency when used in battles.",
    "In the Pokémon series, Professor Oak, the first Pokémon professor, is known for his iconic line: 'Are you a boy or a girl?'",
    "The Pokémon Gengar is believed to be the shadow of Clefable, another Pokémon, according to its Pokédex entry.",
]

class PokemonBots(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='requestlist', help='Gives link for Special Request List.')
    async def requestlist_link(self, ctx):
        requestlist_url = "https://docs.google.com/spreadsheets/d/1eP8sh8rtrB_1QY4Ti5muOf4uRXKzbF4fbU_58XiCoEs/edit?usp=sharing"
        await ctx.send(f"Heres a link to the special request list:\n{requestlist_url}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='raidsheet', help='Gives link for all possible Raid Pokemon.')
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
        await ctx.send(f"{trade_commands}\nPokemon Scarlet Violet - `!svtrade`\nPokemon Sword Shield - `!swshtrade`\n Pokemon Legends: Arceus - `!platrade`")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")


class PokemonSets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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


class PokeFacts(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pokefacts', help='Get a random Pokémon fact.')
    async def pokefacts(self, ctx):
        # Select a random Pokémon fact from the list
        random_fact = random.choice(pokemon_facts)
        # Send the fact as a message
        await ctx.send(f'**Random Pokémon Fact:**\n{random_fact}')

def setup(bot):
    bot.add_cog(PokemonBots(bot))
    bot.add_cog(PokemonSets(bot))
    bot.add_cog(PokeFacts(bot))
