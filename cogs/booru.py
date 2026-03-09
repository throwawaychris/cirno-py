import datetime
import asyncio
import aiohttp

import discord
import ast
from discord.ext import commands, tasks
from discord import option

from utils import log, http
from utils.config import Config

logger = log.Logger(__name__)

class Booru(commands.Cog):
    """
    Handles various booru functions and tasks,

    1. Get json from booru
    2. Get organize json into embed
    3. Post 


    task:
    1. scan every 30 min
    2. if its not sunday ~ monday: terminate
    3. if 
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        await logger.on_load(__class__.__name__)

        if Config.BOT_TAWAWA_AUTOSTART:
            await self.check_monday_tawawa.start()

    """
    Process URL for retrieving danbooru post through http
    """
    def get_booru_url(self, booru:str, tags:str = None, id = None) -> str:
        if tags:
            return f"https://{booru}.donmai.us/posts/random.json?tags={tags}"
        if id:
            return f"https://{booru}.donmai.us/posts/{id}.json"
        else:
            return f"https://{booru}.donmai.us/posts/random.json"

    """
    Get dict keys from booru
    """
    async def get_booru_post(self, url:str) -> dict:
        try:
            r = await http.get(url, "json")         # Retrieve post
        except Exception as e:
            raise Exception("Couldn't get post...") from e

        if "success" in r.response:                 # When you get a response but couldn't get a post
            raise Exception("Bad tags or ID...") from None

        if "id" not in r.response:                  # If it's a collection of posts
            r.response = r.response[0]              # Choose latest post

        c_url = f"https://danbooru.donmai.us/posts/{r.response["id"]}/artist_commentary.json"

        try:
            c = await http.get(c_url, "json")       # Retrieve post commentary
        except Exception as e:
            raise Exception("Couldn't get commentary...") from e

        if "file_url" not in r.response:
            raise Exception("Post has no media...")
        post = dict(
            id                      = r.response["id"],
            file_url                = r.response["file_url"],
            sample_file_url         = r.response["media_asset"]["variants"][3]["url"],
            created_at              = r.response["created_at"],
            tag_string_artist       = r.response["tag_string_artist"],
            tag_string_copyright    = r.response["tag_string_copyright"],
            tag_string_character    = r.response["tag_string_character"],
            original_title          = "",
            original_description    = "",
            translated_title        = "",
            translated_description  = ""
        )
        if "success" not in c.response:
            post["original_title"]          = c.response["original_title"]
            post["original_description"]    = c.response["original_description"]
            post["translated_title"]        = c.response["translated_title"]
            post["translated_description"]  = c.response["translated_description"]

        return post

    """
    """
    @commands.slash_command(name="danbooru",description="get a danbooru post")
    @option("tags",description="tags to search (max 2)",required=False)
    @option("id",description="id of post",required=False)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def danbooru(self, ctx, tags, id):
        await logger.on_execute(ctx.command.name, ctx.author)
        await ctx.defer()

        # Get danbooru post
        try:
            danbooru_post = await self.get_booru_post(self.get_booru_url("danbooru", tags, id))
        except Exception as e:
            await ctx.respond(f"***{e}***", ephemeral = True)
            return

        # Construct and send embed
        danbooru_embed = discord.Embed(
            title       = danbooru_post["translated_title"] or danbooru_post["original_title"],
            description = danbooru_post["translated_description"] or danbooru_post["original_description"],
            url         = f"https://danbooru.donmai.us/posts/{danbooru_post["id"]}",
            color = discord.Colour.orange()
        )
        danbooru_embed.set_author(
            name        = danbooru_post["tag_string_artist"], 
            icon_url    = "https://danbooru.donmai.us/packs/static/danbooru-logo-128x128-ea111b6658173e847734.png")
        danbooru_embed.set_image(
            url         = danbooru_post["sample_file_url"])
        danbooru_embed.set_thumbnail(
            url         = "https://danbooru.donmai.us/packs/static/danbooru-logo-128x128-ea111b6658173e847734.png")
        danbooru_embed.set_footer(
            text        = f"{danbooru_post["created_at"]} / (ID: {danbooru_post["id"]})")
        danbooru_embed.add_field(
            name        = "Copyright", 
            value       = danbooru_post["tag_string_copyright"])
        danbooru_embed.add_field(
            name        = "Character", 
            value       = danbooru_post["tag_string_character"])

        await ctx.respond(embed = danbooru_embed)
        
    """
    """
    @commands.slash_command(name="safebooru",description="get a safebooru post")
    @option("tags",description="tags to search (max 2)",required=False)
    @option("id",description="id of post",required=False)
    @commands.cooldown(1,5,commands.BucketType.user)
    async def safebooru(self, ctx, tags, id):
        await logger.on_execute(ctx.command.name, ctx.author)
        await ctx.defer()

        # Get safebooru post
        try:
            safebooru_post = await self.get_booru_post(self.get_booru_url("safebooru", tags, id))
        except Exception as e:
            await ctx.respond(f"***{e}***", ephemeral = True)
            return

        # Construct and send embed
        safebooru_embed = discord.Embed(
            title       = safebooru_post["translated_title"] or safebooru_post["original_title"],
            description = safebooru_post["translated_description"] or safebooru_post["original_description"],
            url         = f"https://safebooru.donmai.us/posts/{safebooru_post["id"]}",
            color = discord.Colour.blue()
        )
        safebooru_embed.set_author(
            name        = safebooru_post["tag_string_artist"], 
            icon_url    = "https://danbooru.donmai.us/packs/static/danbooru-logo-128x128-ea111b6658173e847734.png")
        safebooru_embed.set_image(
            url         = safebooru_post["sample_file_url"])
        safebooru_embed.set_thumbnail(
            url         = "https://danbooru.donmai.us/packs/static/danbooru-logo-128x128-ea111b6658173e847734.png")
        safebooru_embed.set_footer(
            text        = f"{safebooru_post["created_at"]} / (ID: {safebooru_post["id"]})")
        safebooru_embed.add_field(
            name        = "Copyright", 
            value       = safebooru_post["tag_string_copyright"])
        safebooru_embed.add_field(
            name        = "Character", 
            value       = safebooru_post["tag_string_character"])

        await ctx.respond(embed = safebooru_embed)

    """
    Tawawa task related commands
    """
    tawawa = discord.SlashCommandGroup("tawawa", "tawawa task related commands")

    """
    """
    def get_tawawa_embed(self, post_dict):
        # Construct and return embed
        tawawa_embed = discord.Embed(
            title       = post_dict["original_title"],
            description = post_dict["translated_title"],
            url         = post_dict["sample_file_url"] or post_dict["file_url"],
            color       = discord.Colour.blue(),
        )
        tawawa_embed.set_author(
            name        = "比村奇石 (@Strangestone)")
        tawawa_embed.set_image(
            url         = post_dict["file_url"])
        tawawa_embed.set_thumbnail(
            url         = "https://pbs.twimg.com/profile_images/557819686662844416/RMwCGmCU_400x400.png")
        tawawa_embed.set_footer(
            text        = f"{post_dict["created_at"]} / (ID: {post_dict["id"]})")

        return tawawa_embed

    """
    """
    def record_id(self, id):
        record_dict = {"previous_id": id, "recorded_at": f"{datetime.datetime.now()}"}

        try:
            with open(Config.BOT_TAWAWA_ID_RECORD, 'w') as file:
                file.write(str(record_dict))
        except Exception as e:
            raise Exception("Error writing to file...") from e

    """
    """
    def retrieve_id(self):
        try:
            with open(Config.BOT_TAWAWA_ID_RECORD, 'r') as file:
                data_string = file.read()

            loaded_dict = ast.literal_eval(data_string)

            return loaded_dict["previous_id"]
        
        except Exception as e:
            raise Exception("Error reading from file...") from e

    """
    """
    @tawawa.command(name = "get_post", description = "Get a tawawa post; latest if no id")
    @option("id", description = "Post ID to get", required = False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def get_tawawa_post(self, ctx, id):
        await logger.on_execute(ctx.command.name, ctx.author)
        await ctx.defer()

        if id:
            url = f"https://danbooru.donmai.us/posts/{id}.json"
        else:
            url = f"https://danbooru.donmai.us/posts.json?tags=himura_kiseki+getsuyoubi_no_tawawa"

        # Get danbooru post
        try:
            tawawa_post = await self.get_booru_post(url)
        except Exception as e:
            await ctx.respond(f"***{e}***", ephemeral = True)

        # Get embed
        tawawa_embed = self.get_tawawa_embed(tawawa_post)

        # Record post id as previous id
        self.record_id(tawawa_post["id"])

        # Post embed
        await ctx.respond(embed = tawawa_embed)

    """
    """
    @tawawa.command(name = "get_previous_id", description = "Get the previous ID")
    async def get_previous_id(self, ctx):
        await logger.on_execute(ctx.command.name, ctx.author)
        await ctx.respond(f"Previous Tawawa post ID: **{self.retrieve_id()}**")

    """
    """
    @tasks.loop(minutes = 30.0)
    async def check_monday_tawawa(self):
        await logger.info("Checking tawawa...")

        if datetime.date.today().weekday() != 0:
            return                                          # If it's not monday; terminate

        url = "https://danbooru.donmai.us/posts.json?tags=himura_kiseki+getsuyoubi_no_tawawa"
        
        try:
            tawawa_post = await self.get_booru_post(url)    # Get post
        except Exception as e:
            await logger.error(f"Danbooru down?: {e}")
            return

        if tawawa_post["id"] == self.retrieve_id():
            return                                          # If ID is same as previous; terminate
        else:
            self.record_id(tawawa_post["id"])               # Assign new ID as previous ID
        
        tawawa_embed = self.get_tawawa_embed(tawawa_post)   # Create embed
        
        ch = await self.bot.fetch_channel(Config.BOT_TAWAWA_CHANNEL_ID)
        await ch.send(f"***It's Monday!*** <@{self.bot.owner_id}>", embed = tawawa_embed)

    """
    """
    @tawawa.command(name = "start", description= "Start checking monday tawawa")
    @commands.is_owner()
    async def start(self, ctx):
        await logger.on_execute(ctx.command.name, ctx.author)

        if not self.check_monday_tawawa.is_running():
            self.check_monday_tawawa.start()
            await ctx.respond("Started checking monday tawawa!", ephemeral = True)
        else:
            await ctx.respond("Already running!", ephemeral = True)

    """
    """
    @tawawa.command(name = "stop", description= "stop checking monday tawawa")
    @commands.is_owner()
    async def stop(self, ctx):
        await logger.on_execute(ctx.command.name, ctx.author)

        if self.check_monday_tawawa.is_running():
            self.check_monday_tawawa.stop()
            await ctx.respond("Stopped checking monday tawawa...", ephemeral = True)
        else:
            await ctx.respond("Task is not running!", ephemeral = True)

    """
    """
    @tawawa.command(name = "restart", description= "restart checking monday tawawa")
    @commands.is_owner()
    async def restart(self, ctx):
        await logger.on_execute(ctx.command.name, ctx.author)

        self.check_monday_tawawa.restart()
        await ctx.respond("Restarted checking monday tawawa!", ephemeral = True)

    """
    """
    @tawawa.command(name = "cancel", description= "cancel checking monday tawawa")
    @commands.is_owner()
    async def cancel(self, ctx):
        await logger.on_execute(ctx.command.name, ctx.author)

        self.check_monday_tawawa.cancel()
        await ctx.respond("Canceled task.", ephemeral = True)

    @check_monday_tawawa.before_loop
    async def before_check_monday_tawawa(self):
        await self.bot.wait_until_ready()

    @check_monday_tawawa.after_loop
    async def after_check_monday_tawawa(self):
        await logger.info(f"{self.bot}")

    @check_monday_tawawa.error
    async def cancel_check_monday_tawawa(self, error):
        await logger.error(f"tawawa task is being cancelled; error: {error}...")
        await self.check_monday_tawawa.stop()

def setup(bot: commands.Bot):
    bot.add_cog(Booru(bot))