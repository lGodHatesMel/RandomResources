import discord
from discord.ext import commands
import datetime
import asyncio

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sticky_messages = {}  # Store sticky messages for each channel

    @commands.command(name='botdown', help='[#Channel] [Message]')
    @commands.has_role("Admin")  # Restrict this command to users with the "Admin" role
    async def botdown_command(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(f"**Bot Down:**\n{message}")
        await ctx.send(f"Bot Down message sent to {channel.mention}.")

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")


    @commands.command(name='announcement', help='[#Channel] [Message]')
    @commands.has_role("Admin")
    async def announcement(self, ctx, channel: discord.TextChannel, *, message):
        await channel.send(f"**Announcement:**\n{message}")
        await ctx.send(f"Announcement sent to {channel.mention}.")

    @commands.command(name='addsticky', help='[#Channel] [Message]')
    @commands.has_role("Admin")
    async def sticky_note(self, ctx, channel: discord.TextChannel, *, message):
        # Send the sticky note message to the specified channel
        sticky_msg = await channel.send(f"*STICKY NOTE:*\n`{message}`")
      
        # Store the sticky message for future reference
        self.sticky_messages[channel] = sticky_msg
      
        await ctx.send(f"Sticky note added to {channel.mention}.")

    @commands.command(name='removesticky', help='[#Channel]')
    @commands.has_role("Admin")
    async def remove_sticky(self, ctx, channel: discord.TextChannel):
        if channel in self.sticky_messages:
            sticky_msg = self.sticky_messages.pop(channel)
            await sticky_msg.delete()
            await ctx.send(f"Sticky note removed from {channel.mention}.")
        else:
            await ctx.send(f"No sticky note found in {channel.mention}.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the message is not from the bot itself and it's in a channel with a sticky note
        if not message.author.bot and message.channel in self.sticky_messages:
            # Get the original sticky message
            original_sticky_msg = self.sticky_messages[message.channel]
            # Add Delay before deleting old sticky and reposting new one
            await asyncio.sleep(3)
            # Delete the old sticky message
            await original_sticky_msg.delete()
            # Send the new sticky message with the latest message content
            new_sticky_msg = await message.channel.send(f"{original_sticky_msg.content}")
            # Update the reference to the sticky message
            self.sticky_messages[message.channel] = new_sticky_msg


    # @commands.Cog.listener()
    # async def on_message(self, message):
    #     # Check if the message is not from the bot itself and it's in a channel with a sticky note
    #     if not message.author.bot and message.channel in self.sticky_messages:
    #         # Get the original sticky message
    #         original_sticky_msg = self.sticky_messages[message.channel]

    #         # Delete the old sticky message
    #         await original_sticky_msg.delete()

    #         # Send the new sticky message with the latest message content
    #         new_sticky_msg = await message.channel.send(f"{original_sticky_msg.content}")

    #         # Update the reference to the sticky message
    #         self.sticky_messages[message.channel] = new_sticky_msg

def setup(bot):
    bot.add_cog(Admin(bot))
