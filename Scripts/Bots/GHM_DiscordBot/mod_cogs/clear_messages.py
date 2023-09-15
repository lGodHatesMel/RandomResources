import discord
from discord.ext import commands

def has_mod_or_higher():
    async def predicate(ctx):
        required_roles = ["Moderator", "Admin"]
        if ctx.author.id == ctx.guild.owner_id:
            return True

        for role_name in required_roles:
            required_role = discord.utils.get(ctx.guild.roles, name=role_name)
            if required_role and required_role in ctx.author.roles:
                return True

        await ctx.send("You don't have the required role or higher to use this command.")
        return False

    return commands.check(predicate)

class ClearMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge"])
    @has_mod_or_higher()
    async def clear_messages(self, ctx, amount: int):
        """
        Clear a specified number of messages from the channel.
        Usage: !clear <amount>
        """
        if amount <= 0:
            await ctx.send("Please specify a valid number of messages to clear.")
            return

        if amount > 100:
            await ctx.send("You can only clear up to 100 messages at a time.")
            return

        try:
            # Delete the command message
            await ctx.message.delete()
            # Delete the specified number of messages
            deleted_messages = await ctx.channel.purge(limit=amount)

            await ctx.send(f"Cleared {len(deleted_messages)} messages.", delete_after=5)

        except commands.MissingPermissions:
            await ctx.send("Bot doesn't have the necessary permissions to clear messages.")

def setup(bot):
    bot.add_cog(ClearMessages(bot))
