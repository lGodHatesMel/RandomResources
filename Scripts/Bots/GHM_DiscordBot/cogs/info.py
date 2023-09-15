import discord
from discord.ext import commands
import datetime

class INFO_COMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='commands', help='Gives a list of commands you can use.')
    async def help_commands(self, ctx):
        help_commands = "!twitch, !youtube, !requestlist, !raidsheet, !donate"
        await ctx.send(f"Available commands:\n{help_commands}")

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='donate', aliases=['tip'], help='Gives a donation link.')
    async def donate_link(self, ctx):
        donate_url = "https://streamelements.com/lgodhatesmel/tip"
        await ctx.send(f"Here's how you can donate by using this link:\n{donate_url}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='ping', help='Just checks to see if bot is running')
    async def ping(self, ctx):
        await ctx.send('Pong!')
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

def setup(bot):
    bot.add_cog(INFO_COMMANDS(bot))