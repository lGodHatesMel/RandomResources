import discord
from discord.ext import commands
import json
from datetime import datetime

class MessageLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Check if the message is from a user and not a bot
        if message.author.bot:
            return

        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            message_logger_channel_id = config.get("message_logger_channel_id")

        if not message_logger_channel_id:
            print("Message logger channel ID is not set in config.json.")
            return

        logging_channel = self.bot.get_channel(message_logger_channel_id)

        # Create an embed with a custom format for the deleted message
        embed = discord.Embed(color=discord.Color.red())
        embed.set_author(name=f"{message.author.name}", icon_url=message.author.avatar_url)
        embed.description = f"Message deleted in {message.channel.mention}"
        embed.add_field(name="Deleted Message", value=message.content, inline=False)
        embed.set_footer(text=f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC | User ID: {message.author.id} | Message ID: {message.id}")

        await logging_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(MessageLogger(bot))
