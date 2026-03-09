import os
import psutil

import discord
from discord.ext import commands, tasks
from utils.config import Config

from utils import log
logger = log.Logger("bot")

class DiscordBot(discord.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.Version = Config.BOT_VERSION

        self.Updating = False
        self.Debugging = False
        self.Maintaining = False

        self.process = psutil.Process(os.getpid())

    async def close(self):
        await logger.info("Shutting down...")

        await super().close()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_presence(activity=discord.Game(f"Version {Config.BOT_VERSION}"))
        await logger.info(f"Logged in as {self.user}!")
        await logger.info(self.owner_id)