import discord
from discord.ext import commands
import datetime

class Streams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='twitch', help='Get the Twitch channel link.')
    async def twitch_link(self, ctx):
        twitch_url = "https://www.twitch.tv/lgodhatesmel"
        await ctx.send(f"Here's the Twitch link:\n{twitch_url}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='youtube', help='Get the YouTube channel link.')
    async def youtube_link(self, ctx):
        youtube_url = "https://www.youtube.com/@lGodHatesMel"
        await ctx.send(f"Here's the Youtube link:\n{youtube_url}")
        
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

def setup(bot):
    bot.add_cog(Streams(bot))