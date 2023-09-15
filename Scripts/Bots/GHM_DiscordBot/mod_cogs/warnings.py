import discord
from discord.ext import commands
import json
import os
import datetime

with open('config.json', 'r') as config_file:
    config = json.load(config_file)

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

class WarningsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data_folder = 'data'
        self.warnings_file = os.path.join(self.data_folder, 'warnings.json')
        self.log_mod_stuff = config.get('log_mod_stuff')
        self.load_warnings()  # Load the warnings when the cog is initialized

    def load_warnings(self):
        if not os.path.exists(self.warnings_file):
            self.warnings_data = {}
            self.save_warnings()  # Create an empty JSON file
        else:
            with open(self.warnings_file, "r") as f:
                try:
                    self.warnings_data = json.load(f)
                except json.JSONDecodeError:
                    self.warnings_data = {}  # Handle JSON decoding error

    def save_warnings(self):
        with open(self.warnings_file, "w") as f:
            json.dump(self.warnings_data, f, indent=4)

    async def remove_warning(self, member, idx):
        user_id = str(member.id)

        if user_id not in self.warnings_data:
            return -1  # User has no warnings

        warns = self.warnings_data[user_id].get("warns", [])

        if not warns:
            return -1  # User has no warnings

        if idx <= 0:
            return -3  # Warn index below 1
        if idx > len(warns):
            return -2  # Warn index is higher than warn count

        removed_warn = warns.pop(idx - 1)
        self.save_warnings()

        return discord.Embed(
            title="Warning Removed",
            description=f"**Removed by:** {ctx.author.mention}\n"
                        f"**User:** {member.mention}\n"
                        f"**Issuer:** {removed_warn['issuer_name']}\n"
                        f"**Reason:** {removed_warn['reason']}",
            color=discord.Color.green(),
        )

    @commands.command(name="listwarns")
    @has_mod_or_higher()
    async def listwarns(self, ctx, user: discord.User = None):
        """Lists warnings for a user"""
        if user is None or user == ctx.author:
            user = ctx.author

        embed = discord.Embed(color=discord.Color.dark_red())
        embed.set_author(name="Warns for {}".format(user), icon_url=user.avatar_url)

        if str(user.id) in self.warnings_data:
            warns = self.warnings_data[str(user.id)].get("warns", [])
            if len(warns) == 0:
                embed.description = "There are none!"
                embed.color = discord.Color.green()
            else:
                for idx, warn in enumerate(warns):
                    embed.add_field(
                        name="{}: {}".format(idx + 1, warn["timestamp"]),
                        value="Issuer: {}\nReason: {}".format(warn["issuer_name"], warn["reason"])
                    )
        else:
            embed.description = "There are none!"
            embed.color = discord.Color.green()

        await ctx.send(embed=embed)

    @commands.command(name="warn")
    @has_mod_or_higher()
    async def warn(self, ctx, member: discord.Member, *, reason=""):
        """Warn a user. Staff only."""
        issuer = ctx.message.author
        for role_name in ["Moderator", "Admin"]:
            required_role = discord.utils.get(ctx.guild.roles, name=role_name)
            if required_role and required_role in member.roles:
                await ctx.send("You cannot warn another staffer!")
                return

        warn_count = len(self.warnings_data.get(str(member.id), {}).get("warns", []))
        msg = "You were warned on GodHatesMe Pokemon Centre Discord Server."
        if reason:
            msg += f" The given reason was: {reason}"

        if warn_count >= 5:
            msg += "\n\nYou were automatically banned due to five or more warnings."
            try:
                try:
                    await member.send(msg)
                except discord.errors.Forbidden:
                    pass
                await member.ban(reason=reason, delete_message_days=0)
            except Exception:
                await ctx.send("No permission to ban the warned member")
        elif warn_count >= 3:
            msg += "\n\nYou were kicked because of this warning. You can join again right away. Reaching 5 warnings will result in an automatic ban. Permanent invite link: https://discord.gg/SrREp2BbkS."
            try:
                try:
                    await member.send(msg)
                except discord.errors.Forbidden:
                    pass
                await member.kick(reason="Three or Four Warnings")
            except Exception:
                await ctx.send("No permission to kick the warned member")
        else:
            if warn_count == 2:
                msg += " __The next warn will automatically kick.__"
            
            # Customize the message based on other conditions, for example:
            if "bad_word" in reason.lower():
                msg += " Your warning contains offensive language."
            elif "spam" in reason.lower():
                msg += " Your warning is related to spamming."

            try:
                await member.send(msg)
            except discord.errors.Forbidden:
                pass

        # Add the warning to the database
        self.add_warning(member, reason, issuer)

        msg = f"⚠️ **Warned**: {issuer.name} warned {member.mention} (warn #{warn_count}) | {member}"
        if reason:
            msg += f" The given reason is: {reason}"

        await ctx.send(msg)
        await self.bot.get_channel(self.log_mod_stuff).send(msg)

    def add_warning(self, member, reason, issuer):
        warn_data = {
            "timestamp": str(datetime.datetime.utcnow()),  # Use datetime.datetime.utcnow() to get the current UTC time
            "issuer_name": str(issuer),
            "reason": reason,
        }
        user_id = str(member.id)

        if user_id not in self.warnings_data:
            self.warnings_data[user_id] = {"warns": []}

        self.warnings_data[user_id]["warns"].append(warn_data)
        self.save_warnings()

    @commands.command(name="clearwarns")
    @has_mod_or_higher()
    async def clearwarns(self, ctx, member: discord.Member):
        """Clears warns of a specific member"""
        warnings_file = os.path.join(self.data_folder, 'warnings.json')
        with open(warnings_file, "r") as f:
            warnings_data = json.load(f)
        
        if str(member.id) not in warnings_data:
            await ctx.send("{} has no warns!".format(member.mention))
            return
        
        warn_count = len(warnings_data[str(member.id)].get("warns", []))
        
        if warn_count == 0:
            await ctx.send("{} has no warns!".format(member.mention))
            return
        
        warnings_data[str(member.id)]["warns"] = []
        
        with open(warnings_file, "w") as f:
            json.dump(warnings_data, f, indent=4)
        
        await ctx.send("{} no longer has any warns!".format(member.mention))
        msg = "🗑 **Cleared warns**: {} cleared {} warns from {} | {}".format(ctx.author.name, warn_count, member.mention, str(member))
        await ctx.send(msg)
        await self.bot.get_channel(self.log_mod_stuff).send(msg)
    
    @commands.command(name="delwarn")
    @has_mod_or_higher()
    async def delwarn(self, ctx, member: discord.Member, idx: int):
        """Remove a specific warning from a user. Staff only."""
        returnvalue = await self.remove_warning(ctx, member, idx)
        warnings_file = os.path.join(self.data_folder, 'warnings.json')
        with open(warnings_file, "r") as f:
            rsts = json.load(f)
            warn_count = len(rsts.get(str(member.id), {}).get("warns", []))
        if isinstance(returnvalue, int):
            if returnvalue == -1:
                await ctx.send("{} has no warns!".format(member.mention))
            elif returnvalue == -2:
                await ctx.send("Warn index is higher than warn count ({})!".format(warn_count))
            elif returnvalue == -3:
                await ctx.send("Warn index below 1!")
            return
        else:
            msg = "🗑 **Deleted warn**: {} removed warn {} from {} | {}".format(ctx.message.author.name, idx, member.mention, str(member))
            await ctx.send(msg)
            await self.bot.get_channel(self.log_mod_stuff).send(msg, embed=returnvalue)

    # Modify the remove_warning method to accept ctx as a parameter
    async def remove_warning(self, ctx, member, idx):
        user_id = str(member.id)

        if user_id not in self.warnings_data:
            return -1  # User has no warnings

        warns = self.warnings_data[user_id].get("warns", [])

        if not warns:
            return -1  # User has no warnings

        if idx <= 0:
            return -3  # Warn index below 1
        if idx > len(warns):
            return -2  # Warn index is higher than warn count

        removed_warn = warns.pop(idx - 1)
        self.save_warnings()

        return discord.Embed(
            title="Warning Removed",
            description=f"**Removed by:** {ctx.author.mention}\n"
                        f"**User:** {member.mention}\n"
                        f"**Issuer:** {removed_warn['issuer_name']}\n"
                        f"**Reason:** {removed_warn['reason']}",
            color=discord.Color.green(),
        )

def setup(bot):
    bot.add_cog(WarningsCog(bot))
