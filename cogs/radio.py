import discord
import sys
import re

from discord.ext import commands, tasks
from discord import option

from utils import log, http
from utils.config import Config

logger = log.Logger(__name__)

class Radio(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.previous_line = None
        self.previous_dj = None

    async def _get_line(self):
        url = "https://need.moe/radio/djlog/djlog.txt"

        try:
            r = await http.get(url)
            
            lines = r.response.strip().splitlines()

            if not lines:
                return None

            return lines[-1].strip()

        except Exception as e:
            await logger.error(f"Error: {e}")
            return f"Error: {e}"

    async def _get_dj(self, line):
        dj_pattern = re.compile(r"\(([^)]+)\)$")

        if not line:
            return None
        
        match = dj_pattern.search(line)
        
        if not match:
            return None

        if match.group(1) == "AFK":
            return "Hanyuu-sama"

        return match.group(1)

    @commands.Cog.listener()
    async def on_ready(self):
        await logger.on_load(__class__.__name__)

        if Config.BOT_RADIO_AUTOSTART:
            await self.update_radio_status.start()

    @tasks.loop(minutes = 4)
    async def update_radio_status(self):
        await logger.debug("Checking for DJ change...")

        try:
            current_line = await self._get_line()
        except Exception as e:
            await logger.error(e)
            return

        if not current_line:
            return

        if current_line != self.previous_line:
            current_dj = await self._get_dj(current_line)

            if current_dj:
                await logger.info(f"New DJ; changing activity to {current_dj}")
                await self.bot.change_presence(activity=discord.Streaming(
                    name = f"🎶 {current_dj}",
                    url = "https://r-a-d.io"
                ))

            self.previous_line = current_line
            self.previous_dj = current_dj

    @update_radio_status.before_loop
    async def before_update_radio_status(self):
        await self.bot.wait_until_ready()

    @update_radio_status.after_loop
    async def after_update_radio_status(self):
        try:
            await self.bot.change_presence(activity=discord.Game(
            name=f"Version {Config.BOT_VERSION}"
            ))
        except Exception as e:
            await logger.info(f"{e}; closing without changing presence")

        self.previous_dj = None
        self.previous_line = None

    @update_radio_status.error
    async def error_update_radio_status(self):
        await logger.error(f"tawawa task is being cancelled; error: {error}...")
        await self.update_radio_status.stop()

    radio = discord.SlashCommandGroup("radio", "r/a/dio related commands")

    @radio.command(name="getdj", description="Gets DJ Log")
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def getdj(self, ctx):
        """
        Get currently playing DJ on r/a/dio
        """
        await logger.on_execute(ctx.command.name, ctx.author)
        
        try:
            dj = await self._get_dj(await self._get_line())

            await ctx.respond(f"**{dj}** is currently playing")

        except Exception as e:
            await ctx.respond(e, ephemeral = True)

    # Start the scan
    @radio.command(name="start", description="Start the check radio task")
    @commands.is_owner()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def start(self, ctx: discord.ApplicationContext):
        """
        Starts the r/a/dio task
        """
        await logger.on_execute(f"radio.{ctx.command.name}", ctx.author)

        if not self.update_radio_status.is_running():
            self.update_radio_status.start()
            await ctx.respond("Started checking r/a/dio!", ephemeral = True)

        else:
            await ctx.respond("Task is already running!", ephemeral = True)

    # Stops the scan
    @radio.command(name="stop", description="Stops the check radio task")
    @commands.is_owner()
    async def stop(self, ctx: discord.ApplicationContext):
        """
        Stops the r/a/dio task
        """
        await logger.on_execute(f"radio.{ctx.command.name}", ctx.author)

        if self.update_radio_status.is_running():
            self.update_radio_status.stop()
            await ctx.respond("Stopped checking r/a/dio...", ephemeral = True)
        
        else:
            await ctx.respond("Task isn't running!", ephemeral = True)

    # Cancels the scan
    @radio.command(name="cancel", description="Cancels the check radio task")
    @commands.is_owner()
    async def cancel(self, ctx: discord.ApplicationContext):
        """
        Cancels the r/a/dio task
        """
        await logger.on_execute(f"radio.{ctx.command.name}", ctx.author)

        if self.update_radio_status.is_running():
            self.update_radio_status.cancel()
            await ctx.respond("Terminating r/a/dio task...", ephemeral = True)
        
        else:
            await ctx.respond("Task isn't running!", ephemeral = True)

    # Restarts the scan
    @radio.command(name="restart", description="Restarts the check radio task")
    @commands.is_owner()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def restart(self, ctx: discord.ApplicationContext):
        """
        Restarts the r/a/dio task
        """
        await logger.on_execute(f"radio.{ctx.command.name}", ctx.author)

        self.update_radio_status.restart()
        await ctx.respond("Restarted checking r/a/dio...", ephemeral = True)

def setup(bot: commands.Bot):
    bot.add_cog(Radio(bot))