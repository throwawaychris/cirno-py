# Cirno-py
A super basic cirno themed discord bot made with pycord.

## Prerequisite
- Python version should be ```>3.10``` and ```<=3.13```. It breaks otherwise
- Docker ```>=29.3.0```

## Setup
First, clone this repository recursively:
```bash
git clone https://github.com/throwawaychris/cirno-py.git
```

Fill out your personal data into ```.env_example``` and rename to ```.env```
```bash
mv .env_example .env
```

## Configuration
Bot config is managed in ```utils/config.py```. Do not change bot related directory paths in the config.

Some routine tasks should be off at start-up; consider turning them on at your pleasure.
```python
BOT_RADIO_AUTOSTART          = False
BOT_TAWAWA_AUTOSTART         = False
```
They can be turned on or off during runtime with built in slash-commands

## Running
Start the dockerfile
```bash
docker-compose up -d --build
```

## Modifying & Adding features
Adding a cog file to the cogs directory is recommended for adding features
```python
# your_cog.py

import discord
from discord.ext import commands
from discord import option
from utils import log

class YOUR_COG(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # Your commands/components here

def setup(bot: commands.Bot):
    bot.add_cog(Events(bot))
```
Consider browsing through pycord's [documentation](https://guide.pycord.dev/popular-topics/cogs) if you are not familar.

**Logging** is handled through built-in logger functions in ```log/log.py```. Use them like this:
```python
await logger.on_execute(ctx.command.name, ctx.author)    # When command is executed
await logger.on_load(__class__.__name__)    # When cog is loaded
await logger.info("info")
await logger.debug("debug")
await logger.warning("warning")
await logger.error("error")
```

# License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
