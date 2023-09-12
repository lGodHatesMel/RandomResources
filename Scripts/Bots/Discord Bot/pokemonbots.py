import discord
from discord.ext import commands
import datetime

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

    @commands.command(name='raidsheet', help='Gives link for Raid Pokemon.')
    async def raidsheet_link(self, ctx):
        raidsheet_url = "https://drive.google.com/drive/folders/1dWCQnNXs8JvCWh99PjU8s39aaa2m9l9N"
        await ctx.send(f"Heres the link to the Raids you can request for raids:\n{raidsheet_url}")
        
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

def setup(bot):
    bot.add_cog(PokemonBots(bot))