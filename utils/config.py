import os
import discord
from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

@dataclass
class Config:
    BOT_NAME: str                = "Cirnopy"
    BOT_TOKEN: str               = os.getenv("BOT_TOKEN")
    BOT_OWNER: int               = int(os.getenv("BOT_OWNER"))
    BOT_DESCRIPTION: str         = "A Cirno themed discord bot powered by pycord!"
    BOT_PREFIX: str              = "&"
    BOT_VERSION: str             = "2.2.1"
    BOT_GUILD_ID: str            = os.getenv("BOT_GUILD_ID")
    BOT_TAWAWA_CHANNEL_ID: str   = os.getenv("BOT_TAWAWA_CHANNEL_ID")

    BOT_ROOT_DIR                 = Path(__file__).parent
    BOT_COGS_DIR                 = BOT_ROOT_DIR / "cogs"
    BOT_LOGS_DIR                 = BOT_ROOT_DIR / "logs"

    BOT_LOGS_FORMAT              = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    BOT_LOGS_RICH                = "%(message)"

    BOT_INTENTS                  = discord.Intents.all()
    BOT_INTENTS.message_content  = True
    BOT_INTENTS.members          = True 
    BOT_INTENTS.guilds           = True

    BOT_RADIO_AUTOSTART          = True
    BOT_TAWAWA_AUTOSTART         = True

    BOT_TAWAWA_ID_RECORD         = 'id_record.txt'