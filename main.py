import os
import discord
from discord.ext import commands

from utils import log, bot
from utils.config import Config

logger = log.Logger("bot")

bot = bot.DiscordBot(
    dscription = Config.BOT_DESCRIPTION,
    prefix = Config.BOT_PREFIX,
    owner_id = Config.BOT_OWNER,
    intents = Config.BOT_INTENTS,
    case_insensitive = True,
    help_command = None,
)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(Config.BOT_TOKEN)