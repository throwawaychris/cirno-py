import discord

from discord.ext import commands
from discord import option

from utils import log

logger = log.Logger(__name__)

class Events(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await logger.on_load(__class__.__name__)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        """
        Global error handling for commands
        """
        
        if isinstance(error, commands.CommandNotFound):
            await ctx.respond("Command doesn't exist!", ephemeral = True)
        
        if isinstance(error, commands.NotOwner):
            await ctx.respond("Only the owner can use this command!", ephemeral = True)
        
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond("You don't have permissions...", ephemeral = True)

        if isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I don't have permissions to do this...", ephemeral = True)


def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))