import discord
from discord.ext import commands
import datetime
import asyncio

class ADMIN_COMMANDS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sticky_messages = {}  # Store sticky messages for each channel

    async def check_role(self, ctx, required_role):
        role = discord.utils.get(ctx.guild.roles, name=required_role)

        if role is None or role not in ctx.author.roles:
            await ctx.send(f"You don't have the required role ({required_role}) to use this command.")
            return False

        return True

    @commands.command(name='botdown', aliases=['bd', 'down'], help='[#Channel] [Message]')
    async def botdown_command(self, ctx, channel: discord.TextChannel, *, message):
        if not await self.check_role(ctx, "Admin"):
            return

        await channel.send(f"**Bot Down:**\n{message}")
        await ctx.send(f"Bot Down message sent to {channel.mention}.")

        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        author = ctx.message.author
        command = ctx.command.name
        print(f"{current_time} - {author.name} used the *{command}* command.")

    @commands.command(name='announcement', aliases=['announce', 'am'], help='[#Channel] [Message]')
    async def announcement(self, ctx, channel: discord.TextChannel, *, message):
        if not await self.check_role(ctx, "Admin"):
            return

        await channel.send(f"**Announcement:**\n{message}")
        await ctx.send(f"Announcement sent to {channel.mention}.")

    @commands.command(name='addsticky', aliases=['as'], help='[#Channel] [Message]')
    async def sticky_note(self, ctx, channel: discord.TextChannel, *, message):
        if not await self.check_role(ctx, "Moderator"):
            return

        # Send the sticky note message to the specified channel
        sticky_msg = await channel.send(f"*STICKY NOTE:*\n`{message}`")
      
        # Store the sticky message for future reference
        self.sticky_messages[channel] = sticky_msg
      
        await ctx.send(f"Sticky note added to {channel.mention}.")

    @commands.command(name='removesticky', aliases=['rs'], help='[#Channel]')
    async def remove_sticky(self, ctx, channel: discord.TextChannel):
        if not await self.check_role(ctx, "Moderator"):
            return

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

def setup(bot):
    bot.add_cog(ADMIN_COMMANDS(bot))
