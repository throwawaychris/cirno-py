import os

import discord
from discord import option
from discord.commands import permissions
from discord.ext import commands

from utils import log, http
from utils.config import Config

logger = log.Logger(__name__)

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await logger.on_load(__class__.__name__)

    @commands.slash_command(
        guild_ids=[Config.BOT_GUILD_ID], 
        name = "reload",
        description="Reload extensions (owner-only command)"
        )
    @commands.is_owner()
    async def reload(self, ctx):
        """
        Reload extensions
        """
        await logger.on_execute(ctx.command.name, ctx.author)

        for file in os.listdir("cogs"):
            if file.startswith("__"):
                continue
            cog_name = file[:-3]
            try:
                self.bot.reload_extension(f"cogs.{cog_name}")
            except Exception as e:
                logger.error(f"Failed to load cog {cog_name}: {e}", exc_info=e)
        await ctx.respond(f"Reloaded extensions!", ephemeral = True)

    change = discord.SlashCommandGroup("change", "change various bot properties")


    @change.command(
        name="activity", 
        description="Changes bot's activity status"
        )
    @commands.cooldown(1, 60, commands.BucketType.user)
    @option("activity", description="Enter new activity status", required=True)
    async def activity(self, ctx, activity: str):
        """
        Change the bot's activity status
        """
        await logger.on_execute(ctx.command.name, ctx.author)

        if activity:
            await self.bot.change_presence(activity=discord.Game(activity))

            await logger.info(f"Changed {self.bot.user}'s activity status to '{activity}'!") # Logging
            await ctx.respond(f"Changed my activity status to '***{activity}***'!")
        else:
            await ctx.respond("Error changing activity status... (Improper input)", ephemeral=True)


    @change.command(
        name="banner", 
        description="Changes bot's banner image"
        )
    @commands.is_owner()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @option("banner", description="Set banner image to attachment", required=True)
    async def banner(self, ctx, banner_file: discord.Attachment):
        """
        Change the bot's banner image
        """
        await logger.on_execute(ctx.command.name, ctx.author)

        await ctx.defer(ephemeral = True)

        if not banner_file or not banner_file.content_type.startswith("image/"):
            await ctx.send_followup("Error changing banner... (Improper attachment)", ephemeral = True)
            return

        try:
            r = await http.get(banner_file.url, "read")

        except discord.HTTPException as e:
            await ctx.send_followup(f"An error occured: {e}", ephemeral = True)

        except Exception as e:
            await ctx.send_followup(f"An unexpected error occured: {e}", ephemeral = True)

        await self.bot.user.edit(banner = r.response)
        await ctx.send_followup("Changed my banner!")
        return

def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))